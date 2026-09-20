# -*- coding: utf-8 -*-
"""库浏览器：从库生成单文件 HTML（schema 字典 + 每张表 / 视图的全部数据 + 表间关系 + 计算规则 + 改库账），离线可开、可搜索、id 可跳转。
用法（pipeline/ 下）：python3 gen_browser.py [库路径]  → schema_browser.html
与 SCHEMA.md 同源（schema_doc / relation_doc / calc_rule），区别是把「字段定义」和「按该定义收集到的值」放在同一屏。"""
import duckdb, os, sys, json, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
DB = sys.argv[1] if len(sys.argv) > 1 else (os.environ.get('ANATOLE_DB') or os.path.join(HERE, 'anatole_ai_monitor.duckdb'))
OUT = os.path.join(HERE, 'schema_browser.html')
con = duckdb.connect(DB, read_only=True)
LAYERS = [
  ('接入层', '人 / agent 的登记格式：一行一个事实', ['stg_observation']),
  ('资产层 · doc21', '实体两轴 · 指标定义 R · 边 E · 四类事实 fct + 仓位 · 来源', ['entity_master','entity_ticker_map','metric_entity','metric_registry','edge_registry','fct_quant','fct_event','fct_opinion','fct_frontier','fct_position','source_master','source_override']),
  ('治理层 · 判断表', '判断 ≠ 数据：各自带 owner / status', ['assumption','coefficient','metric_factor','observation_direction','key_fact','calendar','calendar_metric']),
  ('元数据层', '字典 / 关系 / 规则 / 改库账', ['schema_doc','relation_doc','calc_rule','migration_log','change_log','etl_log']),
  ('思路层 · 元数据', '主线 → 分叉 → 产物；v_column_origin 反查', ['thesis_node','decision_fork','artifact_anchor','v_column_origin']),
  ('视图 · 可推导的一律作视图', 'doc21 §四 两视图 + 打分 + 数据岗', ['v_signal_latest','v_ticker_map','v_early_signal','v_metric_latest','v_metric_score','v_edge_scored','v_edge_calc','v_ticker_weight','v_metric_headline','v_metric_guidance','v_metric_prior','v_metric_position','v_obs','v_fct','v_entity','v_health','v_review_due','v_source_master','v_calendar','v_schema_coverage']),
]
TDESC = {
 'stg_observation': '登记记录（= 原 13-观测记录.csv 的形状）。record_id 主键；routed_to 记路由去向。只增不改，纠错用新行 + superseded_by。',
 'entity_master': 'doc21 §一 实体主表：layer L1–L6 × maturity 两轴；in_book 标是否在 13F 书里。',
 'entity_ticker_map': '实体 → 公开票映射（doc18 补丁③ map_path）；weight_override 可覆盖规则权重。',
 'metric_entity': '指标挂实体（N:M）。', 'metric_registry': '真源 R：指标只存定义（口径 / 单位 / 频率 / 来源 / 依赖 / 可得性 / 下次发布），不存值；值在 fct_*。',
 'edge_registry': '真源 E：六类边 × 跳数 × T1–T3；mechanism / evidence_ids / cert_score / lead_measured；记录分数与规则算分在 v_edge_calc 对账。',
 'fct_quant': '类1 量价：数值 / 期间 / 同比环比 / 修订 / 换算假设 + doc17 通用元数据。', 'fct_event': '类2 实体事件：类型 / 主客体 / 金额与金额类型 / 是否估计。',
 'fct_opinion': '类3 观点 / 表述：变量 / 发言人 / 分级 / 强度 / 方向 / codebook 版本。', 'fct_frontier': '类4 前沿 / 知识：榜单 / 分数 / 机构 + doc29 两道闸（source_stance / verifiability / industry_impact）。',
 'fct_position': '13F 仓位事实（本体，不属四类）。', 'source_master': 'doc23 来源总账：tier / kind / 覆盖 / access / verify_status；从记录派生，override 覆盖。', 'source_override': '来源访问状态的人工覆盖。',
 'assumption': 'doc30 假设台账（状态机 assumption → calibrating → validated → retired）。', 'coefficient': 'A1–A8 的系数，视图读这里；改一处全部分数跟着变。',
 'metric_factor': '节点五因子 r/e/l/s/φ（doc21 §6.1），B 规则初稿，D 复核。', 'observation_direction': '每条记录的方向判断（A11）：↑↓→!—。', 'key_fact': '有作者的简报：前因 / 关键数据 / 相关方 / 后果 + 关注 + 一句话现状 + 证伪条件。',
 'calendar': '排期（日期依据类型：公司公告 / 规则推定 / 估计 / 待定）。', 'calendar_metric': '排期挂指标。',
 'schema_doc': '字段字典：每列含义 / 设计出处 / 是否可推导。库里每列必有一条（checks 校验）。', 'relation_doc': '表间关系。', 'calc_rule': '计算规则 R1–R14：公式 / 输入 / 输出视图 / 挂哪些假设。',
 'migration_log': '改库记录：每个 migrations/ 脚本一行，checksum 锁定。', 'change_log': '字段级改动账：表 / 行 / 列 / 改前 / 改后 / 依据 / owner / 时间。', 'etl_log': '建库各步骤行数。',
 'v_signal_latest': '视图 A「AI 发展监测树」：按 dim 组织，节点最近方向。', 'v_ticker_map': '视图 B「持仓蝴蝶结」：按 to_ticker 组织边 + 节点最近状态。', 'v_early_signal': '早期信号层（doc16 三子流作视图）。',
 'v_metric_latest': 'registry + 推导值（标题值 / 指引 / 上期 / 仓位 / 节点分），看板基础。', 'v_metric_score': 'R1 valuable_score。', 'v_edge_scored': '边 + 记录分数数值化 + tier 归一。', 'v_edge_calc': 'R2–R6：c / τ / tradable / warning 规则算分，并与记录分数对账（reconcile_flag）。',
 'v_ticker_weight': 'R7 每票上游边归一权重（weight_override 优先）。', 'v_metric_headline': '每指标标题值。', 'v_metric_guidance': '每目标期间最新一版指引。', 'v_metric_prior': '每指标最近上期值。', 'v_metric_position': '每指标最近仓位。',
 'v_obs': '登记记录 + 方向 + 路由去向（不含被取代行）。', 'v_fct': '四类 fct 合回通用形状。', 'v_entity': '实体 + 指标数。', 'v_health': '数据岗健康：过期 / 缺记录 / 标记。', 'v_review_due': '复验队列（P2–P5）。', 'v_source_master': '来源 + 引用数。', 'v_calendar': '排期 + 简报。', 'v_schema_coverage': '每表每列有值率。',
 'thesis_node': '一级：核心思考主线，7 个节点（认知 7±2），每节点合并若干思维链环。', 'decision_fork': '二级：关键决策分叉，只记有取舍的熵减点；weight=core 面试主讲，detail 折叠。', 'artifact_anchor': '三级：决策落到库里的产物（表 / 列 / 视图 / 规则 / 假设 / 校验），思路 → 数据方向。', 'v_column_origin': '数据 → 思路方向：某表 / 某列来自哪个节点、哪个决策。',
}
def ser(v):
    if v is None: return None
    if isinstance(v, dt.datetime): return v.isoformat(sep=' ')[:19]
    if isinstance(v, dt.date): return v.isoformat()
    if isinstance(v, float): return round(v, 6)
    return v
doc = {}
for (t, c, m, ref, der, view) in con.execute('SELECT table_name, column_name, meaning, design_ref, derivable, served_by_view FROM schema_doc ORDER BY rowid').fetchall(): doc.setdefault(t, {})[c] = (m, ref, der, view)
tables = {}
for layer, _, names in LAYERS:
    for t in names:
        try: cur = con.execute(f'SELECT * FROM "{t}"')
        except Exception as ex: tables[t] = dict(kind='view', n=0, cols=[], rows=[], error=str(ex)[:200]); continue
        cols = [d[0] for d in cur.description]; types = [str(d[1]) for d in cur.description]
        rows = [[ser(v) for v in r] for r in cur.fetchall()]
        n = len(rows); fills = [sum(1 for r in rows if r[i] not in (None, '')) for i in range(len(cols))]
        cdefs = []
        for i, c in enumerate(cols):
            m, ref, der, view = doc.get(t, {}).get(c, (None, None, None, None))
            cdefs.append(dict(name=c, type=types[i], meaning=m, ref=ref, derivable=bool(der), view=view, fill=fills[i]))
        tables[t] = dict(kind='view' if t.startswith('v_') else 'table', n=n, cols=cdefs, rows=rows, desc=TDESC.get(t, ''))
rel = [dict(zip(['from_table','from_col','to_table','to_col','card','meaning'], r)) for r in con.execute('SELECT * FROM relation_doc ORDER BY rowid').fetchall()]
rules = [dict(zip(['id','name','formula','inputs','output_view','assumptions','ref','note'], [ser(x) for x in r])) for r in con.execute('SELECT * FROM calc_rule ORDER BY rowid').fetchall()]
mig = [dict(zip(['id','applied_at','checksum','owner','n','note'], [ser(x) for x in r])) for r in con.execute('SELECT migration_id, applied_at, checksum, owner, n_changes, note FROM migration_log ORDER BY 1').fetchall()]
as_of = str(con.execute('SELECT max(knowledge_date) FROM v_fct').fetchone()[0])
# 思路层：主线 → 分叉 → 产物；origin = 每个表 / 列的反向锚点
nodes = [dict(zip(['node_id','seq','title','question','conclusion','rings','doc_refs','owner','status'], [ser(x) for x in r])) for r in con.execute('SELECT node_id, seq, title, question, conclusion, rings, doc_refs, owner, status FROM thesis_node ORDER BY seq').fetchall()]
forks = [dict(zip(['fork_id','node_id','seq','question','options','chosen','rationale','before_after','weight','log_ref','owner','status'], [ser(x) for x in r])) for r in con.execute('SELECT fork_id, node_id, seq, question, options, chosen, rationale, before_after, weight, log_ref, owner, status FROM decision_fork ORDER BY node_id, seq').fetchall()]
for f in forks: f['options'] = json.loads(f['options'])
anchors = [dict(zip(['anchor_id','fork_id','kind','ref','how'], r)) for r in con.execute('SELECT anchor_id, fork_id, kind, ref, how FROM artifact_anchor ORDER BY anchor_id').fetchall()]
origin = {}
for r in con.execute('SELECT ref, kind, node_id, node_title, fork_id, fork_question, chosen, how FROM v_column_origin').fetchall():
    origin.setdefault(r[0], []).append(dict(kind=r[1], node_id=r[2], node_title=r[3], fork_id=r[4], fork_question=r[5], chosen=r[6], how=r[7]))
data = dict(thesis=dict(nodes=nodes, forks=forks, anchors=anchors, origin=origin), db=os.path.basename(DB), as_of=as_of, generated=dt.datetime.now().strftime('%Y-%m-%d %H:%M'), layers=[dict(name=a, desc=b, tables=c) for a, b, c in LAYERS], tables=tables, relations=rel, rules=rules, migrations=mig,
            n_records=con.execute('SELECT count(*) FROM stg_observation').fetchone()[0], n_visible=con.execute('SELECT count(*) FROM v_obs').fetchone()[0], n_changes=con.execute('SELECT count(*) FROM change_log').fetchone()[0])
payload = json.dumps(data, ensure_ascii=False, default=str).replace('</', '<\\/')
html = open(os.path.join(HERE, 'browser_template.html'), encoding='utf-8').read().replace('__DATA__', payload)
open(OUT, 'w', encoding='utf-8').write(html); print('written', OUT, len(html) // 1024, 'KB;', len(tables), 'tables/views')
