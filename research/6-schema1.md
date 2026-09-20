

21 wave0 可落库schema ddl · MD
Wave 0 · 可落库 schema(建表语句 + 四补丁 + edge_registry + 字段计算逻辑)
骨架层,不依赖选哪只深挖标的,可先建。实现 doc 17 通用元数据层 + 四类 schema + 逻辑分层,并入 doc 18 四补丁。E21 加 edge_registry(边真源 E)。E23 修实体层两轴分离 + §六 字段计算逻辑。E24 进一步:三子流由字段改视图(Q1 建模原则)。 source_master DDL 见 doc 23;假设/系数台账见 doc 30。PostgreSQL 方言,受控词表 CHECK。主导:C(人定 schema·AI 出 DDL)。

〇、建模原则(E24 · Q1:字段 vs 视图)
字段存"不可再推导的原子事实";视图存"任何可从字段推导出来的分组"。同一"可推导层级"的东西必须一致处理。

maturity(research/private/pre_ipo/public)= 实体的原子属性 → 字段。
「早期信号层」= maturity∈{research,private} → 完全可推导 → 视图(存成字段会与 maturity 冗余、要维护同步,违反规范化)。
三子流(研究前沿/创业一级/人才资本)也可推导:它们 = "监测这个早期实体的哪一类信号" = data_class(类4=研究前沿 / 类2 funding=创业一级 / 类2 personnel=人才资本);而且同一实体(如 Reflection)可被三流同时监测(它的 paper / 融资 / 人才)——所以 stream 是"看它的角度",属信号(metric)层,不属实体。→ 三子流也做视图,不做字段。
结论:实体只存两条不可推导的轴 layer(L1-L6 价值栈)+ maturity(成熟度);早期层与三子流都做视图。上一版把 signal_stream 做成字段是不一致(= 你察觉的"重合":它与 maturity+data_class 可互推),已删。
一、实体层:主数据 + 映射(所有数据挂到这)
sql
-- 实体主表:公司/机构/人/赛道 —— 只存两条不可推导的轴:layer(价值栈) + maturity(成熟度)
CREATE TABLE entity_master (
  entity_id     TEXT PRIMARY KEY,             -- ent_nbis / ent_reflection
  name          TEXT NOT NULL,
  aliases       TEXT[] DEFAULT '{}',
  type          TEXT CHECK (type IN ('company','institution','person','track')),
  layer         TEXT CHECK (layer IN ('L1','L2','L3','L4','L5','L6')),  -- 价值栈六层(在哪变现),不含早期层
  maturity      TEXT CHECK (maturity IN ('research','private','pre_ipo','public')), -- 成熟度轴(信号多早)
  track         TEXT,                          -- 光互连 / neocloud / 前沿模型 ...
  country       TEXT CHECK (country IN ('CN','US','HK','other')),
  ticker        TEXT,
  parent_id     TEXT REFERENCES entity_master(entity_id),
  created_at    TIMESTAMPTZ DEFAULT now()
);

-- 实体→公开 ticker 映射(一个实体可影响多只票,含传导路径)
CREATE TABLE entity_ticker_map (
  map_id        BIGSERIAL PRIMARY KEY,
  entity_id     TEXT REFERENCES entity_master(entity_id),
  ticker        TEXT NOT NULL,
  relation      TEXT CHECK (relation IN ('self','supplier','customer','competitor','supply_chain_read','demand_driver')),
  map_path      TEXT,                          -- 【补丁③】传导链
  weight        NUMERIC                        -- 相对权重(算法见 §6.4)
);

-- 早期信号层 + 三子流:都是【视图】,从 maturity(实体)+ data_class/event_type(信号)推导
CREATE VIEW v_early_signal AS
SELECT e.entity_id, e.name, m.metric_id,
       CASE WHEN m.data_class = 4                              THEN 'research_frontier'  -- 研究前沿
            WHEN m.data_class = 2 AND ev.event_type='funding'  THEN 'startup_vc'         -- 创业一级
            WHEN m.data_class = 2 AND ev.event_type='personnel'THEN 'talent_capital'     -- 人才资本
       END AS signal_stream
FROM entity_master e
JOIN metric_registry m ON m.entity_id = e.entity_id
LEFT JOIN fct_event ev ON ev.metric_id = m.metric_id
WHERE e.maturity IN ('research','private');    -- 「早期信号层」= 这个 WHERE
二、指标层:metric_registry(唯一真源 R,= panel 视图A/B 的节点)
sql
CREATE TABLE metric_registry (
  metric_id      TEXT PRIMARY KEY,
  name           TEXT NOT NULL,
  entity_id      TEXT REFERENCES entity_master(entity_id),
  track          TEXT, layer TEXT,             -- layer = L1–L6(价值栈)
  dim            TEXT CHECK (dim IN ('D1','D2','D3','D4','D5','D6','D7')), -- AI发展7维(doc24v2)
  data_class     SMALLINT CHECK (data_class IN (1,2,3,4)),   -- 1量价 2事件 3观点 4前沿(三子流从这推)
  signal_role    TEXT CHECK (signal_role IN ('predictor','expectation_base','regime','arbiter','human_input')),
  source_ids     TEXT[] DEFAULT '{}',
  frequency      TEXT,
  lead_time_est  INTERVAL,                      -- 【补丁④】领先期先验(假设,见 doc30)
  kou_jing       TEXT, unit TEXT,
  owner          CHAR(1) CHECK (owner IN ('A','B','C','D')),
  valuable_score NUMERIC,                       -- 节点固有价值,算法见 §6.2
  upstream_deps  TEXT[] DEFAULT '{}',
  status         TEXT CHECK (status IN ('testing','production','deprecated')),
  last_validated DATE
);
二.5 边层:edge_registry(边真源 E · = panel 视图B)
sql
CREATE TABLE edge_registry (
  edge_id        TEXT PRIMARY KEY,
  from_metric    TEXT REFERENCES metric_registry(metric_id),
  to_ticker      TEXT NOT NULL,
  side           TEXT CHECK (side IN ('supply','demand','regime','self','compete')),
  edge_type      TEXT CHECK (edge_type IN ('E1_self','E2_supplier','E3_customer','E4_competitor','E5_theme','E6_flow')),
  hops           SMALLINT,
  map_path       TEXT, mechanism TEXT,
  cert_tier      TEXT CHECK (cert_tier IN ('T1_backtest','T2_structural','T3_directional')),
  cert_method    TEXT, cert_score NUMERIC, lead_measured INTERVAL,
  tradable_score NUMERIC, warning_score NUMERIC,
  is_key         BOOLEAN DEFAULT false,
  evidence_ids   TEXT[] DEFAULT '{}',
  owner          CHAR(1) CHECK (owner IN ('A','B','C','D')),
  status         TEXT CHECK (status IN ('testing','production','deprecated')),
  last_validated DATE
);
三层确定性验证(cert_tier):T1 可回测 · T2 结构+真值对账+敏感性(langfuse §5)· T3 方向。执行见 doc 28 §七。

三、信号层:四类 fct 表(通用元数据层 + 各类 payload)
通用元数据(每张 fct 表都含):record_id, metric_id, entity_id, knowledge_time, source_id, source_url, anchor, snapshot_id, ingest_time, owner, confidence, code_score, status, ticker_map, map_path, valuable_score。

sql
CREATE TABLE fct_quant (   -- 类1 量价
  record_id BIGSERIAL PRIMARY KEY, metric_id TEXT REFERENCES metric_registry(metric_id), entity_id TEXT,
  period DATERANGE, value NUMERIC, unit TEXT, currency TEXT, yoy NUMERIC, qoq NUMERIC,
  revision_flag TEXT CHECK (revision_flag IN ('initial','revised')),
  conversion_assumption TEXT, assumption_source TEXT,          -- 【补丁①】
  knowledge_time TIMESTAMPTZ NOT NULL, source_id TEXT, source_url TEXT, anchor TEXT, snapshot_id TEXT,
  ingest_time TIMESTAMPTZ DEFAULT now(), owner CHAR(1), code_score JSONB, status TEXT,
  ticker_map JSONB, map_path TEXT, valuable_score NUMERIC );
CREATE TABLE fct_event (   -- 类2 事件
  record_id BIGSERIAL PRIMARY KEY, metric_id TEXT, entity_id TEXT,
  event_type TEXT CHECK (event_type IN ('funding','launch','personnel','order','approval','contract')),
  subject_entity TEXT, object_entity TEXT, relation TEXT, amount NUMERIC, currency TEXT,
  amount_type TEXT CHECK (amount_type IN ('one_time','multi_year_cap','annualized','range')), -- 【补丁②】
  is_estimate BOOLEAN DEFAULT false, round TEXT, event_date DATE,
  knowledge_time TIMESTAMPTZ NOT NULL, source_id TEXT, source_url TEXT, anchor TEXT, snapshot_id TEXT,
  ingest_time TIMESTAMPTZ DEFAULT now(), owner CHAR(1), confidence NUMERIC, status TEXT,
  ticker_map JSONB, map_path TEXT, valuable_score NUMERIC );
CREATE TABLE fct_opinion ( -- 类3 观点
  record_id BIGSERIAL PRIMARY KEY, metric_id TEXT, entity_id TEXT, variable TEXT, speaker TEXT,
  speaker_role TEXT CHECK (speaker_role IN ('management','analyst_q','expert','media','official')),
  level SMALLINT, strength TEXT, direction TEXT, anchor_quote TEXT, codebook_version TEXT, model_version TEXT,
  knowledge_time TIMESTAMPTZ NOT NULL, source_id TEXT, source_url TEXT, anchor TEXT, snapshot_id TEXT,
  ingest_time TIMESTAMPTZ DEFAULT now(), owner CHAR(1), code_score JSONB, judge_score NUMERIC, status TEXT,
  ticker_map JSONB, map_path TEXT, valuable_score NUMERIC );
CREATE TABLE fct_frontier ( -- 类4 前沿(= doc29 前沿雷达主表;新增源立场/影响力字段见 doc29)
  record_id BIGSERIAL PRIMARY KEY, metric_id TEXT, entity_id TEXT,
  topic_cluster TEXT, method TEXT, benchmark TEXT, score NUMERIC, institution TEXT, authors TEXT[],
  citation_velocity NUMERIC,
  knowledge_time TIMESTAMPTZ NOT NULL, source_id TEXT, source_url TEXT, anchor TEXT, snapshot_id TEXT,
  ingest_time TIMESTAMPTZ DEFAULT now(), owner CHAR(1), status TEXT,
  ticker_map JSONB, map_path TEXT, valuable_score NUMERIC );
四、呈现层:视图(信号三态,供 panel 调)
sql
-- 视图A「AI发展监测树」按 dim(D1-D7) + 早期信号层(v_early_signal)组织
CREATE VIEW v_signal_latest AS
SELECT r.metric_id, r.name, r.entity_id, r.dim, r.data_class, r.signal_role, r.owner,
       r.lead_time_est, r.valuable_score, r.status, s.direction, s.confidence, s.knowledge_time, s.anchor
FROM metric_registry r LEFT JOIN LATERAL (/* 各 fct 最近三态 */) s ON true;

-- 视图B「映射/持仓树」按 to_ticker 组织边 + 节点三态(蝴蝶结)
CREATE VIEW v_ticker_map AS
SELECT e.to_ticker, e.side, e.edge_type, e.hops, e.cert_tier, e.tradable_score, e.warning_score, e.is_key,
       r.metric_id, r.name AS node_name, r.dim, r.owner, s.direction, s.confidence
FROM edge_registry e JOIN metric_registry r ON r.metric_id = e.from_metric
LEFT JOIN LATERAL (/* 该节点最近三态 */) s ON true;
五、可追踪 / 可管理怎么被这套 DDL 坐实
可追踪:fct 带 knowledge_time+snapshot_id+anchor,Langfuse trace 写 code_score;边带 evidence_ids。
可管理:双真源 R(metric_registry)+ E(edge_registry);受控词表 CHECK;可推导的分组一律做视图(早期层/三子流),避免冗余失同步。
诚实标注:conversion_assumption/amount_type+is_estimate/owner A-D/边 cert_tier;打分系数是假设,记 doc30 台账。
六、字段计算逻辑(node valuable_score / edge scores / weight · Q2)
承 doc 25 §1.3。系数是先验假设、当前只用于排序(见 doc30);回测后再标定精确值,不编假精度。

6.1 因子锚点(每因子 0–1)
因子	含义	H≈0.9	M≈0.6	L≈0.3
r 可靠性	由 provenance(doc23)	P1 一手	P2/P3	P4 估算
e 独家性	别人拿不拿得到	自建/中国侧独家	半公开	全公开
l 固有领先性	天然领先	一级融资/研究前沿	供应链月度	财报同步
s 可观测/信噪	可量化/噪声	干净结构化	需抽取有噪	高噪(arXiv 灌水)
φ 频率适配	更新够不够	≥所需	勉强	太疏
边侧:c = cert_base × 0.9^hops(base T1=0.9/T2=0.6/T3=0.3);τ = min(1, 0.25·hops + 0.5·l)。(0.9、0.25、0.5 均为假设,见 doc30)

6.2 节点固有价值 → metric_registry.valuable_score
valuable_score(node) = 0.45·e + 0.25·s + 0.20·r + 0.10·φ(与哪只票无关、不含跳数)。例:中际旭创 → 0.735。

6.3 边两产出 → edge_registry(节点质量取 from_node,传导取 edge)
tradable_score = c·r·s·φ(可交易度→定仓位);warning_score = τ·l·e(预警度→watchlist)。 例:光模块→NBIS 0.32/0.16(偏可交易);lab 融资→NBIS 0.10/0.77(强预警)。印证 doc25 定性。

6.4 实体→票权重 → entity_ticker_map.weight
weight(edge_i→ticker) = max(tradable_i, warning_i) / Σ_j max(tradable_j, warning_j)(该票所有上游边归一)。人可覆盖(owner D)。

系数(0.45/0.25/0.20/0.10、0.9^hops、tier base、τ 式)全部是假设——当前只用于排序,绝对值不承载意义;回测后用实现的信号有用性/P&L 归因标定,那时绝对值才用于 sizing。全部登记在 doc 30 假设台账。

下一步:doc 28 全链路已跑通;第四类前沿独立采集见 doc 29;假设台账 doc 30;呈现总装 doc 27(待建)。




22 wave1 nbis指标树样板 真实数据实例化 · MD
Wave 1 · NBIS 指标树样板:一条 thesis 两端对账(真实数据实例化)
把 doc 21 的 schema 用真实数据灌进去,做出深度样板的一支树:NBIS 算力周期 thesis 的供给端读 ⟷ 需求端读,以及把两者合流的对账节点。每个节点都标 data_class / signal_role / owner(A–D) / lead_time_est / valuable_score。所有 value 均真实、可溯源;每个数字的一手/二手/电话会/估算分级 = doc 23《来源总账》(数字是真数;valuable_score/lead_time_est 是设计层评分,非数据值)。主导:D(她定样板形态)+ B(AI 查证实例化)+ C(人定 schema)。已按 2026-09-19 核验回填:Reflection 同体已确认;NBIS ARR/backlog 标为电话会口径 P2;估值项标时效。

一、这一支树长什么样(总览)
NBIS 算力周期 thesis(entity=ent_nbis)
│
├─ 【供给端读】算力"在建多少" —— 成熟层 · 可回测 · 进 nowcast
│   │
│   ├─ 赛道层 L1 光互连(挂 track,喂多只票)
│   │   ├─ m_cn_optics_zte    中际旭创季度营收/YoY      类1 predictor  A  lead 18d
│   │   ├─ m_cn_optics_eoptolink 新易盛季度营收/YoY     类1 predictor  A  lead 18d
│   │   ├─ m_cn_optics_customs 海关光通信月度出口(反推) 类1 predictor  B  lead 20d
│   │   └─ m_800g_shipment    800G+ 全球出货量           类1 predictor  A  lead —
│   │
│   └─ 单票层 L2 NBIS 本体(idiosyncratic)
│       ├─ m_nbis_arr         ARR / 收入 / EBITDA率       类1 expect_base A  lead —
│       ├─ m_nbis_backlog     合同 backlog / 客户预付      类2 expect_base B  lead —
│       ├─ m_nbis_capacity    5GW 产能上电执行             类2 predictor  B  lead 90d
│       └─ m_nbis_calltone    电话会措辞(单价/利用率口径) 类3 arbiter    B  lead —
│
├─ 【需求端读】算力"需求真不真、续不续" —— 早期信号层 · 给方向/预警 · 不直接下注
│   ├─ m_lab_funding          前沿 lab 一级融资(NBIS 客户) 类2 predictor  B  lead 180d
│   ├─ m_infer_progress       推理进展/推理时算力趋势        类4 predictor  B  lead —
│   └─ m_talent_capital       顶尖研究员/Nvidia 系资金流向   —  human_input  C  lead —
│
└─ 【对账节点】供给态 × 需求态 → regime(信念/中性/泡沫预警)
    └─ m_reconcile_nbis       命中 NBIS 分析点②           —  arbiter      D  lead —
                              (alpha 所在,华尔街不做的交叉验证)
一句话:左边可回测的量价(beta 周期在建强度)+ 右边独家的早期预警(alpha 需求真伪),两条独立数据源、独立失败模式,在对账节点合流成一个仓位含义。

二、实体层实例(entity_master + entity_ticker_map)
sql
INSERT INTO entity_master (entity_id, name, type, layer, track, maturity, country, ticker) VALUES
 ('ent_nbis',        'Nebius Group N.V.',      'company','L2','neocloud',   'public','other','NBIS'),      -- 阿姆斯特丹,NASDAQ
 ('ent_optics_cn',   '中国光模块出口(赛道)',    'track',  'L1','光互连',     'public','CN', NULL),
 ('ent_zte_photonics','中际旭创',               'company','L1','光互连',     'public','CN','300308.SZ'),
 ('ent_eoptolink',   '新易盛',                  'company','L1','光互连',     'public','CN','300502.SZ'),
 ('ent_reflection',  'Reflection AI(前沿 lab,NBIS 客户已确认:2026-07 $1B 算力合同)','company','early_A','前沿模型','private','US',NULL),
 ('ent_cohere',      'Cohere',                  'company','early_A','企业 LLM','private','US',NULL);

-- 一个实体可影响多只票 + 传导路径(map_path = 补丁③)
INSERT INTO entity_ticker_map (entity_id, ticker, relation, map_path, weight) VALUES
 ('ent_optics_cn',  'NBIS','supply_chain_read','光模块出货↑→AI集群在建↑→neocloud容量↑(赛道→单票,间接)', 0.4),
 ('ent_optics_cn',  'CIEN','supply_chain_read','光模块赛道读→美股光通信同赛道', 0.3),  -- 基金过往持仓 CIEN/LITE/AAOI/POET
 ('ent_zte_photonics','NBIS','supply_chain_read','旭创 800G 出货≈NVIDIA 集群建设强度→neocloud 容量', 0.3),
 ('ent_reflection', 'NBIS','demand_driver','AI 进展→推理/训练需求→neocloud 用量→NBIS backlog(远端,预警向)', 0.5),
 ('ent_cohere',     'NBIS','demand_driver','企业 LLM 商用→推理需求→neocloud 用量→NBIS', 0.3);
读法:光模块挂在赛道(track)、relation=supply_chain_read、喂 NBIS + 一串同赛道美股票(不是 NBIS 专属);前沿 lab 挂 demand_driver、map_path 是间接传导链、weight 低——正是"离 ticker 远、独家性高、只给方向"的落库形态。

三、指标层实例(metric_registry 行,= panel 的 R)
metric_id	name	class	signal_role	owner	freq	lead_time	valuable	口径要点
m_cn_optics_zte	中际旭创季度营收/YoY	1	predictor	A	quarterly	18d	0.65	海外营收占比拆出 AI 敞口;领先美股光通信名财报~2–3周
m_cn_optics_eoptolink	新易盛季度营收/YoY	1	predictor	A	quarterly	18d	0.60	1.6T/Google NPO 敞口
m_cn_optics_customs	海关光通信月度出口(反推光模块)	1	predictor	B	monthly	20d	0.55	HS8517 宽口径×换算假设(补丁①);系数待标定,现只做方向
m_800g_shipment	800G+ 全球出货量	1	predictor	A	quarterly	—	0.45	第三方,AI-capex 强度旁证(2026 为预测值)
m_nbis_arr	NBIS ARR/收入/EBITDA率	1	expectation_base	A	quarterly	—	0.35	收入/EBITDA 一手(P1);ARR 为电话会口径(P2)
m_nbis_backlog	NBIS 合同 backlog/客户预付	2	expectation_base	B	event	—	0.40	multi_year_cap(补丁②);电话会口径 P2,需判合同质量
m_nbis_capacity	NBIS 5GW 产能上电执行	2	predictor	B	event	90d	0.55	最关键可观测量:延期=收入递延;需拼电力/建设进度
m_nbis_calltone	NBIS 电话会措辞(单价/利用率)	3	arbiter	B	event	—	0.50	LLM 抽 management 表述,codebook 版本化
m_lab_funding	前沿 lab 一级融资(NBIS 客户)	2	predictor	B	event	180d	0.60	需求持续性领先读;判真需求 vs 投机囤算力
m_infer_progress	推理进展/推理时算力趋势	4	predictor	B	event	—	0.50	map_path:AI 进展→推理需求→NBIS
m_talent_capital	顶尖研究员/Nvidia 系资金流向	—	human_input	C	event	—	0.55	人定义口径·AI 执行采集;研究员回流大厂=转冷信号
m_reconcile_nbis	供给×需求 对账 → regime	—	arbiter	D	event	—	0.85	规则人定(C)、裁量担责(D);命中分析点②,alpha 所在
owner 词表(= doc 09,同一套贯穿体系):D 人定 · C 人定义·AI执行 · B AI初稿·人必复核 · A AI独立·人抽检。 valuable_score = 离 ticker 距离 × 独家性(0–1 打分,设计层评分,非数据值):对账节点最高(0.85,独家交叉判断),NBIS 财报本体最低(0.35,人人可读)。

四、信号层实例(fct 记录,真实数据 + as-of)
类1 量价(fct_quant)—— 供给端可回测
sql
INSERT INTO fct_quant (metric_id, entity_id, period, value, unit, currency, yoy,
       conversion_assumption, assumption_source, knowledge_time, source_url, owner, revision_flag) VALUES
-- 中际旭创:2025 全年 + 2026Q1(真数,海外91%;Q1 营收增 192.12% 为交易所公告口径 P1)
 ('m_cn_optics_zte','ent_zte_photonics','[2025-01-01,2025-12-31]', 38200000000,'CNY','CNY', 0.60,
   NULL,NULL,'2026-04','300308 年报','A','initial'),                             -- ¥382亿 +60%,海外91%(回年报)
 ('m_cn_optics_zte','ent_zte_photonics','[2026-01-01,2026-03-31]', 19496000000,'CNY','CNY', 1.9212,
   NULL,NULL,'2026-04-16','深交所 300308 一季报公告','A','initial'),             -- ¥194.96亿 +192.12%(净利~57亿 +262%)
-- 新易盛:2025 全年(真数,海外~80%;现引自媒体 P3,待回年报)
 ('m_cn_optics_eoptolink','ent_eoptolink','[2025-01-01,2025-12-31]', 24800000000,'CNY','CNY', 1.87,
   NULL,NULL,'2026-04','semisino(待回 300502 年报)','A','initial'),             -- ¥248亿 +187%
-- 800G+ 全球出货量(真数):2025 ~24M → 2026 ~63M 只(2026 为预测)
 ('m_800g_shipment','ent_optics_cn','[2025-01-01,2025-12-31]', 24000000,'units',NULL, NULL,
   NULL,NULL,'2026-Q1','semisino','A','initial'),
 ('m_800g_shipment','ent_optics_cn','[2026-01-01,2026-12-31]', 63000000,'units',NULL, NULL,
   NULL,NULL,'2026-Q1','semisino','A','revised'),                               -- 预测值,revised
-- 海关反推示范(补丁①换算假设摊明;系数 placeholder,信号现只做方向):
 ('m_cn_optics_customs','ent_optics_cn','[2026-07-01,2026-07-31]', NULL,'USD','USD', NULL,
   '光模块占 HS8517 出口 ≈ X%(待用招股书/协会数据标定)','东吴/行业协会口径(待补)','2026-08','海关总署','B','initial'),
-- NBIS 本体(收入/EBITDA 一手 P1;ARR 为电话会口径 P2):
 ('m_nbis_arr','ent_nbis','[2026-04-01,2026-06-30]', 582300000,'USD','USD', 4.54,
   NULL,NULL,'2026-08-12','businesswire Nebius Q2 2026 results(P1)','A','initial'), -- 收入$582.3M +454%
 ('m_nbis_arr','ent_nbis','[2026-06-30,2026-06-30]', 3000000000,'USD','USD', 5.98,
   NULL,NULL,'2026-08-12','NBIS Q2 电话会 highlights(P2,钉 transcript)','A','initial'); -- ARR$3.0B(电话会口径)
类2 实体事件(fct_event)—— 执行监控 + 需求端一级资本
sql
INSERT INTO fct_event (metric_id, entity_id, event_type, subject_entity, amount, currency,
       amount_type, is_estimate, event_date, knowledge_time, source_url, owner, confidence) VALUES
-- NBIS backlog / 预付(电话会口径 P2;补丁②:多年上限,非年化)
 ('m_nbis_backlog','ent_nbis','contract','ent_nbis', 40000000000,'USD','multi_year_cap',false,
   '2026-06-30','2026-08-12','NBIS Q2 电话会 highlights(P2)','B'),               -- backlog $40B(电话会,钉 transcript)
 ('m_nbis_backlog','ent_nbis','contract','ent_nbis',  9000000000,'USD','annualized', true,
   '2026-12-31','2026-08-12','NBIS Q2 电话会 highlights(P2)','B'),               -- 2026 客户预付~$9B+(指引,估)
-- NBIS 产能上电执行(最关键可观测量;电话会目标 P2/P4;补丁④ lead 90d)
 ('m_nbis_capacity','ent_nbis','launch','ent_nbis', NULL,NULL,'range', true,
   '2026-12-31','2026-08-12','NBIS Q2 电话会 highlights(P2)','B'),               -- 目标 5GW by 年底,800MW–1GW 上电 by Dec
-- 需求端:Reflection↔NBIS $1B 算力合同(同体已确认,P1;补丁④ lead 180d)
 ('m_lab_funding','ent_reflection','contract','ent_nbis', 1000000000,'USD','multi_year_cap', false,
   '2026-07-14','2026-07-14','TechCrunch/Bloomberg/Reuters Reflection–Nebius $1B(P1)','B'), -- 确认 Reflection=NBIS 客户
-- 需求端:Reflection 一级融资(P1 已核)
 ('m_lab_funding','ent_reflection','funding','ent_reflection', 2000000000,'USD','one_time', false,
   '2025-10-09','2025-10-09','TechCrunch Reflection raises $2B(P1)','B'),        -- $2B @ 估值$8B,Nvidia 领投
 ('m_lab_funding','ent_reflection','funding','ent_reflection', 2500000000,'USD','one_time', true,
   '2026','2026','Turing Post/roic(P3,在谈)','B'),                              -- 二轮~$2.5B,估值 $20–27B 在谈(口径不一)
-- 需求端:Cohere(P3;估值时效敏感)
 ('m_lab_funding','ent_cohere','funding','ent_cohere', 240000000,'USD','annualized', false,
   '2026','2026','FNEX/Sacra(P3)','B');                                          -- $240M ARR;估值 ~$7B→在谈~$20B
类3 观点/表述(fct_opinion)—— 电话会措辞
sql
INSERT INTO fct_opinion (metric_id, entity_id, variable, speaker, speaker_role,
       direction, strength, anchor_quote, codebook_version, knowledge_time, source_url, owner) VALUES
 ('m_nbis_calltone','ent_nbis','单位经济/单价','NBIS 管理层','management','up','strong',
   '中期合同 $20–25M/MW,短期 $40–50M/MW;AI 分部利润率 50%','icl-codebook 同架 v1','2026-08-12',
   'App Economy Insights / NBIS 电话会(P2)','B');  -- 单价锚,判利用率/资本效率
类4 前沿/知识(fct_frontier)—— 推理进展
sql
INSERT INTO fct_frontier (metric_id, entity_id, topic_cluster, method, knowledge_time, source_url, owner) VALUES
 ('m_infer_progress','ent_reflection','开源前沿模型/推理时算力','citation+发布追踪','2026',
   'Sacra / Reflection AI(P3)','B'); -- Reflection ex-DeepMind,"American DeepSeek",开源前沿路线
五、对账节点:三态判定(命中 NBIS 分析点②)
m_reconcile_nbis:把左树(供给态)× 右树(需求态)合流成一个 regime。规则人定(C)、最终裁量与仓位含义人担责(D)。

供给端态(在建强度)	需求端态(融资/进展/人才)	→ regime	仓位含义
↑ 猛建	↑ 融资涌 / 进展快 / 人才流入	信念(健康)	backlog 可信,支持加仓
↑ 猛建	→ 平	中性/观察	盯背离是否扩大
↑ 猛建	↓ 一级转冷 / 进展停滞 / 人才回流大厂	泡沫预警	neocloud 循环融资风险,减仓/看做空侧
→ / ↓ 放缓	↑	供给瓶颈(另一类信号)	单独议
当前真实读数(as of 2026Q2,全真数,分级见 doc 23):

供给端 = ↑ 猛建:中际旭创 2026Q1 营收 ¥194.96亿(+192.12%,交易所公告 P1)、800G 出货 24M→63M只、NBIS 收入 $582.3M(+454%,一手 P1)、ARR $3.0B / backlog $40B(电话会口径 P2)、5GW 产能在建。
需求端 = ↑ 融资涌:Reflection(NBIS 客户已确认,2026-07 $1B 算力合同)一年 $130M→$2B@$8B(2025-10,Nvidia 领投)→二轮 ~$2.5B、估值 $20–27B 在谈;Cohere $240M ARR(估值 ~$7B→在谈 ~$20B)。
⇒ 当前 regime = 信念(同向)。但背离风险明确挂账:NVIDIA–CoreWeave–Nebius 循环融资、neocloud 被称 "WeWork 2.0"——所以此节点的价值不是当下拍"加仓",而是持续监测右树何时先转冷(一级融资领先 backlog 数季度,lead 180d),在供给端还在猛建时提前发出泡沫预警。这正是分析点② 的可执行化,也是华尔街覆盖 NBIS 的分析师一般不做的交叉验证。
六、人机分工汇总(A/B/C/D)—— 交付物 3 素材
节点	谁做	为什么是这一级
中际旭创/新易盛季度营收、800G 出货、NBIS 收入/EBITDA	A AI 独立·人抽检	干净结构化财报,公式算 YoY,结构化数据不喂 LLM
海关月度反推光模块	B AI 初稿·人复核	换算系数(占 HS8517 比)是估算,人必须复核标定源
NBIS backlog/预付、产能上电、电话会措辞	B AI 初稿·人复核	合同质量、上电是否延期、措辞方向要人判断担责
前沿 lab 融资、推理进展	B AI 初稿·人复核	事件抽取易,但"真需求 vs 投机囤算力"要人判
人才/资本流向	C 人定义·AI 执行	口径(哪些算"回流大厂")人定,采集 AI 跑
对账节点 → regime	D 人定(规则 C·裁量 D)	三态规则可写死,但 regime 判定与仓位含义人裁量、人担责
规律(可对面试官讲的一句):离干净结构化数据越近 → 越靠 A/code;越需要判断真伪、越接近下注决策(杠杆越高)→ 越靠 B/C/D、越要人担责。 与 panel 的 type 判据(code/llm/human/mix)同源。

七、可追踪 / 可管理怎么在这支树上被坐实
可追踪:每条 fct 带 knowledge_time(as-of)+ source_url(锚)+ revision_flag(初值/修正,如 800G 2026 是预测值标 revised)。Langfuse trace_id 写进 code_score → 任一信号回溯到"哪天、哪份原始、哪步处理"。
可管理:metric_registry 单一真源(改数据只动它,= panel 的 R);受控词表 CHECK 约束防口径漂移;codebook_version 进 fct_opinion。
诚实标注(本样板已示范):conversion_assumption+assumption_source(海关反推系数摊明)、amount_type+is_estimate(backlog=multi_year_cap 真实 / 预付=annualized 估 / 产能=range 估)、owner A–D(每条谁做)。
必须上台前坐实的两点(诚实边界):

provenance 分级(见 doc 23《来源总账》):NBIS 收入/EBITDA 已一手核实(P1),但 ARR/backlog/5GW/指引为电话会口径(P2),须钉官方 call transcript/IR deck 后才当硬数;中际旭创 Q1 已一手(P1),2025 年报与新易盛待回原文;海关系数为 placeholder(用前必标定)。knowledge_time 部分只精到月/季的须钉一手披露时间戳,否则 point-in-time 会漏看未来函数。
Reflection 同体——已核销:NBIS 客户"Reflection"即前沿 lab Reflection AI 已确认(2026-07-14 双方 $1B 算力合同,TechCrunch/Bloomberg/Reuters),verify_status 待核→confirmed。
八、这支树证明了什么(给面试官的三条)
懂 beta vs alpha 分层:光模块=赛道周期(beta)挂 track 喂多票、可回测;NBIS backlog/产能=单票(部分 alpha);对账=独家 alpha。
懂 neocloud 的真实风险:不是只读"在建多少",而是用需求端早期信号做泡沫/循环融资预警,直接命中市场对 NBIS 的头号担忧。
懂人机边界与可回溯:每个节点 A–D 分工清楚、每条数据 as-of 可追、估算处摊明、每个数字带 provenance 分级(doc 23)——这就是第一考核"链稳不稳、可回溯"的实证。
下一步选项:①把这支树渲染成 panel.html 的一支(R 数组新增上述 metric_registry 行 + 节点 chip 显 A–D,可下钻抽屉);或 ② 进 step3(agent trace & harness:把 m_lab_funding / m_nbis_calltone 这类 LLM 窄口子接 Langfuse,做 eval/dataset/报警的可跑切片)。


