

30 假设台账 持续管理 · MD
假设台账(assumptions ledger · 持续管理)
回应 Q2:value/weight 里的系数、以及全程做过的所有假设/先验,集中登记、持续管理,随信息加入逐步明晰。总原则:这些系数当前只用于排序(ordinal),绝对值不承载意义;回测/真值到位后再标定,标定后绝对值才用于 sizing。 这是 langfuse §5"能算的别假设、不编假精度"的落地。与 doc 23(来源总账)并列:一个管"数据从哪来",一个管"我们假设了什么"。主导:D(她要求)+ B(登记)。建于 2026-09-19。

〇、怎么读这本台账(状态机)
每条假设带四栏:

类型:先验(judgment prior)/ 占位(placeholder,待标定)/ 预测(forecast)/ 设计选择(design choice)/ 时效(会过期)。
现在影响什么:🔵仅排序(绝对值不重要)/ 🟠也影响绝对量(sizing/阈值,必须标定后才用)。
用什么信息细化:需要哪种数据/回测才能把它从假设变成标定值。
状态:assumption(未验)/ calibrating(在标)/ validated(已定)/ retired(已被事实取代)。
铁律:🟠 类只要还是 assumption,就不能用于定仓位/触发报警的绝对阈值,只能排序。

一、打分与公式系数(doc 21 §六 / doc 25 §1.3)
#	假设	当前值	类型	影响	用什么细化	状态
A1	因子 H/M/L 锚	0.9 / 0.6 / 0.3	先验	🔵仅排序	回测:实现有用性对因子分档	assumption
A2	节点价值权重	0.45·e+0.25·s+0.20·r+0.10·φ	先验	🔵仅排序	回归:信号有用性 ~ 因子	assumption
A3	传导确定性衰减	c=base×0.9^hops	先验	🟠也影响绝对	回测:每跳实际信息衰减率	assumption
A4	cert_base	T1=0.9 / T2=0.6 / T3=0.3	先验	🟠	各 tier 边的实测命中率	assumption
A5	领先期归一 τ	min(1, 0.25·hops+0.5·l)	先验	🔵仅排序	实测各边 lead 分布	assumption
A6	两产出乘积式	tradable=c·r·s·φ;warning=τ·l·e	设计选择	🔵	是否该乘积(假设因子独立)vs 加权;回测选形	assumption
A7	权重归一	max(tradable,warning) 占比	设计选择	🟠	是否该用 max vs 加和;P&L 归因检验	assumption
A8	provenance→r 映射	P1=0.9/P2·3=0.6/P4=0.3	设计选择	🔵	—	assumption
一句话:第一节全部是排序用的先验,没有一个数是"实测"。回测到位前,它们只回答"谁比谁更值",不回答"值多少"。

二、领先期 / 传导 先验(metric_registry.lead_time_est、边 lead)
#	假设	当前值	类型	影响	用什么细化	状态
B1	中际旭创营收领先美股名	~18d	先验	🟠	lead-lag 实测(doc28 §七①)	assumption
B2	海关月度领先财报	~20d	先验	🟠	同上	assumption
B3	lab 融资领先 NBIS backlog	~180d	先验	🟠	事件间隔实测(Reflection 已一例)	calibrating
B4	NBIS 产能上电领先收入	~90d	先验	🟠	上电→收入确认实测	assumption
三、数据 / 领域 假设
#	假设	当前值	类型	影响	用什么细化	状态
C1	海关光模块占 HS8517 系数	X%(未填)	占位	🟠	招股书/协会口径标定	placeholder
C2	800G 2026 出货	~63M 只	预测	🔵	逐季实际替换	assumption
C3	中际旭创+新易盛 = 全球 AI 建设强度代理	覆盖~60% NVIDIA 800G	先验	🟠	覆盖率核 + 与 capex 对账	assumption
C4	NBIS 单票回测借 hyperscaler capex/CoreWeave 延长历史	用代理	设计选择	🟠	代理与 NBIS 的相关性检验	assumption
C5	NBIS 收入预合同化 → 执行监控非 nowcast	定性成立	先验	🔵定性	后续披露验证	validated(定性)
C6	供需对账"背离"阈值	未定	占位	🟠	历史 regime 标注定阈	placeholder
C7	Cohere/Reflection 估值	在谈 $20–27B	时效	🔵	季度复验(doc23)	assumption(时效)
C8	前沿信号"影响程度"如何量化(Q3 引出)	未定	占位	🟠	见 doc29 影响力评分设计	placeholder
四、已被事实取代 / 已核销(retired)
#	原假设	结局
R1	Reflection 是否即 NBIS 客户	✅ 已证(2026-07 $1B 合同)→ retired
R2	early_A 作 layer 值	✅ 已修(两轴分离,E23)→ retired
R3	signal_stream 作字段	✅ 已改视图(E24)→ retired
五、持续管理机制
出账即登记:任何新系数/先验/占位一出现,进本台账,默认 assumption。
状态机:assumption → calibrating(拿到部分数据)→ validated(回测/真值定死)→ retired(被事实取代)。
🟠 闸门:🟠 类未 validated 禁止用于定仓位或报警绝对阈值(只排序)。这条闸门直接接 edge 的 T3"不下注"、doc23 的 P2"不当硬数"。
回测标定队列(现在最该做的)**:C1 海关系数、C6 对账阈值、A3/A4 传导系数、B1–B4 领先期——这几条是把系统从"排序"升到"能定仓位/报警"的关键。
与 doc23 分工:doc23 管"数据可信度(P1-5)",本台账管"我们假设了什么";一条信号的可信 = 数据 provenance(doc23)× 假设成熟度(doc30)。
一句话给面试官:我把每个系数、每个先验都当假设登记、标"现在只排序不定量、待回测标定"——这不是心虚,恰恰是"不编假精度"的纪律:系统在没有真值前,诚实地只做它能做的(排序),把定量的权力留到数据够了再交出去。


