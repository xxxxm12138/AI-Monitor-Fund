# PLAN · 面板重构对齐 spec —— 从「日历罗列」到「事件传播图」

**日期** 2026-09-20 ｜ **性质** 对齐 spec（B 起草 · 待 D 确认后动工）｜ **上游** `JEV-intelligence-graph.md`（四算子）· `PLAN-decision-layer.md`（决策层）· 现面板 `16-AI发展监测日历.html` ｜ **触发** D：现面板把节点/票的非-AI 信息当成独立重要页面在铺，无 extra value；真正有价值的是 AI 事件、及其对节点/票的影响怎么拆解

---

## 〇 一句话思想（第一位，必须正确）

监测体系的**主对象是 AI 发展事件**；系统的工作是把一个事件**在有向加权图上传播到它的实质影响**。节点（公司/赛道/指标）和基金持仓票**不是目的**，是传播路径上的**传导节点与测量点**——它们的重要性由事件传播**算出来**，而不是各自占一个页面。一个数据是否呈现，只问一句：**它会不会改变我们对某个 AI 发展影响的判断（extra value）**；不会就沉到库里，不上主面板。

这是 JEV 对齐的落地形态：不是「更多罗列」，而是 REPRESENT（把事件压成源）→ PROPOSE（枚举它打到哪些节点）→ PREDICT（每条路径的方向与量级）→ SELECT（剪到有价值的路径）。

## 一 三类对象的新定位

| 类 | 旧定位（现面板） | 新定位 |
|---|---|---|
| **AI 事件**（fct_event / fct_frontier，~107 条） | 和量价、观点混在日历行里 | **主对象、导航入口**。每个事件是一棵传播树的根 |
| **节点 / 持仓票**（entity / metric，非 AI 本体信息） | 各自独立页面，铺上下游/指标/来源/基本面 | **无独立主页面**；永远在库里；**按 salience 涌现**——被活跃事件传播照亮到够亮，才出现在主面板或图上某节点，点开是「它在这条路径上的角色」而非全基本面 |
| **仓外潜在标的**（entity in_book=FALSE 被事件打到） | 无（面板只画 13 只持仓） | **新管理类**。AI 事件打到仓外公司、且证据足够明确（cert_tier ≥ T2 或 provenance ≥ P2），进「潜在标的」池，纳入管理（未来标的候选） |

**"砍" 的精确含义**：砍的是"节点/票作为独立重要页面"，不是砍数据。数据全留库里；判据 = extra value（改不改变某个 AI 影响判断）。已 retired 的非 AI 持仓（STAA 等）本就不在图上。

## 二 计算范式：DAG 上的概率影响传播（不是 Dijkstra）

- 源 = 一个 AI 事件（某指标的一条 fct 记录）。
- 传播 = 从源沿 `edge_registry` 的有向边走，经**一等中间节点**，扇出到多个影响落点（持仓 + 仓外潜在标的 + regime 读数）。
- 路径打分 = ∏（边确定性 c = base_tier·decay^hops）×（节点质量 r·s·φ）× 方向；**乘法衰减、求最高可信/最高影响路径**，非加法最短路。
- 剪枝（SELECT / extra value）= 低于阈值的路径默认折叠；只显示「有价值 + 可测量」的路径。
- 落点验证闸（graphify 的 EXTRACTED/INFERRED = 我们的 T1/T2/T3）：每条路径标注落点**可测量**（能对账的持仓 / regime 读数）还是**纯推断**；仓外潜在标的须 ≥ 证据阈值才浮现，挡住无因果的主题炒作（排除项纪律）。

## 三 主面板重构

- **主视图 = 传播图**（现"映射图·打到谁"从副 tab 升为主视图）：选一个事件 → 展开它的传播树（源 → 中间节点 → 影响落点），节点带含义、边带权重/方向/跳数/tier。
- **日历降为副筛选**（"什么时候来"）：时间轴变成"最近有哪些活跃事件源"的入口，不再是主罗列。
- **节点/票 = 抽屉式下钻**：图上点一个节点 → 侧栏出"它在这条路径上的角色 + 当前读数 + 来源/P 级"，不是独立页面、不铺全基本面。
- **潜在标的区**：仓外被照亮的落点单列一小块（证据级 + 触发它的事件 + 到它的路径）。

## 四 数据模型改动（有界，走 migration）

1. **map_path 文本 → 一等中间节点**：现在 map_path 是 `"全球 AI 集群在建强度 → neocloud 扩张环境"` 这种字符串，35 条边约 40–60 个中间段。升成一等节点（含义/所属维/可选指标/来源），使路径可遍历、中间节点"代表什么"可点开。**主要新工作。**
2. **sink 扩到持仓之外**：`edge_registry.to_ticker` 现在只指 13 持仓；放开到可指仓外 entity / 赛道 / regime。加落点类型标注（持仓 / 潜在标的 / regime / 层）。
3. **节点 salience（涌现规则）**：不是存字段，是**视图**——节点亮度 = 打到它的活跃事件路径的聚合权重 × 时效。定一条 `v_node_salience`。阈值登记为假设（新 C22，🟠）。
4. **潜在标的管理**：仓外落点 ≥ 证据阈值 → 进池；促成"潜在标的"是一次 SELECT 判断，接决策层（candidate_pool / 或新 decision 类型 d_target_watch）。

## 五 复用与关系（这是 70% 重构，不是从零）

- 图已在库：`edge_registry` 35 条有向加权边 = 传播图本体（一直被当打分表用）。
- 事件源已在库：~107 条 fct_event / fct_frontier。
- 四算子已有决策层承接：REPRESENT=fct+元数据 · PROPOSE=candidate_pool · PREDICT=observation_direction+lead_time · SELECT=tradable/warning 阈值 + deprecated/retired。
- **d_factor 因子复核直接决定这张图的路径权重**（路径权重 = tradable/warning = 因子算出）——改完因子，哪些路径够粗、默认显示就变了。所以因子复核不是白做，是这张图的"边宽"来源；等图形态定了一起落更合理。

## 六 渲染选型

- **建议 Cytoscape.js**（cdnjs 单文件可嵌，Artifact 允许）：图为主视图后，需要多路径、扇出、展开/折叠、力导向布局，inline SVG 手写会失控。
- 备选 inline SVG（我们蝴蝶结已会、最稳、零依赖），但只适合固定小图，不适合可遍历扇出图。
- 出版：本地 `16-*.html` 重构 + 可选同时发一个 claude.ai 可分享 Artifact。

## 七 时间盒出版步骤（时间过半）

1. 锁本 spec（D 确认/修订）。
2. migration：map_path 升一等节点 + sink 放开 + v_node_salience + 证据阈值假设。
3. 面板重构：传播图主视图 + 日历副筛选 + 节点抽屉下钻 + 潜在标的区（Cytoscape.js）。
4. 出版（本地 HTML +（可选）Artifact）。

## 八 已定（D 2026-09-20）

1. 思想（第〇节）确认。
2. 中间节点升一等：**先只升 NBIS 主链**（约 15 个）赶出版，其余迭代。
3. 潜在标的证据阈值：cert_tier ≥ T2 **或** provenance ≥ P2（登记为 C22）。
4. 渲染：**Cytoscape.js**。
5. d_factor 9 改：随本轮 Phase 1 一起落（图权重更准）。

---

## 九 呈现形式：图（结构）+ 三张决策卡（字段）

### 9.0 三种可选对象 → 三张卡（解决「一个节点既是事件又是影响」）

卡的类型**跟着你选中什么走**，不是节点的属性：
- **信号**（有日期的一条 fct 记录）→ **信号卡**：什么发生了。
- **路径**（一条边 / 一条链）→ **路径卡**：影响怎么传导。
- **节点**（持久 entity / metric）→ **节点档案**：一个对象、双角色分区（既被推动、又发信号）。

一个节点（如 NBIS）天然既是"被光模块 / lab 融资推动的影响"，又是"自己发财报事件的源"。它**只有一个档案**，内含「入边（什么在推动它）」与「出信号（它发出什么、传给谁）」两个分区——点节点看完整档案，点具体一条打到它的路径看路径卡，点它发出的某条信号看信号卡。不打架。

**extra-value 判据贯穿全部**：Bloomberg/FactSet 已有的（价格、市值、原始营收、一致预期）一律沉到「折叠·本体读数」，默认不显；lead 的永远是"从 AI 事件到 P&L 驱动因子的因果翻译"。

### 9.1 信号卡（选中一条 fct 记录）

| 字段 | 来源列 | 为什么 lead / 或折叠 |
|---|---|---|
| 一句话是什么 | metric_registry.name + stg_observation.value/note | lead：事件本体 |
| 何时可知 | fct_*.knowledge_time | lead：point-in-time，成长股靠早 |
| 证据级 P1–P5 + 来源 | fct_*.provenance · source_master.name/url · snapshot_id | lead：诚实标定，不吹 |
| 对主线方向 | observation_direction.direction（↑↓→!—） | lead |
| 点燃哪些路径 | edge_registry WHERE from_metric = 本记录指标 | lead：它扇出到哪 |
| so-what 一句 | 最强边的落点 + 方向（max tradable/warning） | lead：最重要那条影响 |
| 原文长描述 | fct_*.anchor_quote / note | 折叠 |

### 9.2 路径卡（选中一条边 / 链）——核心 extra value

| 字段 | 来源列 | 说明 |
|---|---|---|
| 拆解链（可点开每个中间节点） | edge_registry.from_metric → map_path（升一等后）→ to_ticker | 中间节点点开 = 它代表什么 |
| 每跳机制 | edge_registry.mechanism / 中间节点含义 | 因果翻译 |
| 跳数 | edge_registry.hops | |
| 领先期（P&L 何时显现） | edge_registry.lead_measured · metric_registry.lead_time_est | lead：早不早 |
| 确定性 T1/T2/T3 + 方法 | edge_registry.cert_tier / cert_method | lead：能回测 / 只给方向 |
| 方向 × 权重 | v_edge_calc.tradable_calc / warning_calc / dominant | lead：= d_factor 因子算出的边宽 |
| 可测量检查点 | 该路径关键指标的 next_release / calendar | lead：下一个确认/证伪点 |
| 2×2 定位 | 领先期 × 证据级 → act/watch/priced/ignore（算出） | lead：直接指导动作 |
| 边类型 E1–E6 | edge_registry.edge_type | |

### 9.3 节点档案（选中一个 entity / metric）

| 分区 | 字段 | 来源列 |
|---|---|---|
| 头 | 名称 · 层 L1–L6 · 维 D1–D7 · 成熟度 · **在册权重 或 潜在标的+证据级** · 中国侧独家标 | entity_master · metric_registry · fct_position · v_ticker_weight |
| **入边（什么在推动它）** | 打到它的路径：各源 / 方向 / 权重 / lead / tier | edge_registry WHERE to = 本节点 + v_edge_calc |
| **出信号（它发出什么、传给谁）** | 它最近的事件/读数 + 从它出发的边 | fct（本节点实体的记录）+ edge_registry WHERE from 属本节点 |
| 传导（过境） | 经过它的路径 | map_path 含本节点 |
| 当前读数（extra-value） | 最新方向 · regime（信念/观察/泡沫预警）· falsifier · 下一个数据点 | v_metric_latest · key_fact.status_line/falsifier · calendar |
| salience | 当前被多少活跃事件照亮 | v_node_salience |
| 本体读数（commodity） | 营收 / PE / 一致预期等 | 折叠，默认不显 |

### 9.4 抬头框架：领先期 × 证据级（开枪 vs 瞄准）

面板顶部常驻一个 2×2，把当前视图里的路径按 领先期 × 证据级 分格：硬+长 = 现在动；软+长 = 观察名单；硬+短 = 大概率已 priced；软+短 = 忽略。这是给 PM 的"抬头就看"。

---

## 十 一天出版详细计划（~8–10 工时；只做 NBIS 主链）

### Phase 1 · 数据（migration，~2.5h）
- `0020_nbis_chain_firstclass`：NBIS 主链 map_path 文本 → 一等中间节点（约 15 个：全球 AI 集群在建强度 / neocloud 扩张环境 / lab 算力采购力 / 推理需求 / GPU 供给成本 / 数据中心用电审批 等），带 含义 / 所属维 / 来源；`edge_registry` 拆成 源→中间→中间→落点 的多跳可遍历边（保留原 edge_id 作聚合）。
- 同脚本：`to_ticker` sink 放开到可指仓外 entity / regime；落点加 sink_type（持仓 / 潜在标的 / regime / 层）。
- `d_factor` 9 改一并落（决策层记 D 复核 + 更新 metric_factor + 重算边宽）。
- 假设 C22（潜在标的证据阈值 T2/P2，🟠）。
- 验收：`migrate.py && checks.py` ERROR 0；重放对账一致。

### Phase 2 · 视图 + 导出（~1.5h）
- `v_node_salience`（节点亮度 = 打到它的活跃事件路径聚合权重 × 时效）；`v_graph_nodes` / `v_graph_edges`（Cytoscape 用的图 JSON：节点带层/维/salience/sink_type，边带 tier/方向/tradable/warning/hops/lead）；三张卡各一个取数视图。
- `build_graph.py`：库 → graph.json（内嵌进 HTML）。
- 验收：JSON 节点/边数对得上；NBIS 主链能从任一源遍历到落点。

### Phase 3 · 面板（Cytoscape.js，~4h）
- 主视图 = 传播图（力导向 / 分层布局；节点大小=salience，边宽=权重，边色=方向，线型=tier；中国侧独家高亮）。
- 右侧三卡（信号 / 路径 / 节点档案，按选中对象切换，字段照 §九）。
- 顶部 2×2 抬头框架；日历降为副筛选（"最近活跃事件源"入口）；潜在标的区一小块。
- 折叠层放 commodity 本体读数。

### Phase 4 · 校验 + 出版（~1h）
- checks ERROR 0；手机宽度、深浅色、无横向滚动、控制台无报错。
- 出版：重构本地 `16-*.html` + 发一个 claude.ai 可分享 Artifact。
- 协作日志记 E##；spec 状态转 done。

### 落在后面迭代（不进本轮）
- 其余非 NBIS 边的中间节点升一等；潜在标的接决策层新判断类型 d_target_watch；salience 阈值校准。

---

## 十一 KPI 落点（sink）呈现设计（竞品调研 → 定稿）

**背景**：sink 不止 ticker，可以是**可观测 KPI**（解决"数据墙缓解"这类过闸却无票可打的信号）。竞品调研(YipitData/M Science/Daloopa/Visible Alpha/TickerTrends/AlphaSense)结论:TickerTrends 的 KPI 落点最全、Daloopa 的 provenance 最硬、Visible Alpha 有共识离散度,**但没有一家把 KPI 当因果链终点呈现**——那是我们的差异化。详见 `COMPETITIVE-INSPIRATION.md`。

### 11.1 两类 sink,同一张卡
- **票-KPI**：如 NBIS 云收入(有票 + 可 nowcast)。
- **纯 KPI**：如"有效 token 供给 / 数据受限程度"(无票,但可观测,r500 数据墙的落点)。
区别只在"票"那一栏有无;其余字段相同。

### 11.2 KPI-sink 卡字段(借鉴 → 映射我们已有字段)

| 呈现元素 | 借自 | 我们用什么落 |
|---|---|---|
| 一行:Actual / 预期基准 / Prior / **Δ vs 共识** | TickerTrends + 现日历三值 | 日历 Actual/Forecast/Prior 已有;**Δ 提为一等列** |
| **修正 sparkline + hover PIT 历史** | TickerTrends | supersede-不删 + change_log **本身就是修正史** → 画 sparkline |
| **MOE(回测历史误差)/ Confidence 两列分开** | TickerTrends | MOE = cert_tier T1 可回测实测误差;Confidence = 当前证据 P 级 |
| **逐格 provenance 到一手** | Daloopa | provenance P1–P5 + snapshot + anchor + source_url(已达标) |
| 共识**离散 / outlier** | Visible Alpha | 预期基准从单点扩成分布(后续) |
| **← 传播来路(差异化,别人没有)** | 我们独有 | 该 KPI 是哪条 AI 发展经因果链推到的终点(路径卡) |

卡样式:
```
KPI:<名> [层·维] · 可nowcast档 T1/T2/T3   [票:XXX 或 纯KPI]
 Actual … 预期基准 … Prior …  Δ vs 共识 …  证据 P? · MOE ±?%
 修正 ▁▂▃▅(hover:更新n次/初值/最新)   nowcast 前置读数:<领先读数>(领先~N周)
 ← 传播来路:[AI事件] → <机制…> → 本KPI          ← 竞品没有的一行
 源:<一手>(P?)[原文锚点]
```

### 11.3 与影响力闸新框架的耦合(框架已换)
影响力闸弃用 doc29 原 5 条清单,**换成第一性重构**(D 2026-09-20 定):
> **影响力 = 会发生吗(likelihood:被采用 × 落地路径 × 证伪闸可验证性) × 动多大(magnitude,经四渠道之一:需求 / 成本 / 供给瓶颈 / 竞争替代) × 动哪个可观测 KPI**
- 原 doc29 5 条的问题:不互斥(⑤瓶颈层与①需求②成本重叠)、不完备(漏"竞争替代"渠道,而 doc25 E4 竞对边需要它)。
- **magnitude 的终点 = 某可观测 KPI;该 KPI 的可 nowcast 档 = cert_tier**(T1 可 nowcast / T2 可对账 / T3 只方向)。TickerTrends 的 MOE(历史误差)/Confidence(当前信心)两列,正好是 tier 客观化的呈现模板。

### 11.4 待做(接队列)
1. 影响力闸 20 条按新框架(likelihood × 渠道 × KPI)重判(替换 0021 的旧框架起草)。
2. **可 nowcast KPI 清单**:逐个 KPI 定 T1/T2/T3(判据:有无前置地面读数能预判)——先照持仓侧现有指标列一版给 D 核。
3. 面板把 KPI-sink 卡画出来(§11.2),含纯 KPI sink。
