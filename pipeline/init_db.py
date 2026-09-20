# -*- coding: utf-8 -*-
"""首次建库：schema + 根目录 13-*.csv 一次性导入 + 治理层 / 元数据层 + 视图。登记为 migration_log 0000_bootstrap。
用法（pipeline/ 下）：python3 init_db.py            # 库已存在则拒绝（库是真源，不能被 CSV 覆盖）
                     python3 init_db.py --force    # 明确要从头重建：删库 → 导入 → 之后由 migrate.py 重放 migrations/
之后每一次改库（新记录 / 填字段 / 取代）都走 migrate.py，不再改根目录 CSV，也不再重跑本脚本。"""
import csv, os, re, sys, json, hashlib, duckdb, datetime as dt
from core import *
def read(name):
    with open(os.path.join(ROOT, 'data', 'tables', name), newline='', encoding='utf-8') as fh: return list(csv.DictReader(fh))

if os.path.exists(DB) and '--force' not in sys.argv:
    sys.exit(f'!! 库已存在：{DB}\n   库是真源。要改数据请写 migrations/ 脚本并运行 migrate.py；确认要从头重建再加 --force。')
if os.path.exists(DB): os.remove(DB)
con = duckdb.connect(DB)
con.execute(open(os.path.join(HERE, 'schema.sql'), encoding='utf-8').read())
log = []
def L(step, i, o, note=''): log.append((step, i, o, note))

# ---------------- 接入层 ----------------
O = read('13-观测记录.csv')
con.executemany('INSERT INTO stg_observation VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
    [(r['record_id'], r['metric_id'], r['entity'], r['obs_type'], r['value'], r['unit'], r['period'], r['knowledge_time'], r['source'], prov_norm(r['provenance']), r['note'], None) for r in O])
L('stg_observation', len(O), len(O))

# ---------------- 资产层：实体 / 指标 / 边 ----------------
emod = mod('entities')
con.executemany('INSERT INTO entity_master (entity_id,name,aliases,type,layer,maturity,track,country,ticker,parent_id,in_book,owner,status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
    [(e[0], e[1], None, e[2], e[3], e[4], e[5], e[6], e[7], None, e[8], 'B', 'draft') for e in emod.E])
M = read('13-指标总表.csv')
me = []
for m in M:
    tgt = emod.MAP.get(m['ticker_or_entity'], 'ent_frontier_cap')
    for t in (tgt if isinstance(tgt, list) else [tgt]): me.append((m['metric_id'], t))
me = sorted(set(me))
L('entity_master', len(emod.E), len(emod.E))
LAYER_BY_ENT = {e[0]: e[3] for e in emod.E}
prim = {}
for mid, ent in me: prim.setdefault(mid, ent)
con.executemany('INSERT INTO metric_registry VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
    [(r['metric_id'], r['name'], prim.get(r['metric_id']), r['ticker_or_entity'], r['entry'], None, LAYER_BY_ENT.get(prim.get(r['metric_id'])), r['dim'], r['data_class'], r['signal_role'],
      None, r['source_family'], r['frequency'], r['lead_time_est'], None, None, r['owner'] or None, None, r['availability'], r['next_release'], r['next_release_basis'],
      'testing', r['status'], r['notes_assumption_ids'], None) for r in M])
con.executemany('INSERT INTO metric_entity VALUES (?,?)', me)
L('metric_registry', len(M), len(M))
E = read('13-边总表.csv')
con.executemany('INSERT INTO edge_registry VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
    [(r['edge_id'], r['from_metric'], r['to_ticker'], r['side'], r['edge_type'], int(r['hops']), r.get('chain', ''), None, r['cert_tier'], r['cert_method'], None, None,
      r['tradable_score'], r['warning_score'], r['is_key'], None, r['evidence'], None, r['status'], r['notes'], None) for r in E])
REL = {'self': 'self', 'supply': 'supplier', 'demand': 'customer', 'compete': 'competitor', 'regime': 'demand_driver'}
etm = []
for i, r in enumerate(E, 1):
    ents = [t for (mid, t) in me if mid == r['from_metric']]
    for t in ents[:1]: etm.append((i, t, r['to_ticker'], REL[r['side']], r.get('chain', ''), None, 'B', 'draft'))
con.executemany('INSERT INTO entity_ticker_map VALUES (?,?,?,?,?,?,?,?)', etm)
L('edge_registry', len(E), len(E))

# ---------------- 资产层：来源（从记录派生）+ 四类 fct 路由 ----------------
con.executemany('INSERT INTO source_override VALUES (?,?,?,?)', SOURCE_OVERRIDE)
mcls = {m['metric_id']: m['data_class'] for m in M}
ent_of = {}
for mid, ent in me: ent_of.setdefault(mid, ent)
n_src = 0
for r in O: n_src += upsert_source(con, r, mcls.get(r['metric_id']))[1]
L('source_master', len(O), n_src, '从观测记录派生；access / verify_status 由 source_override 覆盖')
buckets = {}; routed = []
for r in O:
    t, row = fct_row(r, mcls.get(r['metric_id']), ent_of.get(r['metric_id']))
    buckets.setdefault(t, []).append(row); routed.append((t, r['record_id']))
for t, rows_ in buckets.items(): insert_rows(con, t, rows_)
con.executemany('UPDATE stg_observation SET routed_to = ? WHERE record_id = ?', routed)
L('fct_route', len(O), len(routed), json.dumps({t: len(v) for t, v in buckets.items()}, ensure_ascii=False))

# ---------------- 治理层 ----------------
A = read('13-假设台账.csv'); seen = set(); A = [r for r in A if not (r['assumption_id'] in seen or seen.add(r['assumption_id']))]
con.executemany('INSERT INTO assumption VALUES (?,?,?,?,?,?,?,?)', [(r['assumption_id'], r['section'], r['text'], r['current_value'], r['kind'], r['impact'], r['refine_by'], r['status']) for r in A])
con.executemany('INSERT INTO coefficient VALUES (?,?,?,?)', [
    ('w_e',0.45,'A2','节点价值权重 e'),('w_s',0.25,'A2','节点价值权重 s'),('w_r',0.20,'A2','节点价值权重 r'),('w_phi',0.10,'A2','节点价值权重 φ'),
    ('decay',0.9,'A3','c = base × decay^hops'),('base_T1',0.9,'A4','cert_base T1'),('base_T2',0.6,'A4','cert_base T2'),('base_T3',0.3,'A4','cert_base T3'),
    ('tau_hops',0.25,'A5','τ = min(1, tau_hops·hops + tau_l·l)'),('tau_l',0.5,'A5','同上'),
    ('r_P1',0.9,'A8','provenance→r'),('r_P23',0.6,'A8','provenance→r'),('r_P4',0.3,'A8','provenance→r'),
    ('anchor_H',0.9,'A1','因子锚 H'),('anchor_M',0.6,'A1','因子锚 M'),('anchor_L',0.3,'A1','因子锚 L')])
fmod = mod('factors')
best = {r[0]: r[1] for r in con.execute("SELECT metric_id, min(provenance) FROM stg_observation WHERE provenance LIKE 'P%' GROUP BY 1").fetchall()}
con.executemany('INSERT INTO metric_factor VALUES (?,?,?,?,?,?,?,?,?)', [(m['metric_id'],) + fmod.assign(m, best.get(m['metric_id'])) + ('B','draft') for m in M])
dmod = mod('directions')
def _dir(r):
    if r.get('direction'): return (r['direction'], r.get('direction_note', ''))
    return tuple(dmod.assign(r))
con.executemany('INSERT INTO observation_direction VALUES (?,?,?,?,?)', [(r['record_id'],) + _dir(r) + ('B','draft') for r in O])
K = read('13-关键事实.csv')
con.executemany('INSERT INTO key_fact VALUES (?,?,?,?,?,?,?,?,?)', [(r['kf_id'], r['target_type'], kdate(r['date']) if r['date'] else None, r['target'], r['brief'], r['watch'], r['refs'], r['owner'], r['status']) for r in K])
C = read('13-日历排期.csv'); mids = {m['metric_id'] for m in M}; cal_rows, cm_rows = [], []
for i, r in enumerate(C, 1):
    cid = f'c{i:03d}'; d = kdate(r['date']) if re.match(r'^\d{4}-\d{2}-\d{2}$', r['date']) else None
    cal_rows.append((cid, r['date'], d, r['date_precision'], r['event'], r['entity_or_ticker'], r['dim_or_entry'], r['related_metric'], r['basis'], r['source_or_rule'], r['notes']))
    for m in [x.strip() for x in r['related_metric'].split('/')]:
        if m in mids: cm_rows.append((cid, m))
con.executemany('INSERT INTO calendar (cal_id,date_raw,date,date_precision,event,entity_or_ticker,dim_or_entry,related_metric,basis,source_or_rule,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)', cal_rows); con.executemany('INSERT INTO calendar_metric VALUES (?,?)', cm_rows)
L('governance', len(A) + 16 + len(M) + len(O) + len(K) + len(C), 0, '假设 / 系数 / 因子 / 方向 / 简报 / 排期')

# ---------------- 元数据层 ----------------
meta = mod('metadata')
con.executemany('INSERT INTO schema_doc VALUES (?,?,?,?,?,?)', meta.SCHEMA_DOC)
con.executemany('INSERT INTO relation_doc VALUES (?,?,?,?,?,?)', meta.RELATIONS)
con.executemany('INSERT INTO calc_rule VALUES (?,?,?,?,?,?,?,?)', meta.CALC_RULES)
missing = con.execute("""SELECT c.table_name, c.column_name FROM information_schema.columns c
  LEFT JOIN schema_doc d ON d.table_name=c.table_name AND d.column_name=c.column_name
  WHERE c.table_schema='main' AND d.column_name IS NULL AND c.table_name NOT LIKE 'v_%'""").fetchall()
if missing: sys.exit(f'!! schema_doc 缺字段说明: {missing}')

con.execute(open(os.path.join(HERE, 'views.sql'), encoding='utf-8').read())
run = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
con.executemany('INSERT INTO etl_log VALUES (?,?,?,?,?,?)', [(f'{run}-{i}', dt.datetime.now(), s[0], s[1], s[2], s[3]) for i, s in enumerate(log)])
srcs = ''.join(open(os.path.join(ROOT, 'data', 'tables', f), encoding='utf-8').read() for f in ('13-观测记录.csv','13-指标总表.csv','13-边总表.csv','13-假设台账.csv','13-关键事实.csv','13-日历排期.csv'))
con.execute('INSERT INTO migration_log (migration_id, checksum, owner, n_changes, note) VALUES (?,?,?,?,?)',
    ['0000_bootstrap', hashlib.sha256(srcs.encode()).hexdigest()[:16], 'B', len(O), '首次导入根目录 13-*.csv（checksum = 六份 CSV 合并 sha256）'])
for t in ['stg_observation','entity_master','metric_registry','edge_registry','fct_quant','fct_event','fct_opinion','fct_frontier','fct_position','source_master','metric_factor','observation_direction','key_fact','calendar','schema_doc']:
    print(f'{t:22s}', con.execute(f'SELECT count(*) FROM {t}').fetchone()[0])
con.close(); print('bootstrap →', DB, '；接下来 python3 migrate.py 重放 migrations/')
