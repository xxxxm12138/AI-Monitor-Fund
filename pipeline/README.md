# pipeline · 数据侧工具与步骤

**真源 = `anatole_ai_monitor.duckdb`**（DuckDB 单文件，schema v2 = doc 21 / 17 / 18 / 23 / 29 / 30 的完整落地）。
`data/tables/13-*.csv` 只是**首次建库的导入底稿**，建库后冻结；之后每一次改库（新记录 / 填字段 / 取代 / 新边）都是 `migrations/` 下一个编号脚本，由 `migrate.py` 应用并登记在库里（`migration_log` + 字段级 `change_log`）。库能从零复现：`init_db.py --force` + `migrate.py` = 重放全部改库历史。

## 为什么是「库 + 改库脚本」而不是「改 CSV 再重灌」
| | 改 CSV 再重灌（旧） | 库 + 改库脚本（现） |
|---|---|---|
| 真源 | CSV；库是缓存 | 库；CSV 只是初始导入 |
| 一次填字段 | 长格式 CSV 一行，加载器 UPDATE | `m.set(表, 主键, 列, 值, basis=…)`，主键不存在 / 列不存在 / 快照缺失即拒绝 |
| 可溯源 | basis 在 CSV 里，库里查不到 | `change_log`：表 / 行 / 列 / 改前 / 改后 / 依据 / owner / 时间，SQL 可查 |
| 可复现 | 全量重建 | 全量重建（bootstrap + 重放）或增量应用 |
| 错误暴露 | UPDATE 0 行静默通过（本次迁移就抓到 17 行写错表） | 事务内报错整体回滚 |

## 五层
| 层 | 表 / 视图 |
|---|---|
| 接入 | `stg_observation`（一行一个事实，人 / agent 的登记格式） |
| 资产（doc21） | `entity_master`（layer × maturity 两轴）· `entity_ticker_map` · `metric_registry`（R，只存定义）· `edge_registry`（E，六类边 × 跳数 × T1–T3）· `fct_quant` / `fct_event` / `fct_opinion` / `fct_frontier`（四类事实 + doc17 通用元数据 + doc18 四补丁 + doc29 两道闸）· `fct_position` · `source_master`（doc23） |
| 治理（判断表，带 owner / status） | `assumption`（doc30）· `coefficient`（A1–A8）· `metric_factor`（r/e/l/s/φ）· `observation_direction`（A11）· `key_fact` |
| 治理·决策层（JEV-IG §四 / PLAN-decision-layer） | **`decision_registry`**（第三张登记表：R 管指标、E 管边、这张管每类重复判断的 I/O 契约与 calib_status 状态机）· **`decision_log`**（六元组过程账：state_anchor / candidates / choice / confidence / basis / outcome；retro 行禁编造置信度）· **`candidate_pool`**（PROPOSE 落点：背离解释候选，open → selected/rejected）。校准闸 = 🟠闸扩到判断：未 validated 禁 assisted/auto（checks 7l） |
| 元数据 | `schema_doc` · `relation_doc` · `calc_rule` · `etl_log` · **`migration_log`** · **`change_log`** |
| 思路层（元数据） | **`thesis_node`**（7 个主线节点）· **`decision_fork`**（关键取舍，core / detail）· **`artifact_anchor`**（决策 → 表 / 列 / 视图 / 规则 / 假设）· `v_column_origin`（反查某列来自哪一步决策）。浏览器默认「按思考脉络」，数据层每列旁有 ← 锚点 |
| 视图 | doc21 §四：`v_signal_latest`（视图 A）· `v_ticker_map`（视图 B）· `v_early_signal`；打分：`v_metric_score` · `v_edge_calc`（含与记录分数对账）· `v_ticker_weight`；数据岗：`v_health` · `v_review_due` · `v_source_master` · `v_schema_coverage`；决策层：`v_decision_health`（吞吐 / 升级率 / 欠账，R16）· `v_calibration`（置信度分桶 vs 命中率，R15）· `v_divergence`（背离清单 + 候选欠账，R17；背离 = PROPOSE 触发器） |

路由规则（接入 → 资产，`core.py`）：按指标 data_class 优先，再按记录类型：类4 → fct_frontier；类3 → fct_opinion；数值或类1 → fct_quant；event / state → fct_event；position → fct_position。去向写回 `stg_observation.routed_to`。

## 文件
| 文件 | 作用 |
|---|---|
| `schema.sql` | 29 张表（见分层）。PRIMARY KEY / FOREIGN KEY / CHECK 词表在建表时生效 |
| `views.sql` | 可推导的一律作视图 |
| `core.py` | 共用规则：解析 / 归一 / 来源 slug 与类型 / 路由 / 字段类型转换 / 来源 upsert。建库与改库共用，保证两条路径写出的行同构 |
| `init_db.py` | 首次建库：schema + data/tables/ CSV 导入 + 治理 / 元数据 + 视图；登记 `0000_bootstrap`（checksum = 六份 CSV）。库已存在则拒绝，`--force` 才删库重建 |
| `migrate.py` | 改库：应用 `migrations/` 里未应用的脚本，每个脚本一个事务；登记 `migration_log`（含脚本 checksum，已应用脚本不可再改）与 `change_log`。`--status` 看进度 |
| `migrations/NNNN_name.py` | 一次改库 = 一个脚本：`OWNER = 'B'`，`def up(m)` 里用 `m.observe()`（登记事实，自动路由 / 来源 / 方向）· `m.set()`（填一个字段，带 basis）· `m.supersede()`（旧记录被取代，不删）· `m.insert()`（新边 / 新假设等整行）· `m.sql()`（兜底） |
| `snapshots/` | 来源原文本地快照，snapshot_id = 文件名；`m.set(..., 'snapshot_id', ...)` 时文件必须存在 |
| `checks.py` | 约束之外的业务规则：已填无记录、chain 与跳数、排期引用、事件无简报、过期、未登记假设、路由完整性、字典完整性、打分对账、证据引用、快照存在、change_log 指向存在、脚本 checksum、data/tables/ CSV 建库后漂移 |
| `factors.py` / `entities.py` / `directions.py` / `metadata.py` | 因子规则 / 实体主表 / 方向规则 / 字典·关系·规则（均 B 初稿，D 复核） |
| `gen_schema_doc.py` | 从库生成 `SCHEMA.md`（每列有值率） |
| `gen_browser.py` + `browser_template.html` | 从库生成 `schema_browser.html`：按思考脉络（主线 → 分叉 → 产物，演示模式一键折叠细节）/ 按数据层级（字典 + 数据 + 关系 + 改库账），思路与字段双向锚定 |
| `build_dashboard.py` + `template.html` | 视图 → JSON → 看板 HTML（../assets/16-AI发展监测日历.html） |

## 数据岗七步
1. **登记 / 填充**：新建 `migrations/NNNN_名字.py`。新事实用 `m.observe(record_id, metric_id, entity, obs_type, value, unit, period, knowledge_time, source, provenance, note=…)`；填字段用 `m.set(table, key, column, value, basis=…)`；纠错用新 record_id + `m.supersede(old, new, reason)`，不改旧行。新指标 / 新边 / 新假设用 `m.insert(table, {...}, basis=…)`。
2. **原文留档**：来源原文抽成 `snapshots/<snapshot_id>.txt`，记录里 `snapshot_id` 指向它。
3. **应用并校验**：`python3 migrate.py && python3 checks.py`。ERROR 必须清零；WARN 逐条看。失败即整体回滚，脚本改好再跑。
4. **看改了什么**：`SELECT * FROM change_log WHERE migration_id='NNNN_…'`；`SELECT * FROM change_log WHERE table_name='metric_registry' AND pk='m_nbis_arr'` 看某一行的全部改动史。
5. **看健康**：`SELECT * FROM v_health WHERE overdue IS NOT NULL OR flag IS NOT NULL`；复验：`SELECT * FROM v_review_due`。
6. **重建看板与文档**：`python3 build_dashboard.py && python3 gen_schema_doc.py && python3 gen_browser.py`。
7. **看覆盖**：`SCHEMA.md` 每列「有值 非空/总行」。
8. **判断顺手记**（决策层）：做判断（tier 提议、来源分级、方向改判、排期入围、背离解释选择等）时用 `m.decide(decision_id, choice, basis, target='表:主键', confidence='H'/'M'/'L', state_anchor={...})`；置信度三档映射 .9/.6/.3（C21），敢写才能校准。`m.observe(direction=…)` 的人工改判自动落 d_direction 判断。背离处理：`v_divergence` 有欠账 → 解释候选进 `candidate_pool`（B/llm 提出），选择必须 D（choice = cand_id，同步候选 status/resolved_by）。outcome 事后回填并入复验节奏（超 60 天 WARN）。判断类型清单：`SELECT * FROM decision_registry`。

从零复现：`python3 init_db.py --force && python3 migrate.py`（bootstrap + 重放全部脚本，结果与增量应用一致）。

## 与生产设计的关系
doc 21 的 Postgres DDL 是生产设计；本库是它的 DuckDB 实例化（数组改文本、JSONB 改文本、INTERVAL 改文本）。迁 Postgres / Tiger 时只需改方言，视图逻辑不变；`migrations/` 即 Alembic / Flyway 的角色。
