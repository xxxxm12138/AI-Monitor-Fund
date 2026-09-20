

24 ai发展监测层 数据源指标字段 扣题视图 · MD
AI 发展监测层:数据源 · 获取方式 · 指标 · 字段(扣题视图)
专门回答"扣题":题面是"搭建监测 AI 发展 的追踪体系"。本文把散在 doc 16(全景口径)、doc 17(字段/数据源)、doc 19–23(NBIS 样板)里的东西,按"AI 发展本身的维度"重新端平,让"监测 AI 发展"成为一等交付物,而不是让整套读起来像"给 NBIS 选股"。不造新 schema——全部落到 doc 21 的四类 fct 表。主导:D(她提扣题)+ B(AI 梳理)。

〇、先把扣题讲死:题目问什么、我答什么
题面拆解:①搭建监测 AI 发展 的追踪体系;②自定分析角度/数据源/更新频率/展现方式;③讲清逻辑 + 标 AI/human。

"AI 发展"有两义,题目两义都要,但最容易漏第一义:

能力前沿发展(scientist 义):AI 能做什么、边界往哪迁——模型能力、推理范式、开源追赶、新范式(世界模型/具身/AI4S)、research、人才。这一义最贴"AI 发展"字面,且完全不经过任何股票。
产业/变现发展(投研义):算力/芯片/光模块/云/电力/adoption——AI 怎么落到收入。这一义近 ticker、可回测。
我的角度(题面允许自定):投研驱动 + scientist 口径,两义合流(doc 16 口径)。demand-anchored(锚基金持仓)只决定先把哪部分做深,不把监测对象缩成一只股票。监测对象始终是"AI 发展"整体(下面五维度);NBIS 只是把监测输出落到一个可观测节点的验证点。

一、AI 发展监测的五个维度(监测对象 = AI 发展本身)
把"AI 发展"拆成五个可监测维度,横切 doc 16 的价值栈六层。维度①④⑤前半 = 能力前沿义(纯 AI 发展,无 ticker);②③⑤后半 = 产业变现义(近 ticker)。

维度	监测什么(AI 发展的哪一面)	主数据类	领先性	直接扣"AI 发展"?
① 能力/技术前沿	模型能力、推理范式、开源vs闭源、新范式拐点	类4+类3	最早(领先二级数季度~数年)	✓✓ 最字面
② 算力/基础设施	光模块/芯片/云容量/电力——AI 在建强度	类1+类2	领先财报 2–3 周	✓(产业义)
③ 资本/生态	前沿 lab 融资、赛道资金流、估值、pre-IPO	类2	领先 backlog 数季度	✓
④ 人才	顶尖研究员流向、明星团队 spin-out	类2	最领先的动量信号	✓✓
⑤ 商用/落地	API/token、企业 adoption/ARR、应用留存	类1+类2	同步~略领先	✓
二、核心梳理:每维度 → 指标 → 数据源 → 获取方式 → 字段 → owner → 频率
字段列 = 落到 doc 21 哪张 fct 表 + 该表关键 payload 字段(每条还都强制带 doc 17 §2.1 通用元数据层:knowledge_time / source_id / anchor / entity_id / data_class / signal_role / owner / valuable_score)。

维度① 能力/技术前沿(纯 AI 发展,不经 ticker)
指标	数据源	获取方式	落表.字段	类	角色	owner	频率
前沿模型能力(benchmark 分)	LMArena / SWE-bench / GPQA / ARC-AGI 榜、官方技术报告	榜单 API / 爬取 / RSS	fct_frontier(benchmark, score, method, institution, knowledge_time)	4	方向/仲裁	A/B	事件+日
论文主题斜率(范式拐点)	arXiv、顶会(NeurIPS/ICML/ICLR/CVPR/ACL)、引用	arXiv API / OpenAlex / Semantic Scholar	fct_frontier(topic_cluster, citation_velocity, authors, method)	4	方向	A/B	日
推理时算力趋势	技术报告、Epoch AI、论文	爬取 / 整理	fct_frontier(topic_cluster, method) + fct_opinion(direction)	4/3	方向	B	事件
开源 vs 闭源差距	HuggingFace 下载、GitHub star、开源模型发布	HF/GitHub API	fct_frontier(score 对比, benchmark)	4	方向	A/B	周
新范式信号(世界模型/具身/AI4S)	顶会主题、lab 博客、demo	主题聚类	fct_frontier(topic_cluster)	4	预警/方向	B	事件
维度② 算力/基础设施(AI 在建强度,近 ticker · 可回测)
指标	数据源	获取方式	落表.字段	类	角色	owner	频率
光模块出货/营收	中际旭创·新易盛财报、海关 HS8517、第三方出货	akshare/cninfo、海关平台	fct_quant(period, value, yoy, conversion_assumption, assumption_source)	1	预测变量	A/B	季/月
hyperscaler capex	电话会 / 10-Q	edgartools / 转写	fct_quant + fct_opinion(direction, anchor_quote)	1/3	预期基准+预测	B	季
GPU 租赁价/交货周期	云价格页、访谈	爬取 / 专家访谈	fct_quant(value, revision_flag)	1	预测/regime	A/B	周
neocloud 容量/backlog	公告、电话会	新闻 / 转写	fct_event(contract, amount, amount_type, is_estimate)	2	预测+预警	B	事件
数据中心电力/散热订单	PPA、机组订单公告	公告 / 新闻	fct_event(order, amount, event_date)	2	预测	B	事件
维度③ 资本/生态(钱往哪涌 = 需求真伪的领先读)
指标	数据源	获取方式	落表.字段	类	角色	owner	频率
前沿 lab 融资	Crunchbase / PitchBook / CB Insights、SEC Form D、官方博客、TechCrunch	API / news	fct_event(funding, amount, amount_type, round, subject_entity, is_estimate)	2	预测(需求持续性)+预警	B	事件
赛道资金流/估值轮动	PitchBook、IT桔子 / 烯牛(中国一级)	API / 爬取	fct_event 聚合	2	方向/轮动	B	事件
pre-IPO 池 / 打新	一级 DB、招股书	API / 整理	fct_event + entity_master(maturity=pre_ipo)	2	方向	C	事件
维度④ 人才(最领先的动量信号,纯 AI 发展)
指标	数据源	获取方式	落表.字段	类	角色	owner	频率
顶尖研究员流向	领英、论文署名变化、GitHub、团队页	爬取 / 半自动+人工	fct_event(personnel, subject_entity, object_entity, relation)	2	方向(动量)	C	事件
明星团队 spin-out	新闻、工商注册	news / 工商	fct_event(personnel/launch)	2	方向/预警	B/C	事件
维度⑤ 商用/落地(AI 变现的终点)
指标	数据源	获取方式	落表.字段	类	角色	owner	频率
API 调用/token 消耗/降价曲线	官方价格页、第三方	爬取	fct_quant(value, yoy)	1	预测	A/B	周/月
企业 AI adoption / ARR(如 RBRK)	财报、招聘 JD、支出调查	edgartools / 爬取	fct_quant + fct_event(order)	1/2	预测/预期基准	A/B	季/事件
AI 应用留存/渗透(中国出海)	App 活跃/下载/榜单	第三方数据	fct_quant(value)	1	预测	A/B	日/周
三、扣题自检表(逐条对题面)
题面硬要求	本体系怎么答	落点
① 监测 AI 发展	五维度覆盖 能力前沿①+基础设施②+资本③+人才④+落地⑤;①④及⑤前半是纯能力前沿监测,不经任何 ticker	本文§一/§二 + doc 16 口径
② 自定分析角度	投研驱动 + scientist 口径,两义合流;demand-anchored 决定做深顺序,非缩小对象	doc 16 §一
② 自定数据源	每指标一源(§二每行)	§二 + doc 17 §5.1
② 自定更新频率	每指标一频率:日(论文/榜/应用)、周(GPU价/开源)、月(海关/光模块)、季(capex/ARR)、事件(融资/人才/发布)	§二"频率"列 + §四
② 自定展现方式	类1→时序/三态;类2→事件流/关系图/watchlist;类3→分级表/情绪;类4→主题热力/斜率曲线;统一挂指标树、节点带 A/B/C/D chip	doc 17 §三
③ 讲清逻辑 + 标 AI/human	每指标 owner A–D(§二);全链 Langfuse trace + knowledge_time 可回溯	§二 + doc 22 §六
一句话扣题结论:题目要"监测 AI 发展",我给的是五维度全景监测(能力前沿是第一等公民,独立于任何股票);"自定角度/源/频率/展现"逐项在表里;"AI/human + 讲清逻辑"由 owner 分级 + trace 落实。

四、更新频率总览(题面明确要"更新频率",单独列清)
频率	维度/指标	为什么这个频率
日	论文主题斜率①、benchmark 榜①、应用活跃/下载⑤	高频流,量大必须 AI 筛
周	GPU 租赁价②、开源模型发布①、API 降价⑤	中频,趋势观测
月	海关②、光模块营收②(实为季)、DRAM 价	领先财报的地面数据
季	hyperscaler capex②、企业 ARR⑤、公司财报	定期披露锚
事件驱动	融资③、人才流④、模型发布①、订单/合作②、监管获批	离散事件,不规则
五、和 NBIS 样板的关系(讲清"不是选股")
监测对象 = AI 发展(五维度全景,本文)。这是回答题目的主体。
NBIS 样板(doc 19–23) = 把监测输出落到一个可观测、可投资的节点做验证——证明这套监测"读得出、对得上、用得上",不是学术空转。
NBIS 的需求端读(前沿 lab 融资 / 推理进展 / 人才)其实就是本文维度①③④,只是被挂到了 NBIS 客户身上做交叉验证;解锚后它本身就是通用 AI 发展监测线。
供给端读(光模块/海关)则是维度②的一个实例。
可对面试官说的一句:"我的监测对象是 AI 发展本身(能力/算力/资本/人才/落地五维);选 NBIS 深挖,是因为它同时被算力供给(②)和前沿需求(①③④)两端夹住,是验证'监测→可投资'闭环最省的一个点,不是把系统缩成读一只票。"

六、诚实缺口(交付前补,否则"能力前沿"这义仍偏薄)
维度①④目前只有 schema + 源清单,尚无实跑样本(NBIS 深度在②③)。若时间够,建议给①补一个小实例:抓 1–2 周 arXiv/benchmark 主题斜率或一次模型发布,落成 fct_frontier 几条真records——哪怕小,也把"能力前沿监测"从"说了"变成"做了",端平两义。
维度④人才流向的数据获取合规/可得性要标注(领英爬取受限)——诚实写"半自动+人工"。
五维度的 valuable_score 排序与采集优先级沿用 doc 17 §5.3(中国侧近 ticker 独家的先抓;能力前沿独家但远,做 watchlist)。
下一步选项:①按§六给维度①补一条真实 fct_frontier 小样本(把能力前沿这义做实,最补扣题);或 ② 直接把五维度渲染进 panel(AI 发展监测树,与 NBIS 验证树并列);或 ③ 你先核这份扣题视图,再定。




26 ai发展五维度 专家审查 科研与工程双视角 · MD
doc 24 五维度专家审查:科研 + 工程双视角
Point 2:以顶级 AI 科研专家(拆得全不全/准不准、来源全不全)+ 数据工程师(可行性/工程量、指标齐全性/去重/重要性排序)双视角,审 doc 24 的 AI 发展五维度。结论驱动 doc 24 v2 的重建。主导:B(AI 以专家视角审)+ D(她定审查标准)。审查日 2026-09-19。

〇、一句话结论
doc 24 五维度方向对、但不完整、且有两处重叠。作为科研专家看:漏了三块一等要素——数据、算法/架构、政策·能源·安全(regime 约束);作为工程师看:指标基本可行,但④人才 ROI 低、①的主题聚类工程量被低估。建议从 5 维扩到 7 维、分四族,并给两套重要性排序(科研视角 vs 基金视角)——这两套的差本身是给面试官的洞见。

一、科研专家视角:拆得全不全、准不准
1.1 完整性 —— 三个一等缺口(必须补)
AI 发展的第一性 = 投入要素(compute × data × algorithm × talent × capital)→ 能力产出 → 落地变现,外加约束/regime。拿这把尺子量 doc 24,漏了:

缺口①:数据要素(data)。 训练数据/合成数据/数据标注/版权与获取,是与算力同级的投入要素。合成数据质量突破、数据枯竭("data wall")、版权诉讼直接决定能力前沿能不能续。doc 16 L4 提过,但 doc 24 五维度没把数据列为一等维度——重大遗漏。
缺口②:算法与架构范式(algorithm)。 doc 24 把"新范式"塞在①能力前沿里,但架构/方法的转变(MoE、状态空间/Mamba、test-time training、扩散语言模型、RL 后训练)是能力的供给侧驱动,与 benchmark(能力结果)是两回事。科研上必须显式,否则只盯结果不盯"为什么变强"。
缺口③:政策·能源·安全(regime 约束)。 出口管制(GPU/HBM/设备对华)、能源与电网(数据中心用电审批、核电/PPA)、AI 监管与安全事故——这些是 AI 发展的约束条件与 regime 变量,直接重排算力供给与格局。对一个 96% 压在 AI 算力上的基金,出口管制是头号 regime 变量(直接砸 NVIDIA 中国收入、国产替代、光模块需求),doc 24 完全没有政策维度——最危险的遗漏。
1.2 准确性 —— 三处措辞要收紧
①"论文主题斜率 = 范式拐点最早信号":对,但 arXiv 计量有灌水与会议周期噪声,须去季节性 + 引用加权,否则假斜率。
②"光模块领先财报 2–3 周":精确说是"A股光模块季报领先美股光通信/算力名财报",不是领先"AI 发展"本身——措辞别偷换。
④人才流向:领英爬取合规受限(ToS),准确度与可得性都打折,doc 24 §六已标,保留。
1.3 来源全不全 —— 缺几个一等源(必补)
维度	doc 24 已有	缺的一等源(补)
能力/算法前沿	arXiv/顶会、LMArena、SWE-bench/GPQA、HuggingFace	Epoch AI(算力/训练成本/模型规模权威追踪)、Artificial Analysis(推理性价比/延迟/质量基准,极关键且新)、Stanford AI Index、OpenAlex/Papers with Code
算力/基础设施	中际旭创/新易盛、海关、capex、GPU价	SemiAnalysis(算力/数据中心/供应链最权威付费源)、TrendForce/DIGITIMES、云 spot 价
资本	Crunchbase/PitchBook、IT桔子/烯牛、SEC Form D	The Information(一手融资)、Dealroom、官方博客一手
数据(新)	—	Scale/Surge 招聘与定价、Common Crawl 体量、版权诉讼动态(NYT×OpenAI 等)
政策(新)	—	BIS 出口管制清单(美商务部)、工信部/国务院政策、各国 AI 法案、IEA 电力
二、工程师视角:可行性 / 工程量 / 指标质量
2.1 可行性与工程量(每维度打分)
维度	数据可得性	工程量	合规风险	工程结论
算力/基础设施	高(财报/海关结构化)	低(已有 akshare/edgartools)	低	最先做,ROI 最高
算法与能力前沿	高(API/榜单)	benchmark 抓取低;主题聚类/斜率 中–高(embedding+聚类+趋势检测)	低	benchmark 先上,主题斜率二期
资本	中(付费 API 或 NLP 抽取)	中(免费源需事件抽取)	低	中优先
数据(新)	中(招聘/诉讼/体量分散)	中	中(版权敏感)	中优先,信号价值高
商用落地	中–高	低–中	低	中优先
政策(新)	高(公开文本)	抓取低、判读需人(D)	低	低工程高价值,人判为主
人才	低(领英受限)	高	高(ToS)	降优先/半人工,ROI 最低
工程洞见:doc 24 把①的"论文主题斜率"和④"人才流向"摆得偏高,但前者工程量被低估、后者 ROI 最低。先做结构化、可回测、合规干净的(算力/benchmark/落地),NLP 密集与合规敏感的(主题聚类/人才)放二期。

2.2 指标 (a) 齐全性 —— 每维度补哪些
能力前沿:补 推理性价比曲线(Artificial Analysis)、上下文长度/多模态能力、agentic 任务完成率、训练算力规模(Epoch)。
算力:补 HBM 代际/产能、CoWoS 先进封装产能、电力上电进度、液冷渗透(doc 16 有,doc 24 漏)。
落地:补 推理成本下降曲线(cost/token)、净留存 NRR、AI 原生 vs 套壳判据。
2.3 指标 (b) 去重 —— 两处真重叠(必须切开)
"推理"在 ①能力前沿 与 ⑤商用落地 各出现一次:①的"推理时算力趋势"是能力供给(test-time compute 让模型更强),⑤的"API/token 消耗"是需求变现(用了多少 token)。→ 切开:①留"推理方法进展",⑤留"推理用量/成本"。
"资本"在 ③资本 与 ④人才 各出现一次:doc 24 ④混进了"Nvidia 系资金流向"。→ 资本归一到③,④只留人才(研究员/团队流动)。
2.4 指标 (c) 重要性排序 —— 两套,别混
科研视角(对"AI 发展"本身最本质): ① 算法与能力前沿 ≈ 数据要素 > 算力 > 资本 > 人才 > 商用落地 > 政策约束。 (能力从哪来、数据够不够、算力够不够,是 AI 能走多远的第一性。)

基金视角(对这本 96% 押算力的书最直接,= 映射优先级主判据): ① 算力/基础设施(书直接沾)> 政策/出口管制(regime,直接砸 NVIDIA 链/国产替代/光模块)> 资本(需求真伪/泡沫预警,命中 NBIS 风险)> 算法能力前沿(决定算力持续性)> 商用落地(RBRK/adoption)> 人才(最早但最虚)。

这两套排序的落差本身就是洞见:能力前沿对"AI 发展"最本质,但对我们书,算力 + 政策 + 资本更直接。面试时先讲科研排序(证明懂 AI),再讲基金排序(证明懂映射到书)——这正是 doc 25 映射要用的优先级。

三、审查结论 → doc 24 v2 的改法(交给重建)
5 维 → 7 维,分四族:
投入要素:① 算力供给 · ② 数据供给(新) · ③ 资本 · ④ 人才
能力:⑤ 算法与能力前沿(并入架构范式)
变现:⑥ 商用落地与 token 经济
约束/regime:⑦ 政策·能源·安全(新)
去重:推理拆成 ⑤(方法)vs ⑥(用量/成本);资本归③、人才归④。
补源:Epoch AI / Artificial Analysis / SemiAnalysis / BIS 出口管制 / 版权诉讼 等(见 §1.3)。
补指标:HBM/CoWoS/电力/液冷、推理性价比、cost/token、NRR 等(见 §2.2)。
双重要性排序入 v2,基金视角那套作为 doc 25 映射的优先级主判据。
可行性标注:每维度标工程量与合规,人才维度明确降优先/半人工。
下一步:据本审查产出 doc 24 v2(7 维度 scope 全集,= 映射的上游候选池),再进 doc 25(AI 发展→ticker 映射范式 + 逐票向上游 + 重点节点)。




24v2 ai发展scope全集 7维度 映射上游候选池 · MD
AI 发展 scope 全集(7 维度 · 映射的上游候选池)—— doc 24 v2
承 doc 26 审查重建。取代 doc 24 五维度:补三缺口(数据/算法架构/政策 regime)、去两重叠(推理拆方法vs用量、资本归③人才归④)、补源补指标、给双重要性排序。这是"AI 发展"监测对象的完整、去重、可映射节点全集——即 doc 25 映射时"持仓票向上游反推"的候选池。主导:B(AI 以科研+工程视角重建)+ D(她定 scope 原则)。所有节点落 doc 21 四类 fct 表。

〇、结构:四族 7 维(第一性 = 投入要素 → 能力 → 变现,外加 regime 约束)
投入要素 ── D1 算力供给   D2 数据供给   D3 资本   D4 人才
能力     ── D5 算法与能力前沿(架构范式 + benchmark + 推理方法)
变现     ── D6 商用落地与 token 经济
约束regime ─ D7 政策·能源·安全
〇.5 子节点生成框架(每维度的"拆解主轴",保证 complete-by-construction)
方法(答"子节点怎么列、全不全、是先框架还是边分析边补"):两头对齐。

先 top-down:给每维一条拆解主轴(一条"完整路径"),沿主轴把子节点族生成出来 → 保覆盖、保方向全面。
再 bottom-up:用 doc 25 逐票分析去补充/验证具体子节点 → 保不漏细节。
子节点不抠死细节,但主轴必须能覆盖 AI 发展的该一面。新出现的具体信号(某新架构、某条新政策)自然落到主轴的某一环,无处安放 = 主轴漏了,要补主轴而非只补节点。
维度	拆解主轴(生成原则 = 一条完整路径)	沿主轴的子节点族(覆盖点)
D1 算力供给	算力物理供应链全栈:硅 → 封装 → 互连 → 整机 → 数据中心 → 分发	芯片(逻辑GPU/存储HBM)· 先进封装(CoWoS)· 光/电互连 · 服务器整机 · 电力/散热/网络 · 云容量/利用率/价格
D2 数据供给	数据生命周期:来源 → 加工 → 权属 → 稀缺	真实/合成数据 · 标注 · 版权/授权/合规 · data wall / 稀缺性
D3 资本	资本流动层级:早 → 晚 → 战略 → 退出 → 异常	一级融资(种子-成长-pre-IPO)· 估值/轮动 · 战略投资(Nvidia系)· 并购/IPO 退出 · 异常结构(循环融资)
D4 人才	人才流动方向:进 → 出 → 重组	顶尖研究员流向 · 团队 spin-out · 关键 hire/离职 · lab 重组
D5 算法与能力前沿	投入方法 → 能力维度 → 输出效率 三段	①方法/架构(预训练/后训练/推理时/新架构)②能力(推理/代码/多模态/agentic/长上下文)③效率(推理性价比/开源闭源差/端侧)
D6 商用落地	变现漏斗:用量 → 单位经济 → 采用 → 留存	token 用量 · cost/token 与毛利 · 企业 adoption/ARR/NRR · 应用留存/渗透
D7 政策·能源·安全	约束来源:地缘 → 产业 → 能源 → 监管 → 安全	出口管制 · 国产替代政策 · 能源/电网 · AI 监管/合规 · 安全/对齐事故
为什么这样就"全面":每条主轴是该维度的一条完整路径(D1 = 一颗算力从硅到可租用的全程;D5 = 能力从"怎么变强 → 强在哪 → 多便宜";D6 = 一块钱从 token 到留存的全程)。主轴走通,子节点族即铺满该维度;下面第一节的具体节点表 = 主轴的当前实例化,可随赛道演进只加行、不改主轴。

一、7 维度 × 节点 × 源 × 获取 × 字段 × owner × 频率(主轴的当前实例化)
字段列 = 落 doc 21 哪张 fct 表;每条另强制带 doc 17 通用元数据层(knowledge_time/source_id/entity_id/data_class/signal_role/owner/valuable_score)。

族 A · 投入要素
D1 算力供给(compute) — 基金重要性【高】· 科研【中】· 工程量【低】· 合规【低】

节点	数据源	获取	落表	类	owner	频率
光互连出货(800G/1.6T)	中际旭创/新易盛财报、海关HS8517、SemiAnalysis	akshare/cninfo、海关、付费	fct_quant	1	A/B	季/月
GPU/加速器出货与代际	财报、SemiAnalysis、TrendForce	付费/整理	fct_quant	1	B	季
HBM 代际/产能、CoWoS 先进封装产能	SK海力士/美光、TrendForce/DIGITIMES	整理	fct_quant	1	B	季
neocloud 容量/backlog	公告/电话会	新闻/转写	fct_event	2	B	事件
数据中心电力上电/PPA、液冷渗透	PPA/机组订单、IEA	公告/新闻	fct_event	2	B	事件
GPU 租赁价/交货、云 capex	云价格页、hyperscaler 电话会	爬取/edgartools	fct_quant+opinion	1/3	A/B	周/季
D2 数据供给(data)【新】 — 基金【中】· 科研【高】· 工程【中】· 合规【中】

节点	数据源	获取	落表	类	owner	频率
数据枯竭("data wall")/合成数据突破	arXiv、Epoch AI	API/整理	fct_frontier	4	B	事件
数据标注支出/定价	Scale/Surge 招聘与定价	爬取	fct_quant+event	1/2	B	事件
版权诉讼与授权(NYT×OpenAI 等)	诉讼动态、licensing 新闻	news	fct_event	2	B	事件
D3 资本(capital) — 基金【高】· 科研【中】· 工程【中】· 合规【低】

节点	数据源	获取	落表	类	owner	频率
前沿 lab 融资(额/估值/领投)	Crunchbase/PitchBook/The Information、SEC Form D、官方博客	API/news	fct_event(funding)	2	B	事件
赛道资金流/轮动、估值	PitchBook、IT桔子/烯牛	API/爬取	fct_event 聚合	2	B	事件
Nvidia 系战略投资/循环融资信号	新闻、io-fund 类	news	fct_event	2	B	事件
pre-IPO 池/打新	一级 DB、招股书	整理	fct_event+entity(maturity)	2	C	事件
D4 人才(talent) — 基金【低】· 科研【中】· 工程【高】· 合规【高】→ 降优先/半人工

节点	数据源	获取	落表	类	owner	频率
顶尖研究员流向、明星团队 spin-out	领英/论文署名/GitHub/新闻	半自动+人工	fct_event(personnel)	2	C	事件
族 B · 能力
D5 算法与能力前沿(algorithm & capability) — 基金【中】· 科研【最高】· 工程【benchmark低/主题聚类中-高】

节点	数据源	获取	落表	类	owner	频率
架构/方法范式(MoE/SSM/test-time training/扩散语言/RL后训练)	arXiv/顶会、lab 博客	API/主题聚类	fct_frontier	4	B	日/事件
benchmark 能力(推理/代码/多模态/agentic)	LMArena/SWE-bench/GPQA/ARC-AGI	榜单 API	fct_frontier	4	A/B	事件
推理方法进展(test-time compute)、上下文长度	技术报告/arXiv	整理	fct_frontier	4	B	事件
推理性价比(质量/延迟/成本)	Artificial Analysis	API/爬取	fct_frontier	4	A/B	周
开源 vs 闭源差距	HuggingFace 下载/GitHub star	API	fct_frontier	4	A/B	周
训练算力规模/成本趋势	Epoch AI、Stanford AI Index	整理	fct_frontier	4	B	事件
新范式(世界模型/具身/AI4S)	顶会主题/demo	聚类	fct_frontier	4	B	事件
族 C · 变现
D6 商用落地与 token 经济(monetization) — 基金【中】· 科研【中低】· 工程【低-中】

节点	数据源	获取	落表	类	owner	频率
推理用量/token 消耗	官方/第三方(OpenRouter)	爬取	fct_quant	1	A/B	周
推理成本下降曲线(cost/token)、API 降价	官方价格页、Artificial Analysis	爬取	fct_quant	1	A	周/事件
企业 AI adoption/ARR(RBRK 类)、NRR	财报、招聘 JD、支出调查	edgartools/爬取	fct_quant+event	1/2	A/B	季/事件
AI 应用留存/渗透(中国出海)	App 活跃/下载/榜单	第三方	fct_quant	1	A/B	日/周
族 D · 约束 / regime
D7 政策·能源·安全(governance/energy/safety)【新】 — 基金【高】· 科研【中】· 工程【抓取低/判读需人】

节点	数据源	获取	落表	类	owner	频率
出口管制(GPU/HBM/设备对华)	BIS 出口管制清单、新闻	公开文本	fct_event+opinion	2/3	B/D	事件
国产替代政策	工信部/国务院	公开文本	fct_event	2	B/D	事件
能源/电网(用电审批、核电/PPA)	IEA、地方审批、机组订单	公开	fct_event	2	B	事件
AI 监管(EU AI Act/美各州)、安全事故	法案文本、新闻	公开	fct_event+opinion	2/3	B/D	事件
二、双重要性排序(= doc 25 映射的优先级依据)
科研视角(对"AI 发展"最本质): D5 算法与能力前沿 ≈ D2 数据 > D1 算力 > D3 资本 > D4 人才 > D6 商用落地 > D7 政策约束。

基金视角(对这本 96% 押算力的书最直接 = 映射优先级主判据): D1 算力/基础设施 > D7 政策/出口管制(regime)> D3 资本 > D5 算法能力前沿 > D6 商用落地 > D2 数据 > D4 人才。

两套的落差 = 洞见:能力前沿对"AI 发展"最本质,但对我们书,算力 + 政策 + 资本更直接。 doc 25 逐票向上游映射时,用基金视角这套排优先级,中国侧/可回测仅作旁注标签。

三、去重与准确性(已落实 doc 26 的修订)
推理拆两处:D5 = 推理方法进展(能力供给);D6 = 推理用量/成本(需求变现)。不再重叠。
资本/人才拆开:资本(含 Nvidia 系资金)归 D3;D4 只留人才流动。
算法架构显式:从"新范式"里拎出架构/方法范式,进 D5 一等节点。
措辞收紧:光模块 lead 精确为"A股季报领先美股光通信/算力名财报";arXiv 斜率须去季节性+引用加权。
四、这份 scope 怎么被 doc 25 用
节点全集 = 映射候选池。 doc 25 对每只持仓票向上游反推时,答案只能落在上面这 7 维(主轴生成)的某几个节点上;逐票分析同时反过来补充/验证子节点(bottom-up),补进来的新信号必须能挂到某维主轴的某一环。 若某票追不到任何节点 = 该票非 AI 敞口(如 STAA 医疗、SLMT)→ 标注为方法论样板或出 scope。"是否映射到持仓票 × 票分量 × 映射杠杆"决定哪些节点是重点(基金视角排序),中国侧/可回测作旁注。

下一步(Point 1):doc 25 —— AI 发展 → ticker 映射范式(思考逻辑 + 有向图)+ 逐票向上游映射(NBIS/RBRK/STAA/FCEL + 算力尾仓)+ 重点 AI 发展节点排序。




29 第四类前沿 独立监测模块 ai前沿雷达 · MD
第四类前沿 · 独立监测模块(AI 前沿雷达)
回应 Bonnie 的洞见(对的):第四类前沿(论文 / research lab / 前沿大厂研究动态 / paper / benchmark)是"监测 AI 发展"最本源、最重要的领域,但标的驱动(从票向上游反推)天然拉不到多少第四类。所以第四类必须独立于任何标的、topic-driven 采集,单独成模块 = panel 视图A 主料 / 早期信号层子流A / Phase2 雷达。E24 细化(Q3):数据源分层 + 质量×频率×立场分级 + 两大难点(证伪、影响程度)+ 对 ticker 选取的影响。 主导:D(她提)+ B(设计)。

一、诊断:为什么第四类会被标的驱动"饿死",必须独立
需求锚定(标的驱动)	前沿驱动(topic-driven)
出发点	从持仓票向上游反推	直接扫前沿本身
近端拉到	D1 量价 + D3 事件(类1/2)	D5 能力前沿(类4)
第四类占比	少(多跳远端,顺带)	主产地
结论:标的驱动系统性欠采第四类(doc22/28 里 fct_frontier 只有零星两条,正是证据)→ 名为"监测 AI 发展"实为"监测持仓"。定位:前沿雷达产出 = 方向/范式/watchlist,不直接下注(多跳 T3);独立跑,选择性接回需求端读做泡沫预警。

二、监测对象(topic-driven,不挂票)
承 doc24v2 D5 + doc16 子流A + 五前沿向量:研究前沿 · research lab/大厂动态 · 能力基准 · 开源生态 · 算力成本量化 · 范式向量(scaling/推理时计算/新范式/开源闭源/数据飞轮)。

三、数据源(细分 —— 不同方向/厂/人/平台分开,Q3)
3.1 研究前沿 · 顶会按方向分(不同方向不同顶会)
方向	顶会	用途
通用 ML	NeurIPS · ICML · ICLR	范式主战场、主题斜率
视觉/多模态	CVPR · ICCV · ECCV	世界模型/具身感知
NLP/LLM	ACL · EMNLP · NAACL	语言/推理方法
RL/机器人	CoRL · RSS · ICRA · IROS	具身/VLA
系统/MLSys	MLSys · OSDI · NSDI	训练/推理效率(接算力)
综合/理论	AAAI · IJCAI · COLT	补面
arXiv/OpenReview(预印,最快但未评审)· OpenAlex/Semantic Scholar(引用图/citation velocity)。
3.2 research lab / 大厂研究动态(厂 × focus × 平台)
海外:OpenAI · Anthropic(safety/agentic)· Google DeepMind(science/RL)· Meta FAIR/Superintelligence · Microsoft Research · NVIDIA Research · xAI · Mistral · SSI/Thinking Machines。
国内:DeepSeek(效率/开源)· 阿里 Qwen · 字节 Seed/豆包 · 月之暗面 Kimi · 智谱 GLM · MiniMax · 阶跃 StepFun · 百度文心 · 腾讯混元 · 华为盘古 · 面壁 MiniCPM。
每厂三读:①发布/技术报告/model card(能力+方法)②focus(它押哪条范式)③发表平台各不同——官方博客 / arXiv / X / 微信公众号 / 知乎 / GitHub / HuggingFace / 播客(Dwarkesh 类)。采集要按平台分管道(X 有 API 限制、公众号需另抓)。
3.3 人才维度(顶尖研究员,非机构)
顶尖研究员个人追踪:focus 是什么、focus 在不在变、动向(跳槽/spin-out)。源:Google Scholar(引用/h-index)· X 动态 · GitHub · 领英 · 论文署名迁移。读法:最好的人 focus 迁移 = 范式最早信号(接面试官 network moat);属早期信号层子流C(人才),owner C/D、合规敏感、半人工。

3.4 能力基准 / 开源 / 算力(第三方,中立)
LMArena · SWE-bench · GPQA · ARC-AGI · Artificial Analysis(智能指数/性价比)· HuggingFace 下载 · GitHub star · Epoch AI(训练算力/成本)。

3.5 社媒 / PR(有立场,只做线索)
X · 微信公众号 · Reddit(r/MachineLearning)· HackerNews · 自媒体。默认低权重、只做早期线索,触发去查一手。

三.5 源分级框架(质量 × 频率 × 立场 → 使用层次)—— 解析数据的地基
每个源三维打标,决定"怎么筛、怎么用、用在哪一层":

维	分档
质量/权威	T_a 一手权威(peer-reviewed 顶会、官方 technical report/model card、第三方实测 Epoch/AA)> T_b 半权威(arXiv 预印未评审、大厂官方博客[含 PR 成分])> T_c 社媒/自媒体
频率	日(arXiv/X/HF)· 周(榜单/AA)· 会议周期(顶会)· 事件(发布)
立场/偏见	中立(学术/第三方评测)vs 有立场(厂商 PR 自报 SOTA、自媒体流量)
使用层次(筛选规则):

T_a × 中立 → 可入信号(定量/方向)。
T_b / 有立场 → 先证伪 + 降权,入 watchlist 线索。
T_c 社媒 → 只做早期 leads,触发去查一手,不入定量。
一句话:source 质量是后面解析的地基——先把源分好级,坏源永远不许进定量层,否则 AI 快、信息杂,噪声会污染整条链。

四、前沿数据两大难点(Q3 · 她点的,必须显式化)
难点① 及时性 + 证伪(含金量辨别)
AI 快、信息驳杂;PR/社媒有立场 → 先辨真含金量。证伪四手段:

交叉源验证(多个独立源 confirm);
可复现性(有无开源代码/权重、可复跑 benchmark);
第三方独立测(Artificial Analysis/LMArena 而非厂商自报);
详实度(technical report/peer-review vs 一句 PR)。 → 落 fct_frontier 新字段:source_stance(neutral/vendor_pr/social)、verifiability(reproducible / third_party_verified / claimed_only / rumor)。owner:B 抽取 + D 判。
难点② 影响程度判断(顶刊 ≠ 产业影响)
即便来源可靠(顶刊),也不一定对产业/ticker 有大影响 → 单独判影响力。判据:

是否改变算力需求结构(训练→推理迁移)?
是否降本(cost/token 曲线下移)?
是否被产业采用(大厂跟进 / 开源社区采纳)?
是否有清晰商业化/落地路径?
是否触及瓶颈层(算力/数据/能源)? → 落 fct_frontier 新字段:industry_impact(高/中/低 + 评分)、impact_rationale。owner:D 主判(AI 辅助)。量化方法仍是占位(记 doc30 假设台账 C8,待细拆)。
这两道闸对监测体系 + ticker 选取的影响
前沿信号进 watchlist / 外溢到 ticker 前,必过两道闸:证伪(含金量)→ 影响力(产业相关)。只有 高含金量 × 高产业影响 的前沿信号,才值得沿多跳映射去影响 ticker 判断;其余留在雷达、不外溢。

正例:某开源模型把推理成本砍半(可复现、第三方证、高产业影响)→ 影响 D6 token 经济 → neocloud 需求结构 → NBIS/推理算力票。
反例:厂商 PR 吹 SOTA,无开源无第三方证 → verifiability=claimed_only,只挂 watchlist,不动 ticker。
这两道闸 = owner D 判 + B 抽,是"AI 快、信息杂"下防噪声污染定量层的护栏。
五、处理管线(类4 专线,承 doc17 §5.2)
高频抓取 → 落快照(knowledge_time) → 【源分级过滤(§三.5)】 → LLM/embedding 主题聚类
   → 趋势/斜率检测 + 异常检测 → 【证伪闸 + 影响力闸(§四)】 → 主题时序 → 热力/斜率/watchlist
量大必须 AI(A/B);源分级/证伪/影响力/范式判断人复核(D)。核心信号:主题斜率(范式拐点最早)、benchmark 突破速度、开源追赶闭源差距、训练算力/成本趋势、能力/性价比。

六、字段(落 fct_frontier + metric_registry,承 doc21)
metric_registry:dim=D5、data_class=4、signal_role=predictor(方向)、owner=A/B、maturity=research(三子流由 v_early_signal 视图推,不再存字段,见 doc21 §〇)。 fct_frontier(原有 + E24 新增):topic_cluster/method/benchmark/score/institution/authors/citation_velocity + source_stance / verifiability / industry_impact / impact_rationale(证伪+影响力,§四)。

七、小真实样本(证明能跑,非示例值)
sql
INSERT INTO fct_frontier (metric_id, entity_id, topic_cluster, benchmark, score, institution, source_stance, verifiability, industry_impact, knowledge_time, source_url, owner) VALUES
 ('m_infer_progress','ent_frontier_cap','前沿训练算力','训练算力年增速',4.5,'Epoch AI','neutral','third_party_verified','高(定算力需求量级)','2026','epoch.ai(P1)','B'),  -- +4–5x/年
 ('m_infer_progress','ent_frontier_cap','模型能力前沿','Artificial Analysis 智能指数(榜首)',53,'Artificial Analysis','neutral','third_party_verified','中(能力前沿方向)','2026-09','artificialanalysis.ai(P2)','B');
真数已核:Epoch AI 训练算力 +4–5x/年;Artificial Analysis 智能指数榜首 = 53(2026-09)——两条都是 T_a 中立第三方,直接过证伪闸;其余榜单/下载量同源一次 API 即扩。

八、松映射回票 + 人机分工
前沿信号 → 多跳(T3)→ 票,默认不下注;仅"前沿热 × 供给猛建"背离/共振时,喂 doc22 对账三态做泡沫/信念判断。 分工:抓取/聚类/斜率 = A;源分级 + 证伪 + 影响力 + 范式判断 = D(这是前沿雷达最吃人判的地方);呈现 = 视图A 主题热力 + 斜率 + watchlist,可下钻原文(anchor)。

九、执行优先级(诚实)
独立模块,Phase2 主铺;骨架现在能建(源全免费公开,工程量在 NLP 聚类 + 源分级/证伪管线,中–高)。
两条腿:标的驱动(视图B,可回测定仓位)+ 前沿雷达(视图A,前沿给方向)——合起来才既"监测 AI 发展"又"落到书"。
诚实缺口:industry_impact 量化仍占位(doc30 C8);人才维度合规受限;社媒源需强证伪。
下一步:①接 panel 视图A;②扩样本(SWE-bench/开源差距,一次 API);③纳入 doc27 总装图作"视图A 主料"。


