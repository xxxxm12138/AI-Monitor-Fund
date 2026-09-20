# -*- coding: utf-8 -*-
"""0010 · 决策层 DDL：decision_registry / decision_log / candidate_pool 三张表 + 字典 + 关系 + R15–R17 · owner B · 2026-09-20
上游：pipeline/JEV-intelligence-graph.md §四（三块增量）· pipeline/PLAN-decision-layer.md P1（P0 已拍板：四个开放问题均按 B 建议）。
判断成为与 R（指标）、E（边）并列的一等公民：registry 登记每类重复判断的 I/O 契约，decision_log 记六元组过程账，candidate_pool 承接 PROPOSE。
幂等设计：DDL 用 CREATE TABLE IF NOT EXISTS（与 schema.sql 同文）；字典 / 关系 / 规则用 INSERT OR REPLACE（fresh init 由 metadata.py 提供同样内容，
本脚本重放时幂等覆盖）——增量路径（现库）与从零重建（init_db --force + migrate）两条路径结果一致。
配套代码（非本脚本）：core.py PK 注册、migrate.py m.decide() 与 observe 人工改判钩子、views.sql 三视图、checks.py 规则 7j–7o。"""
OWNER = 'B'
REF_P, REF_J = 'PLAN-decision-layer §二', 'JEV-intelligence-graph §四'

DDL = [
"""CREATE TABLE IF NOT EXISTS decision_registry (
  decision_id      TEXT PRIMARY KEY,
  name             TEXT NOT NULL,
  question         TEXT NOT NULL,
  state_schema     TEXT NOT NULL,
  candidates       TEXT NOT NULL,
  output_home      TEXT,
  executor_kind    TEXT NOT NULL CHECK (executor_kind IN ('rule','human','llm','model')),
  executor         TEXT NOT NULL,
  freq_est         TEXT,
  escalation       TEXT,
  calib_status     TEXT NOT NULL CHECK (calib_status IN ('human','shadow','assisted','auto')),
  assumption_ids   TEXT,
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired')),
  design_ref       TEXT,
  notes            TEXT
)""",
"""CREATE TABLE IF NOT EXISTS decision_log (
  dec_id           TEXT PRIMARY KEY,
  decision_id      TEXT NOT NULL REFERENCES decision_registry(decision_id),
  target_table     TEXT,
  target_pk        TEXT,
  target_column    TEXT,
  state_anchor     TEXT,
  candidates_shown TEXT,
  choice           TEXT NOT NULL,
  confidence       DOUBLE CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
  executor_kind    TEXT CHECK (executor_kind IS NULL OR executor_kind IN ('rule','human','llm','model')),
  executor         TEXT,
  escalated        BOOLEAN DEFAULT FALSE,
  basis            TEXT NOT NULL,
  decided_at       TIMESTAMP DEFAULT current_timestamp,
  retro            BOOLEAN DEFAULT FALSE,
  outcome          TEXT CHECK (outcome IS NULL OR outcome IN ('correct','wrong','mixed','unresolved')),
  outcome_basis    TEXT,
  outcome_at       DATE,
  note             TEXT
)""",
"""CREATE TABLE IF NOT EXISTS candidate_pool (
  cand_id          TEXT PRIMARY KEY,
  decision_id      TEXT NOT NULL REFERENCES decision_registry(decision_id),
  trigger_ref      TEXT NOT NULL,
  kind             TEXT NOT NULL CHECK (kind IN ('explanation','new_edge','new_edge_type','new_metric','new_assumption')),
  candidate_text   TEXT NOT NULL,
  proposed_by      TEXT NOT NULL,
  status           TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','selected','rejected','merged')),
  created_at       DATE,
  resolved_by      TEXT,
  note             TEXT
)"""]

DICT = {  # 与 metadata.py 同文（表 → {列: (含义, 设计出处)}）
'decision_registry': {'decision_id': ('判断类型主键 d_*', REF_P), 'name': ('名称', REF_P), 'question': ('这类判断在问什么（一句）', REF_P),
  'state_schema': ('输入 state 由哪些表列 / 视图构成（= 未来专用模型的输入契约）', REF_J + '.1'), 'candidates': ('候选词表 JSON 数组（= 输出契约）；开放候选 = open→candidate_pool', REF_J + '.1'),
  'output_home': ('判断结果写回哪张表哪列（表.列；复合列 + 连接；只落 decision_log 则空）', REF_P), 'executor_kind': ('rule / human / llm / model', REF_P), 'executor': ('A–D / 规则名 / 模型名', 'doc09'),
  'freq_est': ('发生频率量级', REF_P), 'escalation': ('升级规则：首版 = 现状描述，数值阈值挂 C9', 'PLAN-decision-layer §六 Q3'), 'calib_status': ('human → shadow → assisted → auto（doc30 状态机平移）', REF_J + '.2'),
  'assumption_ids': ('挂的假设', 'doc30'), 'owner': ('A–D', 'doc09'), 'status': ('draft / reviewed / retired', '实现'), 'design_ref': ('设计出处', '元数据'), 'notes': ('说明', '实现')},
'decision_log': {'dec_id': ('判断实例 id = migration_id-dec 序号', REF_P), 'decision_id': ('哪类判断', REF_P), 'target_table': ('判断对象所在表', REF_P), 'target_pk': ('对象主键', REF_P), 'target_column': ('列级判断的列', REF_P),
  'state_anchor': ('判断时刻输入的引用 JSON（record_id 集合 + as_of），判断可复现', REF_J + '.2'), 'candidates_shown': ('判断时刻 registry.candidates 快照', REF_P), 'choice': ('选择', REF_P),
  'confidence': ('置信度 0–1；人按 H/M/L 写映射 .9/.6/.3（C11）', 'PLAN-decision-layer §六 Q1'), 'executor_kind': ('rule / human / llm / model', REF_P), 'executor': ('本次判断的执行者', 'doc09'), 'escalated': ('是否从默认执行者升级（R16 分子）', REF_P),
  'basis': ('依据（六元组之一）', 'doc14 A1 可溯源'), 'decided_at': ('判断时间', '实现'), 'retro': ('回填行：confidence 允许空，禁止编造', 'PLAN-decision-layer P3'), 'outcome': ('事后对错 correct / wrong / mixed / unresolved', REF_J + '.2'),
  'outcome_basis': ('回填依据', 'PLAN-decision-layer §六 Q4'), 'outcome_at': ('回填日期', '实现'), 'note': ('说明', '实现')},
'candidate_pool': {'cand_id': ('候选 id', REF_P), 'decision_id': ('属于哪类判断（通常 d_divergence_explain）', REF_P), 'trigger_ref': ('触发对象 record:<id> / ticker:<t> / metric:<id>，与 v_divergence.div_key 对齐', REF_J + '.3'),
  'kind': ('explanation / new_edge / new_edge_type / new_metric / new_assumption', REF_J + '.3'), 'candidate_text': ('候选内容', REF_P), 'proposed_by': ('A–D / llm', 'doc09'),
  'status': ('open / selected / rejected / merged：选中前不是结论', 'PLAN-decision-layer F-b'), 'created_at': ('提出日期', '实现'), 'resolved_by': ('选中 / 否决它的判断（decision_log.dec_id）', REF_P), 'note': ('说明', '实现')},
}
RELS = [  # 与 metadata.py RELATIONS 同文
  ('decision_log','decision_id','decision_registry','decision_id','N:1','每次判断属于登记过的一类判断'),
  ('decision_log','(target_table, target_pk)','任意资产 / 治理表','主键','N:1','判断结果写回的家（output_home）；choice 与家中现值由校验对账'),
  ('candidate_pool','decision_id','decision_registry','decision_id','N:1','候选属于哪类判断（通常 d_divergence_explain）'),
  ('candidate_pool','resolved_by','decision_log','dec_id','N:1','选中 / 否决该候选的那次判断'),
]
RULES = [  # 与 metadata.py CALC_RULES 同文
  ('R15','校准误差','calib_error = |bucket 命中率 − bucket 置信度|（按 decision_id × round(confidence,1) 分桶；只统计 outcome ∈ correct/wrong）','decision_log','v_calibration','C10,C11','PLAN-decision-layer §五','校准未 validated 的决策类型禁标 assisted / auto（🟠闸扩展）'),
  ('R16','升级率','escalation_rate = 升级次数（escalated）/ 判断次数，按 decision_id','decision_log','v_decision_health','C9','PLAN-decision-layer §五','越低说明下层执行者越可信'),
  ('R17','背离判定','① 记录级：最新未取代观测 direction=! ｜ ② 票级：同票供给侧与需求侧最新方向相反（布尔版；数值阈值待 C6）','v_obs × edge_registry × candidate_pool','v_divergence','C6','JEV-intelligence-graph §四.3','背离 = PROPOSE 触发器：超 7 天无候选记 WARN'),
]

def up(m):
    for ddl in DDL:
        m.sql(ddl, basis=REF_P + '（与 schema.sql 同文，IF NOT EXISTS 幂等）')
    for t, cols in DICT.items():
        for c, (mean, ref) in cols.items():
            m.sql('INSERT OR REPLACE INTO schema_doc VALUES (?,?,?,?,false,NULL)', basis='字典同步（fresh init 由 metadata.py 提供，此处幂等覆盖）', params=[t, c, mean, ref])
    for row in RELS:
        m.sql('INSERT OR REPLACE INTO relation_doc VALUES (?,?,?,?,?,?)', basis='关系字典同步', params=list(row))
    for row in RULES:
        m.sql('INSERT OR REPLACE INTO calc_rule VALUES (?,?,?,?,?,?,?,?)', basis='计算规则 R15–R17（输出视图在 views.sql）', params=list(row))
