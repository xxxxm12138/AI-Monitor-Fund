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

**这不是一个普通的“AI 新闻爬虫”，而是一张从基金持仓票向上游反推、每条边过验证、每个数可溯源、每个判断有主的因果图 (Intelligence Graph)。**

[阅读指南](#-面试官阅读指南) • [核心差异](#1-为什么要做这套系统-why) • [系统架构](#3-三层架构落地-what) • [实战案例](#4-实战案例-nbis-的交叉证伪) • [5分钟复现](#5-快速启动与复现-quick-start)

</div>

---

## 📌 面试官阅读指南

为了展示完整的思维逻辑和工程落地能力，本仓库包含了从破题、推翻重来到最终收敛的全过程。建议您按以下**黄金路径**阅读：

1. **[本页 (README.md)](#)**：总览全貌。涵盖为何做、怎么做、落地的三层架构，并提供到底层代码的直达跳链。
2. **[docs/22-解题思路与分工.md](docs/22-解题思路与分工.md)**：按真实的思考顺序，还原十个核心环节的“决策过程”与“人机分工”。
3. **深入验证 (按需深挖)**：
   - 🔍 **数据源在哪？** → [docs/21-数据来源说明](docs/21-数据来源与处理方法说明.md)
   - 🤔 **每个分叉怎么取舍的？** → [docs/23-取舍明细](docs/23-解题思路.md)
   - 📊 **最后给 PM 看什么？** → [日历式看板 Demo](assets/16-AI发展监测日历.html)
   - 💻 **底层 DuckDB 怎么跑？** → [pipeline/README.md](pipeline/README.md)

> ⚠️ **避坑提示**：`docs/13`、`docs/process/` 以及 `research/` 目录下的文件均为早期探索和过程废稿，请勿从这些文件开始阅读。

---

## 1. 为什么要做这套系统？ (Why)

在 Anatole 深度自下而上、高集中的对冲基金语境里，一套泛泛的 AI 资讯聚合毫无意义。投研是典型的 **Decision-native (决策原生)** 负载，我们要的是能服务于最终交易决策的“因果链”。

| 传统 AI 追踪体系 | 本项目：Intelligence Graph |
| :--- | :--- |
| ❌ **大海捞针**：抓取全网 AI 新闻，信息过载且难以量化影响。 | 🎯 **需求侧锚定 (Demand-anchored)**：以 13F 真实重仓（NBIS/RBRK）为锚点，逆向反推需要观测的 AI 发展节点。 |
| ❌ **拿华尔街的二手料**：看同样的财报和研报，毫无信息差。 | 🚀 **中国地面数据 Nowcast**：利用中国光模块排产/海关出口等地面数据的“时间差”，前瞻预测美股 KPI。 |
| ❌ **黑盒判断**：系统直接给出一个“利好/利空”的结论。 | 🔍 **高度可解释与可溯源**：每一条传导路径均可追溯至原文快照，每个先验系数均登记在“假设台账”。 |

---

## 2. 系统怎么转起来的？ (How)

借鉴一级市场“VC 投资看数据”的方法论，我们将庞杂的 AI 发展抽象为严谨的**实体建模（点与边）**，并用高级理论范式将其自动化。

### 🧩 实体建模：点与边

<div align="center">
<img src="assets/readme/bowtie.svg" alt="供需对接:AI 供给 D1–D7 → 六类边 → 持仓 ticker" width="100%">
</div>

- **点（指标 Node）**：定义了需要追踪什么。供给侧划分为 **7 个维度** (D1算力 - D7政策)。指标库（[`metric_registry` ↗](pipeline/SCHEMA.md#tbl-metric_registry)）只存定义，真实数据分发至 **4 类事实表**（[`fct_quant` 量价 ↗](pipeline/SCHEMA.md#tbl-fct_quant)、事件、观点、前沿）。
- **边（映射 Edge）**：定义了“AI 的风如何吹到票”。总结为 6 类传导机制（[`edge_registry` ↗](pipeline/SCHEMA.md#tbl-edge_registry)），每条边必须通过 **T1(可回测) / T2(结构对账) / T3(定性方向)** 三层验证，并附带计算权重。

<details>
<summary><b>💡 展开看：Intelligence Graph (JEV) 范式如何精炼这些点和边？</b></summary>
<br/>

<div align="center">
<img src="assets/readme/paradigm.svg" alt="计算范式" width="90%">
</div>

为了不让系统变成“堆砌新闻的工具”，我们引入了 Intelligence Graph 计算范式，拆解为四个可迭代算子：
1. **REPRESENT (压缩表征)**：把混乱的新闻压成带标签的、Point-in-time 的标准化事实。
2. **PROPOSE (生成候选空间)**：顺着“边”扇出，枚举出该事件可能打到哪些持仓票的所有路径。
3. **PREDICT (指标预判)**：利用提前收集的“领先期”，预判未来财报的动向。
4. **SELECT (剪枝选择)**：通过“证伪”与“影响力”两道闸门打分，过滤掉无效噪音，形成最终决策输入。
</details>

---

## 3. 三层架构落地 (What)

为了满足以上范式，整个工程在底层落地为三层严谨的架构：

### 🛠️ 第一层：源数据与处理层 (Data Pipeline)
- **绝对真实，绝无示例**：318 条记录、177 个来源，全部遵循 **P1(一手) - P5(设计值)** 五级溯源（[`source_master` ↗](pipeline/SCHEMA.md#tbl-source_master)），彻底隔离市场 Rumor。
- **频率不靠拍脑袋**：更新频率严格遵循公式：`信源天然节奏 × 服务决策时刻 × 边领先期`。
- **稳健的入库工具链**：采集 → 抽取 → `core.py` 路由 → `checks.py` 业务校验 → `migrate.py` 事务性入库，确保**0 漏、0 错**。

### 🧠 第二层：判断与治理层 (Governance)

<div align="center">
<img src="assets/readme/calibration-loop.svg" alt="校准复盘双控制器闭环" width="80%">
</div>

这是体现基金投研“克制与严谨”的核心层：
- **【亮点】假设台账 (Assumptions Ledger)**：打分权重、领先天数等一切带有主观预判的参数，全被剥离进 [`assumption` 表 ↗](pipeline/SCHEMA.md#tbl-assumption)。**未经验证的假设亮 🟠 闸，只用于排序，坚决不用于仓位 Sizing**。
- **人机协同分工 (ABCD 矩阵)**：
  - **D (人定)**：方向与底线原则由我制定。
  - **C (人定义，AI执行)**：规则引擎与清洗脚本。
  - **B (AI 初稿，人必复核)**：因子打分、方向初判，交由 AI 起草，未经人确认则标为 draft。
  - **A (AI 独立，人抽检)**：底层数据的爬取与路由。
- **接入 Langfuse Trace**：将 LLM 承担的非结构化抽取任务上卷到 Langfuse 进行打分与 Trace 回溯，让 AI 变成可管理的打工人。

### 📊 第三层：结果与面板层 (Presentation)
摒弃了让数据岗和 PM 混用同一个看 Schema 的后台，将出口定制为**日历式看板**和**影响卡 (Impact Card)**：
- **只回答 PM 的四个拷问**：*这是什么？ → 影响书里哪只票？ → 逻辑多确定？ → 下一步盯什么？*
- **👉 [点击体验看板 Demo](assets/16-AI发展监测日历.html)**

---

## 4. 实战案例：NBIS 的交叉证伪

我们以占据仓位 51% 的 **NBIS** 为例，看看系统是如何在真实场景中运作的：

<div align="center">
<img src="assets/readme/nbis.svg" alt="NBIS 供需对账" width="85%">
<br/><br/>
<img src="assets/readme/evidence-structure.svg" alt="证据结构图:稳健性 = 最小割" width="60%">
</div>

1. **供给猛建 ↔ 需求对账**：通过底层数据追踪上游（如光模块排产暴增、前沿 Lab $2B 级别融资），沿着“边”传导预测 NBIS 的需求激增。
2. **直击管理层水分 (Falsification)**：系统通过对比“供给端在建多少”与“需求端融资是否转冷”，一旦出现背离，触发 `PROPOSE` 预警，有效防范 FF 式的虚假指引。
3. **战绩回填**：预测“光模块↑ → NBIS↑”，提前约 90 天捕获 NBIS Q2 营收激增的预期差。

---

## 5. 快速启动与复现 (Quick Start)

我们以 **DuckDB** 为真值源，全套业务逻辑可在一分钟内从零推演复现。

```bash
# 1. 安装依赖
pip install duckdb

# 2. 进入核心工程目录
cd pipeline

# 3. 从底层 CSV 引导建库（冻结数据基线）
python3 init_db.py --force

# 4. 事务性重放所有改库历史（体验字段级追踪与 change_log 沉淀）
python3 migrate.py

# 5. 跑所有业务一致性校验（验证 0 漏 0 错的工程纪律）
python3 checks.py
```

### 🔭 诚实披露：不足与下一步
这套系统已跑完 **Phase 1** (广度骨架 + 深度样板)。当前诚实披露以下待办：
- **回测深度不够**：目前收集的数据大多是点状快照，尚不足以支撑 T1 级别的严谨量化回测。
- **判断层自动化未完全贯通**：部分因子、方向状态目前仍处于 B 级（AI 初稿，待人复核），后续需接入完善的自动化调度队列。
