# -*- coding: utf-8 -*-
"""0014 · 决策层挂思路层：两个分叉 + 16 个锚点 · owner B · 2026-09-20
上游：PLAN-decision-layer P5。JEV 读后设计（pipeline/JEV-intelligence-graph.md）落库后，思路层要能回答「为什么长出决策层」——
F3.13（core，挂 N3 数据）：判断怎么留痕；F2.15（detail，挂 N2 分析角度）：背离怎么处理。v_column_origin 反查照常，checks 7i 校验锚点真实存在。"""
import json
OWNER = 'B'
J = lambda *xs: json.dumps(list(xs), ensure_ascii=False)

FORKS = [
  ('F3.13', 'N3', 13, '判断怎么留痕',
   J('判断只留结果在各判断表（方向 / 闸 / tier 散落，无过程账）', '判断一等公民化：decision_registry 登记 I/O 契约 + decision_log 六元组过程账 + candidate_pool 候选池'),
   '判断一等公民化：decision_registry 登记 I/O 契约 + decision_log 六元组过程账 + candidate_pool 候选池',
   'JEV 读后（Computation Specialization：REPRESENT / PROPOSE / PREDICT / SELECT 分算子设计）：R 管指标、E 管边，但体系里数量最大的计算是 SELECT 型判断，只留结果不留过程 = 攒不出校准集。六元组（state / candidates / choice / confidence / basis / outcome）成本 ≈ 0（人本来在判断，多写一档置信度），却让每天的人工判断都为未来的 decision model 攒标注；registry 每行 = 未来一个专用小模型的岗位描述，执行者（人 / 规则 / 模型）成为可替换件。cascade 两端已存在：d_route 是 auto（确定性代码），d_direction 是 assisted（规则初判 + 人改判）。',
   '判断散落 → 第三张登记表 + 过程账；校准闸 = 🟠闸从系数扩到判断（未 validated 禁 assisted/auto）', 'core',
   'pipeline/JEV-intelligence-graph.md §四 · PLAN-decision-layer · migrations/0010–0013'),
  ('F2.15', 'N2', 15, '背离怎么处理',
   J('背离只是预警标签（三态之一，挂账观察）', '背离 = PROPOSE 触发器：先扩张解释候选空间（candidate_pool），再 SELECT（选择必须 D），选中项生成后续动作'),
   '背离 = PROPOSE 触发器：先扩张解释候选空间（candidate_pool），再 SELECT（选择必须 D），选中项生成后续动作',
   'selector 选不出没进候选空间的解释（reranker 排不出 retriever 没召回的文档）。背离出现时真正难的不是在三个按钮里选，而是先提出正确的解释（口径不可比 / 资料过时 / 真泡沫…）——这是全图唯一需要开放式生成的位置，生成被压到图的边缘。kf055.falsifier 的证伪条件反向登记为预置候选，背离真出现时 selector 已有候选可选。首个实例：r166 BIS（doc28 定论 retro 选中）+ r133 循环融资（四候选待 D 选）。',
   '背离 = 标签 → 背离 = 候选扩张指令（R17 + 7 天欠账 WARN）', 'detail',
   'JEV-intelligence-graph §四.3 · migrations/0013 · v_divergence'),
]
ANCHORS = [  # a112 起
  ('F3.13', 'table', 'decision_registry', '第三张登记表：每类判断的 I/O 契约（state_schema 输入 × candidates 输出）与 calib_status 状态机'),
  ('F3.13', 'table', 'decision_log', '六元组过程账：change_log 记改了什么，这张记怎么判断的、多有把握、事后对不对'),
  ('F3.13', 'view', 'v_decision_health', '健康观从「填了多少行」走向 判断吞吐 / 升级率 / 置信度与 outcome 欠账'),
  ('F3.13', 'view', 'v_calibration', '校准曲线的表形式：置信度分桶 vs 命中率，decision model 的验收标准'),
  ('F3.13', 'rule', 'R15', '校准误差公式'),
  ('F3.13', 'rule', 'R16', '升级率公式'),
  ('F3.13', 'assumption', 'C20', '校准闸口径：未 validated 禁 assisted / auto（🟠闸从系数扩到判断）'),
  ('F3.13', 'assumption', 'C21', '置信度三档锚 H/M/L = .9/.6/.3，与 A1 因子锚同词表'),
  ('F3.13', 'assumption', 'C19', '升级阈值占位：数值待 v_calibration 累积，首版 escalation 只作现状描述'),
  ('F3.13', 'migration', '0010_decision_layer_ddl', '三表 DDL + 字典 + R15–R17'),
  ('F3.13', 'migration', '0012_decision_log_backfill', '最小回填：只回填有据可查的四组，retro 行禁编造置信度'),
  ('F3.13', 'file', 'pipeline/JEV-intelligence-graph.md', 'JEV 读后设计立场文：四算子对照 + 三块增量'),
  ('F3.13', 'file', 'pipeline/PLAN-decision-layer.md', '实施计划（P0 拍板记录：四个开放问题均甲案）'),
  ('F2.15', 'table', 'candidate_pool', 'PROPOSE 的落点：候选在选中前不是结论，与 key_fact 分开'),
  ('F2.15', 'view', 'v_divergence', '背离清单：记录级 shock + 票级供需反向，join 候选数暴露欠账'),
  ('F2.15', 'migration', '0013_divergence_propose', '首个 expand–prune 实例：r166 走通 open→selected，r133 四候选待 D'),
]

def up(m):
    for fid, nid, seq, q, opts, chosen, why, ba, w, ref in FORKS:
        m.insert('decision_fork', dict(fork_id=fid, node_id=nid, seq=seq, question=q, options=opts, chosen=chosen,
                 rationale=why, before_after=ba, weight=w, log_ref=ref, owner='B', status='draft'), basis=ref)
    for i, (fid, kind, ref, how) in enumerate(ANCHORS, 112):
        m.insert('artifact_anchor', dict(anchor_id=f'a{i:03d}', fork_id=fid, kind=kind, ref=ref, how=how), basis='思路 ↔ 数据双向锚定（决策层）')
