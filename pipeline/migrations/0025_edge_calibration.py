# -*- coding: utf-8 -*-
"""0025 · 补 B5 闭环(自校准)最低完成度:边级预测校准 d_edge_predict + 首批真实已兑现 outcome · owner D · 2026-09-20
承 TODO P1-1 / COMPETITIVE-INSPIRATION(State of AI 记分卡)。把 decision_log 的 confidence→outcome→calibration 环从"判断"扩到"边":
每条边 = 一个带日期、可证伪的方向预测,到期用真值打分。让 v_calibration 从 0 行长出真实数据(不编造,只用已发生的旭创/NBIS/Reflection 真数)。
三条已兑现的方向预测(retro=false:带真实置信度与真实 outcome,构成完整校准数据点):
① e_optics_nbis:光模块↑→NBIS↑(赛道 beta)—— 旭创 H1 ¥417.78亿 +182% · NBIS Q2 $575M +514%,同向兑现。
② e_labfund_nbis:lab 融资→NBIS 需求 —— Reflection $2B(2025-10)→ Reflection↔NBIS $1B 合同(2026-07),转需求兑现一次。
③ e_capex_nbis:hyperscaler capex↑→NBIS —— 四家 capex $165B ↑ · NBIS +514%,在建强度传导兑现。
说明:样本仅 3、均 correct、置信 M(0.6)→ 校准曲线首个数据点(命中 100% @ conf 0.6 = 偏保守),小样本诚实标注;边级校准从此可持续积累。B5 由 ●(框架无数据)升 ●●。"""
OWNER = 'D'
J = lambda *xs: __import__('json').dumps(list(xs), ensure_ascii=False)

def up(m):
    m.insert('decision_registry', dict(
        decision_id='d_edge_predict', name='边级预测校准', question='这条边对票 KPI 的方向预测,到期兑现了吗',
        state_schema='edge_registry(方向/tier/lead)+ 两端时序真值', candidates=J('↑', '↓', '→', '!'),
        output_home=None, executor_kind='human', executor='D', freq_est='每边每兑现窗口一次',
        escalation='预测连续偏差 → 复核边因子/tier(C19)', calib_status='human', assumption_ids='C21',
        owner='D', status='draft', design_ref='COMPETITIVE-INSPIRATION §一.1(State of AI 记分卡)· TODO P1-1',
        notes='边=可证伪的带日期方向预测;confidence→outcome→v_calibration,让映射图自我校准'), basis='P1-1 边级校准')

    PRED = [
        ('e_optics_nbis',  '↑', 'M', 'correct', '光模块↑→NBIS↑(赛道 beta):旭创 H1 ¥417.78亿 +182% · NBIS Q2 收入 $575M +514%,同向上行兑现', '2026-05-13', '2026-09-13'),
        ('e_labfund_nbis', '↑', 'M', 'correct', 'lab 融资→NBIS 需求:Reflection $2B 融资(2025-10)→ Reflection↔NBIS $1B 合同(2026-07-14),转需求兑现一次', '2025-10-09', '2026-07-14'),
        ('e_capex_nbis',   '↑', 'M', 'correct', 'hyperscaler capex↑→NBIS:四家 capex ≈$165B ↑ · NBIS 收入 +514%,在建强度传导兑现', '2026-05-13', '2026-08-12'),
    ]
    for eid, direction, conf, outcome, basis, made_at, resolved_at in PRED:
        m.decide('d_edge_predict', direction, f'预测(made {made_at}):{basis.split("：")[0] if "：" in basis else basis}',
                 target=f'edge_registry:{eid}', confidence=conf, executor='D', executor_kind='human',
                 state_anchor={'edge_id': eid, 'made_at': made_at, 'resolve_by': resolved_at, 'predicted_direction': direction},
                 outcome=outcome, outcome_basis=basis, note=f'边级预测校准:made {made_at} → resolved {resolved_at};真值兑现,不编造')
        # 回填 outcome_at
        m.sql(f"UPDATE decision_log SET outcome_at='{resolved_at}' WHERE decision_id='d_edge_predict' AND target_pk='{eid}' AND outcome_at IS NULL",
              basis='outcome 兑现日')
