# schema 设计 · 建模原则与分层

> **为什么这么做** — 前三步(供给 / 指标 / 对接)是思路,要能"可追踪、可管理、可回测",必须落成一套有纪律的表结构,否则永远是 PPT。
> **思路** — 一条硬原则贯穿:**原子事实进字段,可推导的一律进视图**;实体只存不可推导的两条轴;判断与数据分表;每条记录强制带元数据。schema 服务的是"监测 AI 发展本身",不是"给某只股票选股"。
> **目标** — 一套骨架层 schema(实体 → 指标 R → 边 E → 四类事实 → 判断 → 元数据),不依赖选哪只票、可先建、可复用;字段级真源见 [`pipeline/SCHEMA.md`](../../pipeline/SCHEMA.md)。

---

## 一、扣题:schema 服务"监测 AI 发展本身"

题面是"搭建**监测 AI 发展**的追踪体系"。最容易漏的是第一义——**能力前沿**(AI 能做什么、往哪迁),它完全不经过任何股票。所以 schema 的第一等公民是"AI 发展"整体,拆成五个可监测维度(横切价值栈六层),NBIS 只是把监测输出落到一个可观测节点的**验证点**:

| 维度 | 监测什么 | 主数据类 | 领先性 | 直接扣"AI 发展"? |
|---|---|---|---|---|
| ① 能力 / 技术前沿 | 模型能力、推理范式、开源 vs 闭源、新范式拐点 | 类4 + 类3 | 最早(领先二级数季度~数年) | ✓✓ 最字面 |
| ② 算力 / 基础设施 | 光模块 / 芯片 / 云容量 / 电力——AI 在建强度 | 类1 + 类2 | 领先财报 2–3 周 | ✓(产业义) |
| ③ 资本 / 生态 | 前沿 lab 融资、赛道资金流、估值、pre-IPO | 类2 | 领先 backlog 数季度 | ✓ |
| ④ 人才 | 顶尖研究员流向、明星团队 spin-out | 类2 | 最领先的动量信号 | ✓✓ |
| ⑤ 商用 / 落地 | API / token、企业 adoption / ARR、应用留存 | 类1 + 类2 | 同步~略领先 | ✓ |

每个维度 → 指标 → 数据源 → 获取方式 → **落到四类 fct 表的哪张 + 关键字段**,不造新 schema。demand-anchored(锚基金持仓)只决定"先把哪部分做深",不把监测对象缩成一只股票。

---

## 二、核心建模原则:字段 vs 视图

**字段存"不可再推导的原子事实";视图存"任何可从字段推导出来的分组"。** 同一"可推导层级"的东西必须一致处理。举例:

- `maturity`(research / private / pre_ipo / public)= 实体的**原子属性** → 字段。
- 「早期信号层」= maturity ∈ {research, private} → **完全可推导** → **视图**(存成字段会与 maturity 冗余、要维护同步)。
- 三子流(研究前沿 / 创业一级 / 人才资本)也可推导:它们 = "监测这个早期实体的哪一类信号" = data_class(类4 = 研究前沿 / 类2 funding = 创业一级 / 类2 personnel = 人才资本);同一实体(如 Reflection)可被三流同时监测——所以 stream 是"看它的角度",属信号层,不属实体 → 也做视图。

**结论**:实体只存两条不可推导的轴——`layer`(L1–L6 价值栈)+ `maturity`(成熟度);早期层与三子流都做视图。这条原则同时修掉了早期版本把 `signal_stream` 做成字段的**不一致**(它与 maturity + data_class 可互推)。

> 这条"原子事实 vs 推导"的纪律,是整套 schema 最难被复制的地基——它保证了库里没有脏写、没有两张皮。

---

## 三、逻辑分层(六层)

| 层 | 表 / 视图 | 职责 |
|---|---|---|
| 接入 | `stg_observation` | 一行一个事实,人 / agent 的登记格式 |
| 资产 | `entity_master`(实体,两轴)· `entity_ticker_map`(映射 + map_path)· **`metric_registry`(指标真源 R)** · **`edge_registry`(边真源 E)** · 四类 `fct_quant / event / opinion / frontier` · `source_master` | 不可推导的原子事实 |
| 治理(判断表) | `assumption` · `coefficient` · `metric_factor` · `observation_direction` · `key_fact` | 人的判断,与数据分表 |
| 决策层 | `decision_registry`(判断类型的 I/O 契约)· `decision_log`(六元组过程账)· `candidate_pool` | 每类重复判断可登记、可校准 |
| 元数据 | `schema_doc` · `migration_log` · `change_log` · 思路层锚点 | 自描述 + 审计 |
| 视图 | 可推导的一律作视图(打分 / 健康 / 早期信号 / 校准) | 杜绝脏写 |

**三条真源(R / E / 判断)分开登记**是设计的关键:改指标只动 `metric_registry`,改边只动 `edge_registry`,判断进 `decision_log`——各有单一真源,互不污染。

---

## 四、四类事实表(数据类型驱动,承 ② 指标体系)

四类 fct 表(`fct_quant / event / opinion / frontier`)共享**通用元数据层**(knowledge_time / provenance / anchor / snapshot_id / owner / confidence / status),再各带专有 payload。为什么分四张而不是一张宽表:四类的处理管线、AI / 人比例、能不能进回归本质不同(见 [② 指标体系](02-指标体系.md) §一),分表才能各自受控。

- **路由规则**:接入记录按指标 data_class 优先、再按记录类型,自动分发到四张 fct 之一,去向写回 `stg_observation.routed_to`。

---

## 五、边真源 edge_registry 与确定性验证

边(传导关系)是独立真源 `edge_registry`,每条边带 `cert_tier`(T1 可回测 / T2 结构对账 / T3 方向)+ `evidence_ids` + `last_validated`。**边不是画完就完**——像指标一样持续验、持续管(详见 [⑤ 映射范式](05-映射范式-点边权重.md) §七)。

---

## 六、迁移纪律(从"改 CSV"到"改库脚本")

真源 = DuckDB 单文件库。任何改库都走一个编号迁移脚本,由 `migrate.py` 应用并在库内登记(`migration_log` + 字段级 `change_log`),已应用脚本 checksum 冻结。为什么这样:

| | 改 CSV 再重灌(旧) | 库 + 改库脚本(现) |
|---|---|---|
| 真源 | CSV;库是缓存 | 库;CSV 只是初始导入 |
| 可溯源 | basis 在 CSV 里,库里查不到 | `change_log`:表 / 行 / 列 / 改前 / 改后 / 依据 / owner,SQL 可查 |
| 错误暴露 | UPDATE 0 行静默通过 | 事务内报错整体回滚 |

库能从零复现:`init_db.py --force` + `migrate.py` = 重放全部改库历史。

---

→ 字段级真源见 [`pipeline/SCHEMA.md`](../../pipeline/SCHEMA.md);逐票映射与权重见 [⑤ 映射范式](05-映射范式-点边权重.md);真实数据实跑见 [⑥ NBIS 实例](06-NBIS实例.md)。
