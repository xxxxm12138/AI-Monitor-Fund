-- ============================================================================
-- Anatole · AI 发展监测体系 · 资产层 schema v2（DuckDB 实例化；生产设计 = doc 21 Postgres DDL）
-- 分层：接入 stg_* → 资产（doc21）entity / metric / edge / fct_* / source → 治理（判断表）→ 元数据（字典 / 关系 / 规则）→ 视图（views.sql）
-- 原则（doc21 §〇）：表只存不可再推导的原子事实与人的判断；可推导的一律作视图。设计中为字段但可推导者，在 schema_doc 标 served_by_view。
-- 字段级说明不写在这里，写在 schema_doc 表（load 时灌入），SCHEMA.md 由它生成。
-- ============================================================================

-- ---------- 接入层 ----------
CREATE TABLE IF NOT EXISTS stg_observation (            -- 人 / agent 的登记格式：一行一个事实（= 13-观测记录.csv）
  record_id        TEXT PRIMARY KEY,
  metric_id        TEXT NOT NULL,
  entity           TEXT NOT NULL,
  obs_type         TEXT NOT NULL CHECK (obs_type IN ('actual','prior','guidance','target','event','state','position','computed')),
  value            TEXT NOT NULL,
  unit             TEXT,
  period           TEXT,
  knowledge_time   TEXT NOT NULL,
  source           TEXT NOT NULL,
  provenance       TEXT NOT NULL,
  note             TEXT,
  routed_to        TEXT                                 -- 路由到的资产表：fct_quant / fct_event / fct_opinion / fct_frontier / position
);

-- ---------- 资产层：实体（doc21 §一）----------
CREATE TABLE IF NOT EXISTS entity_master (
  entity_id        TEXT PRIMARY KEY,
  name             TEXT NOT NULL,
  aliases          TEXT,                                -- JSON 数组文本（Postgres: TEXT[]）
  type             TEXT CHECK (type IN ('company','institution','person','track','index')),
  layer            TEXT CHECK (layer IS NULL OR layer IN ('L1','L2','L3','L4','L5','L6')),
  maturity         TEXT CHECK (maturity IS NULL OR maturity IN ('research','private','pre_ipo','public')),
  track            TEXT,
  country          TEXT CHECK (country IS NULL OR country IN ('CN','US','HK','EU','other')),
  ticker           TEXT,
  parent_id        TEXT,
  in_book          BOOLEAN DEFAULT FALSE,
  created_at       TIMESTAMP DEFAULT current_timestamp,
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired'))
);
CREATE TABLE IF NOT EXISTS entity_ticker_map (          -- 实体 → 公开票（补丁③ map_path；weight 由 v_ticker_weight 推导，人可用 weight_override 覆盖）
  map_id           INTEGER PRIMARY KEY,
  entity_id        TEXT NOT NULL REFERENCES entity_master(entity_id),
  ticker           TEXT NOT NULL,
  relation         TEXT NOT NULL CHECK (relation IN ('self','supplier','customer','competitor','supply_chain_read','demand_driver')),
  map_path         TEXT,
  weight_override  DOUBLE,
  owner            TEXT CHECK (owner IN ('A','B','C','D')),
  status           TEXT CHECK (status IN ('draft','reviewed','retired'))
);
CREATE TABLE IF NOT EXISTS metric_entity (
  metric_id        TEXT NOT NULL,
  entity_id        TEXT NOT NULL REFERENCES entity_master(entity_id),
  PRIMARY KEY (metric_id, entity_id)
);

-- ---------- 资产层：指标（真源 R，doc21 §二）----------
CREATE TABLE IF NOT EXISTS metric_registry (
  metric_id        TEXT PRIMARY KEY,
  name             TEXT NOT NULL,
  entity_id        TEXT,                                -- 主实体（多实体见 metric_entity）
  ticker_or_entity TEXT NOT NULL,                       -- 登记时的实体 / 票标签（原文），映射见 metric_entity
  entry            TEXT NOT NULL CHECK (entry IN ('持仓','AI')),
  track            TEXT,
  layer            TEXT CHECK (layer IS NULL OR layer IN ('L1','L2','L3','L4','L5','L6')),
  dim              TEXT,                                -- D1–D7（doc24v2），可 'D1/D7'
  data_class       TEXT,                                -- 1 量价 2 事件 3 观点 4 前沿，可 '1/3'
  signal_role      TEXT,                                -- predictor / expectation_base / regime / arbiter / human_input
  source_ids       TEXT,                                -- JSON 数组文本 → source_master
  source_family    TEXT,
  frequency        TEXT,
  lead_time_est    TEXT,                                -- 补丁④ 领先期先验（假设 B*）
  kou_jing         TEXT,                                -- 口径定义
  unit             TEXT,
  owner            TEXT CHECK (owner IN ('A','B','C','D','A/B','B/C','B/D','C/D')),
  upstream_deps    TEXT,                                -- JSON 数组文本
  availability     TEXT,                                -- 🟢🟡🔵⚪
  next_release     TEXT,
  next_release_basis TEXT,
  status           TEXT,                                -- testing / production / deprecated（实现中暂用填数状态词表）
  fill_status      TEXT,
  notes_assumption_ids TEXT,
  last_validated   DATE
);

-- ---------- 资产层：边（真源 E，doc21 §二.5 + doc25 §六）----------
CREATE TABLE IF NOT EXISTS edge_registry (
  edge_id          TEXT PRIMARY KEY,
  from_metric      TEXT NOT NULL REFERENCES metric_registry(metric_id),
  to_ticker        TEXT NOT NULL,
  side             TEXT NOT NULL CHECK (side IN ('supply','demand','regime','compete','self')),
  edge_type        TEXT NOT NULL CHECK (edge_type IN ('E1_self','E2_supplier','E3_customer','E4_competitor','E5_theme','E6_flow')),
  hops             INTEGER NOT NULL CHECK (hops BETWEEN 0 AND 4),
  map_path         TEXT,                                -- 中间机制节点（'→' 分隔）；跳数 = 中间节点数 + 1
  mechanism        TEXT,
  cert_tier        TEXT NOT NULL,                       -- T1 可回测 / T2 结构对账 / T3 方向（可带 候选 / 提议）
  cert_method      TEXT,
  cert_score       DOUBLE,                              -- 验证得分（回测 / 对账写回）
  lead_measured    TEXT,                                -- 实测领先期（Postgres: INTERVAL）
  tradable_recorded TEXT,                               -- 记录的可交易度（doc28 手写 / 早期计算），与 v_edge_calc 对账
  warning_recorded  TEXT,
  is_key           TEXT,
  evidence_ids     TEXT,                                -- JSON 数组文本（record_id / trace id）
  evidence         TEXT,
  owner            TEXT CHECK (owner IN ('A','B','C','D')),
  status           TEXT CHECK (status IN ('testing','production','deprecated')),
  notes            TEXT,
  last_validated   DATE
);

-- ---------- 资产层：四类 fct（doc21 §三 + doc17 §2.1 通用元数据 + doc18 四补丁 + doc29 前沿字段）----------
-- 通用元数据（每张 fct 都有）：record_id · metric_id · entity_id · knowledge_time / knowledge_date · source_id · source_url · anchor · snapshot_id · ingest_time · owner · confidence · code_score · judge_score · status · superseded_by · provenance
CREATE TABLE IF NOT EXISTS fct_quant (                  -- 类1 量价
  record_id        TEXT PRIMARY KEY,
  metric_id        TEXT NOT NULL REFERENCES metric_registry(metric_id),
  entity_id        TEXT,
  obs_type         TEXT NOT NULL CHECK (obs_type IN ('actual','prior','guidance','target','computed')),
  period           TEXT,
  period_start     DATE,
  period_end       DATE,
  value            DOUBLE,
  value_text       TEXT,                                -- 无法数值化的原文（区间 / ≈ / ±）
  unit             TEXT,
  currency         TEXT,
  yoy              DOUBLE,
  qoq              DOUBLE,
  revision_flag    TEXT CHECK (revision_flag IS NULL OR revision_flag IN ('initial','revised')),
  conversion_assumption TEXT,                           -- 补丁①
  assumption_source TEXT,
  knowledge_time   TEXT NOT NULL,
  knowledge_date   DATE,
  source_id        TEXT,
  source_url       TEXT,
  anchor           TEXT,                                -- 原文锚点 / 短引
  snapshot_id      TEXT,
  ingest_time      TIMESTAMP DEFAULT current_timestamp,
  provenance       TEXT NOT NULL,
  owner            TEXT,
  confidence       DOUBLE,
  code_score       TEXT,                                -- JSON 文本（Postgres: JSONB）
  judge_score      DOUBLE,
  status           TEXT,
  superseded_by    TEXT,
  note             TEXT
);
CREATE TABLE IF NOT EXISTS fct_event (                  -- 类2 实体事件
  record_id        TEXT PRIMARY KEY,
  metric_id        TEXT NOT NULL REFERENCES metric_registry(metric_id),
  entity_id        TEXT,
  event_type       TEXT CHECK (event_type IS NULL OR event_type IN ('funding','launch','personnel','order','approval','contract','policy','litigation','investment','pricing','other')),
  subject_entity   TEXT,
  object_entity    TEXT,
  relation         TEXT,
  amount           DOUBLE,
  amount_text      TEXT,
  currency         TEXT,
  amount_type      TEXT CHECK (amount_type IS NULL OR amount_type IN ('one_time','multi_year_cap','annualized','range')),   -- 补丁②
  is_estimate      BOOLEAN DEFAULT FALSE,
  round            TEXT,
  event_date       DATE,
  event_date_text  TEXT,
  knowledge_time   TEXT NOT NULL,
  knowledge_date   DATE,
  source_id        TEXT,
  source_url       TEXT,
  anchor           TEXT,
  snapshot_id      TEXT,
  ingest_time      TIMESTAMP DEFAULT current_timestamp,
  provenance       TEXT NOT NULL,
  owner            TEXT,
  confidence       DOUBLE,
  status           TEXT,
  superseded_by    TEXT,
  note             TEXT
);
CREATE TABLE IF NOT EXISTS fct_opinion (                -- 类3 观点 / 表述
  record_id        TEXT PRIMARY KEY,
  metric_id        TEXT NOT NULL REFERENCES metric_registry(metric_id),
  entity_id        TEXT,
  variable         TEXT,
  speaker          TEXT,
  speaker_role     TEXT CHECK (speaker_role IS NULL OR speaker_role IN ('management','analyst_q','expert','media','official')),
  level            INTEGER,
  strength         TEXT,
  direction        TEXT,
  anchor_quote     TEXT,
  codebook_version TEXT,
  model_version    TEXT,
  knowledge_time   TEXT NOT NULL,
  knowledge_date   DATE,
  source_id        TEXT,
  source_url       TEXT,
  anchor           TEXT,
  snapshot_id      TEXT,
  ingest_time      TIMESTAMP DEFAULT current_timestamp,
  provenance       TEXT NOT NULL,
  owner            TEXT,
  code_score       TEXT,
  judge_score      DOUBLE,
  status           TEXT,
  superseded_by    TEXT,
  note             TEXT
);
CREATE TABLE IF NOT EXISTS fct_frontier (               -- 类4 前沿 / 知识（doc29 前沿雷达主表）
  record_id        TEXT PRIMARY KEY,
  metric_id        TEXT NOT NULL REFERENCES metric_registry(metric_id),
  entity_id        TEXT,
  doc_id           TEXT,
  topic_cluster    TEXT,
  method           TEXT,
  benchmark        TEXT,
  score            DOUBLE,
  score_text       TEXT,
  institution      TEXT,
  authors          TEXT,                                -- JSON 数组文本
  citation_velocity DOUBLE,
  source_stance    TEXT CHECK (source_stance IS NULL OR source_stance IN ('neutral','vendor_pr','social')),          -- doc29 证伪闸
  verifiability    TEXT CHECK (verifiability IS NULL OR verifiability IN ('reproducible','third_party_verified','claimed_only','rumor')),
  industry_impact  TEXT,                                -- doc29 影响力闸（高 / 中 / 低 + 评分；C8 占位）
  impact_rationale TEXT,
  knowledge_time   TEXT NOT NULL,
  knowledge_date   DATE,
  source_id        TEXT,
  source_url       TEXT,
  anchor           TEXT,
  snapshot_id      TEXT,
  ingest_time      TIMESTAMP DEFAULT current_timestamp,
  provenance       TEXT NOT NULL,
  owner            TEXT,
  status           TEXT,
  superseded_by    TEXT,
  note             TEXT
);
CREATE TABLE IF NOT EXISTS fct_position (               -- 13F 仓位（本体事实，不属四类；持仓侧需求锚）
  record_id        TEXT PRIMARY KEY,
  metric_id        TEXT NOT NULL REFERENCES metric_registry(metric_id),
  ticker           TEXT NOT NULL,
  period           TEXT,
  weight           TEXT,
  note             TEXT,
  knowledge_time   TEXT NOT NULL,
  knowledge_date   DATE,
  source_id        TEXT,
  provenance       TEXT NOT NULL
);

-- ---------- 资产层：来源（doc23 §二）----------
CREATE TABLE IF NOT EXISTS source_master (
  source_id        TEXT PRIMARY KEY,
  name             TEXT NOT NULL,
  publisher        TEXT,
  source_tier      TEXT CHECK (source_tier IS NULL OR source_tier IN ('P1','P2','P3','P4','P5')),
  source_kind      TEXT CHECK (source_kind IS NULL OR source_kind IN ('ir_release','exchange_filing','prospectus','customs','call_transcript','broker_research','news_media','data_aggregator','official','court','company_blog','api')),
  data_class       TEXT,                                -- JSON 数组文本
  covers_entity    TEXT,
  covers_metric    TEXT,
  url              TEXT,
  access           TEXT CHECK (access IS NULL OR access IN ('open','paywall','blocked')),
  frequency        TEXT,
  reliability_note TEXT,
  verify_status    TEXT CHECK (verify_status IS NULL OR verify_status IN ('confirmed','pending','stale','placeholder')),
  superseded_by    TEXT,
  first_seen       DATE,
  last_validated   DATE
);

-- ---------- 治理层：判断表（判断 ≠ 数据，各自带 owner / status）----------
CREATE TABLE IF NOT EXISTS assumption (                 -- doc30 假设台账
  assumption_id    TEXT PRIMARY KEY,
  section          TEXT NOT NULL,
  text             TEXT NOT NULL,
  current_value    TEXT,
  kind             TEXT CHECK (kind IN ('先验','占位','预测','设计选择','时效','领域事实')),
  impact           TEXT CHECK (impact IN ('🔵','🟠')),
  refine_by        TEXT,
  status           TEXT NOT NULL CHECK (status IN ('assumption','calibrating','validated','retired','placeholder'))
);
CREATE TABLE IF NOT EXISTS coefficient (                -- 系数（A1–A8），视图读这里
  coef_id          TEXT PRIMARY KEY,
  value            DOUBLE NOT NULL,
  assumption_id    TEXT REFERENCES assumption(assumption_id),
  note             TEXT
);
CREATE TABLE IF NOT EXISTS metric_factor (              -- 节点五因子（doc21 §6.1）
  metric_id        TEXT PRIMARY KEY REFERENCES metric_registry(metric_id),
  r DOUBLE CHECK (r BETWEEN 0 AND 1), e DOUBLE CHECK (e BETWEEN 0 AND 1), l DOUBLE CHECK (l BETWEEN 0 AND 1),
  s DOUBLE CHECK (s BETWEEN 0 AND 1), phi DOUBLE CHECK (phi BETWEEN 0 AND 1),
  rationale        TEXT,
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired'))
);
CREATE TABLE IF NOT EXISTS observation_direction (      -- 方向判断（A11）
  record_id        TEXT PRIMARY KEY REFERENCES stg_observation(record_id),
  direction        TEXT NOT NULL CHECK (direction IN ('↑','↓','→','!','—')),
  direction_note   TEXT,
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired'))
);
CREATE TABLE IF NOT EXISTS key_fact (                   -- 简报（有作者）
  kf_id            TEXT PRIMARY KEY,
  target_type      TEXT NOT NULL CHECK (target_type IN ('event','ticker','metric')),
  date             DATE,
  target           TEXT NOT NULL,
  brief            TEXT NOT NULL,
  watch            TEXT,
  refs             TEXT,
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired'))
);
CREATE TABLE IF NOT EXISTS source_override (
  source_pattern   TEXT PRIMARY KEY,
  access           TEXT CHECK (access IN ('open','paywall','blocked')),
  verify_status    TEXT CHECK (verify_status IN ('confirmed','pending','stale','placeholder')),
  note             TEXT
);

-- ---------- 治理层：决策层（判断的登记 / 过程账 / 候选池；JEV-intelligence-graph §四 · PLAN-decision-layer §二）----------
-- 增量落库走 migrations/0010（CREATE TABLE IF NOT EXISTS 与此处同文，两条路径幂等）。
CREATE TABLE IF NOT EXISTS decision_registry (           -- 第三张登记表：R 管指标、E 管边、这张管体系里每类重复发生的判断
  decision_id      TEXT PRIMARY KEY,
  name             TEXT NOT NULL,
  question         TEXT NOT NULL,                        -- 这类判断在问什么（一句）
  state_schema     TEXT NOT NULL,                        -- 输入 state 由哪些表列 / 视图构成（= 未来专用模型的输入契约）
  candidates       TEXT NOT NULL,                        -- JSON 数组词表（= 输出契约）；开放候选 = 'open→candidate_pool'
  output_home      TEXT,                                 -- 判断结果写回哪张表哪列（表.列；复合列 ' + ' 连接；只落 decision_log 则 NULL）
  executor_kind    TEXT NOT NULL CHECK (executor_kind IN ('rule','human','llm','model')),
  executor         TEXT NOT NULL,                        -- A–D / 规则名 / 模型名
  freq_est         TEXT,                                 -- 发生频率量级
  escalation       TEXT,                                 -- 升级规则（首版 = 现状描述；数值阈值挂假设 C19，未校准不发明数字）
  calib_status     TEXT NOT NULL CHECK (calib_status IN ('human','shadow','assisted','auto')),   -- 状态机，平移自 doc30
  assumption_ids   TEXT,
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired')),
  design_ref       TEXT,
  notes            TEXT,
  research_tier    TEXT CHECK (research_tier IS NULL OR research_tier IN ('A','B','C'))   -- 投研重要性分层（0015 ALTER 补；A 直接投研 / B 准入可信 / C 运维流程）
);
CREATE TABLE IF NOT EXISTS decision_log (                -- 六元组过程账：change_log 记「改了什么」，这张记「怎么判断的、当时多有把握、事后对不对」
  dec_id           TEXT PRIMARY KEY,
  decision_id      TEXT NOT NULL REFERENCES decision_registry(decision_id),
  target_table     TEXT,
  target_pk        TEXT,
  target_column    TEXT,
  state_anchor     TEXT,                                 -- JSON：判断时刻的输入（record_id 集合 + as_of），判断可复现
  candidates_shown TEXT,                                 -- 判断时刻 registry.candidates 的快照
  choice           TEXT NOT NULL,
  confidence       DOUBLE CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),   -- 人按 H/M/L 写，映射 .9/.6/.3（C21）
  executor_kind    TEXT CHECK (executor_kind IS NULL OR executor_kind IN ('rule','human','llm','model')),
  executor         TEXT,
  escalated        BOOLEAN DEFAULT FALSE,                -- 本次是否从默认执行者升级（R16 分子）
  basis            TEXT NOT NULL,
  decided_at       TIMESTAMP DEFAULT current_timestamp,
  retro            BOOLEAN DEFAULT FALSE,                -- 回填行：confidence 允许空，禁止编造历史置信度
  outcome          TEXT CHECK (outcome IS NULL OR outcome IN ('correct','wrong','mixed','unresolved')),
  outcome_basis    TEXT,
  outcome_at       DATE,
  note             TEXT
);
CREATE TABLE IF NOT EXISTS candidate_pool (              -- PROPOSE 的落点：背离 / 新机制的候选；选中前不是结论（与 key_fact 分开）
  cand_id          TEXT PRIMARY KEY,
  decision_id      TEXT NOT NULL REFERENCES decision_registry(decision_id),
  trigger_ref      TEXT NOT NULL,                        -- 触发对象：record:<id> / ticker:<t> / metric:<id>（与 v_divergence.div_key 对齐）
  kind             TEXT NOT NULL CHECK (kind IN ('explanation','new_edge','new_edge_type','new_metric','new_assumption')),
  candidate_text   TEXT NOT NULL,
  proposed_by      TEXT NOT NULL,                        -- A–D / llm
  status           TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','selected','rejected','merged')),
  created_at       DATE,
  resolved_by      TEXT,                                 -- 选中 / 否决它的那次判断（decision_log.dec_id）
  note             TEXT
);

-- ---------- 呈现辅助：排期 ----------
CREATE TABLE IF NOT EXISTS calendar (
  cal_id           TEXT PRIMARY KEY,
  date_raw         TEXT NOT NULL,
  date             DATE,
  date_precision   TEXT,
  event            TEXT NOT NULL,
  entity_or_ticker TEXT,
  dim_or_entry     TEXT,
  related_metric   TEXT,
  basis            TEXT NOT NULL,
  source_or_rule   TEXT,
  notes            TEXT
,
  status           TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','retired'))   -- retired = 事件本身与 AI 发展无关（如非 AI 持仓的业绩），不进呈现
);
CREATE TABLE IF NOT EXISTS calendar_metric (
  cal_id           TEXT NOT NULL REFERENCES calendar(cal_id),
  metric_id        TEXT NOT NULL REFERENCES metric_registry(metric_id),
  PRIMARY KEY (cal_id, metric_id)
);

-- ---------- 元数据层：字典 / 关系 / 规则 / 日志（SCHEMA.md 由此生成）----------
CREATE TABLE IF NOT EXISTS schema_doc (
  table_name       TEXT NOT NULL,
  column_name      TEXT NOT NULL,
  meaning          TEXT NOT NULL,
  design_ref       TEXT,                                -- doc21 §x / doc17 §2.1 / doc18 补丁① …
  derivable        BOOLEAN DEFAULT FALSE,               -- 设计为字段但可推导 → 实现为视图
  served_by_view   TEXT,
  PRIMARY KEY (table_name, column_name)
);
CREATE TABLE IF NOT EXISTS relation_doc (
  from_table TEXT NOT NULL, from_col TEXT NOT NULL, to_table TEXT NOT NULL, to_col TEXT NOT NULL,
  cardinality TEXT, meaning TEXT,
  PRIMARY KEY (from_table, from_col, to_table, to_col)
);
CREATE TABLE IF NOT EXISTS calc_rule (
  rule_id          TEXT PRIMARY KEY,
  name             TEXT NOT NULL,
  formula          TEXT NOT NULL,
  inputs           TEXT,
  output_view      TEXT,
  assumption_ids   TEXT,
  design_ref       TEXT,
  note             TEXT
);
CREATE TABLE IF NOT EXISTS etl_log (
  run_id           TEXT PRIMARY KEY,
  run_at           TIMESTAMP DEFAULT current_timestamp,
  step             TEXT,
  rows_in          INTEGER,
  rows_out         INTEGER,
  note             TEXT
);

CREATE TABLE IF NOT EXISTS migration_log (              -- 改库记录：库是真源，每一次改库 = migrations/ 下一个编号脚本，应用后登记于此（脚本改动 → checksum 不符 → 拒绝）
  migration_id     TEXT PRIMARY KEY,                    -- 0000_bootstrap / 0001_nbis_round1 …
  applied_at       TIMESTAMP DEFAULT current_timestamp,
  checksum         TEXT NOT NULL,                       -- 脚本 sha256 前 16 位
  owner            TEXT,
  n_changes        INTEGER,                             -- 本次写入 change_log 的行数
  note             TEXT
);
CREATE TABLE IF NOT EXISTS change_log (                 -- 字段级改动账：谁 / 何时 / 依据什么 / 把哪张表哪一行哪一列从什么改成什么（可溯源的最后一环）
  change_id        TEXT PRIMARY KEY,
  migration_id     TEXT NOT NULL REFERENCES migration_log(migration_id),
  table_name       TEXT NOT NULL,
  pk               TEXT NOT NULL,
  column_name      TEXT NOT NULL,                       -- 列名；整行新增记 '(insert)'
  old_value        TEXT,
  new_value        TEXT,
  basis            TEXT,                                -- 依据：原文页码 / 快照 / doc 编号 / 规则
  owner            TEXT,
  applied_at       TIMESTAMP DEFAULT current_timestamp
);

-- ---------- 思路层（元数据）：思考主线 → 决策分叉 → 落地产物；字段可反查「我是哪一步决策来的」（v_column_origin）----------
CREATE TABLE IF NOT EXISTS thesis_node (                -- 一级：核心思考主线（7 个节点，面试主讲；每节点合并若干环）
  node_id          TEXT PRIMARY KEY,                    -- N1…N7
  seq              INTEGER NOT NULL,
  title            TEXT NOT NULL,
  question         TEXT NOT NULL,                       -- 这一节点在问什么（一句）
  conclusion       TEXT NOT NULL,                       -- 核心结论（一句到三句）
  rings            TEXT,                                -- 对应思维链环号（doc31 环 0–11 / doc17 环 12–20 / 本轮 21–22）
  doc_refs         TEXT,                                -- doc / E## 出处
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired'))
);
CREATE TABLE IF NOT EXISTS decision_fork (              -- 二级：关键决策分叉（只记有取舍的熵减点；weight=detail 的在演示模式折叠）
  fork_id          TEXT PRIMARY KEY,                    -- F1.1 …
  node_id          TEXT NOT NULL REFERENCES thesis_node(node_id),
  seq              INTEGER NOT NULL,
  question         TEXT NOT NULL,                       -- 分叉在问什么
  options          TEXT NOT NULL,                       -- JSON 数组：备选方案
  chosen           TEXT NOT NULL,                       -- 最终选择（options 之一）
  rationale        TEXT NOT NULL,                       -- 决策依据
  before_after     TEXT,                                -- 改前 → 改后
  weight           TEXT NOT NULL CHECK (weight IN ('core','detail')),
  log_ref          TEXT,                                -- 环 / E## / doc
  owner            TEXT NOT NULL CHECK (owner IN ('A','B','C','D')),
  status           TEXT NOT NULL CHECK (status IN ('draft','reviewed','retired'))
);
CREATE TABLE IF NOT EXISTS artifact_anchor (            -- 三级：决策落到库里的产物（表 / 列 / 视图 / 规则 / 假设 / 系数 / 校验 / 文件），双向锚定
  anchor_id        TEXT PRIMARY KEY,
  fork_id          TEXT NOT NULL REFERENCES decision_fork(fork_id),
  kind             TEXT NOT NULL CHECK (kind IN ('table','column','view','rule','assumption','coefficient','check','migration','file')),
  ref              TEXT NOT NULL,                       -- table / table.column / v_x / R# / A# / coef_id / 7d / 0003_… / 路径
  how              TEXT                                 -- 怎么体现这一决策（一句）
);
