# -*- coding: utf-8 -*-
"""0007 · 非 AI 持仓退出监测范围：题目是搭建 AI 发展追踪体系，STAA（ICL 晶体）/ SLMT（加密）/ 0679.HK（电镀设备）与 AI 无关，不再采集其经营数据 · owner B · 2026-09-20
她的判断："如果说和 AI 无关的话，那我们这次的题目是搭建 AI 发展的追踪体系，那就不需要找这个数据啊"。
处理原则：不删已采数据（append-only），经营指标标 deprecated 并写明原因，呈现视图与看板不再显示；13F 仓位事实保留（书要加得起来：AI 相关仓 ≈ 91.5%，非 AI ≈ 8.5% 本身是「需求锚」的诚实标注），
STAA 的仓位记录挪到新的仓位专用指标 m_staa_position（与尾仓 m_tail_* 同构）；相关排期与简报标 retired。"""
OWNER = 'B'
WHY = '非 AI 敞口，退出 AI 发展监测范围（E46）；数据保留供审计，不进呈现'
def up(m):
    m.insert('metric_registry', dict(metric_id='m_staa_position', name='STAAR Surgical（ICL，非 AI）13F 仓位', entity_id='ent_staa', ticker_or_entity='STAA', entry='持仓', track='医疗 ICL（非 AI）', layer='L5', dim='—', data_class='—', signal_role='expectation_base',
        source_ids='["src_sec_13f_hr_2026q2_anatole_13f_2023q2_2026q2_1_xl"]', source_family='SEC 13F-HR', frequency='季', lead_time_est='—', kou_jing='13F 申报权重（市值 / 13F 总值）；非 AI 敞口只记仓位不记经营', unit='%', owner='A', upstream_deps='[]',
        availability='🟢', next_release='2026-11-16', next_release_basis='规则推定（季末 + 45 天，13F 2026Q3）', status='testing', fill_status='已填', notes_assumption_ids='out-of-AI-scope；仓位事实保留使书完整', last_validated='2026-09-20'), basis='与尾仓 m_tail_* 同构的仓位专用指标')
    m.sql("INSERT INTO metric_entity VALUES ('m_staa_position','ent_staa')", basis='指标挂实体')
    m.insert('metric_factor', dict(metric_id='m_staa_position', r=0.9, e=0.3, l=0.3, s=0.9, phi=0.6, rationale='仓位事实：r←P1；不参与 AI 侧打分', owner='B', status='draft'), basis='factors.py 规则')
    for rid in ('r238', 'r240'):
        m.set('stg_observation', rid, 'metric_id', 'm_staa_position', basis='仓位记录挪到仓位专用指标'); m.set('fct_position', rid, 'metric_id', 'm_staa_position', basis='同上')
    for mid in ('m_staa_sales', 'm_staa_china', 'm_staa_units', 'm_staa_ni', 'm_staa_event'):
        m.set('metric_registry', mid, 'status', 'deprecated', basis=WHY); m.set('metric_registry', mid, 'fill_status', '退出范围', basis=WHY); m.set('metric_registry', mid, 'last_validated', '2026-09-20', basis=WHY)
    for mid, note in (('m_slmt', 'out-of-AI-scope；仓位事实保留使书完整；不采集经营数据'), ('m_hkex_0679', 'out-of-AI-scope；HKEX DI 仓位事实保留；不采集经营数据；C15 待验证假设保留')):
        m.set('metric_registry', mid, 'notes_assumption_ids', note, basis=WHY); m.set('metric_registry', mid, 'last_validated', '2026-09-20', basis=WHY)
    m.set('calendar', 'c041', 'status', 'retired', basis='STAAR 业绩与 AI 发展无关'); m.set('calendar', 'c026', 'status', 'retired', basis='0679.HK 中期业绩与 AI 发展无关')
    m.set('key_fact', 'kf041', 'status', 'retired', basis='STAAR 业绩简报退出范围')
    m.set('entity_master', 'ent_staa', 'status', 'reviewed', basis='非 AI 持仓，定性已定'); m.set('entity_master', 'ent_slmt', 'status', 'reviewed', basis='同上'); m.set('entity_master', 'ent_0679', 'status', 'reviewed', basis='同上')
