# JEV 读后 · 从监测体系到 Intelligence Graph —— 为什么这套 schema 是在为后来的基建做设计

**日期** 2026-09-20 ｜ **性质** 设计立场文（B 初稿 · 待 D 复核）｜ **上游** `pipeline/JEV`（文章原文）· doc 21 / 25 / 29 / 30 · `13-思路总梳理.md`

---

## 〇 一句话

JEV 火的不是那个模型，是它暴露的前提：**能用 Generation 表达的智能，不一定应该用 Generation 计算**。投研恰好是最典型的 decision-native（而非 generation-native）工作负载——我们这套体系的最终形态不是"一个会写研报的 AI"，而是一张 **Intelligence Graph**：把混乱世界压成可比较的表征（REPRESENT），提出候选解释（PROPOSE），在指标空间做预测（PREDICT），高频地剪枝与选择（SELECT），并让每一次判断都留下可校准的痕迹，最终塑造整条 表征→预测→剪枝→选择 链路的权重。现有 schema 的每一层都已经站在这四个算子的位置上；本文说清楚差的三块增量，以及为什么今天的每一行数据同时是明天专用模型的 I/O 契约和训练集。

---

## 一 JEV 真正说了什么（压缩到五点）

1. **Universal Interface ≠ Universal Computation**。Token 是统一接口，但分类、路由、验证、评分这类"有限候选、typed 输出"的判断，没必要走自回归生成的计算路径。计算图（serial depth / 并行度 / 成本）才是本质，不是输出格式。
2. **四个算子**：REPRESENT（把世界压成可计算 state）· PROPOSE（扩张候选空间）· PREDICT（预判"这样做会怎样"）· SELECT（把空间压回来）。智能是这四者的 expand–prune 循环，不是一次 Generation。
3. **开枪低频、瞄准高频**。一年真正下注个位数次，中间是几万次"这件事值不值得再多看一眼"。真正消费 intelligence 的是高频的筛选、路由、注意力分配——这才是系统经济学的大头。
4. **校准（RLCD）是自动化分流的前提**。模型说 90% 把握时真的对 90%，才能建立"高置信自动执行 / 中置信升级复核 / 低置信转人工"的 cascade。类型正确 ≠ 判断正确；未校准的置信度不能用于决策。
5. **SELECT 被优化后，瓶颈移到 REPRESENT**。把混乱世界压成稳定 deterministic state、把无限空间压成 high-recall 候选集，是下一段成本所在。评价一个 AI 系统的问题会从"你底层用哪个模型"变成"你完成一次任务的 Intelligence Graph 长什么样"。

## 二 投研本来就是这个形状

投研的最终产出不是文本，是**一连串决策节点组成的推理链条**：这篇 arXiv 值不值得看作者 → 这个 repo 是玩具还是创业意图 → 这条融资新闻是信号还是噪音 → 这个矛盾该追问 founder 还是降优先级 → 这条边该升 tier 还是挂账 → 这个背离是泡沫预警还是口径问题。每个节点：输入 state 很复杂（多源证据、可信度、口径是否可比），输出却是有限候选上的一个选择加一个置信度。

这正是 Jev 定义的 "unstructured state in, typed probabilistic decisions out"。所以结论不是"我们要用 Jev"，而是：**基金的投资体系应该按这个计算范式来设计**——重决策、压缩、预测、剪枝，生成只在图的边缘出现（写简报、向人解释、提出新解释候选）。计算的执行者今天是人和通用 LLM，明天可以是 for-representation / for-prediction / for-selection 的专用小模型；只要 schema 提前把每个决策点的 I/O 定成 typed 的，换执行者不换结构。

## 三 对照：四个算子在现有 schema 里已经各就各位

| 算子 | 文章里的含义 | 本体系的现有落点 | 说明 |
|---|---|---|---|
| **REPRESENT** | 把混乱世界压成稳定、可比较、point-in-time 的内部 state | `stg_observation` → 四类 fct 表；通用元数据层（knowledge_time / P1–P5 / anchor / snapshot_id / owner）；两轴实体表；`source_master` | 文章说 REPRESENT 会成为下一个瓶颈、没有标准化组件——我们的回答就是 schema 纪律本身：一行一个事实、缺元数据不进资产库、原文快照留档。**这层做得越 deterministic，上面的判断就越便宜** |
| **PROPOSE** | 扩张候选空间：新解释、新机制、新候选从哪来 | `edge_registry` 六类边 E1–E6（本体/供应链/下游需求/竞对/主题/资金人才）；前沿雷达（topic-driven，不挂票）；假设台账新假设入册 | 六类边就是"AI 发展如何打到票"的**第一版候选解释词表**。之前按供应链、竞对去分析，本质是在一个人工枚举的 PROPOSE 空间里工作——这个空间本身应该可扩张、可校准（见 §四.3） |
| **PREDICT** | 预判后果；在表征空间而非文本空间预测（JEPA 式） | `lead_time_est` / `expectation_base`（Forecast 列）/ 日历排期的未来行 / warning = τ·l·e | 看板的 Actual vs Forecast 就是预测循环的用户界面：预测发生在指标空间（下期 ARR、下次发布、领先期），不是让模型写一段"我认为会涨" |
| **SELECT** | 有限候选上的高频判断：路由、分级、验证、排序 | 接入路由（四类 fct 分发）· `observation_direction`（方向三值）· 两道闸（证伪 source_stance/verifiability → 影响力 industry_impact）· 三态对账（同向/平/背离）· tradable/warning 排序 · weight 归一 · fill_status 优先级 | **全是 Jev-shaped 工作负载**：候选空间提前定义（词表就在 CHECK 约束里）、typed 输出、高频发生。这是体系里数量最大的一类计算 |

还有一张表已经是 cascade 本身：**A/B/C/D 分工表就是 routing policy**。"离干净结构化数据越近越靠 A；越需判真伪、越接近下注越靠 B/C/D"——这句话就是文章说的 cascade（确定性代码 → 便宜专用判断 → 小生成模型 → frontier reasoning → human）的人力版。未来的演进不是重写这张表，而是**让 A/B/C/D 的边界随校准数据移动**：某类判断上模型校准误差足够低，它就从 B 档下移到 A 档，人只保留升级路径上的裁量。

## 四 差的三块增量（这就是"为基建做设计"的具体含义）

### 1. 决策点一等公民化：R、E 之外的第三张登记表 `decision_registry`

现在指标有真源 R、边有真源 E，但**判断只有结果没有登记**——五张治理表存了判断的输出，没有一张表回答"这个体系里有哪几类重复发生的判断、每类的输入是什么、候选是什么、现在由谁执行"。加一张：

| 列 | 含义 | 例（方向判断） |
|---|---|---|
| `decision_id` | 判断类型主键 | `d_direction` |
| `state_schema` | 输入 state 由哪些列/视图构成 | `fct_*.value, prior, metric_registry.direction_rule` |
| `candidates` | 候选词表（CHECK 约束级别的枚举） | `{bullish, bearish, neutral, unclear}` |
| `owner_tier` | 当前执行档位 A/B/C/D | B |
| `freq_est` | 发生频率量级 | 每条观测一次 |
| `escalation` | 升级规则（什么置信度以下升级给谁） | conf < .7 → D |
| `calib_status` | human → shadow → assisted → auto（状态机，见 §四.2） | human |

现有的路由、方向、两道闸、三态、tier 提议、fill 优先级……每个都是它的一行。**这张表的每一行，就是未来一个专用小模型的岗位描述**：state_schema 是输入契约，candidates 是输出契约，escalation 是部署策略。schema 先把 I/O 钉死，执行者（人 / 通用 LLM / 专用模型 / 规则代码）成为可替换件——这正是"模型可能重新统一，计算不会"在工程上的对应物。

### 2. 每次判断落成六元组，判断表同时是校准集

判断表的行补齐到 **(state_anchor, candidates, choice, confidence, basis, outcome)**：
- `state_anchor`：判断时刻输入 state 的引用（record_id 集合 + as-of 时间），保证判断可复现——这是 point-in-time 纪律从数据层平移到判断层；
- `confidence`：判断者（人或模型）的置信度，敢写才能被校准；
- `outcome`：事后可知的对错（背离最终是不是泡沫、升 tier 的边有没有兑现、降优先级的项目有没有错杀）——由复验节奏顺带回填。

有了这三列，**今天人做判断顺手留下的每一行，就是明天 decision model 的训练与校准数据**。`change_log` + `supersede` 已经在记 trajectory；假设台账的状态机（assumption → calibrating → validated → retired）原样平移到决策类型上：

> **human**（人做，模型不在场）→ **shadow**（模型旁跑，只记不采用，攒校准曲线）→ **assisted**（模型先答，置信度分流：高自动、中复核、低转人）→ **auto**（仅审计抽查）。

🟠闸的纪律原样适用：**校准未 validated 的决策类型，其输出禁用于 sizing 与告警阈值**——这是 RLCD 那一节在本体系的直接翻译，也是我们已经写进 doc 30 的规矩，只是把适用对象从"系数"扩到"判断"。

### 3. 背离即 PROPOSE 触发器：把 Generation 压到图的边缘

三态对账里的"背离"现在只是预警标签。在 Intelligence Graph 里它是**候选空间扩张指令**：背离出现 → 先 PROPOSE（生成若干解释候选：founder 错 / 资料过时 / 口径不可比 / 定义不同 / 真泡沫）→ 再 SELECT（在候选上判断，选出最值得查证的）→ 查证结果回填 outcome。这是整个体系里**唯一真正需要开放式生成的位置**——reranker 排不出 retriever 没召回的文档，selector 也选不出没进候选空间的解释。同理，六类边 E1–E6 这个词表本身也该走这条路：雷达里过了两道闸的新机制，如果六类装不下，就是 PROPOSE 出了第七类边的时刻；哪类边历史上兑现率高，边类型先验也可校准。

## 五 计量与证伪

**计量**：文章第五条说 token 不是 intelligence 的天然单位。这套体系的健康度指标应从"填了多少行"逐步走向：`decisions/week`（判断吞吐）· `cost per decision`（分档位统计）· `escalation rate`（升级率，越低说明下层越可信）· `calibration error`（分决策类型）。`v_health` 的下一个版本按 decision_registry 出这四条。

**证伪标准**（照搬文章的纪律给自己）：如果两年后——判断仍然 100% 由人做、判断表没攒出任何一条校准曲线、A/B/C/D 边界从未因校准数据移动过——那 "Intelligence Graph" 就只是给现有监测树换了个新包装。反过来，只要有一类判断（哪怕只是接入路由）走完 human → shadow → assisted 的状态机，这个设计就兑现了。

## 六 为什么现在就要这样设计（而不是等基建成熟）

1. **不依赖 Jev 存活**。押注的是 Computation Specialization 不是 Model Specialization：四个算子可以是四个小模型，也可以是同一个 foundation model 的四条 inference path。schema 只声明 I/O 契约，不绑执行者。
2. **数据的复利从第一天开始**。六元组判断记录的成本 ≈ 0（人本来就在做判断，只是多写一个置信度），但它让每一天的人工判断都在为未来的自动化攒标注。等基建成熟再设计，前面所有判断都白做了。
3. **这就是 proprietary 的位置**。文章说真正专有的东西在从 prompt 向下移动：候选空间怎么构造、什么置信度自动执行、failure 怎么 recovery、trajectory 如何进入下一轮 learning。对基金而言：**R + E + decision_registry + 校准曲线，合起来就是这支基金的 intelligence architecture**——模型谁都租得到，这张图和它的权重租不到。

---

**与现有文档的关系**：不推翻任何已有设计；§四.1–.3 是 schema v2 之上的增量（一张登记表、判断表补三列、一条三态触发规则），届时以 migrations 形式落库。步骤 2 填数不受影响；本文进入交付物①时，作为"体系的长期形态"一节，回答"这套东西做完笔试之后还能长成什么"。
