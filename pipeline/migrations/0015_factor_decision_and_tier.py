# -*- coding: utf-8 -*-
"""0015 · 补第 11 类判断 d_factor（因子赋值，含领先性 l）+ decision_registry 加投研分层 research_tier · owner B · 2026-09-20
上游：E50（她的三个追问）。① 领先性是判断但没登记——五因子 r/e/l/s/φ 的赋值一直是 factors.py 规则起草 + 人复核（status=draft），
藏在 metric_factor 里没进 decision_registry；补 d_factor。首批待判实例 = 7 条对账分歧边背后的 6 个节点 × 5 因子 = 30 条
（全部规则默认、draft，正是 reconcile_flag WARN 的根因；D 复核任一因子后 tradable_calc 更新、WARN 可清）。
② registry 加 research_tier（A 直接投研 / B 准入可信 / C 运维流程），让复核与注意力分配按重要性排序。
幂等：research_tier 用 ADD COLUMN IF NOT EXISTS（schema.sql 已含该列→rebuild 时 no-op；live 无该列→ALTER 补）。
d_route 保留（cascade 的 auto 底端，标 C）；两道闸保留分立（doc29 B 筛真伪 / D 判影响）——均见 E50 评估，非本脚本删改。"""
import json
OWNER = 'B'
V2A = {0.9: 'H', 0.6: 'M', 0.3: 'L'}   # 因子值 → 锚（A1：H/M/L = .9/.6/.3）
FACTORS = ['r', 'e', 'l', 's', 'phi']
FNAME = {'r': '可靠性', 'e': '独家性', 'l': '固有领先性', 's': '可观测/信噪', 'phi': '频率适配'}
# 7 条对账分歧边 → 去重后的 6 个 from_metric（首批待判实例）
CONFLICT_METRICS = ['m_800g_shipment', 'm_bench_frontier', 'm_cost_per_token', 'm_dc_power_iea', 'm_export_ctrl_bis', 'm_nbis_capacity']

# 10 类现有判断的投研分层（E50 §3）
TIER = {
  'd_direction': 'A', 'd_regime': 'A', 'd_edge_tier': 'A', 'd_divergence_explain': 'A',   # 直接动 thesis
  'd_falsify_gate': 'B', 'd_impact_gate': 'B', 'd_source_tier': 'B',                       # 决定什么信息进得来、信几分
  'd_route': 'C', 'd_fill_priority': 'C', 'd_calendar_scope': 'C',                          # 运维 / 流程
}

def up(m):
    # ② research_tier 列 + 字典
    m.sql("ALTER TABLE decision_registry ADD COLUMN IF NOT EXISTS research_tier TEXT", basis='E50：投研重要性分层（schema.sql 已含，IF NOT EXISTS 幂等）')
    m.sql("INSERT OR REPLACE INTO schema_doc VALUES ('decision_registry','research_tier','投研重要性分层：A 直接投研判断 / B 准入·可信 / C 运维·流程（决定复核与注意力分配的优先级）','E50',false,NULL)", basis='字典同步')
    for did, tier in TIER.items():
        m.set('decision_registry', did, 'research_tier', tier, basis='E50 §3 投研分层')

    # ① d_factor：第 11 类判断（因子赋值，含领先性 l）
    m.insert('decision_registry', dict(
        decision_id='d_factor', name='节点因子赋值（r/e/l/s/φ）',
        question='这个节点的某个因子（可靠性 / 独家性 / 固有领先性 / 可观测信噪 / 频率适配）该给 H / M / L',
        state_schema='metric_registry（dim / data_class / signal_role / availability / frequency / entry）+ 最佳 provenance；factors.py 规则输入',
        candidates=json.dumps(['H', 'M', 'L'], ensure_ascii=False),
        output_home='metric_factor.r + metric_factor.e + metric_factor.l + metric_factor.s + metric_factor.phi',
        executor_kind='rule', executor='factors.py 规则默认 · OVERRIDE / 人复核',
        freq_est='每节点 5 次（现 82 节点 × 5）', escalation='规则与手写分对账分歧（v_edge_calc.reconcile_flag）→ D 逐因子复核；数值阈值挂 C19',
        calib_status='assisted', assumption_ids='A1,A8', owner='B', status='draft', design_ref='E50 · doc21 §6.1',
        research_tier='A', notes='领先性 l 即此判断的一个因子；补上 E50 抓到的缺口。首批待判 = 7 条对账分歧边背后 6 节点 × 5 因子'),
        basis='E50：领先性是判断但未登记；五因子赋值是反复发生且规则/人常分歧的判断', owner='B')

    # 首批待判实例：6 节点 × 5 因子的当前规则默认值，作 retro 回填（置信度留空——规则默认无当时置信度）
    for mid in CONFLICT_METRICS:
        row = m.con.execute('SELECT r, e, l, s, phi, rationale FROM metric_factor WHERE metric_id=?', [mid]).fetchone()
        vals = dict(zip(FACTORS, row[:5])); why = row[5]
        for f in FACTORS:
            anchor = V2A.get(round(float(vals[f]), 1))
            if anchor is None: raise ValueError(f'{mid}.{f} 值 {vals[f]} 不在 H/M/L 锚点')
            m.decide('d_factor', anchor,
                     f'factors.py 规则默认（{FNAME[f]}）：{why}；该节点在 v_edge_calc 有对账分歧（reconcile_flag），待 D 逐因子复核',
                     target=f'metric_factor:{mid}.{f}',
                     state_anchor={'metric_id': mid, 'factor': f, 'value': float(vals[f]), 'source': 'factors.py 规则默认', 'dispute': 'v_edge_calc.reconcile_flag'},
                     executor_kind='rule', executor='factors.py', retro=True,
                     note='回填：规则默认值即当前判断；D 复核改判时记新 prospective 判断，tradable_calc 随之更新')
