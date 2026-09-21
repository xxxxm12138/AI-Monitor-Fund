<div align="center">

<img src="assets/readme/hero.svg" alt="Anatole — AI 发展监测体系 · Intelligence Graph" width="100%">

<br/>

![paradigm](https://img.shields.io/badge/paradigm-Intelligence_Graph-8B5CF6?style=flat-square)
![workload](https://img.shields.io/badge/workload-decision--native-089981?style=flat-square)
![truth source](https://img.shields.io/badge/truth_source-DuckDB-2962FF?style=flat-square)
![Python](https://img.shields.io/badge/Python-3-2962FF?style=flat-square&logo=python&logoColor=white)
![as-of](https://img.shields.io/badge/as--of-2026--09-55617A?style=flat-square)
![status](https://img.shields.io/badge/interview-submission-1E2A44?style=flat-square)

<br/>

**从 13F 持仓反向锚定 AI 供给节点，建成可溯源的点边监测体系（DuckDB 真源）；并以 NBIS 占仓样例跑通 REPRESENT → PROPOSE → SELECT → 披露回写的全链路。**

[阅读指南](#阅读指南) • [第一部分：破题](#i-破题与定位信息降维与需求锚定) • [第二部分：建模](#ii-实体建模与-intelligence-graph-计算范式) • [第三部分：落地](#iii-三层架构落地与工程体系) • [第四部分：示例](#iv-示例以-nbis-为例的全链路推演) • [第五部分：终局](#v-终局数据资产沉淀与未来迭代) • [附录：协作](#附录--人机协作纪实)

</div>

---

## 阅读指南

1. **本页目录**
   1. [I. 破题与定位：信息降维与需求锚定](#i-破题与定位信息降维与需求锚定)
   2. [II. 实体建模与 Intelligence Graph 计算范式](#ii-实体建模与-intelligence-graph-计算范式)
   3. [III. 三层架构落地与工程体系](#iii-三层架构落地与工程体系)
   4. [IV. 示例：以 NBIS 为例的全链路推演](#iv-示例以-nbis-为例的全链路推演)
   5. [V. 终局：数据资产沉淀与未来迭代](#v-终局数据资产沉淀与未来迭代)
   6. [附录 · 人机协作纪实](#附录--人机协作纪实)
2. **重要参考**
   - 决策顺序与人机分工：[docs/22](docs/22-解题思路与分工.md)
   - 数据源与处理链路：[docs/21](docs/21-数据来源与处理方法说明.md)
   - 分叉与取舍：[docs/23](docs/23-解题思路.md)
   - 决策视图：[日历式看板](assets/16-AI发展监测日历.html)
   - 工程复现：[pipeline/README.md](pipeline/README.md)

`docs/13`、`docs/process/`、`research/` 为过程稿，不作为入口。

---

## I. 破题与定位：信息降维与需求锚定

> **核心思路**：拒绝全网抓取噪音。从基金真实持仓反向逆推，利用信息在产业链中的降维，获取华尔街难以企及的领先期（Lead Time）与前瞻预测（Nowcast）优势。

“监测 AI 发展”是一个过于宽泛的命题。从对冲基金数据资产沉淀的视角出发，我们需要的是能够支持最终投资决策的因果链。我的破题逻辑包含两重关键拆解：

*   **需求侧锚定 (Demand-anchored)**：必须从基金当前的 13F 真实持仓（如 NBIS、RBRK）及未来目标票池出发，反向逆推我们需要监测的 AI 节点。通过将“AI 供给”与“持仓需求”进行科学溯源的对接，系统过滤出了高信噪比的候选池。
*   **信息降维 (Information Funnel)**：从 Science Lab 到创业公司再到上市公司的演进，是一个信息降维的漏斗。追踪这个降维过程的核心价值，在于获取**领先期 (Lead Time)** 与**信号的确定性**——早期的非结构化科研突破，最终必将降维成清晰的商业 KPI。
*   **锁定核心优势 (Extra Value)**：结合上述两点，系统准确定位了差异化优势——利用中国供应链地面数据（如光模块排产）的时间差与前瞻性，去精准预测（Nowcast）美股 KPI，并据此拆解实现了所需的资源与路径。

---

## II. 实体建模与 Intelligence Graph 计算范式

> **核心思路**：面对极度非结构化、频率错位的底层数据，系统将其抽象为“点与边”的实体模型，并接入 Intelligence Graph 的计算图（Compute Graph），将大模型的开放式生成收敛为可量化的分类与路由。

**1. 底层数据特征洞察 (Data Insights)**
在确定观测信号池后，系统针对真实底层数据的三大痛点建立了处理基建：
*   **非结构化极其严重**：建立强制降维规则，将形态各异的输入（Paper、宏观政策）压缩为标准化的事实表征。
*   **更新频率存在错位**：前沿突发事件与财报季度披露存在时差。系统必须具备跨周期对齐能力，通过计算“领先期（Lead Time）”抹平频率差。
*   **信噪比参差不齐**：建立严密的五级溯源体系（P1-P5）和八步处理 Pipeline。
*(注：受限于时间，本轮重点实证了 NBIS 等持仓，但针对整体大盘的收集规范与处理体系已全部落定，详见 [数据来源与处理方法说明](docs/21-数据来源与处理方法说明.md)。)*

**2. 基于图论的实体建模 (Entity Modeling)**
面对清洗后的数据，系统完成了实体建模：
*   **点 (Nodes)**：AI 供给侧拆解为 7 个维度及前沿雷达。指标仅存定义，严格区分于事实本身。
*   **边 (Edges)**：借鉴图论视角，边不仅代表关联，更具有方向、权重和脆弱性（如通过计算供应链“最小割”直接定位风险咽喉）；结合运筹学与信息论，量化信号的确定性衰减。每条边历经 T1(可回测)/T2(对账)/T3(定性) 三层验证（[`edge_registry` ↗](pipeline/SCHEMA.md#tbl-edge_registry)）。

**3. 计算图设计：Intelligence Graph**
> *灵感参考：孟醒[《JEV火了，但真正重要的不是JEV》](https://mp.weixin.qq.com/s/m2NUWypKHN3Lv857aNVhSg)——“统一接口（Token）不等于统一计算。能通过 Generation 表达的智能，不意味着都应该通过 Generation 计算。”*

为了进行投资判断，我们不需要大模型去“写一篇 3000 字的生成式研报”。在投研这种 Decision-native 的场景中，**扣动扳机是极低频的，但前期的信息筛选、验证、路由是极高频的。** 如果每一次微小的判断都启动自回归生成器，系统经济学将无法支撑。

因此，系统摒弃了单纯的 Prompt Engineering，转向 **Intelligence Orchestration（智能编排）**。我们将点边模型接入以下计算循环：
*   **REPRESENT (表征)**：这是耗时最长、最依赖 Harness 的一步。将外部非结构化长文，压缩成 Point-in-time 的标准化状态，提取出 Deterministic 的事实。
*   **PROPOSE (提出候选)**：当数据出现背离时，沿传导边展开，枚举出所有可能影响持仓的因果解释。
*   **PREDICT (预判)**：结合领先期评估该信号对未来 KPI 的影响幅度。
*   **SELECT (选择与剪枝)**：系统不再生成长文本，而是直接对有限的候选空间进行概率打分（Scoring），通过证伪与影响力双重闸门，剪枝剔除无效假设。

<div align="center">
<img src="assets/readme/paradigm.svg" alt="计算范式" width="90%">
</div>

---

## III. 三层架构落地与工程体系

> **核心思路**：理论范式必须应对真实工程中的摩擦力。系统被切分为三层实体架构，以实现事实与假设的绝对解耦、AI 模型的可控管理（白盒化），以及向研究员直觉的高效折叠。

### 1. 数据层：事实与假设的解耦 (Data & Pipeline)
在投研中，最危险的是将主观预判当成客观事实。工程上必须做到物理隔离：
*   **绝对真实的底层**：底层只存储绝对干净的、遵循 P1-P5 溯源的事实记录（[`source_master` ↗](pipeline/SCHEMA.md#tbl-source_master)）。
*   **假设台账 (Assumptions Ledger)**：所有涉及主观预判的传导概率与权重系数，全部分离存入独立的“台账”（[`assumption` ↗](pipeline/SCHEMA.md#tbl-assumption)）。预测出现偏差只需调参，真实数据链绝不被污染。
*   **自动化入库**：严格分离指标定义与四类事实表，按 `采集 → 快照 → 抽取 → 路由 → 校验 → 迁移` 的 Pipeline 自动流转。

### 2. 治理层：执行路由与白盒化管理 (Governance)
<div align="center">
<img src="assets/readme/calibration-loop.svg" alt="校准复盘双控制器闭环" width="80%">
</div>

为了将 AI 从黑盒转变为可管理的系统组件，控制流被明确切分：
*   **三路执行路由**：确定性逻辑交给 **Code**（如关系映射、规则计算）；复杂的语义压缩交给 **LLM**；而最终的信号定档与方向复核，必须交由 **人工** 兜底。
*   **Agent Trace (设想与规划)**：未来的规划是全面接入 Langfuse。通过留存每一次 Prompt 与 Output 形成观测轨迹，并建立 Eval 机制对模型分类准确度持续打分，确保高精度数据资产沉淀。

### 3. 呈现层：决策视图重构 (Decision-Oriented Presentation)
底层执行着复杂的图计算，但系统的终端出口必须向研究员的投资直觉靠拢，屏蔽底层的技术复杂度。
*   **日历式主视图与影响卡 (Impact Card)**：抛弃给数据管理者看的复杂 Schema，极简为三个核心决策信息：事件本体描述（这是什么）、传导对象与权重（影响谁）、验证逻辑的时间点（下一步盯什么）。（👉 [点击查看 Demo](assets/16-AI发展监测日历.html)）

---

## IV. 示例：以 NBIS 为例的全链路推演

> **核心思路**：事实表征与因果假说解耦；披露前完成路径选择；披露后将结果回写为可回放的校准记录。沉淀的是判断轨迹，而非单次预测命中。

基于 2026 Q2 13F，**NBIS 权重约 51%**。决策窗口为 Q1 股东信日 **2026-05-13** 至 Q2 披露日 **2026-08-12**（91 天）。海关 HS8517 序列仍为 placeholder，未进入本轮推断。

**路径：** 观测状态（上游供给扩张、订单落地、并网与上季收入尚未同步）→ 候选空间 **{A 天花板 · B 时差 · C 打穿全年}** → SELECT 取 **B** → Q2 兑现：序列收入支持 B，全年指引不支持 C。

<div align="center">
<img src="assets/readme/nbis.svg" alt="NBIS 供需对账" width="85%">
</div>

### 4.1 REPRESENT · 事实表征（不含因果解释）

季报由 **Code** 解析，股东信与电话会由 **LLM** 抽取，统一写入 [`fct_quant`](pipeline/SCHEMA.md#tbl-fct_quant)。回测仅允许使用 `knowledge_time` 不晚于决策时点的记录。

| 传导链 | 事实（as-of Q2 披露前） | knowledge_time |
| :--- | :--- | :--- |
| **供给** | 旭创 Q1 营收 **195 亿元，YoY +192%**（`r320`）；新易盛 Q1 **83 亿元，YoY +106%**（`r328`） | 04-17 / 04-24 |
| **需求** | Reflection 融资 **$2B**，随后与 NBIS 签订算力合同 **$1B**（`r404` / `r406`）；OpenAI $122B、Anthropic $65B | 截至 07-14 |
| **公司** | 合同电力 **>3.5 GW**，年底指引 **>4 GW**；并网 / 可上架 **800 MW–1 GW**（已并网容量 ≠ 合同电力）；Q1 AI cloud **$389.7M**；FY 指引 **$3.0–3.4B** | 05-13 |

抽取职责止于字段映射：旭创一季报 → `r320` actual；Q1 股东信 “more than 4 GW” → `r255` guidance。海关月报保持 placeholder，不进入后续候选空间。

### 4.2 PROPOSE · 互斥候选空间

图结构为三条**并行传导链**，而非串行漏斗：供给侧汇聚于「集群在建」；需求侧经 lab 采购落地；并网属于公司产能执行边，不接入光模块供给。[`graph_data.py`](pipeline/graph_data.py)

<div align="center">
<img src="assets/readme/evidence-nbis.svg" alt="NBIS 传导结构与候选空间 A/B/C" width="92%">
</div>

图中绿色 / 橙色对照即为该冲突。对「尚未同步」至少存在三种互斥解释，披露前均未被证伪：

| 候选 | 因果解释 | 对 Q2 的可证伪预测 | 头寸含义 |
| :--- | :--- | :--- | :--- |
| **A 天花板** | 并网容量构成当期硬约束 | 收入仍接近 Q1 **$390M** | 不增加敞口，等待并网数据 |
| **B 时差** | 并网滞后于合同电力；按假设 B4（产能领先收入约 90 天）计入 Q2 | **环比显著高于 Q1**；不要求 FY 指引上修 | 偏向增持 |
| **C 打穿全年** | 需求强度足以迫使 FY **$3.0–3.4B** 上修 | 当季加速 **且** 全年指引上修 | 提高进攻性敞口 |

打分函数 `c·r·s·φ` / `τ·l·e` 仅用于候选排序；系数仍为先验假设，**不进入 Sizing**（[`assumption`](pipeline/SCHEMA.md#tbl-assumption)）。

### 4.3 SELECT · 披露前路径选择

窗口截止 **2026-08-12 开盘前**。选择 **B**：合同电力已 **>3.5 GW**、Reflection 合同 **$1B** 已落到 NBIS、Q1 已披露 exceeded expectations，更符合入账时滞，而非产能硬约束。排除 A（将时滞误判为约束）；排除 C（全年指引已内含后半程加速，上修构成独立跳跃）。

### 4.4 闭环 · 披露后回写与校准

| 口径 | B 的事前预测 | Q2 实现 | 标签 |
| :--- | :--- | :--- | :--- |
| AI cloud | 环比显著高于 $389.7M | **$575M**（QoQ **+47.6%**） | **B 成立** |
| 集团 | 同上 | **$582.3M**（QoQ **+46.0%**） | **B 成立** |
| ARR | 随产能确认上移 | $1.92B → **$3.0B** | 与 B 同向 |
| FY 指引 | B **不要求**上修 | 仍 **$3.0–3.4B** | **C 不成立**；B 的覆盖范围限于序列收入 |

**误差归因**（按 outcome 落点分层）：

| 情形 | 修正层 | 本例 |
| :--- | :--- | :--- |
| 候选已在池内、路径选错 | **SELECT**：`decision_log` 记 wrong，同类状态下对该路径降权 | 若选 A：并网偏低并不蕴含当季收入无法兑现；A 保留在下一期候选池 |
| 事后成立的解释当时未枚举 | **PROPOSE**：补入 `candidate_pool` | 本例未发生 |
| 字段抽取错误 | **REPRESENT** | 本例未发生 |
| 将 B 的成立自动晋升为 C | 禁止；C 保持独立跳跃 | FY 指引未动，C 记不成立 |

**迭代路径（规划）：**
1. **轨迹**：每次 SELECT 记一条 Agent rollout。observation = `state_anchor`（当时可知的 record_id 与 as-of）；action space = {A,B,C}；action = 选中路径；delayed reward = 披露后的 correct / wrong / mixed。
2. **评测**：离线看校准（置信度是否等于命中率）与候选召回（事后成立的路径当时是否在池内）。
3. **训练**：SELECT 训成离散动作上的 policy head，输出 P(路径 | 状态)；REPRESENT 的抽取轨迹接入 Langfuse，以 span-level eval 迭代抽取器。

工程底座：[`checks.py`](pipeline/checks.py) 拦截未验证假设进入 Sizing；`change_log` 按 as-of 重放当时可见记录；`v_health` 监测信源时效。

## V. 终局：数据资产沉淀与未来迭代

> **核心思路**：真正的护城河不是单次的个股预测，而是系统自身的运行纪律。基于对当前系统断点的诊断，把这套单票验证工具迭代为可横向复制的数据资产。

### 5.1 当前系统的断点与缺陷诊断
1. **回测深度不足，系数仍为假设**：目前的周频/季频数据多为近期的点状快照，缺乏历史时间序列。这导致“点边模型”中的权重和传导系数，绝大多数仍是停留在“假设台账”里的主观先验，无法达到 T1 级别的量化验证。
2. **缺乏自动化调度与排队机制**：虽然架构规划了 Code/LLM/人工的分工，但由于没有引入调度器，数据的采集、抽取和入库尚未形成真正的自动化流转。
3. **LLM 结果缺乏闭环监控**：目前的判断层多为 AI 初稿，但对 LLM 提取的准度缺乏系统的评估（Eval）和反馈循环。

### 5.2 下一步的迭代路径与资源需求
针对上述断点，下一步的演进路径及所需资源如下：
1. **数据纵深回填与系数标定**
   *   **行动**：向历史回溯，补齐过去数个财季与周期的底层数据。
   *   **资源与工具**：需要额外的历史研报、行业数据库授权（如海关历史明细），以及用于大批量回测标定的算力资源。有了历史序列，我们才能将主观假设替换为统计显著的客观系数。
2. **打通自动化调度与 Eval 闭环**
   *   **行动**：引入工作流调度器（如 Airflow 或 Prefect），实现数据管道的定时、自动流转。同时，真实落地 Langfuse，收集 LLM 犯的错形成专属数据集，优化分类与抽取的准确度。
   *   **资源与工具**：需要云端的编排工具基建，以及早期需要更多的人力介入复核，以完成初期 Eval 数据集的标注。
3. **横向扩展：从单票样板到全域资产**
   *   **行动**：在上述基础设施（数据深度、调度、监控）跑稳的前提下，将 NBIS 的迁移脚本与处理逻辑复制到其他通用 AI 标的与未来目标票池中。
   *   **目标**：将这套被验证过的生产线，以极低的边际成本横向复制，最终实现从“验证当前持仓”向“自动推演并发现未来投资机会”的系统升级。

---

## 附录 · 人机协作纪实

> **协作方式**：人定问题边界、取舍标准与验收口径；AI 负责展开、落库与起草。先对齐上下文再动手，关键分叉由人拍板，过程中持续纠偏。以下为不同环节的原始截图，按时间顺序排列。

### 1. 破题启动：手写框架 + 对齐上下文

题面拆解、手写推演，以及开场时要求 AI 先确认基金与任务背景，再按手稿框架推进。

<div align="center">
<img src="assets/readme/collab/01-kickoff.jpg" alt="破题启动" width="88%">
</div>

### 2. 交付物与拆解口径

明确最终要呈现的三块：解题思路（含聊天与手稿）、追踪体系本身、人机分工；并给出供给侧漏斗与需求侧锚定的初步拆法。

<div align="center">
<img src="assets/readme/collab/02-deliverables.jpg" alt="交付物与拆解" width="88%">
</div>

### 3. 动手前再确认理解

供需两侧框定后，先让 AI 复述任务语境与分工，确认对齐再进入逐步执行。

<div align="center">
<img src="assets/readme/collab/03-align.jpg" alt="对齐确认" width="88%">
</div>

### 4. 建模纠偏：跳数、节点质量、D1–D7

对 AI 产出追问价值函数里 hops 的定义、节点质量是否写入公式、七维子节点是自下而上还是先有完备框架。

<div align="center">
<img src="assets/readme/collab/04-model-critique.jpg" alt="建模纠偏" width="88%">
</div>

### 5. 图结构：呈现、边确定性、体系打通

从图论 / 信息论 / 运筹角度讨论布局；节点清楚之后，追问边的论证是否纳入 scope，以及如何回接到监测体系目标。

<div align="center">
<img src="assets/readme/collab/05-graph-questions.jpg" alt="图结构追问" width="88%">
</div>

### 6. 呈现层：表与图互相佐证

参考外部看板形态，要求表不能取消；并客观讨论是否需要公司层筛选、图的触发粒度落在节点还是公司。

<div align="center">
<img src="assets/readme/collab/06-presentation.jpg" alt="呈现层讨论" width="88%">
</div>

### 7. 收敛原则：列是浅层信息

停止堆列；重心放到处理思路、判断层 insight，以及数据 / 文字 / 图表的最优呈现形式。

<div align="center">
<img src="assets/readme/collab/07-judgment-focus.jpg" alt="收敛原则" width="88%">
</div>

### 8. 判断层加厚：信息论 · 图论 · 博弈

在路径打分表之上，要求从信息增益、中心性 / 最小割、共识 vs 异见等角度补 insight，而不是再加静态分数列。

<div align="center">
<img src="assets/readme/collab/08-extra-value.jpg" alt="判断层加厚" width="88%">
</div>
