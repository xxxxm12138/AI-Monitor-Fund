# -*- coding: utf-8 -*-
"""0013 · 背离即 PROPOSE：candidate_pool 首批 + 第一个完整 expand–prune 实例 · owner B · 2026-09-20
上游：PLAN-decision-layer P4 · JEV-intelligence-graph §四.3（背离不只是预警标签，是候选空间扩张指令）。
三组候选（PROPOSE，B 提出）：
① record:r133 循环融资（$35B 合约 NVIDIA 兼投资 / 担保 / 供芯）——4 条解释候选，其中 1 条是 new_metric 提案（把 C18 从占位变成可观测指标）。
  选择留给 D（registry：候选生成 = B / llm，选择必须 D）——decision_log 不代录，checks 7n 因已有候选不再 WARN。
② record:r166 BIS 放开（91 FR 1684）——3 条解释候选；其中「作 D7 regime 变量挂 e_export_nbis、方向不下注」在 doc28 实跑时已有定论
  （e_export_nbis T2 事件研究 + kf002/kf003），据此作 retro 选中，走通 open → selected 生命周期。
③ ticker:NBIS 预置候选——kf055.falsifier 的三侧证伪条件反向登记（供需背离真出现时，selector 已有候选可选，不用现想）。
另：v_divergence 排除 deprecated 指标（views.sql 同步；r033 STAA 属退出范围，不再触发背离）+ R17 文本更新 + 一条 prospective 复核判断
（B 权限内：证伪闸 r148 SWE-bench 规则初判复核，第一条带置信度的前瞻判断，assisted 闭环「规则初判 → 人复核」演示）。"""
import json
OWNER = 'B'
D20 = '2026-09-20'

CANDS = [  # cand_id, decision_id, trigger_ref, kind, candidate_text, proposed_by, note
  # ① r133 循环融资
  ('cd_r133_1', 'd_divergence_explain', 'record:r133', 'explanation',
   '行业性资本结构而非 NBIS 特有风险：NVIDIA 兼供应商 / 股东 / 担保方是本轮 AI 基建普遍结构（投 CoreWeave $2B kf004、投 Nebius $2B kf005、OpenAI 轮 $30B kf006 同款）——读作行业杠杆 regime 监测项，不单独降 NBIS 优先级', 'B',
   '若选中：循环融资升格为 D3 维 regime 指标持续跟踪'),
  ('cd_r133_2', 'd_divergence_explain', 'record:r133', 'explanation',
   '收入质量风险：供芯方入股 + 担保构成需求自我印证，backlog $40B 中 NVIDIA 关联结构的部分应剔除后重读需求真实性', 'B',
   '若选中：kf055 需求侧证伪条件需加一条循环融资敞口阈值'),
  ('cd_r133_3', 'd_divergence_explain', 'record:r133', 'explanation',
   '披露口径未明：$35B 合约的担保与供芯条款细节未披露，可能只是 vendor financing 常规条款——等 10-K / 10-Q 关联交易披露再判', 'B',
   '若选中：进日历排期（下次财报日）'),
  ('cd_r133_4', 'd_divergence_explain', 'record:r133', 'new_metric',
   '新指标提案：循环融资敞口比 = NVIDIA 关联承诺 / 总承诺（把 C18 从 placeholder 变成可观测指标，分子口径 = 投资 + 担保 + 供芯绑定合约）', 'B',
   'C18 现值「$2B / 承诺 $40B 待定义」正缺这个口径'),
  # ② r166 BIS 放开
  ('cd_r166_1', 'd_divergence_explain', 'record:r166', 'explanation',
   '供给侧正面读法：对华逐案审查放开扩大 NVIDIA 出货基本盘、缓和供应链，α 落在上游光模块量价（旭创 T1 边）', 'B', None),
  ('cd_r166_2', 'd_divergence_explain', 'record:r166', 'explanation',
   '需求侧偏负读法：中国云厂可直购 H200 级芯片，海外 neocloud 稀缺性溢价边际下降，利空 NBIS 定价', 'B', None),
  ('cd_r166_3', 'd_divergence_explain', 'record:r166', 'explanation',
   '作 D7 regime 变量处理（doc28 定论）：挂 e_export_nbis（T2 事件研究），方向不下注，跟踪 NVDA 中国 DC 收入披露口径与 232 关税落地', 'B',
   'doc28 实跑 + kf002 / kf003 的现行处理'),
  # ③ ticker:NBIS 预置（kf055.falsifier 反向登记；背离真出现时 selector 已有候选）
  ('cd_nbis_1', 'd_divergence_explain', 'ticker:NBIS', 'explanation',
   'AI 侧证伪解释：Epoch 训练算力增速回落 <2×/年、开源与闭源差距归零且前沿档 API 降价 → 训练需求逻辑弱化', 'B', '预置：kf055.falsifier AI 侧'),
  ('cd_nbis_2', 'd_divergence_explain', 'ticker:NBIS', 'explanation',
   '需求侧证伪解释：Reflection 类客户不续签、lab 融资转冷（半年无 $10B 级新轮）→ 需求真实性存疑', 'B', '预置：kf055.falsifier 需求侧'),
  ('cd_nbis_3', 'd_divergence_explain', 'ticker:NBIS', 'explanation',
   '执行侧证伪解释：12-31 并网 <800MW 或 Q3 预付到账明显低于 >$9B 年度指引节奏 → 判断转观察', 'B', '预置：kf055.falsifier 执行侧'),
]

def up(m):
    for cid, did, trig, kind, text, by, note in CANDS:
        m.insert('candidate_pool', dict(cand_id=cid, decision_id=did, trigger_ref=trig, kind=kind, candidate_text=text,
                 proposed_by=by, status='open', created_at=D20, note=note), basis='PROPOSE：JEV-IG §四.3 · PLAN P4；r133/r166 = v_divergence 现欠账，ticker:NBIS = kf055.falsifier 预置')
    # ② 的选择在 doc28 已有定论 → retro 选中 cd_r166_3，走通 open → selected（confidence 留空：当时未记）
    dec = m.decide('d_divergence_explain', 'cd_r166_3',
                   'doc28 实跑定论：BIS 作 D7 regime 变量，e_export_nbis T2 事件研究、方向不下注；kf002（regime 变化简报）/ kf003（法律生效）',
                   target='stg_observation:r166',
                   state_anchor={'record_ids': ['r165', 'r166', 'r167'], 'candidates': ['cd_r166_1', 'cd_r166_2', 'cd_r166_3'], 'as_of': '2026-09-19（doc28）'},
                   executor_kind='human', executor='D', retro=True,
                   note='回填：判断在 doc28 实跑时已做出并过复核，此处补记过程账；候选 1/2 为 B 事后补全的当时备选，留 open 供 regime 复判')
    m.set('candidate_pool', 'cd_r166_3', 'status', 'selected', basis=f'{dec}：doc28 定论')
    m.set('candidate_pool', 'cd_r166_3', 'resolved_by', dec, basis='同上')
    # r133 与 ticker:NBIS 的选择留给 D（registry：选择必须 D，不下放）——候选已备，7n 欠账清零
    # prospective 复核（B 权限内）：证伪闸 r148 SWE-bench Verified 规则初判复核 → 第一条带置信度的前瞻判断
    m.decide('d_falsify_gate', 'stance=neutral; verifiability=third_party_verified',
             'B 复核规则初判：SWE-bench Verified 为独立第三方基准（OpenAI 参与修订但榜单独立运营），中立立场与第三方可验证成立；kf033 同源交叉',
             target='fct_frontier:r148', confidence='H',
             state_anchor={'record_id': 'r148', 'rule_source': '0012 回填的规则初判', 'as_of': D20},
             executor_kind='human', executor='B',
             note='assisted 闭环演示：规则初判（0012 retro）→ 人复核（本条 prospective）；复核结论 = 维持')
