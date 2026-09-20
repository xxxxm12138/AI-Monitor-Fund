# UI 完整规格 · 数据管理者面板(两大类 · 分批)

**日期** 2026-09-20 ｜ **定位** 服务**数据管理者**(先不做研究者版)｜ **组织** 两大类:A 呈现/结论层 · B 过程/管理层 ｜ **原则** 每段落到真实表/字段/视图;路由等设计说明入生成器注释,不上面板;完成度与缺口如实标(卖点)。

**完成度记号** ●●●● 满 / ●●● / ●● / ●(框架有数据无)。**干码 = 落哪个表/视图/列。link = 下钻或外链。**

---

# 第一大类 · A 呈现/结论层(输出:AI 动态 → solid 链 → ticker 结论)

> 上半屏。核心是"**从原数据到 ticker 结论的 solid 链条**"——每一步都可溯源。以 brief 形式呈现。

## A1 · AI 最新动态带(供给侧记分牌,不挂标的)
| 项 | 内容 |
|---|---|
| 内容 | 七维 D1–D7 当前动态读数(训练算力 +5×、开源差距、cost/token、capex、光模块营收、数据供给约束)+ 方向 |
| 干码 | `v_metric_latest`(headline_value/dim)· `v_signal_latest`(direction)· `fct_frontier`(前沿)· knowledge_time |
| link | 点读数 → 源(`source_master`.url / `fct_*`.snapshot_id / anchor) |
| 完成度 | ●●●● |

## A2 · 结论简报卡(核心 · solid 链条:一条 AI 动态 → ticker 结论,五段可溯)
每张卡 = 一条实质结论,链条五段,每段带干码 + link:

| 链段 | 内容 | 干码 | link |
|---|---|---|---|
| ① 源事件 | 是什么 · 何时可知 · **来源等级 P1–P5** · 原文锚点 | `fct_*`(value/knowledge_time/provenance/anchor/snapshot_id)· `source_master`(tier/kind) | 原文 url · 本地快照 |
| ② 筛选 | 可信度验证 + 重要性评估 + 结论(可执行/观察/监测) | `fct_frontier`(verifiability/industry_impact)· `decision_log`(d_falsify_gate/d_impact_gate) | 两闸判断记录 + 复核人 |
| ③ 传导链 | 源 → 机制节点 → ticker,每跳:边类型 E1–E6 · 跳数 · 方向 · 权重 · 验证等级 | `edge_registry`(edge_type/hops/map_path/mechanism/cert_tier/evidence_ids)· `v_edge_calc`(tradable/warning/dominant) | 逐跳证据记录(evidence_ids)· 因子(metric_factor) |
| ④ ticker 结论 | regime(看多确认/中性/过热)· 下一催化剂 · 证伪条件 | `key_fact`(status_line/watch/falsifier)· `v_ticker_map` · `entity_master`(in_book) | 持仓明细 · 排期(calendar) |
| ⑤ 改动史 | 这条结论/链上任一字段改过什么 | `change_log`(表/行/列/改前→改后/依据/owner) | 字段改动史 |
| 完成度 | ●●●(链条可跑;量级 nowcast 待共识/回测数据) | | |

---

# 第二大类 · B 过程/管理层(获取 → 压缩 → 决策 → 结论/KPI 信号 的管线)

> 下半屏。四算子 + 闭环。每板块:**产出 · 干码 · link · 完成度 · 纠错入口(数据管理者)· 演示模式(点开看 schema)**。判断方式(code/human/LLM)与其纠错方式贯穿其中。

## B1 · REPRESENT(获取 + 压缩:把世界压成可计算 state)
| 项 | 规格 |
|---|---|
| 产出 | 四类 fct 302 条 · 元数据层 100% · 源 176(174 有 P 级)· 七维齐 · 两闸填(21/20 of 23) |
| 干码 | `stg_observation` · `fct_quant/event/opinion/frontier`(列:knowledge_time · source_id · anchor · snapshot_id · provenance · owner · confidence · code_score · judge_score · model_version · status)· `source_master`(tier/kind/access/verify_status)· `metric_registry`(dim/data_class/signal_role)· `schema_doc`(字典) |
| link | 每记录 → source_url / snapshot;字段 → schema_doc(为什么这么设);(未来)code_score/model_version → Langfuse trace |
| 完成度 | ●●●●;**缺**:自动分类器仍人工(Claude 当分析师) |
| 纠错入口 | **human**:draft 待复核(317 方向 + 84 因子)· 复验队列 v_review_due(P2 13/P3 21)· supersede 取代 · 钉一手 |
| 演示模式 | 展开四类 fct schema + 元数据层 + **建模原则**(原子事实 vs 推导 / 判断 vs 数据分表 / 可推导作视图)+ 分类器 taxonomy(为什么这样分维/data_class/两闸) |

## B2 · PROPOSE(枚举可能空间:提候选、连因果)
| 项 | 规格 |
|---|---|
| 产出 | edge_registry 36(六类边齐)· 13 一等机制节点 + 36 链 · candidate_pool 10 |
| 干码 | `edge_registry`(from_metric/to_ticker/side/edge_type/hops/map_path/mechanism/cert_tier/evidence_ids)· `candidate_pool`(trigger_ref/kind/candidate_text/status/resolved_by)· `v_divergence` |
| link | 边 → 证据记录;候选 → 触发的背离 + 选中它的判断(decision_log) |
| 完成度 | ●●●;**缺**:只 NBIS 主链机制一等化,其余仍文本;候选池稀 |
| 纠错入口 | **human**:边待定级(36 testing)· 机制/候选人工补 · 证据校验(checks 7e) |
| 演示模式 | 六类边定义(E1–E6)+ 跳数规则(map_path = 中间节点 + 1)+ 候选池生命周期(open→selected/rejected) |

## B3 · PREDICT(预判:方向 / 量级 / 领先期)
| 项 | 规格 |
|---|---|
| 产出 | 方向 173/317 · 领先期 lead_time 仅 10 有值 · 预期基准 40 · 排期 58 |
| 干码 | `observation_direction`(direction ↑↓→!— / note)· `metric_registry`(lead_time_est)· `v_metric_guidance`(expectation_base=Forecast)· `calendar`(next_release/basis) |
| link | 方向 → 依据记录;排期 → calendar 事件 |
| 完成度 | ●●;**缺**:**量级 nowcast 未接**(需共识 + 回测);预期基准都指向未来无可比实测 |
| 纠错入口 | **human**:方向复核(draft)· 钉预期基准 · 补领先期;**code**:方向规则 directions.py |
| 演示模式 | 方向判据(相对 thesis 的 ↑↓→!)+ warning=τ·l·e 公式 + 量级 nowcast 缺口(为什么现在只给方向) |

## B4 · SELECT(打分 / 剪枝 / 守闸)
| 项 | 规格 |
|---|---|
| 产出 | v_edge_calc 36 全算分 · 因子 84 · 系数 16(全登记为假设)· 决策 11 类 92 条 · 两闸 D 复核 |
| 干码 | `v_edge_calc`(tradable_calc=c·r·s·φ / warning_calc=τ·l·e / reconcile_flag / dominant)· `metric_factor`(r/e/l/s/phi)· `coefficient`(值 + 挂 assumption)· `decision_registry`(11 类 · executor_kind · calib_status)· `decision_log`(六元组)· `v_metric_score` · `v_ticker_weight` |
| link | 分数 → 因子 → 系数 → **假设 assumption**;判断 → 依据 + 复核人;对账 → doc28 手写分 |
| 完成度 | ●●●;**缺**:d_factor 7 条对账不一致待复核 |
| 纠错入口 | **code**:对账不一致 7 条(调因子 d_factor / 改系数)· 路由/字典完整性;**human**:两闸/边定级复核 |
| 演示模式 | 打分公式 + 因子锚 H/M/L=.9/.6/.3 + **系数全是假设(只排序,未验证不下注)** + 两闸串联(证伪→影响力) |

## B5 · 闭环(迭代优化 / 自校准)
| 项 | 规格 |
|---|---|
| 产出 | 决策六元组 95 条 · **边级预测校准 d_edge_predict(P1-1 已建)· v_calibration 首批真实数据(3 条已兑现方向预测)** · 假设状态机(25 assumption/3 calibrating/2 validated/7 retired)· 审计 change_log 3,226 + migration 27 |
| 干码 | `decision_log`(confidence / outcome / retro / state_anchor)· `d_edge_predict`(边级预测)· `v_calibration`(置信度分桶 × 命中率:d_edge_predict conf 0.6 · n3 · 命中100% · 误差0.4)· `v_decision_health`(吞吐/升级率/欠账)· `assumption`(status 状态机)· `change_log` / `migration_log` |
| link | 边预测 → outcome 兑现 → 校准曲线;判断 → outcome 回填;假设 → calibrating → validated;每改动 → change_log |
| 完成度 | ●●(0025 补:框架 + 边级校准机制 + 首批真实校准数据 outcome **3/95**;**缺**:样本小、其余判断 outcome 待随复验积累) |
| 纠错/管理入口 | 回填 outcome(43 条 confidence 无 outcome)· 假设升级/退役 · (待建)边级预测记分 |
| 演示模式 | 六元组 schema + 校准视图(结构在,0 行)+ 假设状态机 + "为什么这套会自我校准"(State of AI 记分卡思路) |

---

# 分批建设

- **批次 1 = A 呈现/结论层**(A1 动态带 + A2 结论简报卡 · solid 链条)——最出彩、面向"给谁看结论"。
- **批次 2 = B1 REPRESENT + B2 PROPOSE**(获取+压缩+枚举 · 含纠错工作台 human/code)。
- **批次 3 = B3 PREDICT + B4 SELECT + B5 闭环**(决策+结论+迭代 · 含判断方式占比条 + 校准欠账管理)。

**跨板块常驻**(数据管理者视角):判断方式占比条(code 41%/human 59%/LLM 0%)· 纠错待办计数 · 健康标记(v_health)· checks ERROR/WARN · as-of。

**不上面板**(入注释):路由逻辑 · 内部代号 owner A/B/C/D(改用"数据团队/分析师/自动")· 讨论口语。
