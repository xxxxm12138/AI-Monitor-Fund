# PLAN · 决策层三块增量落地计划

**日期** 2026-09-20 ｜ **性质** 实施计划（已执行完毕）｜ **上游** `pipeline/JEV-intelligence-graph.md` §四 ｜ **对应增量**：① decision_registry ② 判断六元组 ③ 背离即 PROPOSE

> **执行状态（2026-09-20）**：P0 拍板（四问均甲案）→ P1–P5 全部落地 = migrations **0010–0014**，每步 ERROR 0，两次全库重放对账一致。假设编号 C9–C11 落库时已被占用，顺延 **C19–C21**。细节见 `14-协作日志续.md` E49。待 D：registry 10 行逐行复核转 reviewed；r133 / ticker:NBIS 背离解释选择；F3.13 / F2.15 分叉文字。

---

## 〇 目标与非目标（防跑偏的边界，先读这节）

**目标**：把"判断"提升为与 R（指标）、E（边）并列的一等公民——每类重复判断有登记、每次判断留六元组、背离触发候选扩张。全部走 migrations，ERROR=0，从零可复现。

**非目标（本轮明确不做）**：
1. **不接入、不训练任何模型**。shadow / assisted 是未来某个 migration 的事；本轮只铺 schema、记录纪律和视图。
2. **不改现有判断表结构、不搬家现有列**。`observation_direction`、`key_fact`、`fct_frontier` 的闸列全部留在原地；新增的 decision_log 引用它们，不取代它们。
3. **不大规模回填历史判断**。只回填有据可查的少数实例（见 P3），禁止给历史判断编造置信度。
4. **不动看板**。三个新视图先只进 SCHEMA.md 与 checks 输出；前端呈现另起一轮。
5. **不阻塞步骤 2 填数**。`m.decide()` 是可选增强，`m.observe()` 流程一行不改。
6. **所有阈值先登记为假设**。🟠 未 validated 的决策类型禁止标 assisted / auto——doc30 纪律原样扩展。

---

## 一 三个设计分叉（B 已选，D 复核时可推翻）

### F-a 六元组落在哪：每张判断表加列 vs 统一 decision_log —— **选 decision_log**
判断现在散落在**行级**（observation_direction、key_fact）和**列级**（fct_frontier 两道闸、edge_registry.cert_tier、calendar.status、metric_registry.fill_status）。逐表加列覆盖不了列级判断，且要 ALTER 六张表。统一一张 `decision_log`（一行 = 一次判断实例）完全复用 change_log 的肌肉记忆：change_log 记"改了什么"，decision_log 记"为什么这样判断、当时多有把握、事后对不对"。判断的**结果**仍写回原来的家（direction 还在 observation_direction），decision_log 是判断的**过程账**。加一条 checks 规则保证两边不漂移。

### F-b 背离候选落在哪：复用 key_fact vs 新表 candidate_pool —— **选 candidate_pool**
key_fact 是"有作者的简报"，语义是结论；候选解释在被选中前不是结论，混进去会污染简报语义。新表 candidate_pool，行生命周期 open → selected / rejected / merged，选中动作本身是一条 decision_log。

### F-c decision_registry 里放不放打分公式 —— **不放**
可推导一律作视图（doc21 §〇）。registry 只登记判断类型的元数据（输入、候选、执行者、校准状态）；校准误差、吞吐、升级率全是视图（v_calibration / v_decision_health）。

---

## 二 新增对象总览

### 表（3 张，治理层扩容）

**`decision_registry`** —— 真源 D 之外的第三张登记表（R 指标 / E 边 / 这张管判断）：
`decision_id` PK · `name` · `question`（一句在问什么）· `state_schema`（输入由哪些表列/视图构成）· `candidates`（JSON 词表；开放候选标 `open→candidate_pool`）· `output_home`（结果写回哪张表哪列）· `executor_kind` CHECK(rule/human/llm/model) · `executor`（A–D / 规则名 / 模型名）· `freq_est` · `escalation`（升级规则文本 + assumption_id）· `calib_status` CHECK(human/shadow/assisted/auto) · `assumption_ids` · `owner` · `status` · `design_ref` · `notes`

**`decision_log`** —— 六元组过程账（学 change_log，target 用文本对不用 FK）：
`dec_id` PK · `decision_id` REFERENCES decision_registry · `target_table` · `target_pk`（列级判断记 `pk.column`）· `state_anchor`（JSON：record_id 集合 + as-of 时间，判断可复现）· `candidates_shown`（当时的候选，registry 词表的快照）· `choice` · `confidence`（0–1）· `executor_kind` / `executor` · `basis` · `decided_at` · `retro` BOOLEAN（回填行标 true，confidence 允许空）· `outcome` CHECK(correct/wrong/mixed/unresolved) · `outcome_basis` · `outcome_at`

**`candidate_pool`** —— PROPOSE 的落点：
`cand_id` PK · `decision_id`（通常 d_divergence_explain）· `trigger_ref`（触发它的 record / kf / 边）· `kind` CHECK(explanation/new_edge/new_edge_type/new_metric/new_assumption) · `candidate_text` · `proposed_by`（A–D / llm）· `status` CHECK(open/selected/rejected/merged) · `created_at` · `resolved_by`（选中它的 dec_id）· `note`

### 视图（3 个，views.sql）
- `v_decision_health`：按 decision_id 出 判断次数 / 每周吞吐 / executor 分布 / 升级率 / outcome 回填缺口。
- `v_calibration`：decision_log 中 outcome 非空的行，按 decision_id × confidence 分桶出 命中率 vs 置信度（校准曲线的表形式）。初期行数为 0 是预期，视图从第一天就在。
- `v_divergence`：当前背离清单——对账节点两端方向相反、或 direction='!' 的最新观测；LEFT JOIN candidate_pool 暴露"背离无候选"。（C6 数值阈值仍占位，先用方向布尔，不发明阈值。）

### 计算规则（calc_rule 注册）
- R15 校准误差 = |bucket 命中率 − bucket 置信度|（输出 v_calibration）
- R16 升级率 = 升级次数 / 判断次数（输出 v_decision_health）
- R17 背离判定 = 对账 pair 方向相反（阈值版待 C6，输出 v_divergence）

### 代码改动（非 migration 文件，随 P1 一起）
- `core.py`：PK 字典注册三张新表（checks 7g、m.set 依赖）。
- `migrate.py`：新增 `m.decide(decision_id, target, choice, confidence, state_anchor, basis, ...)`——一行写 decision_log，可选同步写 output_home（内部走 m.set，改动照进 change_log）。
- `checks.py`：新规则见 §四。
- `views.sql` + migration 内 `CREATE OR REPLACE VIEW` 双写（0006 先例），保证 init_db --force 重放与增量应用一致。
- `README.md`：治理层表清单 + 七步 SOP 加 m.decide 用法。

---

## 三 decision_registry 首批 10 行（词表 = D 复核的核心对象）

| # | decision_id | 在问什么 | 候选 | 现执行（kind·who） | calib_status | output_home |
|---|---|---|---|---|---|---|
| 1 | d_route | 这条观测进哪张 fct | {fct_quant, fct_event, fct_opinion, fct_frontier, fct_position} | rule · core.py | auto（确定性代码，豁免校准闸） | stg_observation.routed_to |
| 2 | d_direction | 这条观测对 thesis 方向如何 | {↑, ↓, →, !, —} | rule+human · directions.py 初判 B 复核 | assisted（已是人机协作，补记录即可） | observation_direction.direction |
| 3 | d_falsify_gate | 这条前沿信息可证伪吗 | source_stance {neutral, vendor_pr, social} × verifiability {reproducible, third_party_verified, claimed_only, rumor} | human · B | human | fct_frontier.source_stance / verifiability |
| 4 | d_impact_gate | 过闸的前沿信息影响多大 | {高, 中, 低}（量化口径 = C8 占位） | human · D | human | fct_frontier.industry_impact |
| 5 | d_regime | 对账节点三态 | {同向, 平, 背离} | human · D（规则 C6 占位） | human | key_fact.status_line / 看板 regime |
| 6 | d_edge_tier | 这条边的验证档位 | {T1, T2, T3} | human · D 定 gold A 跑回测 | human | edge_registry.cert_tier |
| 7 | d_source_tier | 这个来源什么等级 | {P1, P2, P3, P4, P5} | human · B | human | source_master.source_tier |
| 8 | d_fill_priority | 这个缺口先填谁 | {队列1–9, 跳过}（基金视角排序） | human · D | human | metric_registry.fill_status |
| 9 | d_calendar_scope | 这个排期事件在不在 AI 发展范围 | {active, retired} | human · B 提议 D 复核 | human | calendar.status |
| 10 | d_divergence_explain | 这个背离最可能的解释 | open → candidate_pool | human · D（候选生成 = llm/B） | human | decision_log 本身（选中项回填 candidate_pool.status） |

读法：#1 证明 cascade 的 auto 端已经存在（确定性代码）；#2 证明 assisted 已经存在（directions.py 初判 + 人复核）——**这张表不是愿景，是现状盘点 + 演进路径**。每行的 escalation 与 freq_est 在 P2 落库时补齐。

---

## 四 checks.py 新规则

| 级别 | 规则 |
|---|---|
| ERROR | decision_log.decision_id 必须在 registry；choice 必须 ∈ 当行 candidates_shown（open 类除外） |
| ERROR | decision_log 与 output_home 一致性：最新一条判断的 choice = 目标行当前值（被 supersede 的除外） |
| ERROR | confidence 超出 [0,1]；outcome 非词表值 |
| ERROR | **校准闸**：calib_status ∈ {assisted, auto} 且 executor_kind ∈ {llm, model} 的决策类型，其关联 assumption 必须 validated（🟠闸扩展；rule 豁免） |
| ERROR | candidate_pool.resolved_by 指向的 dec_id 必须存在；selected 候选必须有对应 decision_log |
| WARN | v_divergence 中 open 背离超 7 天无任何 candidate（PROPOSE 欠账） |
| WARN | decision_log 非 retro 行 confidence 为空（敢写才能校准） |
| WARN | outcome 回填缺口：decided_at 超过复验周期仍 unresolved/空 |

---

## 五 分步工序（migration 0010–0014）

### P0 · 拍板（D，不写代码）
复核本计划 + §三词表 + §六开放问题。**P0 不过，后面全部不动**——这是防跑偏的总闸。产物：本文件状态改 reviewed，开放问题四选一落字。

### P1 · `0010_decision_layer_ddl`
三张表 DDL（m.sql）+ schema_doc 全列字典（7c 会挡缺列）+ relation_doc 三条 + calc_rule R15–R17 + views.sql 三视图（双写）+ core.py PK 注册 + migrate.py 加 m.decide + checks.py 新规则。
**验收**：`migrate.py && checks.py` ERROR=0；`init_db.py --force && migrate.py` 重放与增量逐表 hash 一致（E43 先例）；SCHEMA.md 出现三张新表且每列有字典；三视图可 SELECT（允许 0 行）。

### P2 · `0011_decision_registry_seed`
§三的 10 行落库（owner 按表；status=draft 待 D 复核逐行转 reviewed）；新假设登记：C19 升级阈值（🟠）、C20 校准闸口径（🟠）、C21 confidence 三档锚（Q1 甲案，🔵）——原计划编号 C9–C11 落库时已被领域假设占用，顺延；同步 `15-假设台账增补.md`。
**验收**：registry 10 行；每行 candidates 可被 json 解析；assumption 三行入台账且 impact 标对。

### P3 · `0012_decision_log_backfill_minimal`
只回填四组**有据可查**的判断实例（全部 retro=true，confidence 留空不编造）：
1. 6 条已打分边的 tier 判断（basis=doc28 §四，state_anchor=各边 evidence_ids）；
2. 当前 regime=信念 的对账判断（basis=doc20/28，target=kf055）；
3. fct_frontier 已填的 8 条证伪闸判断（state_anchor=各 record 自身）；
4. 0007 的排期 retire 判断（basis=migration 0007，change_log 里有现成依据）。
自此**新判断一律 prospective**：步骤 2 填数中每次 tier 提议、source_tier、方向复核改用 m.decide 顺手记（observe 自动方向仍免记，d_direction 只记人工改判的）。
**验收**：checks 一致性规则通过（decision_log choice 与目标行现值对上）；retro 行数 ≈ 6+1+8+N，无一条非 retro 历史行。

### P4 · `0013_divergence_propose`
落第一个完整的 expand–prune 实例，用现成的真背离风险：B8 挂账的「lab 融资 → backlog 背离风险」（e_labfund_nbis warning 0.77）。写 3–4 条 candidate_pool 解释候选（口径不可比 / 需求前移透支 / 真泡沫 / 数据滞后），D 用 m.decide 选择当前最可信解释并给 confidence，选中候选生成后续动作（排期行或假设行）。同时 kf055 falsifier 里的证伪条件反向登记为该背离的预置候选。
**验收**：v_divergence 至少 1 行且无 WARN 欠账；candidate_pool 生命周期走通 open→selected；decision_log 出现第一条带 confidence 的 prospective 判断。

### P5 · `0014_thesis_anchor` + 文档收尾
思路层挂载：在合适的 thesis_node 下加 decision_fork（question=「判断要不要一等公民化」，options=[继续散落判断表, decision_registry+decision_log]，chosen=后者，log_ref=JEV-intelligence-graph.md）+ artifact_anchor 若干（三表、三视图、m.decide、本计划文件）——7i 会校验锚点真实存在。README 更新（表清单 + SOP 第 8 步：判断用 m.decide 记）。重建 `gen_schema_doc.py && gen_browser.py`（看板脚本不跑，non-goal 4）。协作日志记一条 E##。
**验收**：schema_browser 思路脉络里能看到这个分叉并点到 decision_registry；checks ERROR=0 收尾。

---

## 六 需要 D 拍板的四个开放问题（P0 门槛）

1. **confidence 怎么写**：甲 = 人按 H/M/L 三档写，映射 .9/.6/.3（与因子锚同一词表，成本最低）；乙 = 直接写 0–1 小数。**B 建议甲**——先有校准数据，再谈精度。
2. **d_direction 记录范围**：甲 = 只记人工改判（directions.py 初判不记，量小信噪高）；乙 = 全记（量大，为未来 shadow 攒全量样本）。**B 建议甲**，等有模型旁跑时再切乙。
3. **escalation 首版怎么定**：没有校准数据前，escalation 只能按 executor 现状照抄（human 类无升级、assisted 类"规则不确定→B"）。是否接受"首版 escalation = 现状描述，数值阈值统一挂 C19 待校准"？**B 建议接受**，避免发明数字。
4. **outcome 回填归谁**：甲 = 并入现有复验节奏（v_review_due 逻辑扩到 decision_log，owner 跟原判断走）；乙 = 每月集中一次由 D 批。**B 建议甲**，不新增仪式。

---

## 七 风险与对策

| 风险 | 对策 |
|---|---|
| 词表未拍板就 seed，返工污染 change_log | P0 总闸；0011 之前 registry 不落库 |
| m.decide 增加登记摩擦，步骤 2 变慢 | 可选增强 + 只记人工判断（Q2 甲案）；observe 主流程零改动 |
| decision_log 与判断表漂移 | checks 一致性规则设 ERROR，不是 WARN |
| 历史回填造假置信度 | retro 标记 + confidence 留空 + 只回填四组有 basis 的 |
| DuckDB 方言限制（FK / ALTER） | 新表自带 PK、target 用文本对（change_log 先例）；不 ALTER 现有表 |
| outcome 长期没人回填，校准成空话 | WARN 缺口规则 + Q4 拍板归属；v_decision_health 让欠账可见 |
| 视图双写漏一边，重放不一致 | P1 验收强制跑一次 init_db --force 重放对账 |

---

**完成定义**：0010–0014 全部应用，checks ERROR=0；registry 10 行、log 有 retro 回填 + 至少 1 条 prospective 带 confidence 的判断、candidate_pool 走通一个完整背离实例；SCHEMA.md / browser / README 同步；步骤 2 填数节奏未被拖慢。此后体系新增的每一次人工判断都在为未来的 decision model 攒校准集——增量三件套即兑现「为基建做设计」。
