

33 节点指标库 持仓侧与ai侧 真数填充 · MD
节点指标库 · 持仓侧 + AI侧 · 真数填充(metric_registry R 真源)
这是双真源里的 R(节点/指标库),用真实数据填满。两个入口轴:①持仓侧——从真实 13F 持仓票进入(需求锚),每票 → 它被监测的 KPI 节点 + 该节点上游映射到哪个 AI 维;②AI侧——从 AI 发展 7 维 scope 进入(供给/前沿),每维 → 它的节点 + 真值。两侧共享同一张 metric_registry;两侧的交点(RBRK 自身就是 D6 节点、FCEL 是 D1/D7 节点、NBIS 是 D1 需求锚)就是映射落点。

数据 as-of 2026-09-19;可信度分五级 P1 一手/权威 · P2 电话会口径 · P3 二手聚合 · P4 估算 · P5 设计层(doc 23);人机 owner A/B/C/D;可得性 🟢一手公开 · 🟡待钉一手 · 🔵付费 · ⚪placeholder。承 doc 28(NBIS 已深填)+ doc 24v2(AI侧节点全集)。主导:B(查证实例化)+ C(schema)。

〇、两侧关系(为什么这样切)
      持仓侧(需求锚·从票进)                       AI侧(供给/前沿·从scope进)
      NBIS 51% ─────────────────── D1 算力供给 ◀── 中际旭创/新易盛/海关/GPU·HBM/电力
      RBRK 30% ═(本身就是节点)═════ D6 商用落地 ◀── 企业AI adoption·ARR / token经济
      FCEL 7%  ═(本身就是节点)═════ D1+D7 电力·能源 ◀── 数据中心供电 / IEA
      STAA 8%  ──(无AI敞口)──────── ✗(中国医疗ICL=中国地面数据nowcast,非AI)
                                      D2 数据 · D3 资本 · D4 人才 · D5 算法前沿(见 doc29 雷达)
持仓侧回答"我的书里每只票靠什么活、该盯它哪个数";AI侧回答"AI 发展整体在这 7 维走到哪"。
交点 = 边的落点:一只票向上游映射到的 AI 维节点,就是 doc 21 edge_registry 里那条边的 from_metric。
STAA 是诚实的例外:它 8% 在书里,但是医疗(ICL 近视晶体)、不是 AI;它值钱是因为中国 ICL 销售 = 中国地面数据 nowcast 的教科书标的(切基金"中国数据读美股/港股"的打法),与"监测 AI 发展"无关 → 保留在持仓侧库、标 out-of-AI-scope。
一、持仓侧节点库(13F 2026Q2:NBIS 51.2 / RBRK 29.8 / STAA 8.0 / FCEL 7.1 = 96%)
NBIS 51.2% · Nebius(neocloud/AI 算力)· →D1 · 需求锚
节点	最新真值(as-of)	频率	源/可得性	prov	owner
收入/EBITDA	Q2'26 收入 $582.3M,+454% YoY	季	Nebius IR businesswire 🟢	P1	A
ARR	~$3.0B(退出速率)	季	Q2 电话会 🟡	P2	A
Backlog/预付	$40B multi-year	事件	Q2 电话会 🟡	P2	B
容量(5GW 上电)	目标 5GW;'26 年底 800MW–1GW	事件	Q2 电话会 🟡	P2	B
单位经济	中期合同 $20–25M/MW、短期 $40–50M/MW;AI 分部利润率 ~50%	事件	Q2 电话会 🟡	P2	B
RBRK 29.8% · Rubrik(数据安全/AI 治理)· →D6(+D2)· 本身即 AI侧节点
节点	最新真值(Q2 FY27,期末 2026-07-31,报 08-27)	频率	源	prov	owner
收入	$427.3M,+38% YoY(vs $309.9M)	季	IR/财报 🟢	P1	A
Subscription ARR	$1.66B,+33% YoY	季	IR 🟢	P1	A
Cloud ARR	$1.48B,+39% YoY	季	IR 🟢	P1	A
净新增订阅 ARR	+35% YoY	季	IR 🟢	P1	A
FCF	$65.7M(vs $57.5M)	季	IR 🟢	P1	A
AI 产品线	推 Rubrik AI + Agent Cloud(护 AI agent);$500M 英国投资	事件	新闻 🟢	P1	B
RBRK 是持仓侧与 AI侧的交点:它的 ARR 增速本身就是 D6 企业 AI adoption 的一手读数(AI 落地 → 数据/agent 安全需求)。

STAA 8.0% · STAAR Surgical(医疗 ICL)· out-of-AI-scope(中国 nowcast 标的)
节点	最新真值(Q2'26,期末 2026-07-03)	频率	源	prov	owner
总净销售	$93.535M,+111% YoY	季	10-Q 🟢	P1	A
中国净销售	$52.341M,+887.5% YoY(2025 去库存低基数)	季	10-Q 🟢	P1	A
APAC / ICL 量	APAC +189%,ICL units +216%	季	10-Q 🟢	P1	A
净利	$8.058M($0.16/股),扭亏	季	10-Q 🟢	P1	A
事件	Alcon 收购被否(股东 2026-01-06 反对)→ Broadwood letter	事件	公告 🟢	P1	D
非 AI。留库理由:中国 ICL 销售 = 中国地面数据 nowcast 样本(与 AI 无关,但切基金打法);对"AI 发展监测"贡献 = 0。

FCEL 7.1% · FuelCell Energy(燃料电池/AI 供电)· →D1+D7 · 本身即 AI侧节点
节点	最新真值(Q3 FY26,期末 2026-07-31)	频率	源	prov	owner
收入	$33.0M,−29% YoY(vs $46.7M)	季	globenewswire 🟢	P1	A
Committed backlog	$1.296B(+4.1%);awarded 2.350B;合计 $3.646B	季	IR 🟢	P1	B
首个数据中心供电协议	75MW,德州,大型 DC 运营商(未具名),带预付(季后签)	事件	IR 🟢	P1	B
产能	年化 ~37.1MW → 目标 100MW by Oct'26 → 500MW by Jun'28	事件	IR 🟢	P1	B
净亏/现金	净亏 $(45.3)M(收窄);现金 $737.3M	季	IR 🟢	P1	A
FCEL 是交点:75MW DC 供电协议 = D1 数据中心电力 / D7 能源约束的一手事件读数(AI 算力落地的电力瓶颈)。

尾仓 ~4% · 8 只 AI 算力 · ⚪待补
节点	值	说明
尾仓 8 只名单	⚪ 待补	名单在她上传的 13F excel(本会话磁盘无留存)→ 需她再传/贴。已知:Q1→Q2 从 LITE/SNDK/CIEN/CRCL 轮动出,进 NBIS/RBRK
二、AI侧节点库(D1–D7 · 承 doc 24v2 全集 + doc 28 真值)
D1 算力供给(基金视角最高)
节点	最新真值	频率	源/可得性	prov	owner
中际旭创(300308)光互连	H1'26 营收 ¥417.78亿,净利 +242% YoY;1.6T 供需缺口 ~40%	季/半年	深交所半年报 🟢	P1	A
新易盛(300502)	⚪ 待填最新(交易所有源)	季	交易所 🟢	P1	A
海关光模块出口(HS8517)	月度出口额(⚪占比系数未标定)	月	海关总署 ⚪	P4	B
GPU/HBM/CoWoS 出货	定性紧(免费只拿定性)	季	SemiAnalysis/TrendForce 🔵	P3	B
NBIS 5GW 上电	见持仓侧 NBIS	事件	电话会 🟡	P2	B
hyperscaler capex	作光模块→NBIS 回测的下游代理	季	电话会/edgar 🟢	P2	B
D2 数据供给(科研高·基金中)
节点	最新真值	频率	源	prov	owner
data wall/合成数据	事件驱动(定性)	事件	arXiv/Epoch 🟢	P3	B
数据标注支出/定价	⚪ 待事件	事件	Scale/Surge 招聘 🟢	P3	B
版权诉讼/授权	事件驱动	事件	news 🟢	P3	B
D3 资本(基金高)
节点	最新真值	频率	源	prov	owner
前沿 lab 融资	Reflection $2B@$8B(2025-10,Nvidia 领投);Reflection↔NBIS $1B 算力(2026-07,证边);Cohere $240M ARR(2026)	事件	TechCrunch/官方 🟢	P1–P3	B
赛道资金流/一级估值	付费才全	事件	PitchBook/烯牛 🔵	P3	B
Nvidia 系战略/循环融资	事件驱动	事件	news 🟢	P3	B/D
D4 人才(降优先/半人工)
节点	最新真值	频率	源	prov	owner
顶尖研究员流向	⚪ 合规受限、半人工	事件	领英/论文署名 ⚪	P3–P5	C
D5 算法与能力前沿(科研最高 · 详见 doc 29 前沿雷达)
节点	最新真值	频率	源	prov	owner
前沿训练算力趋势	+4.5x/年	月	Epoch AI 🟢	P1	B
模型能力/智能指数	榜首 53	周	Artificial Analysis 🟢	P2	B
论文主题斜率	需去季节性+引用加权	日	arXiv/OpenAlex 🟢	P3	B
开源 vs 闭源差	HF 下载/GitHub star	周	HF/GitHub 🟢	P3	A/B
D6 商用落地/token 经济(与持仓侧 RBRK 交汇)
节点	最新真值	频率	源	prov	owner
企业 AI adoption/ARR	RBRK Sub-ARR $1.66B,+33%(一手样本)	季	IR 🟢	P1	A
推理 cost/token·用量	分模型、口径杂	周	AA/OpenRouter 🟢	P3	A/B
AI 应用留存/渗透(中国出海)	App 活跃/下载	日/周	第三方 🟢	P3	A/B
D7 政策·能源·安全(基金高 · 与持仓侧 FCEL 交汇)
节点	最新真值	频率	源	prov	owner
出口管制	BIS 放开 H200/MI325X 对华+美方抽成 25%	事件	BIS 新闻稿 🟢	P1	B/D
数据中心电力	IEA ~1000 TWh(2026);FCEL 75MW DC 协议(一手事件)	年/事件	IEA 🟢 / FCEL IR 🟢	P2/P1	B
AI 监管/安全	EU AI Act/美各州(事件)	事件	法案文本 🟢	P3	B/D
三、两侧交点表(持仓票 ↔ AI 维,= edge_registry 的 from_metric 落点)
持仓票	分量	映射到 AI侧节点	关系	已验证?
NBIS	51%	D1 光互连(旭创)· D1 hyperscaler capex · D3 lab 融资 · D7 电力/出口	需求锚,多边入	光模块 T1 / lab 融资 T2(Reflection $1B 已证)
RBRK	30%	D6 企业 AI adoption(它自己就是样本)	本体(0 跳)	一手财报,无需外推
FCEL	7%	D1 数据中心电力 + D7 能源	本体/供给	75MW DC 协议(结构 T2)
STAA	8%	—(无)	非 AI	N/A(中国 nowcast 另账)
尾仓	4%	D1 算力(⚪ 待名单)	供应链	待补
四、缺口 / 待补清单(诚实)
⚪ 尾仓 8 只名单:在她上传的 13F excel,本会话无留存 → 需她再传或贴名单。
⚪ 新易盛 300502 最新值:交易所有源,待填(半年报)。
⚪ 海关光模块占比系数:未标定,用前必标(doc 30 假设台账 C1)。
🟡 NBIS ARR/backlog/5GW:现为电话会 P2 → 钉官方 transcript/IR deck 才升 P1。
🔵 GPU/HBM/CoWoS、一级估值:付费(SemiAnalysis/PitchBook),免费只定性。
⚪ D4 人才:合规受限、半人工、ROI 低 → 降优先。
D2 数据供给:多为事件/定性,无稳定量值节点(如实。)
五、统计与去向
一手可回测(P1,🟢)集中在:持仓侧 NBIS 收入 / RBRK 全口径 / STAA / FCEL;AI侧 D1 中国光模块、D5 Epoch/AA、D7 BIS。这几条是体系里最硬的地基。
owner:量价类多 A(可自动),电话会/事件/判读类 B,系数/影响程度/regime 判读 D。
去向:本库 = doc 21 metric_registry 的真数实例;下一步 →(a)把每条边(from_metric→ticker)按 doc 21 §六算 tradable/warning 填 edge_registry;(b)接 panel 两视图(A 按 D1-D7 读本库、B 按 ticker 读交点表)。
来源(本次新填):

Rubrik Q2 FY2027(stocktitan)https://www.stocktitan.net/news/RBRK/rubrik-reports-second-quarter-fiscal-year-2027-financial-0ru6sfyuq6xe.html
STAAR Surgical Q2 2026 10-Q(stocktitan)https://www.stocktitan.net/sec-filings/STAA/10-q-staar-surgical-co-quarterly-earnings-report-088826ce7e00.html
FuelCell Energy Q3 FY2026(globenewswire)https://www.globenewswire.com/news-release/2026/09/02/3355029/8041/en/fuelcell-energy-reports-third-fiscal-quarter-2026-results-executes-first-data-center-power-agreement-increases-annualized-production-rate-focuses-on-capacity-expansion.html
中际旭创 H1 2026 半年报(营收¥417.78亿/净利+242%,虎嗅/新浪转半年报)https://www.huxiu.com/moment/1273267.html


