# TODO · 按优先级(2026-09-20)

标注:**B**=我可建 · **D**=需你拍板/判断 · 依赖=前置项 · 工时粗估。当前瓶颈见 ★。

---

## P0 · 解锁正确性(便宜、挡着下游、多为 D 判)

| # | 待办 | 谁 | 依赖 | 工时 |
|---|---|---|---|---|
| P0-1 ★ | **跑影响力闸**:23 条前沿记录逐条按五判据起草 industry_impact 高/中/低 + rationale,落 `d_impact_gate` 给 D 复核。**当前外溢瓶颈**——不跑,刚采集的 D5/D2 前沿数据无法进传播(23/23 空) | B 起草 · D 判 | 0020 采集(已done) | 2h |
| P0-2 | **d_factor 9 因子改动落库**:上一轮评审的 9 处因子改(s 滥用 H 等),确认后落库,重算边宽 | D 确认 · B 落 | — | 1h |
| P0-3 | 决策层挂账清:registry 11 行 draft→reviewed;**r133 循环融资 + ticker:NBIS 背离解释选择**;F3.13/F2.15 思路层文字 | D | — | D 决定 |

## P1 · 映射差异化核心(我可建,最高价值)

| # | 待办 | 谁 | 依赖 | 工时 |
|---|---|---|---|---|
| P1-1 ★ | **边级预测校准**:decision_log 的 confidence→outcome→calibration 环扩到 edge_registry(State of AI 记分卡)——让映射图自我校准,**护城河机制,已有半地基** | B | 决策层(已done) | 3h |
| P1-2 | **分类器(REPRESENT)建**:甲案 Claude-as-classifier 走 B1 八步 taxonomy + 两闸接决策层,跑通 COLLECT→classify | B | B1 taxonomy(已done) | 2h |
| P1-3 | **新采集节点接线**:m_arxiv_topic_slope / m_rl_environments 等有数据无边 → 只给**过了两闸**的接进传播图 | B | P0-1 影响力闸 | 2h |
| P1-4 | **graph_data/propagate 固化进库**:mechanism_node + 分叉边做成 migration,脱离脚本 | B | doc25 接线(已done) | 2h |

## P2 · 呈现 / 交付(出版)

| # | 待办 | 谁 | 依赖 | 工时 |
|---|---|---|---|---|
| P2-1 | **面板重构**:Cytoscape 传播图主视图 + 三卡(信号/路径/节点档案)+ 2×2 抬头 + 潜在标的区(PLAN-graph-refactor Phase 3;MVP 已验证形态) | B | P1-3/P1-4 | 4h |
| P2-2 | **出版**:重构本地 `16-*.html` + 发 claude.ai 可分享 Artifact | B | P2-1 | 1h |

## P3 · 打磨 / 迭代(时间够再做)

| # | 待办 | 谁 | 工时 |
|---|---|---|---|
| P3-1 | claimed_only 补核:Kimi K3 / TEMPO / RLVR / 潜空间推理逐条 fetch 一手后决定入库 | B | 2h |
| P3-2 | cert_tier 客观化:用"终点是否可被另类数据 nowcast"定 T1/T2/T3(YipitData 启发) | B/D | 2h |
| P3-3 | dbt exposures:边 → 哪个 ticker 决策消费(edge → decision_registry 反查) | B | 1h |
| P3-4 | 其余非 NBIS 边的中间节点升一等(现只做了 NBIS 主链结构) | B | 3h |
| P3-5 | 潜在标的接决策层 d_target_watch(仓外命中且证据够硬 → 候选池) | B/D | 2h |
| P3-6 | 0015 编号撞车清理(需 init_db --force 重建共享库,择并行会话空窗) | B | 0.5h |

---

## 推荐执行顺序

**P0-1 影响力闸 → P1-1 边级校准 → P1-2 分类器 → P1-3 接线 → P2 面板/出版**。

理由:P0-1 是当前真瓶颈(采集到位了但闸没跑,前沿信号进不了传播);P1-1 是差异化护城河且已有半地基;两者做完,"输入前沿内容→过闸→可能空间→导向 ticker + 会校准"这条完整链就通了,再进 P2 出版。P0-2/P0-3 是你随时可拍的短决策,不挡 B 侧开工。
