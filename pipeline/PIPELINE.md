# PIPELINE · AI 发展监测体系完整运行机制（对齐稿）

**日期** 2026-09-20 ｜ **性质** 运行机制对齐（B 汇总既有文档 · 待 D 复核）｜ **目的** 把"输入一个新 AI 前沿事件 → 画出可能空间 → 最可能路径 → 导向哪个 ticker"这条链的每一环、每一环的数据在哪、谁做，全部梳理清楚，作为叠数据迭代的地基。

**上游文档**：doc16([3-AI侧1](../research/3-AI侧1)) · doc24/24v2/26/29([8-schema_AI](../research/8-schema_AI)) · doc25([9-映射](../research/9-映射)) · doc23([7-data_source](../research/7-data_source)) · JEV-intelligence-graph · PLAN-decision-layer

---

## 〇 一条主链（四算子 = 一条 pipeline）

```
新 AI 前沿内容
  │
  ▼  ① REPRESENT ── 把混乱内容压成图上的一个带标签入口
  │     源分级(T_a/b/c×立场) → 证伪闸 → 影响力闸 → 分【维 D1–D7 / 子节点机制 / data_class】
  │     ↑ 过不了两道闸 = 留在雷达/watchlist，不外溢到票（doc29 护栏）
  ▼  ② PROPOSE ── 从入口沿六类边 E1–E6 扇出，枚举所有可达路径（= 可能空间）
  ▼  ③ PREDICT ── 每条路径的方向(↑↓→!) × 领先期 τ × 传导确定性
  ▼  ④ SELECT ── 路径打分(可交易 c·r·s·φ / 预警 τ·l·e) → 剪枝 → 排序 → 落到 ticker
  │
  ▼  导向哪个 ticker（+ 仓外命中且证据够硬 = 潜在标的）
```

四算子不是新发明，是把既有文档的三段（源 → 分类/闸 → 映射）接成一条可执行链。

---

## 一 REPRESENT：源 + 分类器（Block 1，doc16/24v2/29）

### 1.1 监测对象 = 七维 D1–D7（四族），每维一条"拆解主轴"保证查全（doc24v2 §〇.5）

| 族 | 维 | 拆解主轴 | 基金视角重要性 |
|---|---|---|---|
| 投入 | D1 算力供给 | 硅→封装→互连→整机→数据中心→分发 | **高**（书直接沾）|
| 投入 | D2 数据供给 | 来源→加工→权属→稀缺 | 中 |
| 投入 | D3 资本 | 早→晚→战略→退出→异常(循环融资) | **高**（需求真伪）|
| 投入 | D4 人才 | 进→出→重组 | 低（合规受限）|
| 能力 | D5 算法与能力前沿 | 方法→能力→效率 | 中 |
| 变现 | D6 商用落地/token 经济 | 用量→单位经济→采用→留存 | 中 |
| regime | D7 政策·能源·安全 | 地缘→产业→能源→监管→安全 | **高**（regime 砸全链）|

映射优先级用**基金视角**：D1 > D7 > D3 > D5 > D6 > D2 > D4（doc25 §三 / doc26 §2.4）。

### 1.2 从哪些源收集（每维一套，doc24v2 §一 / doc29 §三）

- **三层信息源漏斗**（doc16 §五）：科研源(给**方向**) → 商业源(给**量级**) → 终端源(给**验证**)；三层打架本身是信号。
- **每维的源 × 获取方式 × 落表 × 频率**：doc24v2 §一逐节点表（如 D1 光互连=中际旭创/新易盛/海关/SemiAnalysis→fct_quant→季/月；D5 benchmark=LMArena/SWE-bench/ARC→fct_frontier→事件；D3 lab 融资=Crunchbase/Form D→fct_event→事件）。
- **前沿雷达源分级**（doc29 §三.5，= 分类器地基）：质量 T_a 一手权威(顶会/官方 report/第三方实测 Epoch·AA) > T_b 半权威(arXiv 预印/大厂博客含 PR) > T_c 社媒；× 频率 × 立场(中立 vs 有立场)。规则：T_a×中立→可入定量；T_b/有立场→先证伪+降权入 watchlist；T_c→只做线索。

### 1.3 分类器 = 两道闸 + 分维/机制（doc29 §四，这是 REPRESENT 的核心，最吃人判）

**新内容进图前必过两道闸**（顺序不可换）：
1. **证伪闸**：source_stance(neutral/vendor_pr/social) × verifiability(reproducible/third_party_verified/claimed_only/rumor)。判据：交叉源、可复现、第三方实测、详实度。
2. **影响力闸**：industry_impact(高/中/低) + rationale。判据：是否改变算力需求结构 / 是否降本 / 是否被产业采用 / 有无落地路径 / 是否触及瓶颈层。

**只有 高含金量 × 高产业影响 才外溢到票**；其余留雷达。分类器输出五元组：`{维 D?, 子节点/机制, data_class(1/2/3/4), 源分级, 两闸结论}`。

> **关键**：这两道闸就是我们决策层里已建的 `d_falsify_gate`(owner B) 和 `d_impact_gate`(owner D)。所以"自动分类"= LLM 抽取 + 分级 + 分维（A/B 可自动）**＋ 两道闸人复核（D）**——不是全自动，是 assisted。这与 JEV / 决策层完全一致。

---

## 二 PROPOSE + PREDICT + SELECT：映射（Block 2，doc25）

### 2.1 六类边 = 传导机制（doc25 §1.1）
E1 本体 · E2 供应链上游 · E3 下游客户需求 · E4 竞对替代 · E5 主题轮动 · E6 资金人才流。

### 2.2 逐票链式图 = 权威接线（doc25 §1.2，我的 graph_data.py 应据此校准）
每票从"收入/利润因子"沿边反推到 AI 节点，数跳。**NBIS 有 7 条链**（光互连→在建强度→neocloud→NBIS 3跳 · backlog 0跳 · 电力上电 1跳★ · lab融资→采购→NBIS 2跳 · 能力→推理→采购→NBIS 3跳 · 电力政策→审批→上电 2跳 · 出口管制→GPU→NBIS 2跳）；RBRK 4 条、FCEL 2 条、尾仓各 1 跳。

### 2.3 打分 = 传导 × 节点质量（doc25 §1.3，权重来源）
- 传导 T：领先期 τ（跳多/靠早期边→领先久）× 传导确定性 c（跳少/结构边→确定）。c 由三层验证 T1/T2/T3 定。
- 节点质量 Q：r 可靠 · e 独家 · l 固有领先 · s 可观测/信噪 · φ 频率。
- **两产出**：可交易度 = c·r·s·φ（进 nowcast/定仓位）；预警度 = τ·l·e（上 watchlist/给方向）。
- **这些权重已在库里**：edge_registry(六类边/跳数/tier) + metric_factor(r/e/l/s/φ) → v_edge_calc 算出 tradable/warning。**graph_data.py 的 w 应直接取这里，不手填。**

---

## 三 数据落点（每一环的数据在哪）

| pipeline 环 | 数据 / 表 | owner |
|---|---|---|
| 源登记 | source_master(P1–P5, kind, tier) · doc23 | B/C |
| 事件/前沿记录 | fct_event · fct_frontier(+source_stance/verifiability/industry_impact) | A/B |
| 分维/机制 | metric_registry(dim/data_class/signal_role) | C |
| 两道闸 | decision_registry: d_falsify_gate / d_impact_gate + decision_log | B/D |
| 六类边/跳数/tier | edge_registry | D 定 gold |
| 节点质量因子 | metric_factor(r/e/l/s/φ) → d_factor 判断 | B/D |
| 打分/两产出 | v_edge_calc(tradable/warning) · v_ticker_weight | 视图 |
| 传播/扇出 | **待建**：node→node 分叉图（graph_data.py 校准到 doc25 后固化） | B/D |
| 潜在标的 | entity_master(in_book=FALSE) + candidate_pool | D |

---

## 四 现状 vs 目标（差什么）

| 环 | 现状 | 差 |
|---|---|---|
| 源 + 七维 + 源分级 | 文档齐全(doc16/24v2/29)，fct 有真数 | 前沿雷达实跑样本少(doc29 §九 缺口) |
| 两道闸 | 决策层已建 d_falsify/d_impact | 分类器把新内容自动跑这两闸的接口未建 |
| 六类边 + 权重 | edge_registry 35 边 + 因子已算 | 因子对账 7 条待 D 复核(d_factor) |
| 传播扇出图 | graph_data.py 初稿(B 手填) | **需据 doc25 §1.2 链式图 + §二因子表校准；权重取 v_edge_calc** |
| 分类器(REPRESENT) | 手动 --dim/--at | 自动分维/机制 + 两道闸接口未建 |

---

## 五 待 D 确认（对齐点）

1. **主链（第〇节）对不对**——四算子 = 源→分类/两闸→映射→票，这条 pipeline 是不是完整运行机制。
2. **分类器 = 两道闸 + 分维**，且两道闸复用决策层 d_falsify_gate/d_impact_gate（assisted，非全自动，D 判闸）——认不认可这个定位。
3. **graph_data.py 校准到 doc25**：接线以 doc25 §1.2 七条 NBIS 链（+RBRK/FCEL/尾仓）为准，权重取 edge_registry/v_edge_calc 已算的 tradable/warning，不手填——确认后我重写 graph_data.py。
4. 顺序：先校准接线(2.2/2.3) → 再建自动分类器(1.3) → 再接传播引擎/图。这个顺序对不对。
