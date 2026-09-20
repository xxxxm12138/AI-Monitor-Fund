# -*- coding: utf-8 -*-
"""共用规则：解析 / 归一 / 来源 slug 与类型 / 接入 → 四类 fct 路由 / 字段类型转换。
init_db.py（首次导入）与 migrate.py（之后每一次改库）都从这里取规则，保证两条路径写出的行同构。"""
import os, re, json, datetime as dt, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DB = os.environ.get('ANATOLE_DB') or os.path.join(HERE, 'anatole_ai_monitor.duckdb')   # ANATOLE_DB=… 可指向副本做测试
SNAP_DIR = os.path.join(HERE, 'snapshots')
PK = {'stg_observation':'record_id','metric_registry':'metric_id','entity_master':'entity_id','edge_registry':'edge_id','fct_quant':'record_id','fct_event':'record_id','fct_opinion':'record_id','fct_frontier':'record_id','fct_position':'record_id',
      'source_master':'source_id','metric_factor':'metric_id','assumption':'assumption_id','key_fact':'kf_id','calendar':'cal_id','observation_direction':'record_id','coefficient':'coef_id',
      'thesis_node':'node_id','decision_fork':'fork_id','artifact_anchor':'anchor_id',
      'decision_registry':'decision_id','decision_log':'dec_id','candidate_pool':'cand_id'}
FCT = ('fct_quant','fct_event','fct_opinion','fct_frontier')

def mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def kdate(s):
    s = (s or '').strip()
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', s)
    if m: return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.match(r'^(\d{4})-(\d{2})$', s)
    if m: return dt.date(int(m[1]), int(m[2]), 15)
    return None
def prov_norm(p):
    p = (p or '').strip()
    if p in ('P1','P2','P3','P4','P5','—','P3–P5'): return p
    m = re.match(r'P[1-5]', p); return m.group(0) if m else '—'
def num(v):
    if v is None: return None
    t = str(v).replace(',', '').replace('≈', '').replace('~', '').replace('−', '-').strip()
    return float(t) if re.match(r'^[+\-]?\d+(\.\d+)?$', t) else None
def url_of(s):
    m = re.search(r'https?://\S+', s or ''); return m.group(0).rstrip('；;）)') if m else None
def slug(s):
    s = re.sub(r'https?://\S+', '', s or '').strip(' ；;（(')
    s = re.sub(r'[^\w一-鿿]+', '_', s).strip('_').lower()
    return ('src_' + s[:48]) if s else 'src_unknown'
def src_name(s): return re.sub(r'https?://\S+', '', s or '').strip(' ；;')[:200]

# ---------- 来源类型（doc23 kind）----------
def kind_of(name, url):
    t = (name + ' ' + (url or '')).lower()
    if 'sec.gov' in t or '交易所' in t or '巨潮' in t or 'cninfo' in t or 'hkexnews' in t or '13f' in t: return 'exchange_filing'
    if 'ir' in t and ('press' in t or 'release' in t) or 'shareholder letter' in t or 'newsroom' in t or 'nvidianews' in t or 'globenewswire' in t: return 'ir_release'
    if '电话会' in t or 'transcript' in t: return 'call_transcript'
    if 'bis.gov' in t or 'govinfo' in t or 'white house' in t or 'iea' in t or '海关' in t: return 'official'
    if 'doj' in t or 's.d.n.y' in t or '法院' in t: return 'court'
    if 'blog' in t or 'x.ai/news' in t or 'anthropic.com/news' in t or 'openai' in t and 'changelog' in t or '定价' in t or 'pricing' in t: return 'company_blog'
    if 'api' in t or 'epoch.ai' in t or 'artificialanalysis' in t or 'arcprize' in t or 'arena.ai' in t or 'swebench' in t or 'openrouter' in t or 'huggingface' in t: return 'data_aggregator'
    if 'techcrunch' in t or 'bloomberg' in t or 'reuters' in t or 'cnbc' in t or 'yahoo' in t or 'pymnts' in t or 'dealroom' in t or 'fortune' in t or 'fool' in t or 'newcomer' in t or 'globe and mail' in t or '媒体' in t or '转述' in t or '镜像' in t or 'wikipedia' in t or 'sacra' in t: return 'news_media'
    return None
SOURCE_OVERRIDE = [('businesswire.com','blocked','confirmed','403 → SEC'),('federalregister.gov','blocked','confirmed','302 → govinfo'),('cnbc.com','blocked','pending','403'),('reuters.com','blocked','pending','不可访问'),
       ('新浪镜像','open','pending','巨潮原链待补'),('电话会转述','open','pending','钉 transcript'),('OpenRouter','open','pending','我方抽核截断，待复核'),('semisino','open','pending','回研报 / 协会'),
       ('海关总署','open','placeholder','系数 C1 未标定'),('SemiAnalysis','paywall','pending','免费只定性'),('PitchBook','paywall','pending','免费只定性')]
def override_of(text):
    for pat, acc, vs, note in SOURCE_OVERRIDE:
        if pat in text: return acc, vs, note
    return ('open', 'confirmed', None)

# ---------- 路由（接入 → 四类 fct）：数据类优先，再看记录类型 ----------
def route(r, dc):
    dc = dc or ''
    if r['obs_type'] == 'position': return 'position'
    if r['obs_type'] in ('actual','prior','guidance','target','computed'):
        if dc.startswith('4'): return 'frontier'
        if dc.startswith('3'): return 'opinion'
        if num(r['value']) is not None or dc.startswith('1'): return 'quant'
        return 'quant' if '1' in dc else 'event'
    if r['obs_type'] == 'event': return 'event'
    if dc.startswith('4'): return 'frontier'
    if dc.startswith('3') or r['metric_id'] in ('m_nbis_calltone', 'm_reconcile_nbis'): return 'opinion'
    return 'event'
def event_type_of(r):
    t = (r['value'] + ' ' + (r['note'] or '') + ' ' + r['metric_id']).lower()
    if '融资' in t or 'series' in t or 'funding' in t or '要约' in t: return 'funding'
    if '合同' in t or 'contract' in t or '协议' in t or 'po ' in t or 'agreement' in t: return 'contract'
    if '投资' in t or 'invest' in t: return 'investment'
    if re.search(r'\bbis\b', t) or 'regulation' in t or '最终规则' in t or ('公告' in t and '232' in t) or 'policy' in t or '出口管制' in t: return 'policy'
    if '诉讼' in t or 'doj' in t or 'statement of interest' in t or 'summary judgment' in t: return 'litigation'
    if '降价' in t or '促销' in t or '涨价' in t or '定价' in t: return 'pricing'
    if 'ceo' in t or '人事' in t: return 'personnel'
    if '推出' in t or '发布' in t or 'launch' in t: return 'launch'
    return 'other'
def amount_type_of(r):
    t = (r['value'] + ' ' + (r['note'] or '') + ' ' + (r['unit'] or ''))
    if 'multi_year' in t or 'multi-year' in t or '承诺' in t or 'backlog' in t.lower(): return 'multi_year_cap'
    if 'annualized' in t or 'ARR' in t or '年化' in t: return 'annualized'
    if '–' in r['value'] or '-' in r['value'] and re.search(r'\d\s*[–-]\s*\d', r['value']): return 'range'
    return 'one_time' if num(r['value']) is not None else None

def fct_row(r, dc, ent):
    """一条接入记录 → (目标表, 行字典)。r = stg_observation 形状的 dict。"""
    dest = route(r, dc)
    kt, kd, sid, url = r['knowledge_time'], kdate(r['knowledge_time']), slug(r['source']), url_of(r['source'])
    qm = re.search(r'[“"]([^”"]{6,})[”"]', r['note'] or ''); anchor = qm.group(1) if qm else None
    prov = prov_norm(r['provenance']); unit = r['unit'] or ''
    cur = unit[:3] if unit[:3] in ('USD','CNY','HKD','EUR') else None
    st = 'pass' if prov == 'P1' else 'pending'
    if dest == 'quant':
        v = num(r['value']); yoy = None
        mm = re.search(r'YoY\s*([+\-−]?\d+(\.\d+)?)%', r['note'] or '')
        if mm: yoy = float(mm.group(1).replace('−','-')) / 100
        return 'fct_quant', dict(record_id=r['record_id'], metric_id=r['metric_id'], entity_id=ent, anchor=anchor, obs_type=r['obs_type'], period=r['period'], value=v, value_text=(None if v is not None else r['value']), unit=unit, currency=cur, yoy=yoy,
                      revision_flag=('revised' if r['obs_type']=='guidance' and '上调' in (r['note'] or '') else 'initial'), knowledge_time=kt, knowledge_date=kd, source_id=sid, source_url=url, provenance=prov,
                      owner=('A' if prov=='P1' and r['obs_type'] in ('actual','prior') else 'B'), status=st, note=r['note'])
    if dest == 'event':
        a = num(r['value'])
        return 'fct_event', dict(record_id=r['record_id'], metric_id=r['metric_id'], entity_id=ent, anchor=anchor, event_type=event_type_of(r), subject_entity=r['entity'], amount=a, amount_text=(None if a is not None else r['value']), currency=cur,
                        amount_type=amount_type_of(r), is_estimate=(r['obs_type'] in ('guidance','target') or 'is_estimate' in (r['note'] or '')), event_date=(kdate(r['period']) or kd), event_date_text=r['period'],
                        knowledge_time=kt, knowledge_date=kd, source_id=sid, source_url=url, provenance=prov, owner='B', status=st, note=r['note'])
    if dest == 'opinion':
        return 'fct_opinion', dict(record_id=r['record_id'], metric_id=r['metric_id'], entity_id=ent, anchor=anchor, variable=(unit if unit not in ('','—') else r['metric_id']), speaker=r['entity'],
                       speaker_role=('management' if 'NBIS' in r['entity'] or '管理层' in r['entity'] else None), anchor_quote=r['value'], knowledge_time=kt, knowledge_date=kd, source_id=sid, source_url=url, provenance=prov, owner='B', status=st, note=r['note'])
    if dest == 'frontier':
        sc = num(r['value']); third = any(k in r['source'] for k in ('Epoch','Artificial Analysis','ARC','arena','swebench'))
        return 'fct_frontier', dict(record_id=r['record_id'], metric_id=r['metric_id'], entity_id=ent, anchor=anchor, benchmark=(unit if unit not in ('','—') else None), score=sc, score_text=(None if sc is not None else r['value']), institution=r['entity'],
                       source_stance=('neutral' if third or 'Hugging' in r['source'] else None), verifiability=('third_party_verified' if third else None), knowledge_time=kt, knowledge_date=kd, source_id=sid, source_url=url, provenance=prov, owner='B', status=st, note=r['note'])
    return 'fct_position', dict(record_id=r['record_id'], metric_id=r['metric_id'], ticker=r['entity'], period=r['period'], weight=r['value'], note=r['note'], knowledge_time=kt, knowledge_date=kd, source_id=sid, provenance=prov)

def insert_rows(con, table, rows):
    if not rows: return
    cols = list(rows[0].keys())
    con.executemany(f'INSERT INTO {table} ({",".join(cols)}) VALUES ({",".join(["?"]*len(cols))})', [tuple(d[c] for c in cols) for d in rows])

# ---------- 字段类型转换（按 information_schema）----------
def column_types(con):
    return {(t, c): d for (t, c, d) in con.execute("SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema='main'").fetchall()}
def cast(types, t, c, v):
    d = types.get((t, c), 'VARCHAR')
    if v is None or v == '': return None
    if isinstance(v, (int, float, dt.date, bool)): return v
    if d in ('DOUBLE', 'FLOAT', 'DECIMAL'): return float(v)
    if d in ('INTEGER', 'BIGINT'): return int(float(v))
    if d == 'DATE': return kdate(v)
    if d == 'BOOLEAN': return str(v).lower() in ('1', 'true', 'yes', 'y')
    return v

# ---------- 来源主表 upsert（从记录派生；access / verify_status 由 source_override 覆盖）----------
def upsert_source(con, r, dc, mcls_of_metric=None):
    sid = slug(r['source']); name = src_name(r['source']); url = url_of(r['source']); prov = prov_norm(r['provenance']); kd = kdate(r['knowledge_time'])
    tier = prov if prov in ('P1','P2','P3','P4','P5') else None
    row = con.execute('SELECT source_tier, data_class, covers_entity, covers_metric, first_seen FROM source_master WHERE source_id = ?', [sid]).fetchone()
    if row is None:
        acc, vs, note = override_of(name + ' ' + (url or ''))
        con.execute('INSERT INTO source_master VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            [sid, name, None, tier, kind_of(name, url), json.dumps([dc or ''], ensure_ascii=False), json.dumps([r['entity']], ensure_ascii=False), json.dumps([r['metric_id']], ensure_ascii=False), url, acc, None, note, vs, None, kd, dt.date.today()])
        return sid, True
    t0, cls, ents, mets, fs = row
    merge = lambda js, v: json.dumps(sorted(set(json.loads(js or '[]')) | {v}), ensure_ascii=False)
    tier2 = min([x for x in (t0, tier) if x]) if (t0 or tier) else None
    con.execute('UPDATE source_master SET source_tier=?, data_class=?, covers_entity=?, covers_metric=?, first_seen=?, last_validated=? WHERE source_id=?',
        [tier2, merge(cls, dc or ''), merge(ents, r['entity']), merge(mets, r['metric_id']), min([d for d in (fs, kd) if d]) if (fs or kd) else None, dt.date.today(), sid])
    return sid, False
