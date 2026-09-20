# AI-Monitor-Fund · AI 发展监测体系

面向成长股基金(港股 / 美股)的 **AI 发展监测体系**:把「一条 AI 前沿动态」压成可计算 state,沿因果链传导,导向具体持仓 ticker 与可观测 KPI,全程可信、可溯、可纠、可校准。

方法论是 **JEV 智能图四算子 + 闭环**:

```
新 AI 前沿内容
  → ① REPRESENT  获取 + 压缩:源分级 → 两道闸(可信度 / 重要性) → 分维 D1–D7 / 机制 / data_class
  → ② PROPOSE    枚举可能空间:沿六类边 E1–E6 扇出所有可达路径
  → ③ PREDICT    每条路径:方向(↑↓→!) × 领先期 τ × 传导确定性
  → ④ SELECT     打分(可交易 c·r·s·φ / 预警 τ·l·e) → 剪枝 → 排序 → 落到 ticker
  → ⑤ 闭环        confidence → outcome → 校准曲线,映射图自我校准
```

**真值源 = `pipeline/anatole_ai_monitor.duckdb`**(DuckDB 单文件)。任何改库都走 `pipeline/migrations/` 下一个编号脚本,由 `migrate.py` 应用并在库内登记(`migration_log` + 字段级 `change_log`),已应用脚本 checksum 冻结。库能从零复现。

---

## 目录结构

```
AI-Monitor-Fund/
├── README.md                本文件:总览 · 结构 · 如何运行
├── pipeline/                工程核心:真值源库 + 代码 + 迁移 + 视图 + 校验
│   ├── anatole_ai_monitor.duckdb   真值源(29 张表 + 视图)
│   ├── schema.sql · views.sql      表结构 / 可推导视图
│   ├── init_db.py · migrate.py · checks.py   建库 / 改库 / 校验
│   ├── core.py · db_read.py · directions.py · factors.py · entities.py · metadata.py
│   ├── migrations/                 0000_bootstrap → 00NN,一次改库 = 一个脚本
│   ├── snapshots/                  来源原文本地快照(证据,snapshot_id = 文件名)
│   ├── build_dashboard2.py · build_panel.py · gen_browser.py · gen_schema_doc.py   产出生成器
│   ├── PIPELINE.md · SCHEMA.md · README.md   运行机制 / 字段字典 / 数据岗手册
│   └── JEV-intelligence-graph.md · PANEL-DESIGN.md · UI-SPEC.md · …   方法与设计文档
├── data/
│   ├── tables/              7 张建库底稿 CSV(建库后冻结,改数走 migrations)
│   └── Anatole_13F_2023Q2-2026Q2_1.xlsx   持仓 13F
├── docs/                    顶层方法 / 协作日志 / 信息架构文档
├── research/                研究过程:AI 侧 · schema 演进 · 映射 · NBIS 实例 · 假设台账 · 数据源
├── submission/             题目 · 二面记录 · 合伙人背景与岗位画像
└── assets/                  独立 HTML 产出(AI 发展监测日历 · schema 浏览器)
```

---

## 如何运行

**环境**:Python 3 + DuckDB。

```bash
pip install duckdb
```

**应用改库并校验**(日常):

```bash
cd pipeline
python3 migrate.py          # 应用 migrations/ 里未应用的脚本,刷新视图
python3 checks.py           # 业务规则校验:ERROR 必须为 0,WARN 逐条看
```

**从零复现真值源**(bootstrap + 重放全部改库脚本,结果与增量应用一致):

```bash
cd pipeline
python3 init_db.py --force  # 从 ../data/tables/ 的底稿 CSV 建库
python3 migrate.py          # 重放 0001…00NN
python3 checks.py           # 应得 ERROR 0
```

**生成产出**:

```bash
cd pipeline
python3 gen_schema_doc.py   # 库 → SCHEMA.md(每列有值率)
python3 gen_browser.py      # 库 → schema_browser.html(按思路 / 按数据层双视图)
python3 build_dashboard2.py # 库 → panel_v2.html(数据管理者面板)
```

**在副本上测试**(不动真值源):设 `ANATOLE_DB` 指向库副本,`ANATOLE_MIGRATIONS` 指向私有迁移目录。

---

## 数据模型(五层)

| 层 | 表 / 视图 |
|---|---|
| 接入 | `stg_observation`(一行一个事实,人 / agent 的登记格式) |
| 资产 | `entity_master` · `metric_registry`(R,指标定义)· `edge_registry`(E,六类边 × 跳数 × T1–T3)· `fct_quant/event/opinion/frontier`(四类事实)· `source_master` |
| 治理 | `assumption` · `coefficient` · `metric_factor`(r/e/l/s/φ)· `observation_direction` · `key_fact` |
| 治理·决策层 | `decision_registry`(每类重复判断的 I/O 契约 + calib_status)· `decision_log`(六元组:state_anchor / candidates / choice / confidence / basis / outcome)· `candidate_pool` |
| 元数据 | `schema_doc` · `migration_log` · `change_log` · `thesis_node` · `decision_fork` · `artifact_anchor` |

完整字典见 [`pipeline/SCHEMA.md`](pipeline/SCHEMA.md);运行机制见 [`pipeline/PIPELINE.md`](pipeline/PIPELINE.md);数据岗操作见 [`pipeline/README.md`](pipeline/README.md)。

---

## 方法与分工

每条判断在库内显式标注执行者:**AI 生成 / 分析师复核 / 数据团队**(`decision_log.executor_kind`),配合 calib_status 状态机(human → shadow → assisted → auto):未经校准验证的判断不得自动化。这既满足题目对 AI / 人分工的要求,也让整套推理链可审计。

---

## 数据说明

本仓库为面试提交材料。市场 as-of 模拟至 2026-09;库内数据混合**真实公开事实**(公开披露的 hyperscaler capex、光模块厂商半年报、benchmark 榜单等)与为演示构造的**示例值**。每条记录的来源、来源等级与可知时间见 `source_master` / `provenance` / `snapshots/`;引用具体数字请回第三方原文核对。
