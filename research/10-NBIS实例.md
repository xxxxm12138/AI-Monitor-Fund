

28 nbis全链路实跑 schema真实填充 源可得性 边验证 · MD
NBIS 端到端实跑 · Wave0 schema 真实填充 × 源可得性 × 边验证执行
用 NBIS 把整套(doc 21 schema:实体→指标→边→四类 fct)灌满真数跑一遍:每字段真实值 + 每层源的可得性/质量(真去找了)+ 节点子节点展开 + 边三层验证怎么具体执行(承 doc 25 §六 + langfuse §5)。诚实标 placeholder / 待一手 / paywall。主导:B(查证实例化)+ C(schema)+ D(定框)。数据 as-of 2026-09-19;数字分级见 doc 23 五级 provenance。E23 已修实体层两轴(§二)。

一、源可得性 × 质量总表(各层真去找的结果)
可得性四档:🟢一手公开可回测 · 🟡二手转述待钉一手 · 🔵付费 · ⚪placeholder/合规受限。

维	节点	真实源	可得性	质量	频率	软肋
D1	中际旭创/新易盛季度营收	深交所公告 / akshare / 巨潮	🟢	P1	季	需按海外占比拆 AI 敞口
D1	海关光模块出口	海关总署月报(HS8517)	⚪	P4	月	光模块占比系数未标定
D1	HBM/CoWoS/GPU 出货	SemiAnalysis / TrendForce	🔵	P3	季	付费;免费只拿定性
D1	NBIS 收入/EBITDA	Nebius IR(businesswire)	🟢	P1	季	—
D1	NBIS ARR/backlog/5GW/单价	Q2 电话会(BigGo/Yahoo 转述)	🟡	P2	季/事件	不在 results release,须钉官方 transcript
D3	前沿 lab 融资	TechCrunch/官方博客/SEC Form D	🟢	P1–P3	事件	估值口径不一、时效敏感
D3	赛道资金流/一级估值	PitchBook / IT桔子·烯牛	🔵	P3	事件	付费
D5	前沿训练算力趋势	Epoch AI(epoch.ai)	🟢	P1	月/事件	权威、免费
D5	模型能力/智能指数	Artificial Analysis / LMArena	🟢	P2	周	免费;榜单口径
D5	论文主题斜率	arXiv/OpenAlex API	🟢	P3	日	需去季节性+引用加权
D6	推理 cost/token、用量	Artificial Analysis / pricepertoken / OpenRouter	🟢	P3	周	分模型、口径杂
D6	企业 adoption/ARR(RBRK 类)	财报 / 招聘 JD	🟢	P1	季	—
D7	出口管制	BIS 新闻稿(bis.gov)	🟢	P1	事件	—
D7	能源/数据中心电力	IEA(Energy and AI / Electricity 2026)	🟢	P2	年/季	预测口径
D4	顶尖研究员流向	领英/论文署名	⚪	P3–P5	事件	合规受限、半人工、ROI 低
一句话结论:能一手公开、可回测的集中在 D1 中国光模块/NBIS 收入、D5 Epoch/Artificial Analysis、D7 BIS/IEA;NBIS 的 ARR/backlog/5GW 是二手电话会口径待钉 transcript;HBM/CoWoS/一级估值付费;海关系数、人才placeholder/合规。这张表本身就是交付物2 的"可得性诚实说明"。

二、实体层实例(entity_master + entity_ticker_map · 真数)
E23(Q1):layer 只放价值栈 L1–L6;早期信号层 = maturity∈research/private 的横切,子流用 signal_stream 标(与 layer 正交)。Reflection/Cohere 是前沿模型 lab,价值栈上属 L3(模型层)、成熟度 private/research、子流 research_frontier——不是 "early_A"(旧写法把两条正交轴塞进 layer,已修)。

sql
INSERT INTO entity_master (entity_id, name, type, layer, maturity, signal_stream, track, country, ticker) VALUES
 ('ent_nbis','Nebius Group N.V.','company','L2','public',NULL,'neocloud','other','NBIS'),
 ('ent_optics_cn','中国光模块出口(赛道)','track','L1','public',NULL,'光互连','CN',NULL),
 ('ent_zte_photonics','中际旭创','company','L1','public',NULL,'光互连','CN','300308.SZ'),
 ('ent_eoptolink','新易盛','company','L1','public',NULL,'光互连','CN','300502.SZ'),
 ('ent_reflection','Reflection AI','company','L3','private','research_frontier','前沿模型','US',NULL),
 ('ent_cohere','Cohere','company','L3','private','research_frontier','企业LLM','US',NULL),
 ('ent_frontier_cap','前沿模型能力(赛道)','track','L3','research','research_frontier','前沿模型','US',NULL);

INSERT INTO entity_ticker_map (entity_id, ticker, relation, map_path, weight) VALUES
 ('ent_optics_cn','NBIS','supply_chain_read','光模块出货→AI集群在建→neocloud扩张→NBIS产能',0.4),
 ('ent_zte_photonics','NBIS','supply_chain_read','旭创800G出货≈NVIDIA集群强度→neocloud容量',0.3),
 ('ent_reflection','NBIS','demand_driver','lab融资→算力采购力→NBIS签约/backlog',0.5),
 ('ent_cohere','NBIS','demand_driver','企业LLM商用→推理需求→neocloud用量',0.3),
 ('ent_frontier_cap','NBIS','demand_driver','模型能力→推理/训练需求→lab采购→NBIS用量',0.3);
（weight 的算法见 doc21 §6.4:该边 max(可交易,预警)/ 该票所有边之和,归一化;上表数字为定性初值,待按 §6 回填。）

三、指标层实例(metric_registry · NBIS 每节点一行 · 真口径)
metric_id	name	dim	class	signal_role	源(可得性)	freq	lead	owner	valuable
m_nbis_rev	NBIS 收入/EBITDA	D1	1	expectation_base	IR🟢P1	季	—	A	0.35
m_nbis_arr	NBIS ARR	D1	1	expectation_base	电话会🟡P2	季	—	A	0.35
m_nbis_backlog	NBIS backlog/预付	D1	2	expectation_base	电话会🟡P2	事件	—	B	0.40
m_nbis_capacity	NBIS 5GW 上电执行	D1	2	predictor	电话会🟡P2	事件	90d	B	0.55
m_nbis_calltone	NBIS 电话会单价/利用率	D1	3	arbiter	电话会🟡P2	事件	—	B	0.50
m_cn_optics_zte	中际旭创季度营收	D1	1	predictor	交易所🟢P1	季	18d	A	0.735(§6.2)
m_cn_optics_customs	海关光模块出口	D1	1	predictor	海关⚪P4	月	20d	B	0.55
m_lab_funding	前沿 lab 融资	D3	2	predictor	新闻🟢P1-3	事件	180d	B	0.60
m_infer_progress	前沿能力/训练算力	D5	4	predictor	Epoch/AA🟢P1-2	月	—	B	0.50
m_token_econ	推理 cost/token·用量	D6	1	predictor	AA/pricepertoken🟢P3	周	—	A/B	0.50
m_export_ctrl	出口管制	D7	2	regime	BIS🟢P1	事件	—	B/D	0.70
m_dc_power	数据中心电力	D7	2	regime/predictor	IEA🟢P2	年/季	—	B	0.55
四、边层实例(edge_registry · 每条边 cert_tier + 验证怎么跑)
edge_id	from节点	side	hops	cert_tier	cert_method	tradable/warning(§6.3)	evidence
e_optics_nbis	m_cn_optics_zte	supply	3	T1	lead-lag/Granger vs hyperscaler capex(NBIS 点少借代理)	0.32 / 0.16	回测id待建
e_power_nbis	m_nbis_capacity	supply	1	T2	结构+上电进度真值对账	~0.4 / ~0.2	电话会
e_labfund_nbis	m_lab_funding	demand	2	T2	结构+真值对账+敏感性	0.10 / 0.77	Reflection $1B deal 已证一次
e_capability_nbis	m_infer_progress	demand	3	T3	方向,不可回归	~0.05 / ~0.4	只 watchlist
e_export_nbis	m_export_ctrl	regime	2	T2	事件研究(BIS 规则→NVIDIA中国收入→算力供给)	~0.2 / ~0.4	BIS 2026 H200 案
e_power_reg_nbis	m_dc_power	regime	2	T2	结构(电力约束上电)	~0.2 / ~0.3	IEA
五、信号层实例(四类 fct · 真实值填满)
sql
-- 类1 量价(真数)
INSERT INTO fct_quant (metric_id, entity_id, period, value, unit, yoy, knowledge_time, source_url, owner) VALUES
 ('m_cn_optics_zte','ent_zte_photonics','[2026-01-01,2026-03-31]',19496000000,'CNY',1.9212,'2026-04-16','深交所300308一季报','A'),  -- ¥194.96亿 +192.12%
 ('m_nbis_rev','ent_nbis','[2026-04-01,2026-06-30]',582300000,'USD',4.54,'2026-08-12','businesswire NBIS Q2(P1)','A'), -- 收入$582.3M +454%
 ('m_infer_progress','ent_frontier_cap','[2026-01-01,2026-12-31]',4.5,'x/yr',NULL,'2026','Epoch AI 训练算力(P1)','B'), -- 前沿训练算力 +4-5x/年
 ('m_infer_progress','ent_frontier_cap','[2026-09-01,2026-09-30]',53,'index',NULL,'2026-09','Artificial Analysis 智能指数 top(P2)','B'), -- 榜首模型 53
 ('m_dc_power','ent_optics_cn','[2026-01-01,2026-12-31]',1000,'TWh',NULL,'2026','IEA 数据中心电力≈翻倍(P2)','B');  -- 2022~460→2026~1000 TWh

-- 类2 事件(真数)
INSERT INTO fct_event (metric_id, entity_id, event_type, amount, currency, amount_type, is_estimate, event_date, knowledge_time, source_url, owner) VALUES
 ('m_nbis_backlog','ent_nbis','contract',40000000000,'USD','multi_year_cap',false,'2026-06-30','2026-08-12','NBIS Q2电话会(P2,钉transcript)','B'), -- backlog $40B
 ('m_nbis_capacity','ent_nbis','launch',NULL,NULL,'range',true,'2026-12-31','2026-08-12','NBIS Q2电话会(P2)','B'),                    -- 5GW/年底,800MW–1GW by Dec
 ('m_lab_funding','ent_reflection','funding',2000000000,'USD','one_time',false,'2025-10-09','2025-10-09','TechCrunch(P1)','B'),          -- $2B@$8B,Nvidia领投
 ('m_lab_funding','ent_reflection','contract',1000000000,'USD','multi_year_cap',false,'2026-07-14','2026-07-14','TechCrunch/Bloomberg(P1)','B'), -- Reflection↔NBIS $1B算力(证边)
 ('m_lab_funding','ent_cohere','funding',240000000,'USD','annualized',false,'2026','2026','FNEX/Sacra(P3)','B'),                        -- Cohere $240M ARR
 ('m_export_ctrl','ent_nbis','approval',NULL,NULL,'range',false,'2026','2026','BIS 新闻稿(P1)','B');   -- BIS 放开 H200/MI325X 对华出口+美方抽成25%

-- 类3 观点(真数)
INSERT INTO fct_opinion (metric_id, entity_id, variable, speaker, speaker_role, direction, anchor_quote, knowledge_time, source_url, owner) VALUES
 ('m_nbis_calltone','ent_nbis','单位经济','NBIS管理层','management','up','中期合同$20–25M/MW,短期$40–50M/MW;AI分部利润率50%','2026-08-12','NBIS Q2电话会(P2)','B');

-- 类4 前沿(真数)
INSERT INTO fct_frontier (metric_id, entity_id, topic_cluster, method, score, institution, knowledge_time, source_url, owner) VALUES
 ('m_infer_progress','ent_frontier_cap','前沿训练算力','Epoch 追踪',4.5,'Epoch AI','2026','epoch.ai(P1)','B'),
 ('m_infer_progress','ent_reflection','开源前沿模型','能力榜',53,'Artificial Analysis','2026-09','artificialanalysis.ai(P2)','B');
第四类前沿目前只有零星两条——这正是标的驱动欠采第四类的证据,专门的前沿雷达见 doc 29。

六、节点怎么展开(子节点主轴 → 真值 · 举 D1)
D1 算力供给沿拆解主轴(硅→封装→互连→整机→数据中心→分发,doc24v2 §〇.5)展开,每子节点填真源/真值:

子节点	真值(as-of)	源/可得性
芯片/HBM	HBM 产能定性紧;GPU 出货季度	SemiAnalysis🔵 / 财报🟢
先进封装 CoWoS	产能定性	TrendForce🔵
光互连	中际旭创 2026Q1 ¥194.96亿 +192%;800G 24M→63M只	交易所🟢 / semisino🔵
整机/服务器	SUPX 中国 AI 服务器订单(事件)	招投标🟢
数据中心电力	IEA ~1000 TWh 2026;NBIS 5GW 目标	IEA🟢 / 电话会🟡
云容量/分发	NBIS ARR $3.0B、backlog $40B、单价$20–25M/MW	电话会🟡P2
→ 主轴保证 D1 铺满,新子节点(如液冷)出现时自然挂到某一环。

七、边验证怎么具体执行(参考 doc25 §六 + langfuse §5)
① e_optics_nbis(光互连→NBIS,T1 可回测)——怎么跑: 取中际旭创+新易盛季度营收(海外占比拆 AI 敞口) 作 X,NBIS 收入 / hyperscaler capex 作 Y;按 knowledge_time 做 point-in-time 对齐 → 算 lead-lag 相关 + Granger → 报领先期与相关系数 + 样本外稳定性。软肋诚实说:NBIS 仅上市约 1 年、季度点太少 → 用 CoreWeave/hyperscaler capex 作延长历史的下游代理(真值对账),不硬回归 NBIS 单票。

② e_labfund_nbis(lab 融资→NBIS backlog,T2 结构)——怎么跑: 不能直接回归(backlog 预合同化、点少)→ 用 langfuse §5 同一纪律:结构论证(lab 有钱才有采购力)+ 真值对账(Reflection 2025-10 融 $2B → 2026-07 果然签 NBIS $1B 算力合同,这条边被现实证了一次 → cert_score 上调)+ 敏感性分析(结论对"融资→采购转化率"在一个区间内稳不稳)。禁止拿它回归自己(循环)。

③ e_capability_nbis(能力进展→NBIS 用量,T3 方向)——怎么跑: 3 跳、能力→需求无法量化因果 → 只做 watchlist / 方向,cert_score 低、永不据此定仓位。Epoch 训练算力 +4–5x/年、Artificial Analysis 智能指数只作"周期还在不在"的方向读。

验证的工程落点(承 langfuse eval loop):每条边一次验证 = 建 gold(真值样本)→ 人核 → 回归/敏感性 → 结果写回 edge_registry.cert_score/lead_measured/evidence_ids(挂 Langfuse trace/dataset id)→ 定期复验。边不是画完就完,是像指标一样持续验、持续管。

八、实跑诚实结论(这一跑证明/暴露了什么)
✅ 能真跑到"可回测信号":D1 光模块(交易所一手、可拆 AI 敞口)、NBIS 收入/EBITDA(IR 一手)、D5 Epoch/Artificial Analysis(免费权威)、D7 BIS/IEA(一手公开)。
🟡 只能到"结构+真值对账":lab 融资→backlog(NBIS 上市短、预合同化)——但 Reflection $1B deal 事后证了这条边一次,是最漂亮的真值对账实例。
🔵 付费才全:HBM/CoWoS(SemiAnalysis)、一级估值(PitchBook)——免费只拿定性。
⚪ placeholder/合规:海关光模块占比系数(用前必标定)、人才流(合规受限、半人工)。
🔴 最该补的一手:NBIS ARR/backlog/5GW 目前是电话会 P2,钉官方 transcript/IR deck 才能从 P2 升 P1;NBIS 单票回测点不足,须借 hyperscaler capex/CoreWeave 延长历史。
🟣 第四类前沿单薄——标的驱动天然欠采,已另立 doc 29 前沿雷达独立补。
这一跑本身就是交付物2 的最强证据:体系不是 PPT——每字段有真值、每源有可得性分级、每条边有验证 tier 与"怎么跑",诚实标出跑不通的地方(placeholder/付费/点少)。这正切"链稳不稳、可回溯"的第一考核。

下一步选项:①把这套真值填进 panel(蝴蝶结 + 指标树,节点/边可下钻到本文的值与验证);②进 step3,把 e_labfund_nbis/m_nbis_calltone 这类接 Langfuse 真跑一次 eval(建 gold→回归→写回 cert_score);③建 doc 27 总装图把全流程串死。


