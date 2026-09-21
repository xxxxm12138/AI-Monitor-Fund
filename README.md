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

> **一句话**:这不是一个"会写 AI 研报"的东西,而是一张**从持仓票向上游反推、每条边过验证、每个数可溯源、每个判断有主的因果图**——供给侧是 AI 发展七维 + 前沿雷达,需求侧是 13F 持仓,交点是边(六类 × 跳数 × 三层验证),节点是只存定义的指标,治理是来源总账 × 假设台账,呈现是日历式看板。

## 目录

- [1 · Intelligence Graph 思路(为什么是这个形状)](#ig)
- [2 · 体系设计(按题面四要求)](#system)
- [3 · 可靠性 + 差异化(给例子)](#proof)
- [4 · AI / human 分工](#roles)
- [5 · 未做与已知不足(不遮)](#gaps)
- [6 · 附录(结构 · 运行 · 复现)](#appendix)

---

<a id="ig"></a>

## 1 · Intelligence Graph 思路

<div align="center">
<img src="assets/readme/paradigm.svg" alt="计算范式:compress → propose → predict → prune → typed decision" width="100%">
</div>

出发点是一个关于**计算范式**的判断:

> **能用 Generation 表达的智能,不一定应该用 Generation 计算。**

投研是最典型的 **decision-native** 工作负载:每个节点输入很复杂(多源证据、可信度、口径可比性),输出却只是**有限候选上的一个选择 + 一个置信度**。所以我没把它做成"一个会写研报的 AI",而是把整套体系设计成一条计算链——四个算子跑一个 expand–prune 循环(全篇只在这里讲一次):

| 算子 | 做什么 | 落到体系里 |
|---|---|---|
| **REPRESENT** 压缩表征 | 把混乱世界压成 point-in-time、可比较的 state | 四类事实表 + 通用元数据 |
| **PROPOSE** 生成候选空间 | 枚举"AI 发展怎么打到票"的所有可达路径 | 六类边 × 跳数 |
| **PREDICT** 指标预判 | 在指标空间预判方向 / 量级 / 领先期 | 领先期 + 预期基准 |
| **SELECT** 剪枝选择 | 有限候选上的高频判断:路由 / 分级 / 验证 / 排序 | 两道闸 + 打分排序 |
| **闭环** 自我校准 | confidence → outcome → 校准曲线,回灌上面每一步 | 决策层六元组 |

这条范式带来两个立场:**候选空间是被设计、可扩张、可校准的**(常规投研按供应链 / 竞对分析,本质就是在一个人工枚举的候选空间里工作);**执行者是可替换件**——每个决策点声明 typed I/O 契约,今天由人和规则执行,明天可换成专用小模型,而**今天每一行判断,同时是明天那个模型的训练集**。这就是"为后来的 AI 基建做设计"。

<sub>本节计算范式**启发自孟醒《JEV 火了，但真正重要的不是 JEV》**;我在此之上的落地贡献是下文的 schema / checks / 中国地面数据 / 证伪闸。全文与读后立场见 [`pipeline/JEV-intelligence-graph.md`](pipeline/JEV-intelligence-graph.md)。</sub>

---

<a id="system"></a>

## 2 · 体系设计

**治理原则(我定,全程不让步)**:真数可溯源 · 假设登记(🟠 闸:未验证不进阈值与仓位)· 扣题(监测对象 = **AI 发展本身**,NBIS 只是验证点)· 映射从票向上游反推 · 边过验证 · 可推导的一律作视图。

<div align="center">
<img src="assets/readme/bowtie.svg" alt="供需对接:AI 供给 D1–D7 → 六类边 → 持仓 ticker" width="100%">
</div>

下面按题面自定的四项展开,每项附当时的**关键取舍**(为什么这么定、纠偏了什么);完整十环节见 [`docs/22 解题思路与分工`](docs/22-解题思路与分工.md) · [`docs/23 取舍明细`](docs/23-解题思路.md)。

### ① 分析角度:AI 发展怎么拆、怎么落到票

供给侧拆成**七维 D1–D7**(算力 / 数据 / 资本 / 人才 / 能力前沿 / 商用 / 政策·能源),每维一条"拆解主轴"保证查全;实体只存两条不可推导的轴 layer L1–L6 × maturity,早期信号层作视图不作字段。

> **全程最大一次纠偏**:参考路线是"VC data → ticker";我把主线改成"**AI 发展 → ticker,从持仓票向上游反推**"——先有票才有分量、有验证点、能对账。每条链数跳数、分六类边 E1–E6。

### ② 数据源:真数、分级、分类

> 我要求"**不要示例值,所有来源做详细分类、持续管理**"。

全部真数:**318 条**接入、**177 个**来源、**五级 provenance**(P1 一手 … P5 设计层)、逐条本地快照 + 原文锚点。按数据结构分**四类事实表**——量价(可回归)/ 事件(可建图)/ 观点(带发言人分级)/ 前沿(知识流)——共享一层通用元数据(来源 / P 级 / 知悉时间 / 快照 / 取代不删 / owner)。

**诚实划界**——主动划范围比假装全覆盖可靠。本体系聚焦 **AI 基建价值链**,因可投资 KPI 与中国地面数据集中于此:

| AI 发展域 | 覆盖 | 落点 |
|---|---|---|
| D1 算力 · D3 资本 · D7 政策 / 能源 | 🟢 深 | 光模块中国厂商月营收 / 海关 / NBIS · lab 融资 · BIS / IEA |
| D6 商用 · D5 能力前沿 · D2 数据 | 🟡 中 | RBRK · Epoch / Artificial Analysis · 前沿雷达样本薄 |
| D4 人才 | ⛔ | 合规受限,只登记原则 |

### ③ 更新频率:频率即领先性

> 频率不是拍的。每个指标按三件事定、写进 registry:**源的天然节奏 × 它服务的决策时刻 × 边的领先期**。

关键洞见:**月频信源领先季频财报,不是巧合,是频率差**。

| 信源(例) | 频率 | 领先(先验) | 采集 |
|---|---|---|---|
| 光模块中国厂商月营收(旭创 / 新易盛) | 月 | ~18d | 交易所 / akshare |
| 海关 HS8517 光模块出口 | 月 | ~20d | 海关月报 |
| NBIS 自有电力上电 | 事件 | ~90d | 电话会 |
| 前沿 lab 融资 | 事件 | 180–278d | 新闻 / Form D |
| hyperscaler capex | 季 | ~财报 −2–3w | 10-Q / 电话会 |

<sub>领先天数多为**先验**(挂假设台账,未验证禁 sizing);lab 融资 180d 已因 Reflection 实测 278d 进入 calibrating。next_release 分四级依据(公司公告 / 规则推定 / 估计 / 待定),估的不当钉死的。</sub>

### ④ 展现方式:面板给研究员 / PM

> 纠偏:AI 第一版看板把 schema 信息塞给研究员。**面板定位是研究员和 PM,不是数据岗**。

主视图**日历式**(实测 / 预期 / 上期);信号列按**五个决策时刻**定(链状态 / 本周动了什么 / 预警 / 领先读),不是活动量与日程;蝴蝶结与整页下钻按需。术语分三层(用户 / 分析 / 方法),使用者读不懂内部词"肯定不行"。

### ⑤ 讲清逻辑:四算子如何落到 schema,以及执行 harness

四算子不是概念,每一步都落到真实表(带真实规模 · ↗ 跳字段结构 · 成熟度如实标):

| 算子 | 落点(真实规模) | 成熟度 |
|---|---|---|
| REPRESENT | [`stg_observation`↗](pipeline/SCHEMA.md#tbl-stg_observation) 318 条单口接入 → `route()` 确定性分四类 [`fct_*`↗](pipeline/SCHEMA.md#tbl-fct_quant) + 仓位(零漏)· 元数据 100% · provenance P1–P5 · snapshot→真快照 · [`source_master`↗](pipeline/SCHEMA.md#tbl-source_master) 177 | 🟢 运行 |
| PROPOSE | [`edge_registry`↗](pipeline/SCHEMA.md#tbl-edge_registry) 36 边(六类 × 跳数 0–3 × `map_path`+`evidence_ids`)· [`candidate_pool`↗](pipeline/SCHEMA.md#tbl-candidate_pool) · [假设台账↗](pipeline/SCHEMA.md#tbl-assumption) 42 | 🟢 运行 |
| PREDICT | [`metric_registry`↗](pipeline/SCHEMA.md#tbl-metric_registry) 85 指标(只存定义)`.lead_time_est` · 预期基准 · [日历↗](pipeline/SCHEMA.md#tbl-calendar) 58 | 🟡 部分 |
| SELECT | 两道级联闸(证伪 → 影响力)· [`observation_direction`↗](pipeline/SCHEMA.md#tbl-observation_direction) · [`metric_factor`↗](pipeline/SCHEMA.md#tbl-metric_factor) 84 × r/e/l/s/φ → `tradable=c·r·s·φ`(**系数登记为假设,只排序、禁 sizing**) | 🟢 运行 |
| 闭环 | [`decision_log`↗](pipeline/SCHEMA.md#tbl-decision_log) 95 六元组 · [`decision_registry`↗](pipeline/SCHEMA.md#tbl-decision_registry) 12 类 I/O 契约 + `calib_status` 状态机 · `v_calibration` | ⚪ 骨架就绪 |

> 纠偏:"**系数你是怎么定的?是假设就要标出来**" → 全部系数登记进假设台账,未验证 🟠 不进阈值。"**为什么还是 CSV?**" → 库为真源,底稿 CSV 冻结为首次导入,每次改库一个脚本 + 一份字段级账。

**执行 harness**(题目②"执行系统",input → trace 六段都可跑):

| 环节 | 落点 |
|---|---|
| input 输入 | 信源采集 → `stg_observation` · `source_master`(tier / kind / access) |
| pipeline 管线 | REPRESENT `route()` → PROPOSE 边 → PREDICT → SELECT → 闭环 |
| rule 规则 | `checks.py` 业务守闸 · `calc_rule` 公式 · `directions.py` / `factors.py` 规则初判 |
| tool 工具 | `migrate.py`(改库) · `core.py`(路由 / 归一) · `gen_*.py`(反生成文档) |
| output 产出 | 视图(`v_edge_calc` / `v_metric_latest` / `v_calibration`)· 面板 · `SCHEMA.md` |
| context 契约 | `schema_doc`(全列字典)· `decision_registry`(每类判断 state_schema × candidates) |
| trace 留痕 | `change_log` 3,559 字段级 · `decision_log` 95 六元组 · `migration_log` · (Langfuse 留位) |

**工程优美性**:改库走编号迁移(checksum 冻结,已应用不可改)· `init_db --force + migrate` 从零重放 = 增量应用 · `checks.py` 每次改库自动跑、ERROR 必须为 0 · 三张单一真源(指标 R / 边 E / 判断 registry)· 可推导一律作视图,`SCHEMA.md` 由库反生成、文档不漂。

---

<a id="proof"></a>

## 3 · 可靠性 + 差异化(给例子)

### 可靠性(岗位第一考核:链稳 / 准 / 断了能第一时间发现)

| 维度 | 证据 |
|---|---|
| 稳(零漏) | 318 条接入 100% 确定性路由,`checks.py` 路由完整性守闸 = 0 漏 |
| 准(分级) | 每条带 provenance P1–P5 + reliability_note;可只按 P1 定仓、隔离 rumor |
| 可溯 | fct → snapshot_id → 真快照文件,`checks.py` 逐条验存;anchor 存原文短引 |
| 可纠 | 取代不删(`superseded_by`)+ `change_log` 3,559 字段级 + migration checksum 冻结 |
| 可复现 | `init_db --force + migrate` 从零重放,结果与增量一致([§6 复现](#appendix)) |

**诚实成熟度**(体系自设证伪标准):🟢 已运行 = 接入 / 路由 / 四类事实 / 六类边 / 判断六元组账;🟡 骨架就绪 = outcome 回填 3/95、校准仅 1 桶、边回测 1/36、模型执行者 0;⛔ 按纪律暂关 = 系数未 validated → 只排序禁 sizing、realized P&L 无行情源**留位不编价**。

### 差异化:中国地面数据 nowcast + 管理层证伪

- **中国地面数据 nowcast(STAAR 范式)**:美股 / 港股上市、真 KPI 由中国决定(手术量、分销库存、光模块出货),而覆盖该票的华尔街分析师**拿不到**中国地面数据。结构上靠[频率差](#system)领先卖方季报。*(领先为先验 / 目标,尚无卖方覆盖日期对照,不作已证声明。)*
- **对管理层声明的证伪**(直击 George 的 FF 教训):用**供需两端对读**交叉验证同一 thesis——供给端"在建多少"⟷ 需求端"需求真不真",背离即预警;证伪闸区分 `source_stance`(vendor_pr vs neutral)× `verifiability`(claimed_only vs third_party)。

**对标竞品——差异化落在哪一格**:

| 你租得到 | 它给你 | 这里多给的一格 |
|---|---|---|
| TickerTrends / M Science | 逐 KPI Bogey / Consensus / Δ% | KPI 有了,**无传导来路**——这里挂 AI 节点 → 边 → 票的因果链 |
| Daloopa / Visible Alpha | 逐格 provenance 到 filing | provenance 有了,**不做因果 / 预判**——这里带 lead_time + 方向 + tier |
| DataHub / dbt | 数据血缘 impact analysis | 血缘有了,**机械无置信度**——这里每条边带 T1/T2/T3 + confidence |
| State of AI / Epoch | AI 数据 + 带日期预测 | 数据 / 预测有了,**不落到票、无逐事实 provenance** |

### 一个完整例子:NBIS

<div align="center">
<img src="assets/readme/nbis.svg" alt="NBIS:AI 发展节点 → 边 → 权重 → 供需对账 + 已兑现" width="100%">
</div>

AI 发展节点(D1–D7)经六类边(带跳数 · tier)传导到 NBIS,再供给 ⟷ 需求两端对账。**稳健性与风险是同一张图**:佐证度 = 源到票的节点不相交路径数 = 最小割(门格尔定理),割点 = 关键风险单点。

<div align="center">
<img src="assets/readme/evidence-structure.svg" alt="证据结构图:稳健性 = 最小割" width="100%">
</div>

- **NBIS**:约 6 条独立通道 → 宽、稳健;但价格主线全汇于 `neocloud 上电` → **主线最小割 = 1**,这是该盯的运营咽喉。
- **RBRK**:看似 4 源,版权 + 监管两条都汇到治理预算节点 → **实为 2 条通道 = 脆弱**(独立性按共享节点算,不是按维度数)。

**三条已兑现方向预测**——诚实标注:这是**事后按真实公开兑现构造的校准点**,`made` 日期为回填,**非实时战绩**:

| 边预测 | made(标)→ 兑现 | 一手佐证 | 结果 |
|---|---|---|---|
| 光模块 ↑ → NBIS ↑ | 2026-05-13 → 2026-09-13 | 旭创 H1 +182% · NBIS Q2 +454%(交易所 / businesswire) | ✓ |
| lab 融资 → NBIS 需求 | 2025-10-09 → 2026-07-14 | Reflection $2B 融资 → 签 NBIS $1B 合同(TechCrunch / Bloomberg) | ✓ |
| capex ↑ → NBIS | 2026-05-13 → 2026-08-12 | 四家 capex ≈$165B · NBIS +454% | ✓ |

**证伪 + 动作**(把监测升级成决策支持,`key_fact.falsifier`):NBIS 的证伪 = 供给猛建但需求侧融资转冷 / 进展停滞 → 动作 减仓 · 关注做空;下一验证点 = Q3 财报。**判断经济学**(不需行情,从 `decision_log` 派生):吞吐 95 决策 · 执行者 human 60% / rule 40% / model 0% · 校准误差 0.4(=｜置信 0.6 − 命中率 1.0｜,n=3 单桶)。完整实跑见 [`docs/process/06-NBIS实例.md`](docs/process/06-NBIS实例.md)。

---

<a id="roles"></a>

## 4 · AI / human 分工

> **分工原则一句话:方向由我定,AI 按定下的方向生成与执行;判断由我定义,AI 出初稿,我复核后才算数。**

库里每一行 owner 用四个字母,分工写进数据:**D** 我定 · **C** 我定义规则 AI 执行 · **B** AI 初稿我必复核 · **A** AI 独立执行我抽检。三类来源也分清:**我做的**(治理原则 / 七维 scope / 映射方向 / 验证层级 / 系数是假设 / 库为真源 / 面板定位 / 审计取舍)· **AI 做的**(初稿 / 查证 / 抽取 / 落库 / 规则初判,全部人复核)· **外部借用**(计算范式启发自孟醒《JEV…》;竞品呈现参考 TickerTrends / Daloopa)。

**谁做判断随校准数据移动**——`executor_kind`{rule / human / llm / model} × `calib_status`{human → shadow → assisted → auto},`checks.py` 校准闸硬约束:未 validated 禁 assisted / auto。

<div align="center">
<img src="assets/readme/calibration-loop.svg" alt="校准复盘双控制器闭环" width="100%">
</div>

**现状诚实**:`decision_log` human 60% / rule 40% / **model 0%**,判断表(方向 / 因子 / 关键事实 / 思路分叉)全为 draft、未经复核——即"会自我校准"目前是 schema-ready 未 running。完整分工总表见 [`docs/22`](docs/22-解题思路与分工.md)。

---

<a id="gaps"></a>

## 5 · 未做与已知不足(不遮)

- **回测层未做**:36 条边 0 条 production;T1"可回测"边仅 2 条真且尚未回测;周频指标多数只有一次快照、季频最多 5 期,历史深度不够做趋势与 nowcast。
- **判断层未经人复核**:方向 / 因子 / 关键事实 / 思路分叉全为 B 初稿(看板已标"未经复核")。
- **自动化未建**:快照 / 抽取 / 登记 / 校验 / 改库账每步都有代码并跑过一轮,但缺**调度器、抽取器、判断队列**三件;`next_release` 仍是文本、过期检测实际不触发。
- **eval / trace / harness(step 3)未建**:`code_score` / `judge_score` / `model_version` 列空着,LLM 抽取质量闸尚无数据。

这些是当前的**分工现状与优先级取舍**,不是终态——诚实标注它们,本身就是数据治理的第一考核。

---

<a id="appendix"></a>

## 6 · 附录

### 目录结构

```
AI-Monitor-Fund/
├── README.md
├── pipeline/     工程核心:真值源 duckdb + 代码 + 迁移 + 视图 + 校验
├── data/tables/  建库底稿 CSV  ·  data/ 13F xlsx
├── docs/         解题思路(22/23)· 判断层(19/20)· 数据来源(21)· process 六篇整理稿
├── research/     原始工作稿(AI侧 · 指标 · 映射 · NBIS · schema 演进)
├── submission/   题目 · 二面记录 · 岗位画像
└── assets/       独立 HTML 产出 · readme 图形
```

### 如何运行 · 5 分钟复现

```bash
pip install duckdb
cd pipeline
python3 init_db.py --force   # 从 ../data/tables 底稿建库
python3 migrate.py           # 重放全部改库脚本
python3 checks.py            # 业务校验:应得 ERROR 0
```

复现后可一条命令复算 README 所有数字:`edge_registry` 36 · `decision_log` 95 · `change_log` 3,559 · `stg_observation` 318 · `checks.py` ERROR 0。生成产出:`gen_schema_doc.py`(SCHEMA.md)· `gen_browser.py`(schema 浏览器)· `build_dashboard2.py`(面板)。

### 数据模型(五层)· 更多

数据模型五层(接入 → 资产 → 治理 → 决策层 → 元数据)字段字典见 [`pipeline/SCHEMA.md`](pipeline/SCHEMA.md);运行机制见 [`pipeline/PIPELINE.md`](pipeline/PIPELINE.md);数据来源与处理方法见 [`docs/21`](docs/21-数据来源与处理方法说明.md);数据岗手册见 [`pipeline/README.md`](pipeline/README.md)。

**数据说明**:面试提交材料;市场 as-of 模拟至 2026-09,库内混合真实公开事实与为演示构造的示例值,来源 / 来源等级 / 可知时间见 `source_master` / `provenance` / `snapshots/`,引用具体数字请回第三方原文核对。
