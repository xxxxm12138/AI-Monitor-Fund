# 竞品扫描 · 对"映射"的启发记录

**日期** 2026-09-20 ｜ **性质** 竞品借鉴(D 提供三组扫描 · B 提炼对映射的启发)｜ **用途** 指导 AI→ticker 映射(edge_registry / propagate / 决策层)的下一步设计

---

## 〇 核心判断:映射是三组竞品都不占的空白

D 扫的三组,没有一个在做我们的**映射**(类型化 AI→ticker 因果边 + 传播 + 假设台账)。它们分别是我们 pipeline 的三段,不是映射的竞品:

| 组 | 是什么 | 对我们 = pipeline 哪一段 |
|---|---|---|
| 一、AI 发展追踪(Epoch / Stanford AI Index / Artificial Analysis / LMSYS / State of AI) | 测"AI 到哪了",不落票 | **COLLECT 的上游源**(已接) |
| 二、另类数据 → KPI nowcast(Daloopa / YipitData / M Science / TickerTrends / AlphaSense·Tegus) | nowcast 下季 KPI,不按 AI 组织、不建类型化因果边 | **SELECT 终点的验证落点** |
| 三、血缘/目录/治理(dbt / DataHub / OpenMetadata / Great Expectations / OpenLineage / ADR) | 数据管道的血缘与治理,非投资因果边 | **整条 pipeline 的治理**(我们手搓 lite 版) |

**结论**:大家都有数据、有 nowcast、有血缘,**没人有"会自我校准的 AI→ticker 因果映射图"**。中间那段映射 = 全部差异化所在。

---

## 一 最该偷的三个机制(按对映射的增值排序)

### 1. State of AI Report 的「预测记分卡」→ 边级预测校准闭环(最高价值)
- **它做什么**:每年发带日期的预测,第二年逐条打分。
- **偷什么**:把这套用在**每条边**上——一条边不只是"AI 事件↑ → NBIS",而是一个**可证伪、带日期的预测**("光模块 H1 放量 → NBIS Q3 收入读数,领先约 X 周"),到期用真值打分。
- **为什么高价值**:把映射图从静态因果图变成**会自我校准的图**;这正是 JEV/决策层已建的 confidence→outcome→calibration 环,只需从"判断"扩到"边"(decision_log 的 retro/outcome/v_calibration 骨架已在)。
- **落点**:edge_registry × decision_log × v_calibration。

### 2. DataHub / OpenMetadata 的 impact analysis → propagate 的原型 + 治理
- **它做什么**:点一个上游表 → 高亮所有下游受影响的表 + 血缘路径;带 ownership / 审批 / deprecation 传播。
- **偷什么**:① 呈现——面板像 impact analysis 那样"点一个 AI 节点 → 亮出所有受影响 ticker + 路径"(= 我们的传播图);② 治理——它的 owner/审批/deprecation 对应我们边的 owner/status/change_log。
- **必须守住的区别**:它的边是**机械的**(SQL 派生,确定性 100%);我们的边是**概率因果**(T1/T2/T3 置信度 + 方向 + 领先期 + 衰减)。**偷 UX 与治理,不偷语义**——带置信度的因果边才是我们比数据目录多出来的。
- **落点**:propagate 呈现 + edge_registry 治理字段(已有 owner/status/last_validated)。

### 3. YipitData / M Science 这类另类数据 → 把 cert_tier 客观化
- **它做什么**:地面数据(信用卡/receipt)nowcast 下季收入/订阅。
- **偷什么**:一条链的 **cert_tier 用"终点是否可被另类数据 nowcast"来客观定义**——终点落在可 nowcast 的 KPI = T1(可回测);落在无法观测的 = T3。把 T1/T2/T3 从手工拍变成有客观判据。
- **附带**:它们本身是三层漏斗里"终端源(给验证)"的供应商。
- **落点**:edge_registry.cert_tier 判据 + d_edge_tier 判断。

---

## 二 次一级启发

- **dbt**:① `exposures`(标"哪个看板消费这个模型")→ 我们标**"哪个 ticker 决策消费这条边"**(边 → decision_registry),实现"某因子一改,哪些 ticker 判断受影响"的反查;② `tests as contracts` = checks.py(已有,reconcile_flag 就是边级 expectation);③ 列级血缘 → evidence_ids 做成可追溯血缘。
- **Daloopa**(KPI + 源链接 + 锚点):= 我们 fct_quant + provenance + snapshot + anchor,**已对齐**。启发 = 一条标准线:映射**终点读数(ticker KPI)必须做到 Daloopa 级锚定**,别在终点松掉。
- **AlphaSense / Tegus**(文档问答检索,不建因果边)= **反面参照**:市场最大玩家不做因果图,确认映射是真空白。**别拼检索**,做它做不了的图;其专家纪要可当**边的证据源**(evidence_ids)。
- **Stanford AI Index**:逐年同口径、中立、可溯源的 taxonomy 纪律 → 我们七维监测层应保持**年年可比的一致性**。
- **OpenLineage / ADR**:run 级血缘事件 → 每次 propagate 可记为一条血缘事件;ADR 架构决策记录 = 我们的思路层(thesis_node/decision_fork)+ JEV 决策层,**已有**。

---

## 三 落到进度的一句话

三组恰好对应 pipeline 三段:**第一组 = COLLECT 源(已接)· 第二组 = SELECT 终点验证落点(YipitData 该用来定 tier)· 第三组 = 治理(dbt/DataHub 手搓 lite)**。没人做、也是全部价值的,是**中间的映射**。三个借鉴里对映射最增值、且已有一半地基的,是 **State of AI 记分卡 → 边级预测校准**(把 decision_log 的 outcome 环扩到 edge_registry)。这和 JEV/决策层是同一件事,现在有竞品佐证:**大家都有数据、nowcast、血缘,没人有会自我校准的因果映射图。**

**下一步候选**:①(推荐)边级预测校准 = edge_registry × decision_log,让映射图会学习;② propagate 呈现按 impact-analysis 范式;③ cert_tier 用另类数据可 nowcast 性客观化。

---

## 四 KPI 落点呈现调研(2026-09-20 · 竞品实测)

sink 可以是可观测 KPI(不止 ticker)。调研 YipitData / M Science / Daloopa / Visible Alpha / TickerTrends / AlphaSense 如何呈现 KPI 落点:
- **TickerTrends 最全**:一行一 KPI = Bogey(隐含买方预期)/ Consensus / **Δ%(分歧)** / Confidence / **MOE(回测历史误差)** + 修正 sparkline(hover PIT)+ 下钻 source-level 信号 + 漏斗动量(唯一接近因果链)。
- **Daloopa**:逐格 provenance 到一手 filing(最硬),Excel 原生;不做估计。
- **Visible Alpha**:行项级共识 + 分析师离散/outlier(共识变分布)。
- **AlphaSense**:历史+前瞻共识,逐格链 filing,但 KPI 是检索命中不建因果。
- **YipitData/M Science**:公开页只露报告/仪表盘/feed,界面级细节需登录,未取到。

**共同缺口 = 我们的差异化**:全部把 KPI **孤立**呈现(会到多少 + 源),**没有一家把 KPI 当作"某条 AI 发展经因果链推到的终点"**。我们的 KPI-sink 卡多一行"传播来路"。
详细卡设计 → `PLAN-graph-refactor.md §十一`。影响力闸框架已换(likelihood × 渠道 × KPI),cert_tier = 该 KPI 可 nowcast 档,MOE/Confidence 两列是 tier 客观化的呈现模板。
