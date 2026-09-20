# -*- coding: utf-8 -*-
"""0012 · decision_log 最小回填：四组有据可查的历史判断（全部 retro=true，confidence 留空不编造）· owner B · 2026-09-20
上游：PLAN-decision-layer P3。只回填 basis 可指认的判断，state_anchor 指向既有 record / change_log；此后新判断一律 prospective（m.decide 顺手记）。
四组：① 6 条已打分边的 tier 判断（basis=doc28 §四，anchor=各边 evidence_ids）② 当前 regime=同向（读法「信念」，basis=doc20/28，target=kf055）
③ 8 条前沿证伪闸（如实记：建库规则初判 core.fct_row 第三方基准判定，executor_kind=rule，待 B 复核）④ 0007 的两条排期 retire 判断（basis=change_log 0007）。
纪律：retro 行 confidence 一律空——历史判断没有当时写下的置信度，补写就是编造（P3 验收项）。"""
OWNER = 'B'

EDGES = [  # edge_id, tier, evidence_ids（= state_anchor）, 依据
  ('e_optics_nbis',    'T1', ['r078','r079','r080','r081','r082'], 'doc28 §四：lead-lag / Granger vs hyperscaler capex（NBIS 点少借代理）；13-边总表'),
  ('e_power_nbis',     'T2', ['r008','r009','r254','r255','r257','r258','r259'], 'doc28 §四：结构 + 上电进度真值对账'),
  ('e_labfund_nbis',   'T2', ['r115','r116','r117'], 'doc28 §四：结构 + 真值对账 + 敏感性；Reflection $1B 证一次（R1）'),
  ('e_capability_nbis','T3', ['r142','r143'], 'doc28 §四：方向级，不可回归，只 watchlist'),
  ('e_export_nbis',    'T2', ['r165','r166','r167'], 'doc28 §四：事件研究（BIS 规则 → NVIDIA 中国收入 → 算力供给）'),
  ('e_power_reg_nbis', 'T2', ['r105','r106'], 'doc28 §四：结构（电力约束上电节奏）'),
]
GATES = ['r142','r143','r148','r149','r150','r151','r152','r172']   # 现库 source_stance / verifiability 已填的 8 条（全为规则初判）

def up(m):
    # ① 边 tier（executor = D 定 gold，doc28 实跑时的人工判断）
    for eid, tier, ev, basis in EDGES:
        m.decide('d_edge_tier', tier, basis, target=f'edge_registry:{eid}',
                 state_anchor={'evidence_ids': ev, 'as_of': '2026-09-19（doc28 实跑）'},
                 executor_kind='human', executor='D', retro=True,
                 note='回填：doc28 全链路实跑时的档位判断；当时未记置信度，留空')
    # ② 三态对账：当前 = 同向（读法 = 信念；背离风险挂账 → 0013 起走 candidate_pool）
    m.decide('d_regime', '同向', 'doc20 §五 / doc28 对账：供给端（光模块 / capex / 上电）与需求端（lab 融资转合同）同向；kf055 status_line 同文',
             target='key_fact:kf055',
             state_anchor={'record_ids': ['r078','r115','r116','r008'], 'as_of': '2026-09-19'},
             executor_kind='human', executor='D', retro=True,
             note='回填：三态读法 同向=信念 / 平=观察 / 背离=泡沫预警（doc22 §五）；阈值 C6 占位，此判断为综合裁量')
    # ③ 前沿证伪闸：如实记为建库规则初判（core.fct_row 第三方基准判定），非人工复核
    for rid in GATES:
        m.decide('d_falsify_gate', 'stance=neutral; verifiability=third_party_verified',
                 '建库路由规则：source 命中第三方基准（Epoch / AA / ARC / SWE-bench / LMArena / HF）→ neutral × third_party_verified（core.fct_row）',
                 target=f'fct_frontier:{rid}',
                 state_anchor={'record_id': rid, 'as_of': '0000_bootstrap'},
                 executor_kind='rule', executor='core.fct_row 第三方基准判定', retro=True,
                 note='回填：规则初值，B 未逐条复核；复核改判时记新判断（prospective）')
    # ④ 排期入围：0007 的两条 retire（change_log 有完整依据）
    m.decide('d_calendar_scope', 'retired', 'migration 0007（E46）：STAAR 业绩与 AI 发展无关', target='calendar:c041',
             state_anchor={'change_log': '0007_retire_non_ai', 'as_of': '2026-09-20'},
             executor_kind='human', executor='B 提议 · D 复核', retro=True)
    m.decide('d_calendar_scope', 'retired', 'migration 0007（E46）：0679.HK 中期业绩与 AI 发展无关', target='calendar:c026',
             state_anchor={'change_log': '0007_retire_non_ai', 'as_of': '2026-09-20'},
             executor_kind='human', executor='B 提议 · D 复核', retro=True)
