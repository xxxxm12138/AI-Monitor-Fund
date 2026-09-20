# -*- coding: utf-8 -*-
"""0009 · NBIS 拆指标 + 合同电力指引序列 + 一处读错纠正 · owner B · 2026-09-20
① 拆：m_nbis_backlog 原来混装「客户承诺 / 预付 / capex / 现金 / 融资事件 / 合同 / 客户名单」，同一 knowledge_date 下抢标题值 → 新建 m_nbis_capex（资本开支，供给猛建的一手量）与 m_nbis_cash（现金与融资）；
   m_nbis_capacity 混装「电力目标 + 站点事件」，事件文本总是压过数值 → 站点 / 短期容量合同事件拆到 m_nbis_sites，capacity 只留合同电力 / 并网电力的数值序列。
② 序列：Q2 股东信图表给出 2026 年底合同电力指引的五次上调：>1 GW（Aug'25）→ >2.5（Nov'25）→ >3（Feb'26）→ >4（May'26）→ 5 GW（Aug'26）；逐版登记，knowledge_time 按月粒度。
③ 纠错：r218 把「3 GW」记成 Q1 版目标；Q1 股东信原文是「合同容量已超 3.5 GW，远超年初 3 GW 目标，上调至 >4 GW」→ r218 被 r255（>4 GW，Q1 版）取代，并补 r254 实际值 >3.5 GW。
④ r012（calltone 里的 capex 指引 20–25B）属量价不属观点 → 由 m_nbis_capex 下的 r256 取代。"""
OWNER = 'B'
SHL_Q2 = 'Nebius Q2 2026 Shareholder Letter https://assets.nebius.com/assets/a6ecfd85-a6cb-4967-8ef7-9a25bd261f9c/SHLQ226.pdf'
SHL_Q1 = 'Nebius Q1 2026 Shareholder Letter https://assets.nebius.com/assets/aa1bc2e6-df83-40cd-a6a2-95e7cda3d16c/Nebius%20SHL_Q1%202026.pdf'
S2, S1 = 'snap_nebius_shl_q2_2026', 'snap_nebius_shl_q1_2026'
SRC = '["src_nebius_q2_2026_shareholder_letter","src_nebius_q1_2026_shareholder_letter"]'
def up(m):
    # ---- 新指标 ----
    m.insert('metric_registry', dict(metric_id='m_nbis_capex', name='NBIS 资本开支', entity_id='ent_nbis', ticker_or_entity='NBIS', entry='持仓', track='neocloud', layer='L2', dim='D1', data_class='1', signal_role='predictor',
        source_ids=SRC, source_family='Nebius SHL（P1）', frequency='季', lead_time_est='1–2 季（capex → 上架容量 → 收入）', kou_jing='季度资本开支（GPU 及相关硬件 + 数据中心建设），SHL 口径；年度指引另记；50–60% 由客户预付自筹', unit='USD B', owner='A', upstream_deps='[]',
        availability='🟢', next_release='2026-11-10（估计）', next_release_basis='估计（P3）', status='testing', fill_status='已填', notes_assumption_ids='从 m_nbis_backlog 拆出；供给猛建的一手量，对账节点 m_reconcile_nbis 的供给侧输入', last_validated='2026-09-20'), basis='一个指标一种量')
    m.insert('metric_registry', dict(metric_id='m_nbis_cash', name='NBIS 现金与融资', entity_id='ent_nbis', ticker_or_entity='NBIS', entry='持仓', track='neocloud', layer='L2', dim='D3', data_class='1', signal_role='expectation_base',
        source_ids=SRC, source_family='Nebius SHL（P1）', frequency='季', lead_time_est='—', kou_jing='期末现金（含短期投资）；融资事件（担保债 / ATM / 可转债）逐条记；循环融资判断在 D3 节点', unit='USD B', owner='A', upstream_deps='[]',
        availability='🟢', next_release='2026-11-10（估计）', next_release_basis='估计（P3）', status='testing', fill_status='已填', notes_assumption_ids='从 m_nbis_backlog 拆出', last_validated='2026-09-20'), basis='一个指标一种量')
    m.insert('metric_registry', dict(metric_id='m_nbis_sites', name='NBIS 站点与容量合同事件', entity_id='ent_nbis', ticker_or_entity='NBIS', entry='持仓', track='neocloud', layer='L2', dim='D1', data_class='2', signal_role='predictor',
        source_ids=SRC, source_family='Nebius SHL（P1）', frequency='事件', lead_time_est='2–4 季（站点 → 上架）', kou_jing='事件：新增合同站点、自有 AI factory、短期容量合同、容量拍卖；数值型电力目标见 m_nbis_capacity', unit='—', owner='B', upstream_deps='[]',
        availability='🟢', next_release='事件驱动', next_release_basis='待定', status='testing', fill_status='已填', notes_assumption_ids='从 m_nbis_capacity 拆出（事件文本不再压过数值标题）', last_validated='2026-09-20'), basis='一个指标一种量')
    for mid, l in (('m_nbis_capex', 0.6), ('m_nbis_cash', 0.3), ('m_nbis_sites', 0.6)):
        m.sql(f"INSERT INTO metric_entity VALUES ('{mid}','ent_nbis')", basis='指标挂实体')
        m.insert('metric_factor', dict(metric_id=mid, r=0.9, e=0.3, l=l, s=(0.6 if mid == 'm_nbis_sites' else 0.9), phi=0.6, rationale='规则默认：r←P1；e=L 全公开；l capex / 站点领先上架 = M，现金 = L；s 结构化 = H、事件 = M；φ=M', owner='B', status='draft'), basis='factors.py 规则')
    # ---- 记录挪到对应量的指标 ----
    for rid, mid, tbl in (('r204', 'm_nbis_capex', 'fct_quant'), ('r217', 'm_nbis_capex', 'fct_quant'), ('r205', 'm_nbis_cash', 'fct_quant'), ('r206', 'm_nbis_cash', 'fct_event'), ('r209', 'm_nbis_sites', 'fct_event'), ('r211', 'm_nbis_sites', 'fct_event')):
        m.set('stg_observation', rid, 'metric_id', mid, basis='拆指标'); m.set(tbl, rid, 'metric_id', mid, basis='拆指标')
    # ---- capex 指引：从观点表移到量价（新记录取代 r012）----
    m.observe('r256', 'm_nbis_capex', 'NBIS', 'guidance', '20–25', 'USD B', 'FY2026', '2026-08-12', SHL_Q2, 'P1', note='取代 r012（原挂在 calltone / 观点表）；“We expect capex for the full year 2026 to be in the range of $20 to $25 billion”')
    m.supersede('r012', 'r256', reason='capex 指引是量价不是观点；原挂错表')
    # ---- 合同电力：实际值 + 指引序列 + 读错纠正（先把指标改成量价类，新记录才路由到 fct_quant）----
    m.set('metric_registry', 'm_nbis_capacity', 'data_class', '1', basis='拆后只剩数值序列'); m.set('metric_registry', 'm_nbis_capacity', 'unit', 'GW', basis='记录单位')
    m.observe('r254', 'm_nbis_capacity', 'NBIS', 'actual', '>3.5', 'GW 合同电力（contracted power）', '2026-05', '2026-05-13', SHL_Q1, 'P1', note='“Contracted capacity already exceeds 3.5 GW, far surpassing the goal of 3 GW we set for the end of the year”')
    m.observe('r255', 'm_nbis_capacity', 'NBIS', 'guidance', '>4', 'GW 合同电力（contracted power）', '2026 年底', '2026-05-13', SHL_Q1, 'P1', note='Q1 版指引（取代 r218 的误读）；“raise our contracted power guidance to more than 4 GW by year-end”')
    m.supersede('r218', 'r255', reason='读错：3 GW 是 Feb 版目标且已被超越，Q1 版指引为 >4 GW')
    m.observe('r257', 'm_nbis_capacity', 'NBIS', 'guidance', '>1', 'GW 合同电力（contracted power）', '2026 年底', '2025-08', SHL_Q2, 'P1', note='指引序列第 1 版（Aug’25），来自 Q2’26 股东信「2026 contracted power guidance」图表；知悉时间按图表月份，月粒度')
    m.observe('r258', 'm_nbis_capacity', 'NBIS', 'guidance', '>2.5', 'GW 合同电力（contracted power）', '2026 年底', '2025-11', SHL_Q2, 'P1', note='指引序列第 2 版（Nov’25），同上')
    m.observe('r259', 'm_nbis_capacity', 'NBIS', 'guidance', '>3', 'GW 合同电力（contracted power）', '2026 年底', '2026-02', SHL_Q2, 'P1', note='指引序列第 3 版（Feb’26），同上；Q1 信称此为「年初 3 GW 目标」')
    m.set('fct_quant', 'r008', 'revision_flag', 'revised', basis='第 5 版：>4 → 5 GW'); m.set('fct_quant', 'r008', 'note', '指引序列第 5 版（Aug’26）：>1 → >2.5 → >3 → >4 → 5 GW，一年内五次上调；“anticipate ending 2026 with 5 GW of contracted power, up from the +4 GW we indicated last quarter”', basis='序列补全')
    for rid, snap in (('r254', S1), ('r255', S1), ('r256', S2), ('r257', S2), ('r258', S2), ('r259', S2)):
        m.set('fct_quant', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_quant', rid, 'confidence', 1.0, basis='一手')
        if rid in ('r255', 'r257', 'r258', 'r259'): m.set('fct_quant', rid, 'period_start', '2026-01-01', basis='目标期间'); m.set('fct_quant', rid, 'period_end', '2026-12-31', basis='目标期间'); m.set('fct_quant', rid, 'revision_flag', ('initial' if rid == 'r257' else 'revised'), basis='指引序列')
    m.set('fct_quant', 'r256', 'period_start', '2026-01-01', basis='FY2026'); m.set('fct_quant', 'r256', 'period_end', '2026-12-31', basis='FY2026')
    # ---- 口径与边证据同步 ----
    m.set('metric_registry', 'm_nbis_backlog', 'name', 'NBIS 客户承诺 / 预付 / 合同', basis='拆后口径'); m.set('metric_registry', 'm_nbis_backlog', 'kou_jing', '客户承诺（customer commitments，multi-year 合同总额上限，非 GAAP backlog）；客户预付为年度指引；里程碑合同与客户名单为状态记录；capex 见 m_nbis_capex、现金与融资见 m_nbis_cash', basis='拆后口径')
    m.set('metric_registry', 'm_nbis_capacity', 'kou_jing', '合同电力 contracted power（已锁定土地与电力承诺，GW）≠ 并网电力 connected power（可上架，MW）；两口径分别记；年底指引逐版登记（revision_flag），实际值为「已超 X GW」类表述', basis='拆后口径')
    m.set('edge_registry', 'e_backlog_nbis', 'evidence_ids', '["r006","r007","r207","r212"]', basis='库：m_nbis_backlog 拆后全部记录'); m.set('edge_registry', 'e_backlog_nbis', 'evidence', '客户承诺 >$40B（r006）；2026 预付 >$9B（r007）；四笔 >$1B TCV（r207）；点名客户（r212）', basis='同上')
    m.set('edge_registry', 'e_power_nbis', 'evidence_ids', '["r008","r009","r254","r255","r257","r258","r259"]', basis='库：m_nbis_capacity 拆后全部记录'); m.set('edge_registry', 'e_power_nbis', 'evidence', '合同电力实际 >3.5 GW（r254，May’26）；年底指引五次上调 >1 → 5 GW（r257/r258/r259/r255/r008）；并网 800–1000 MW 目标（r009）', basis='同上')
