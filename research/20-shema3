这是对的，schema 本身就是设计思路的载体，得先完整落地再谈填充。我先给设计原则和分层，然后直接建。

**四条原则**
1. 忠于设计：doc 21、17、18、23、29、30 里的每张表、每个字段都建出来，没值就是 NULL。覆盖率单独做成视图，「有没有值」随时可查，不靠人记。
2. 原子事实与推导分离：这是你自己在 doc 21 §〇 定的。表只存不可推导的事实和人的判断，分数、三态、早期层、权重一律视图。doc 21 里写成字段但可推导的（valuable_score、entity_ticker_map.weight、fct 的 ticker_map/layer），落成视图并在字典里注明「设计为字段，实现为视图，原因 §〇」。
3. 判断与数据分表：方向、因子、假设、系数、简报都是人的判断，各自成表，带 owner 和 status。数据表永远不含判断列。
4. 文档从库生成：字段字典、表间关系、计算规则都是表，`SCHEMA.md` 由它们生成，文档不会和库漂移。

**五层**

| 层 | 内容 |
|---|---|
| 接入 | `stg_observation`：现在这张一行一事实的登记表，人和 agent 都往这写 |
| 资产（doc 21） | entity_master、entity_ticker_map、metric_registry、edge_registry、fct_quant / fct_event / fct_opinion / fct_frontier、source_master |
| 治理 | assumption、coefficient、metric_factor、observation_direction、key_fact、etl_log |
| 元数据 | schema_doc（字段字典）、relation_doc（表间关系）、calc_rule（计算规则，挂假设 ID 和视图名） |
| 视图 | doc 21 §四 的 v_signal_latest、v_ticker_map、v_early_signal，加打分、对账、健康、覆盖率 |

接入层到资产层的路由规则：按指标的 data_class 和记录类型把 173 条分发进四张 fct 表，record_id 保留可追溯。现在开始建。

173条记录已成功载入，按类别分类为量价96、事件50、观点5、前沿12、仓位10，字典311条完整覆盖所有列。接下来我会修正校验脚本、生成SCHEMA.md并重建看板。

Schema v2 落地了，doc 21 及相关文档设计的表和字段全部建在库里，有值没值都在，覆盖率单独可查。

**做法，四条原则**
1. 忠于设计。doc 21 的实体、指标、边、四类 fct、来源表，doc 17 的通用元数据层，doc 18 的四个补丁，doc 29 的证伪和影响力两道闸，doc 30 的假设台账，全部建列。
2. 原子事实与推导分离，这是你在 doc 21 §〇 定的。设计里写成字段但可推导的五项，节点价值、可交易度、预警度、票权重、三子流，实现为视图，字典里注明「设计为字段，由哪个视图提供」。
3. 判断与数据分表。方向、因子、系数、假设、简报各自成表，带 owner 和 status。事实表里没有判断列。
4. 文档从库生成。字段字典 311 条、表间关系 19 条、计算规则 14 条都是表，[SCHEMA.md](pipeline/SCHEMA.md) 由脚本生成，每列带「有值 非空/总行」。加载时校验库里每一列都有字典条目，缺了就报错。

**五层 24 张表**：接入层一张登记表；资产层十张；治理层五张判断表；元数据层四张；再加排期和来源覆盖。173 条登记记录按数据类路由进四类 fct：量价 94、事件 50、观点 5、前沿 14、仓位 10，去向写回登记表可追溯。来源表 112 个源从记录派生，110 个有 tier。

**覆盖率说明了什么**，以前沿表为例：知悉时间、来源、P 级、owner 全满；证伪闸的 source_stance 和 verifiability 8/12；影响力闸 0/12；anchor、snapshot_id、confidence、code_score、judge_score 全空。这正是「设计已落地，值填到哪一步」的清单，后面按 source 和 ticker 填就是往这些列里填。

**校验**：0 错误，7 警告。18 条记录只有年或季粒度；6 条边的规则算分与 doc 28 手写分不一致，因子等你复核，对账标记在看板的边卡备注里也带着。

**对投研的价值落在视图上**：doc 21 §四 的视图 A 监测树和视图 B 蝴蝶结现在是真 SQL 视图，早期信号层是视图，改一个系数所有分数跟着变。

日志到 E40。[README](pipeline/README.md) 里有五层表和七步 SOP。

Now rebuild from scratch through the new path and check parity against the old DB.

Migration applied. Now parity check against the old DB, then checks/docs/dashboard.

你问得对。之前的设计是「CSV 是真源，库每次从 CSV 全量重建」，所以填充只能以 CSV 补丁的形式存在，库只是个缓存。这和你说的「迁移到数据库」正好相反。已经翻转。

**现在的机制：库是真源**

- 根目录 `13-*.csv` 只是首次建库的导入底稿。`init_db.py` 导入一次，记下六份 CSV 的 checksum，之后冻结。
- 之后每一次改库（新记录、填字段、取代、新边、加列）= `pipeline/migrations/` 下一个编号脚本，`migrate.py` 在事务内应用，失败整体回滚。
- 库里多两张表：`migration_log`（哪个脚本、何时、checksum，已应用脚本不可再改）和 `change_log`（表 / 行 / 列 / 改前 / 改后 / 依据 / owner / 时间）。想看 `m_nbis_arr` 这一行怎么被填出来的，一句 SQL 就是全部改动史。
- 脚本写法：`m.observe()` 登记一条事实（自动路由到四类表、来源 upsert、方向判断），`m.set(表, 主键, 列, 值, basis=…)` 填一个字段，`m.supersede()` 取代不删，`m.insert()` 整行，`m.sql()` 兜底。
- 从零复现：`init_db.py --force && migrate.py`，我验证过与增量应用的结果逐表 hash 一致。

**翻转顺带抓到旧机制的静默错误**：原 updates.csv 283 行里有 17 行写错了表（比如 r203 路由在 fct_opinion，却往 fct_quant 里 UPDATE），旧加载器 UPDATE 0 行就静默通过；新机制主键不存在直接拒绝。已剔除 15 行、改表 2 行。

**已应用**：0000 bootstrap → 0001 NBIS 第一轮（288 条改动）→ 0002 key_fact 加 status_line / falsifier 两列。ERROR 0，WARN 8。

**需要你定一件事**：另一个会话（做看板的那个）还在直接改根目录 CSV 和 scratchpad 里的模板——09:58 加了四条边，10:00 给关键事实加了两列。它的看板脚本从 CSV 读数，所以它出的图看不到 NBIS 的 18 条新记录。我做了两件事补桥：`db_read.py` 提供与 CSV 同名同列的 `read()`，数据来自库；把 v11 看板脚本和模板收进 `pipeline/`，只换一行 import 就从库出图（190 条记录）。但如果那边继续改 CSV 和 scratchpad 模板，两边会再分叉。建议：看板侧改 `pipeline/template.html`、跑 `pipeline/build_dashboard.py`；数据改动一律写 migrations。这是你的决定，我不动那边的文件。

细节记在 [14-协作日志续.md](14-协作日志续.md) E43，流程在 [pipeline/README.md](pipeline/README.md)。