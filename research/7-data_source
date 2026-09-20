

23 数据与资料来源总账 持续管理 · MD
数据与资料来源总账(source registry · 持续管理)
回答两件事:(1) "用的都是真实数据吗?"——诚实分级;(2) 全部数据/资料来源的分类总账 + source_master schema + 持续管理机制。 承 doc 14 数据原则(E13:真实、可溯源、不用示例值)。本轮已对最承重数字做一手核验(见 §一"本轮核验变动")。主导:D(她提要求)+ B(AI 核验)+ C(人定 schema)。最后核验日:2026-09-19。

一、先回答:"用的都是真实数据吗?" —— 诚实分级(五级 provenance)
一句话:是。全部实质数字都可溯源到公开披露/报道,无一编造、无示例值。但"真实"≠ 同一等级——按下面 P1–P5 标注每个数,这套标注本身就是可回溯纪律(= 你 langfuse 那套"核 primary 源、不编假精度"的延伸)。

级	含义	本样板里属于此级的(举要)
P1 一手/权威已核	公司 IR/press release、交易所公告、主流一手报道(TechCrunch/Bloomberg/Reuters)	NBIS 收入 $582.3M/+454%、Adj EBITDA $236.2M(businesswire IR);中际旭创 2026Q1 营收 ¥194.96亿/+192.12%、净利 57亿/+262%(交易所公告);Reflection–Nebius $1B 算力合同(2026-07-14);Reflection $2B@$8B 融资、Nvidia 领投(2025-10-09)
P2 管理层电话会口径(类3)	电话会 highlights 转述,真实但需钉官方 transcript/IR deck	NBIS ARR $3.0B、backlog $40B、客户预付 $9B、5GW 产能、FY2026 指引——这些不在 results press release 里,来自电话会转述
P3 二手媒体/研报/聚合	真数但需回一手	800G 份额、"Nebius AI 分部 $575M/98%"、Cohere/Reflection 生态数(semisino/sacra/fnex/App Economy)
P4 估算/预测/指引(已标)	明确非实测	800G 2026 出货 63M 只(预测)、海关反推光模块、FY guidance
P5 设计层评分(非外部数据)	打分/先验,不是外部事实,不该被当"数据"核	valuable_score、lead_time_est、部分 knowledge_time 精度
本轮核验变动(2026-09-19,把上面几级落实)
✅ 升级为 P1:NBIS 收入/EBITDA(businesswire 一手)、中际旭创 Q1(交易所公告,营收增 192.12% 精确、另净利 +262% 可补)、Reflection–Nebius $1B 合同(TechCrunch/Bloomberg/Reuters)、Reflection $2B@$8B 融资(TechCrunch)。
⚠️ provenance 更正(重要):NBIS ARR $3.0B / backlog $40B / 5GW / 预付 $9B / FY 指引经核不在 Q2 results press release,而是电话会口径→ 从"财报数"降标为 P2,须钉官方 call transcript/IR deck 后才可当硬数用;"Nebius AI 分部 $575M、占 98%"一手未拆分 → 标 P3。
🔄 时效性(估值易过时):Cohere 估值 $7B 可能已过时——新报道为在谈 $2–3B、估值 ~$20B(ARR $240M 仍稳);Reflection 二轮估值报道口径不一($25B / ">$20B"),原文档"$27.5B"偏高 → 已改为"$8B 已确认 + 二轮 $20–27B 在谈"。
✅ 待核销项:doc 20 挂的"Reflection 是否即 NBIS 客户 Reflection AI"——已确认(2026-07 双方 $1B compute deal,Nvidia 算力),verify_status: 待核 → confirmed。
🚫 失效源留痕:雪球(xueqiu.com)被 Aliyun WAF 拦截 → 已用新浪/semisino/证券日报替代,记 access=blocked。
结论回你原话:"都是真实数据分析",但真实分五级;本轮把最承重的 4 组升到一手、把 5 组管理层口径/估值如实降标或标时效、销掉 1 个待核项。以下把这套变成一本能持续管理的账。

二、source_master:来源也要落库(扩展 doc 21 schema)
数据要可追踪,则源本身也必须是一等对象(不能只在 fct 里存一个裸 url)。新增一张表,fct.*.source_id 外键指向它:

sql
CREATE TABLE source_master (
  source_id      TEXT PRIMARY KEY,            -- src_nbis_ir_q2_2026
  name           TEXT NOT NULL,
  publisher      TEXT,                         -- Nebius IR / 深交所 / TechCrunch / Sacra
  source_tier    TEXT CHECK (source_tier IN ('P1','P2','P3','P4','P5')),
  source_kind    TEXT CHECK (source_kind IN
                 ('ir_release','exchange_filing','prospectus','customs',
                  'call_transcript','broker_research','news_media','data_aggregator')),
  data_class     SMALLINT[] DEFAULT '{}',      -- 该源供给哪几类数据 1量价/2事件/3观点/4前沿
  covers_entity  TEXT[] DEFAULT '{}',          -- ent_nbis / ent_zte_photonics ...
  covers_metric  TEXT[] DEFAULT '{}',          -- m_nbis_arr / m_cn_optics_zte ...
  url            TEXT,
  access         TEXT CHECK (access IN ('open','paywall','blocked')),
  frequency      TEXT,                          -- event/quarterly/monthly
  reliability_note TEXT,                        -- 为何是这个 tier / 软肋
  verify_status  TEXT CHECK (verify_status IN ('confirmed','pending','stale','placeholder')),
  superseded_by  TEXT REFERENCES source_master(source_id),  -- 旧源不删,标被谁取代
  first_seen     DATE,
  last_validated DATE
);
它坐实"可追踪/可管理":fct 记录 → source_id → source_master 一行 → tier/kind/access/verify_status 一目了然;改一处源、别处不失控;superseded_by 与 fct 的 revision_flag 同构(旧值留痕)。

三、来源分类总账(inventory,持续管理主体)
A. 一手源(P1 · 优先回归)
source_id	名称 / publisher	kind	类别	覆盖	频率	访问	状态
src_nbis_ir_q2_2026	Nebius Q2 2026 results — Business Wire(IR)	ir_release	1	NBIS 收入/EBITDA	季	open	confirmed
src_zte_300308_q1_2026	中际旭创 2026 一季报 — 深交所公告/新浪F10	exchange_filing	1	中际旭创营收/净利	季	open	confirmed
src_zte_300308_2025ar	中际旭创 2025 年报 — 深交所公告	exchange_filing	1	2025 营收/海外占比	年	open	pending(回原文)
src_eoptolink_300502	新易盛 定期报告 — 深交所公告	exchange_filing	1	新易盛营收	季/年	open	pending(回原文)
src_customs_gac	海关总署 月度出口(HS8517)	customs	1	光模块反推	月	open	placeholder(系数待标定)
src_reflection_nebius_deal	Reflection–Nebius $1B 合同 — TechCrunch/Bloomberg/Reuters(2026-07-14)	news_media	2	客户确认/需求	event	open	confirmed
src_reflection_raise	Reflection $2B@$8B、Nvidia 领投 — TechCrunch(2025-10-09)	news_media	2	一级融资	event	open	confirmed
B. 二手 / 聚合源(P2–P3 · 需回一手)
source_id	名称 / publisher	kind	类别	覆盖	状态
src_nbis_call_q2_2026	NBIS Q2 电话会 highlights — BigGo / Yahoo	call_transcript(转述)	2/3	ARR/backlog/5GW/预付/指引	pending(钉官方 transcript)
src_appeconomy_neocloud	Neocloud Economics — App Economy Insights	news_media	3	单价/单位经济口径	confirmed(观点)
src_graniteshares_nbis	What Nebius Does — GraniteShares	data_aggregator	3	NBIS 业务定性	confirmed(定性)
src_semisino_optics	China's AI Optics Exporters — Semisino	news_media	1/3	800G 出货/份额	pending(回研报/协会)
src_photoncap_optics	Chinese Optical Modules Top10 — Photoncap	news_media	3	中国厂份额	confirmed(定性)
src_sacra_reflection / src_sacra_cohere	Reflection / Cohere — Sacra	data_aggregator	2	ARR/估值/融资	时效敏感
src_fnex_cohere / src_valueaddvc_cohere	Cohere $240M ARR / 估值 — FNEX / ValueAddVC	data_aggregator	2	Cohere ARR/估值	stale(估值)
src_aibusiness_reflection / src_turingpost_reflection	Reflection 融资/估值 — AI Business / Turing Post	news_media	2	二轮估值	时效敏感(口径不一)
src_iofund_circular / src_bisnow_neocloud	循环融资 / "WeWork 2.0" — io-fund / Bisnow	news_media	3	泡沫风险论据	confirmed(观点)
src_mlq_rubrik	Rubrik Q3 FY26 — mlq.ai / Rubrik IR	news_media/ir	1	RBRK(池子对照)	confirmed
C. 待补一手(缺口队列)
NBIS 官方 call transcript / IR deck → 补钉 ARR $3B / backlog $40B / 5GW / 预付 $9B / FY 指引(现为 P2)。
300308 / 300502 招股书 + 年报原文 → 中际旭创/新易盛营收、海外占比、客户集中度、续单率(现引自媒体)。
海关 HS8517 明细 + 光模块占比标定源(行业协会/东吴研报)→ 把 conversion_assumption 的 X% 标定(现 placeholder)。
Reflection / Cohere 一级融资一手(官方博客 / 监管 Form D)→ 融资额与估值(现媒体口径,估值时效敏感)。
四、数据点溯源分级表(每个承重数字 → 值 / tier / 类型 / 状态)
数据点	值	用于 metric	tier	类型	一手源	状态
中际旭创 2026Q1 营收	¥194.96亿(+192.12%)	m_cn_optics_zte	P1	实测	深交所公告	✅confirmed
中际旭创 2026Q1 净利	~57亿(+262%)	(可补)	P1	实测	深交所公告	✅新增可用
中际旭创 2025 营收	¥382亿(+60%,海外91%)	m_cn_optics_zte	P1/回原文	实测	年报/新浪	⚠️回年报
新易盛 2025 营收	¥248亿(+187%)	m_cn_optics_eoptolink	P3	实测	semisino	⚠️回年报
800G+ 出货	2025 24M→2026 63M 只	m_800g_shipment	P3/P4	25 实测·26 预测	semisino	⚠️26 为预测
NBIS 收入	$582.3M(+454%)	m_nbis_arr	P1	实测	businesswire IR	✅confirmed
NBIS Adj EBITDA	$236.2M(~41%)	m_nbis_arr	P1	实测	businesswire IR	✅confirmed
NBIS ARR	$3.0B(+598%)	m_nbis_arr	P2	电话会口径	电话会转述	⚠️钉transcript
NBIS backlog	$40B	m_nbis_backlog	P2	电话会口径	电话会转述	⚠️钉transcript
NBIS 产能	5GW/年底,800MW–1GW by Dec	m_nbis_capacity	P2/P4	电话会·目标	电话会转述	⚠️钉transcript
NBIS 单价	中期$20–25M/MW·短期$40–50M/MW	m_nbis_calltone	P2	电话会口径	电话会转述	⚠️钉transcript
Reflection–Nebius 合同	$1B+ 算力(2026-07-14)	m_lab_funding	P1	实测事件	TechCrunch/Bloomberg	✅confirmed(销待核)
Reflection 融资①	$2B@$8B,Nvidia 领投(2025-10)	m_lab_funding	P1	实测事件	TechCrunch	✅confirmed
Reflection 融资②	二轮 ~$2.5B,估值 $20–27B(在谈)	m_lab_funding	P3	报道/在谈	Turing Post/roic	⚠️口径不一
Cohere ARR	$240M	m_lab_funding	P3	报道	FNEX/Sacra	大致稳
Cohere 估值	~$7B → 在谈 ~$20B	m_lab_funding	P3	报道	Yahoo/Forkast	🔄stale
五、持续管理机制(这本账怎么"活")
append-only + 状态机:每个源/数据点带 verify_status(pending → confirmed → stale)、last_validated。出账即 pending,核销留痕(本轮已销 Reflection 待核)。
superseded_by 链:旧值/失效源不删,标"被谁取代"(与 fct revision_flag、doc 22 的 revised 同构)——回测时可回到任一历史口径,不产生未来函数。
复验节奏(按 tier 差异化):
P2 电话会口径 / P4 指引 / 估值时效项 → 每财报季 + 每融资事件复验(估值最易过时)。
P1 事件类 → 事件驱动(新合同/新融资/新月报出现即落一条)。
placeholder(海关系数) → 用前必标定,否则该信号不进 nowcast、只做方向。
失效源处理:源被墙/改版(如雪球 WAF)→ access=blocked + superseded_by 指到替代源,不假装还能取。
与体系挂钩:source_id 进 fct → Langfuse trace 可回到"哪源、哪天、哪步";source_master 与 metric_registry 一样是单一真源,改源只动它。
触发落账:新财报 / 新融资 / 新海关月报 / 分析师口径变化 / 源失效——任一发生即 append 一条并更新 last_validated。
六、缺口与待办(诚实收尾,= 复验队列)
🔴 海关 HS8517→光模块占比系数:最大 placeholder,标定前该链只做方向不下注。
🟠 NBIS ARR/backlog/5GW/指引:钉官方 call transcript / IR deck,从 P2 升 P1。
🟠 300308 / 300502 年报·招股书原文:落实你 langfuse 纪律"关键数必回一手"(媒体易张冠李戴)。
🟡 Cohere / Reflection 估值:季度复验(现口径不一、易过时)。
🟢 已完成:Reflection↔NBIS 同体核销;NBIS 收入/EBITDA、中际旭创 Q1、Reflection 融资升 P1;雪球失效留痕。
回填提示:本轮更正需回填——doc 20/22 的"Reflection 待核"改 confirmed;doc 19/22 的"Nebius AI 分部 $575M/98%"标 P3;doc 20 的 Cohere/Reflection 估值加时效标注。已在 doc 22 就地更正,doc 19/20 保留原文 + 本账为准(单一真源)。


