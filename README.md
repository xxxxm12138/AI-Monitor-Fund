<div align="center">

<img src="assets/readme/hero.svg" alt="Anatole — AI 发展监测体系 · Intelligence Graph" width="100%">

<br/>

![paradigm](https://img.shields.io/badge/paradigm-Intelligence_Graph-8B5CF6?style=flat-square)
![workload](https://img.shields.io/badge/workload-decision--native-089981?style=flat-square)
![truth source](https://img.shields.io/badge/truth_source-DuckDB-2962FF?style=flat-square)
![Python](https://img.shields.io/badge/Python-3-2962FF?style=flat-square&logo=python&logoColor=white)
![as-of](https://img.shields.io/badge/as--of-2026--09-55617A?style=flat-square)
![status](https://img.shields.io/badge/interview-submission-1E2A44?style=flat-square)

</div>

> 面向成长股基金(港股 / 美股)的 **AI 发展监测体系**——把一条 AI 前沿动态沿**可回溯的因果链**导向持仓 ticker 与可观测 KPI。数据链 **可信 · 可溯 · 可纠 · 诚实标注**;差异化在**中国地面数据领先卖方**与**对管理层声明的证伪**。

> **一次真实命中(NBIS · 事后构造的校准点)**:光模块 ↑ → NBIS ↑ · lab 融资 → $1B 合同 · capex ↑ → NBIS,3 条方向预测按**真实公开兑现**核对全对(旭创 H1 +182% · NBIS Q2 +454%)。诚实边界:n=3、made 日期为回填、**非实时战绩**——是首批校准数据点(详见 [可靠性 + 差异化](#proof))。

## 目录

- [1 · Intelligence Graph 思路](#ig)
- [2 · 体系设计(形态 · 方法论 · harness · 工程优美性)](#system)
- [3 · 可靠性 + 差异化(给例子)](#proof)
- [4 · AI / human 分工](#roles)
- [5 · 附录(结构 · 运行 · 复现 · 数据模型)](#appendix)

---

<a id="ig"></a>

## 1 · Intelligence Graph 思路

<div align="center">
<img src="assets/readme/paradigm.svg" alt="计算范式:compress → propose → predict → prune → typed decision" width="100%">
</div>

> **借用声明**:本节的计算范式**启发自孟醒的文章《JEV 火了，但真正重要的不是 JEV》**;我在此之上的落地贡献是后文的 **schema / checks / 中国地面数据 / 证伪闸**,不是复述范式。

出发点是一个关于**计算范式**的判断:

> **能用 Generation 表达的智能,不一定应该用 Generation 计算。**

投研是最典型的 **decision-native**(而非 generation-native)工作负载:每个节点输入很复杂(多源证据、可信度、口径可比性),输出却是**有限候选上的一个选择 + 一个置信度**。所以不是"造一个会写研报的 AI",而是把体系设计成一条计算链——四个算子跑一个 expand–prune 循环(全篇只在这里讲一次):

| 算子 | 做什么 |
|---|---|
| **REPRESENT** 压缩表征 | 把混乱世界压成 point-in-time、可比较的 state |
| **PROPOSE** 生成候选空间 | 沿六类边枚举"AI 发展怎么打到票"的所有可达路径 |
| **PREDICT** 指标预判 | 在指标空间预判方向 / 量级 / 领先期 |
| **SELECT** 剪枝选择 | 有限候选上的高频判断:路由 / 分级 / 验证 / 排序 |
| **闭环** 自我校准 | confidence → outcome → 校准曲线,回灌上面每一步 |

三个设计立场:

- **候选空间是被设计出来的**:常规投研按供应链、竞对分析,本质就是在一个人工枚举的候选空间里工作;把它显式化成图,这个空间才能扩张、细化、校准。
- **执行者可替换**:每个决策点声明 typed I/O 契约,执行者(人 / 通用 LLM / 专用小模型 / 规则代码)是可换件——押注 **Computation Specialization,而非 Model Specialization**。
- **数据即复利**:今天每一行判断,同时是明天专用模型的 I/O 契约与训练集——这就是"为后来的 AI 基建做设计"。

<sub>范式全文与我的读后立场:[`pipeline/JEV-intelligence-graph.md`](pipeline/JEV-intelligence-graph.md);文章原文存档 [`pipeline/JEV`](pipeline/JEV)。</sub>

---

<a id="system"></a>

## 2 · 体系设计

> 下面每一层都可溯、可校验、诚实标注。先划覆盖范围,再讲怎么搭、落到哪张表、系统骨架。

### 2.0 覆盖范围 · 诚实划界

**主动划界比假装全覆盖更可靠**。本体系聚焦 **AI 基建价值链**(算力 / 资本 / 政策),因为可投资 KPI 与中国地面数据集中于此;不是全 AI 覆盖。

| AI 发展域 | 覆盖 | 真库落点 |
|---|---|---|
| D1 算力(芯片 / 光模块 / 电力 / 云) | 🟢 深 | 32 指标;光模块中国厂商月营收、海关、NBIS 真数 |
| D3 资本(前沿 lab 融资 / 循环融资) | 🟢 | Reflection / Cohere 融资事件 |
| D7 政策 · 能源(出口管制 / 电网) | 🟢 | BIS / IEA 一手 |
| D6 商用(adoption / ARR) | 🟡 中 | RBRK 等 |
| D5 能力前沿(模型 / 开源) | 🟡 | Epoch / Artificial Analysis;前沿雷达样本薄(fct_frontier 23) |
| D2 数据供给 | 🟡 | 少量 |
| D4 人才 | ⛔ | 合规受限,placeholder |

### 2.1 怎么长出来(构建过程 = 思维过程)

<div align="center">
<img src="assets/readme/bowtie.svg" alt="供需对接 bowtie:AI 供给 D1–D7 → 六类边 → 持仓 ticker" width="100%">
</div>

真实构建路径(每步一篇整理稿,末尾标"为什么 · 思路 · 目标";原始工作稿在 `research/`):

| 步 | 做了什么 | 整理稿 |
|---|---|---|
| ① 供给侧建模 | AI 发展拆成 D1–D7 七维节点,每维一条"拆解主轴"保证查全 | [供给侧全景](docs/process/01-供给侧建模.md) |
| ② 指标体系 | 数据类型四分类(量价 / 事件 / 观点 / 前沿)+ 通用元数据层 + 字段规范 | [指标体系](docs/process/02-指标体系.md) |
| ③ 供需对接 | AI 节点 × 持仓 ticker 连成有向图(上图 bowtie)+ 一条 thesis 两端对读 | [供需对接](docs/process/03-供需对接.md) |
| ④ schema 设计 | 节点 → 指标真源 R、边 → 边真源 E、观测 → 四类 `fct_*`、判断 → 决策层;原子事实 vs 可推导、判断与数据分表 | [schema 设计](docs/process/04-schema设计.md) · [`schema.sql`](pipeline/schema.sql) |
| ⑤ 点 · 边 · 权重 | 逐票向上游反推 · 六类边 E1–E6 · 跳数 · 映射价值 = 传导确定性 × 节点质量 · 三层验证 T1/T2/T3 | [映射范式](docs/process/05-映射范式-点边权重.md) |
| ⑥ 实例验证 | NBIS 七条链真数走一遍(见 [§3.3](#proof)) | [NBIS 实例](docs/process/06-NBIS实例.md) |

**更新频率 = 领先性的来源**(题目②"更新频率"落点):月频信源领先季频财报,不是巧合,是频率差。

| 信源(例) | 数据类 | 频率 | 领先(先验) | 采集 |
|---|---|---|---|---|
| 光模块中国厂商月营收(旭创 / 新易盛) | 量价 | 月 | ~18d | 交易所 / akshare |
| 海关 HS8517 光模块出口 | 量价 | 月 | ~20d | 海关月报 |
| NBIS 自有电力上电 | 事件 | 事件 | ~90d | 电话会 |
| 前沿 lab 融资 | 事件 | 事件 | 180–278d | 新闻 / Form D |
| hyperscaler capex | 观点+量价 | 季 | ~财报 −2–3w | 10-Q / 电话会 |
| benchmark / 训练算力(Epoch / AA) | 前沿 | 周 / 月 | 方向 | API |

<sub>领先天数多为**先验**(挂假设台账,未验证禁 sizing);其中 lab 融资 180d 已因 Reflection 实测 278d 进入 calibrating。</sub>

### 2.2 四算子 ↔ schema 落点

四算子不是概念,每步都落到真实表(带真实规模 · ↗ 跳字段结构 · 成熟度如实标):

| 算子 | 落点(真实规模) | 成熟度 |
|---|---|---|
| REPRESENT | [`stg_observation`↗](pipeline/SCHEMA.md#tbl-stg_observation) 317 条单口接入 → `route()` 确定性分五类 fct([`quant`↗](pipeline/SCHEMA.md#tbl-fct_quant) 179 / event 92 / frontier 23 / opinion 8 / position 15,零漏)· 元数据 100% 填 · provenance P1–P5(P1 259)· snapshot 223 → 101 真快照 · `superseded_by` 32 修订链 · [`source_master`↗](pipeline/SCHEMA.md#tbl-source_master) 176 | 🟢 运行 |
| PROPOSE | [`edge_registry`↗](pipeline/SCHEMA.md#tbl-edge_registry) 36 边(E1 2/E2 12/E3 14/E4 2/E5 5/E6 1;hops 0–3 带 `map_path`+`evidence_ids`)· [`candidate_pool`↗](pipeline/SCHEMA.md#tbl-candidate_pool) 10 · [假设台账↗](pipeline/SCHEMA.md#tbl-assumption) 42 | 🟢 运行(剪枝样本少) |
| PREDICT | [`metric_registry`↗](pipeline/SCHEMA.md#tbl-metric_registry)`.lead_time_est` · expectation_base 25 Forecast · [日历↗](pipeline/SCHEMA.md#tbl-calendar) 58 · `warning=τ·l·e` | 🟡 部分(量级待回测) |
| SELECT | `route()`(唯一 auto)· [`observation_direction`↗](pipeline/SCHEMA.md#tbl-observation_direction) 317 · 两道级联闸(证伪→影响力)· [`metric_factor`↗](pipeline/SCHEMA.md#tbl-metric_factor) 84 × r/e/l/s/φ → `tradable=c·r·s·φ`(未 validated 只排序禁 sizing) | 🟢 运行 |
| 闭环 | [`decision_log`↗](pipeline/SCHEMA.md#tbl-decision_log) 95 六元组 · [`decision_registry`↗](pipeline/SCHEMA.md#tbl-decision_registry) 12 类 I/O 契约 + `calib_status` 状态机 · `v_calibration` 首点 | ⚪ 骨架就绪 |

### 2.3 两条线 · 计算范式 ↔ 面板结构

计算范式(动态:信号怎么流)与面板的**交付三层**(静态:数据落在哪 · 给谁看)是同一系统的两个投影:

<div align="center">
<img src="assets/readme/two-axis.svg" alt="两轴桥接:四算子(动态) ↔ 交付三层(静态)" width="100%">
</div>

- **原数据层** ← REPRESENT:四类 fct + 元数据 + per-path 原料表(同质可扫描)。
- **判断层 · 引擎** ← PROPOSE + PREDICT + SELECT:边 / 两道闸 / 因子 / `decision_log`,把边聚合成对每只票的判断。
- **结果层** ← SELECT 产出:每票一张**证据结构卡**(结论 + 稳健性,见 §3.3);闭环把 outcome 回灌判断层。

### 2.4 agent trace & harness

体系即一套可复现的 harness(题目②"执行系统"):

| 环节 | 落点 |
|---|---|
| **input** 输入 | 信源采集 → `stg_observation`(317)· `source_master`(176:tier / kind / access) |
| **pipeline** 管线 | REPRESENT `route()` → PROPOSE 边 → PREDICT → SELECT → 闭环 |
| **rule** 规则 | `checks.py` 业务守闸 · `calc_rule` 公式 · `directions.py` / `factors.py` 规则初判 |
| **tool** 工具 | `migrate.py`(改库) · `core.py`(路由 / 归一) · `gen_*.py`(反生成文档 / 浏览器) |
| **output** 产出 | 视图(`v_edge_calc` / `v_metric_headline` / `v_calibration` …)· 面板 · `SCHEMA.md` |
| **context** 契约 | `schema_doc`(402 列字典)· `decision_registry`(每类判断的 state_schema / candidates I/O 契约) |
| **trace** 留痕 | `change_log` 3,559 字段级 · `decision_log` 95 六元组 · `migration_log` · (Langfuse trace 留位) |

### 2.5 工程优美性

- **改库走迁移**:每次一个编号脚本,`migration_log` 存 checksum,已应用不可改;`init_db.py --force + migrate.py` 从零重放。
- **活守闸**:`checks.py` 每次改库自动跑(路由完整性 / 字典完整性 / 快照存在 / 打分对账 / 校准闸),**ERROR 必须为 0**。
- **单一真源**:指标 R / 边 E / 判断 decision_registry 三张登记表分立,改指标只动 R。
- **原子事实 vs 视图**:可推导的一律作视图,杜绝脏写;`SCHEMA.md` 由库反生成,文档不漂。

---

<a id="proof"></a>

## 3 · 可靠性 + 差异化(给例子)

### 3.1 可靠性(JD 第一考核:数据链稳 / 准 / 可溯 / 诚实)

| 维度 | 证据(真库) |
|---|---|
| 稳(零漏) | 317 条接入 100% 确定性路由到四类 fct,`checks.py` 路由完整性守闸 = 0 漏 |
| 准(分级) | 每条带 provenance P1–P5 + source_tier + reliability_note;可只按 P1 定仓、隔离 rumor |
| 可溯 | 223 条 fct → snapshot_id → 101 个真快照文件,`checks.py` 逐条验文件存在;anchor 存原文短引 |
| 可纠 | `superseded_by` 32 条修订链旧值不删 + `change_log` 3,559 行字段级 + migration checksum 冻结 |
| 可复现 | `init_db --force + migrate` 从零重放,结果与增量一致(见 [§5 复现](#appendix)) |

**诚实成熟度标尺**(按体系自设证伪标准):

- 🟢 **已运行**:接入 / 路由 / 四类 fct · 逐事实 provenance + 修订谱系 · 六类边 + 闭式打分 · 判断六元组账 · 人力版 A/B/C/D 分工。
- 🟡 **骨架就绪、待数据兑现**:outcome 回填 3/95 · v_calibration 仅 1 桶 n=3 · 边 cert_tier 回测 1/36 · 模型执行者(llm/model)0 条、从未跨 human→shadow。
- ⛔ **按纪律暂关**:系数未 validated → 分数只排序、禁 sizing;realized P&L 需行情源,留位**不编价**。

### 3.2 差异化:中国地面数据 nowcast + 管理层证伪

- **中国地面数据 nowcast(STAAR 范式)**:美股 / 港股上市、真 KPI 由中国决定(手术量、分销库存、光模块出货),而覆盖该票的华尔街分析师拿不到中国地面数据。结构上因**频率差**领先卖方季报(见 [§2.1 频率表](#system))。*(领先为先验 / 目标,尚无卖方覆盖日期对照,不作已证声明。)*
- **对管理层声明的证伪**:用**供需两端对读**交叉验证同一 thesis——供给端(在建多少)⟷ 需求端(需求真不真)。背离即预警,直击"管理层 backlog / 指引真不真"。证伪闸区分 `source_stance`(vendor_pr vs neutral)× `verifiability`(claimed_only vs third_party)。

**对标竞品——差异化落在哪一格**:

| 你租得到 | 它给你 | 这里多给的一格 |
|---|---|---|
| TickerTrends / M Science | 逐 KPI Bogey / Consensus / Δ% / MOE | KPI 有了,但**无传导来路**——这里挂上 AI 节点 → 六类边 → 票的因果链 |
| Daloopa / Visible Alpha | 逐格 provenance 到 filing | provenance 有了,但**不做因果 / 预判**——这里带 lead_time + 方向 + cert_tier |
| DataHub / dbt / OpenLineage | 数据血缘 impact analysis | 血缘有了,但**机械无置信度**——这里每条边带 T1/T2/T3 + confidence |
| State of AI / Epoch / AI Index | AI 数据 + 带日期预测 | 数据 / 预测有了,但**不落到票、无逐事实 provenance** |

### 3.3 NBIS 一个完整例子

<div align="center">
<img src="assets/readme/nbis.svg" alt="NBIS:AI 发展节点 → 边(类型/跳数/tier) → 权重 → 供需对账 + 已兑现" width="100%">
</div>

AI 发展节点(D1–D7)经六类边(带跳数 · cert_tier)按权重传导到 NBIS,再供给 ⟷ 需求两端对账。**稳健性与风险是同一张图**——佐证度 = 源到票的节点不相交路径数 = 最小割(门格尔定理),割点 = 关键风险单点:

<div align="center">
<img src="assets/readme/evidence-structure.svg" alt="证据结构图:稳健性 = 最小割" width="100%">
</div>

- **NBIS**:约 6 条独立通道 → 宽、稳健;但价格主线全汇于 `neocloud 上电` → **主线最小割 = 1**,这是该盯的运营咽喉。
- **RBRK**:看似 4 源,但版权 + 监管两条都汇到治理预算节点 → **实为 2 条通道 = 脆弱**(独立性按共享节点算,不是按维度数)。

**三条已兑现方向预测**(事后按真实公开兑现构造的**校准点**;`made` 日期为回填,**非实时战绩**):

| 边预测 | made(标) → 兑现 | 一手佐证 | 结果 |
|---|---|---|---|
| 光模块 ↑ → NBIS ↑ | 2026-05-13 → 2026-09-13 | 旭创 H1 +182% · NBIS Q2 +454%(交易所 / businesswire) | ✓ |
| lab 融资 → NBIS 需求 | 2025-10-09 → 2026-07-14 | Reflection $2B 融资 → 签 NBIS $1B 合同(TechCrunch / Bloomberg) | ✓ |
| hyperscaler capex ↑ → NBIS | 2026-05-13 → 2026-08-12 | 四家 capex ≈$165B · NBIS +454% | ✓ |

**判断经济学**(不需行情,从 `decision_log` / `v_calibration` 派生):

| 指标 | 值(真库) |
|---|---|
| 判断吞吐 | 95 决策(impact_gate 42 · factor 30 · falsify 9 · edge_tier 6 · edge_predict 3 …) |
| 执行者分布 | human 60% / rule 40% / llm·model 0% |
| 校准误差 | 0.4 = ｜置信 0.6 − 命中率 1.0｜,n = 3(单桶,小样本诚实标注) |
| realized P&L | 待接行情源,不编价 |

**证伪 + 动作(把监测升级成决策支持,`key_fact.falsifier` / `status_line`)**:

- **NBIS**:证伪 = 供给猛建但需求侧融资转冷 / 进展停滞 / 人才回流 → 动作 减仓 · 关注做空侧;下一验证点 = Q3 财报 11-10。
- **RBRK**:证伪 = 企业采用单节点失速或 AI-native 挑战者替代 → 动作 降信念。

<sub>完整实跑与源可得性分级见 [`docs/process/06-NBIS实例.md`](docs/process/06-NBIS实例.md)。</sub>

---

<a id="roles"></a>

## 4 · AI / human 分工

题目③:说清哪些我做、怎么指挥、哪些 AI 做、哪些是外部借用。

**三类标注**:

- **我(分析师 / 数据负责人)做的**:定框与方向、定 schema 建模原则、两道闸终判、边定级 gold、关键取舍(`decision_fork`)。
- **AI 做的**:初稿 / 查证 / 抽取 / 落库 / 规则初判(方向、因子),全部人复核。
- **外部借用**:计算范式启发自孟醒《JEV 火了…》(见 [§1 借用声明](#ig));竞品呈现思路参考 TickerTrends / Daloopa 等。

**执行者 × 成熟度**两轴 cascade——谁做判断随校准数据移动:

<div align="center">
<img src="assets/readme/calibration-loop.svg" alt="校准复盘双控制器闭环" width="100%">
</div>

每条判断在库内显式标 `executor_kind`{rule / human / llm / model} × `calib_status`{human → shadow → assisted → auto};`运行档 = min(能力上限, 校准闸允许成熟度)`,`checks.py` 校准闸硬约束:未 validated 禁 assisted/auto。**现状诚实**:human 60% / rule 40% / **model 0%**,`decision_registry` 12 类全 draft 待复核——即"会自我校准"是 schema-ready 未 running。详见 [`docs/20-执行路由与校准闭环.md`](docs/20-执行路由与校准闭环.md)。

---

<a id="appendix"></a>

## 5 · 附录

### 目录结构

```
AI-Monitor-Fund/
├── README.md
├── pipeline/     工程核心:真值源 duckdb + 代码 + 迁移 + 视图 + 校验
├── data/tables/  7 张建库底稿 CSV  ·  data/ 13F xlsx
├── docs/         方法/协作/信息架构 · docs/process 六篇面试版整理稿
├── research/     原始工作稿(AI侧 · 指标 · 映射 · NBIS · schema 演进)
├── submission/   题目 · 二面记录 · 岗位画像
└── assets/       独立 HTML 产出 · readme 图形
```

### 如何运行 · 5 分钟复现

```bash
pip install duckdb
cd pipeline
python3 init_db.py --force   # 从 ../data/tables 底稿建库
python3 migrate.py           # 重放全部改库脚本(0001…)
python3 checks.py            # 业务校验:应得 ERROR 0
```

复现后:`edge_registry` 36 边 · `decision_log` 95 判断 · `change_log` 3,559 · `checks.py` ERROR 0——README 所有数字可一条命令复算。生成产出:`gen_schema_doc.py`(SCHEMA.md)· `gen_browser.py`(schema 浏览器)· `build_dashboard2.py`(面板)。

### 数据模型(五层)

| 层 | 表 / 视图 |
|---|---|
| 接入 | [`stg_observation`↗](pipeline/SCHEMA.md#tbl-stg_observation) |
| 资产 | [`entity_master`↗](pipeline/SCHEMA.md#tbl-entity_master) · [`metric_registry`↗](pipeline/SCHEMA.md#tbl-metric_registry)(R)· [`edge_registry`↗](pipeline/SCHEMA.md#tbl-edge_registry)(E)· 四类 [`fct_*`↗](pipeline/SCHEMA.md#tbl-fct_quant) · [`source_master`↗](pipeline/SCHEMA.md#tbl-source_master) |
| 治理 | [`assumption`↗](pipeline/SCHEMA.md#tbl-assumption) · [`coefficient`↗](pipeline/SCHEMA.md#tbl-coefficient) · [`metric_factor`↗](pipeline/SCHEMA.md#tbl-metric_factor) · [`observation_direction`↗](pipeline/SCHEMA.md#tbl-observation_direction) · [`key_fact`↗](pipeline/SCHEMA.md#tbl-key_fact) |
| 决策层 | [`decision_registry`↗](pipeline/SCHEMA.md#tbl-decision_registry) · [`decision_log`↗](pipeline/SCHEMA.md#tbl-decision_log) · [`candidate_pool`↗](pipeline/SCHEMA.md#tbl-candidate_pool) |
| 元数据 | [`schema_doc`↗](pipeline/SCHEMA.md#tbl-schema_doc) · [`change_log`↗](pipeline/SCHEMA.md#tbl-change_log) · [`migration_log`↗](pipeline/SCHEMA.md#tbl-migration_log) · [`thesis_node`↗](pipeline/SCHEMA.md#tbl-thesis_node) |

完整字典 [`pipeline/SCHEMA.md`](pipeline/SCHEMA.md) · 运行机制 [`pipeline/PIPELINE.md`](pipeline/PIPELINE.md) · 数据岗手册 [`pipeline/README.md`](pipeline/README.md)。

### 数据说明

面试提交材料。市场 as-of 模拟至 2026-09;库内混合**真实公开事实**(hyperscaler capex、光模块厂商半年报、benchmark 榜单等)与为演示构造的**示例值**。来源、来源等级、可知时间见 `source_master` / `provenance` / `snapshots/`;引用具体数字请回第三方原文核对。
