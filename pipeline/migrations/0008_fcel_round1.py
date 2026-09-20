# -*- coding: utf-8 -*-
"""0008 · FCEL 第一轮逐字段填充（registry 口径 / 上期与环比 / Fit Energy 380 MW 协议与 $225M 增发钉日期 / 产能目标提级 P4→P1 / 边机制与证据 / 来源）· owner B · 2026-09-20
一手来源全走 SEC EDGAR：8-K Ex.99.1 Q3 / Q2 FY26、Fit Energy 协议稿、增发定价稿；四份快照。财年 11 月–10 月：Q2 = 2–4 月，Q3 = 5–7 月。
研究上有意义的三点：① 收入 33.0 同比 −29% 环比 −7.3%，但 committed + awarded backlog 3.6B（awarded 2.35B 全是 Fit Energy 350 MW 期权，未签约）——「订单 vs 收入」的口径差本身是信号；
② 数据中心供电从「一份 75 MW 预留协议」变成三层：Fit Energy 380 MW 分四期（Phase 0 30 MW 本财年 Q4 交付）· 75 MW 德州预留（对手方未具名）· 10 GW 管线（未签约）；③ 年化产能 37.1 MW → 目标 10 月 100 MW → 2028-06 500 MW，是这条 D7 能源约束代理边的验证点。"""
OWNER = 'B'
Q3 = 'FuelCell Energy 8-K Ex.99.1 Q3 FY26 (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/886128/000110465926104498/fcel-20260902xex99d1.htm'
Q2 = 'FuelCell Energy 8-K Ex.99.1 Q2 FY26 (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/886128/000110465926071181/fcel-20260608xex99d1.htm'
FIT = 'FuelCell Energy 8-K Ex.99.1 2026-06-23 Fit Energy agreement (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/886128/000110465926077042/fcel-20260622xex99d1.htm'
OFF = 'FuelCell Energy 8-K Ex.99.2 2026-07-07 offering pricing (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/886128/000110465926082100/tm2620028d1_ex99-2.htm'
S_Q3, S_Q2, S_FIT, S_OFF = 'snap_fcel_8k_ex991_q3_fy26', 'snap_fcel_8k_ex991_q2_fy26', 'snap_fcel_8k_ex991_2026_06_22_fit_energy', 'snap_fcel_8k_ex992_2026_07_07_offering'
SRC_OLD = 'src_fuelcell_energy_8_k_ex_99_1_2026_09_02'
SRC = {'q3': 'src_fuelcell_energy_8_k_ex_99_1_q3_fy26_sec_edgar', 'q2': 'src_fuelcell_energy_8_k_ex_99_1_q2_fy26_sec_edgar', 'fit': 'src_fuelcell_energy_8_k_ex_99_1_2026_06_23_fit_energ', 'off': 'src_fuelcell_energy_8_k_ex_99_2_2026_07_07_offering_'}
TRACK = '燃料电池 / 数据中心现场供电（D7 能源约束代理）'
V = '本轮逐字段核 EDGAR 原文'

def up(m):
    # ---- 新增记录 ----
    m.observe('r241', 'm_fcel_rev', 'FCEL', 'prior', '35.6', 'USD M', 'Q2 FY26（期末 2026-04-30）', '2026-06-08', Q2, 'P1', note='YoY −5%；“Revenue of $35.6 million, compared to $37.4 million, a decrease of approximately 5%”')
    m.observe('r242', 'm_fcel_backlog', 'FCEL', 'prior', '1.14', 'USD B backlog', '2026-04-30', '2026-06-08', Q2, 'P1', note='YoY −9.9%；Q2 稿尚未区分 committed / awarded；“Backlog of $1.14 billion as of April 30, 2026, compared to $1.26 billion”')
    m.observe('r243', 'm_fcel_backlog', 'FCEL', 'actual', '3.6', 'USD B committed + awarded capacity backlog', '2026-07-31', '2026-09-02', Q3, 'P1', note='= committed 1.30B + awarded 2.35B；awarded 全部来自 Fit Energy 350 MW 期权（未签约）；“The expansion of our Committed and Awarded Capacity Backlog to $3.6 billion”')
    m.observe('r244', 'm_fcel_backlog', 'FCEL', 'actual', '10', 'GW sales pipeline（未签约）', 'Q3 FY26', '2026-09-02', Q3, 'P1', note='Q2 为 4 GW（较 Q1 +267%）；管线 ≠ 订单，PR 脚注明示不代表已签协议；“Sales pipeline in Q3 2026 increased to a total of approximately 10 gigawatts”')
    m.observe('r245', 'm_fcel_backlog', 'FCEL', 'prior', '4', 'GW sales pipeline（未签约）', 'Q2 FY26', '2026-06-08', Q2, 'P1', note='“Sales pipeline in Q2 2026 totals 4 gigawatts (“GW”), a 267% increase from Q1 2026”')
    m.observe('r246', 'm_fcel_dc_ppa', 'FCEL', 'event', 'Fit Energy 战略协议：最多 380 MW 数据中心现场基荷供电，分四期（Phase 0 30 MW 本财年 Q4 交付；Phase 1 100 / 2 125 / 3 125 MW 由 Fit 单方选择行权，按里程碑付款）', 'MW', '2026-06-23', '2026-06-23', FIT, 'P1',
              note='30 MW 进 committed backlog、350 MW 期权进 awarded capacity backlog（$2.4B）；“a strategic agreement for up to 380 megawatts (MW) of clean, baseload on-site power for data centers”')
    m.observe('r247', 'm_fcel_dc_ppa', 'FCEL', 'event', '与 Siemens 签 MOU：Siemens 供电气 BOP，目标支持 100+ MW 商业项目更快更低成本部署', '—', 'Q3 FY26', '2026-09-02', Q3, 'P1', note='“Signed an MOU with Siemens with the goal of supporting faster, lower-cost deployment of 100+ MW commercial projects”')
    m.observe('r248', 'm_fcel_cash', 'FCEL', 'prior', '440.9', 'USD M 现金', '2026-04-30', '2026-06-08', Q2, 'P1', note='含受限现金；“Cash and cash equivalents and restricted cash and cash equivalents totaled $440.9 million as of April 30, 2026”')
    m.observe('r249', 'm_fcel_cash', 'FCEL', 'event', '普通股增发定价：10,714,286 股 @ $21.00，毛募资 $225M（由 $200M 上调）', 'USD M', '2026-07-07', '2026-07-07', OFF, 'P1', note='解释 Q3 末现金 737.3 vs Q2 末 440.9 的跳升；“The gross proceeds to FuelCell Energy from the Offering are expected to be $225 million”')
    m.observe('r250', 'm_fcel_cash', 'FCEL', 'prior', '−78.7', 'USD M 净亏（归属普通股）', 'Q2 FY26', '2026-06-08', Q2, 'P1', note='“Net loss attributable to common stockholders was $(78.7) million in the second quarter of fiscal 2026”')
    m.observe('r251', 'm_fcel_cash', 'FCEL', 'target', 'Adj. EBITDA 转正', '—', 'Q4 FY27', '2026-09-02', Q3, 'P1', note='前提：awarded → committed 转化、交付节奏、降本；“now targeting achieving positive Adjusted EBITDA results in the fourth quarter of fiscal 2027”')
    m.observe('r252', 'm_fcel_rev', 'FCEL', 'actual', '−24.5', 'USD M 毛亏', 'Q3 FY26', '2026-09-02', Q3, 'P1', note='YoY 毛亏扩大 377%（去年 −5.1）：37.1 MW 产能率下固定制造费用未被吸收；“Gross loss of $(24.5) million, compared to $(5.1) million”')
    # ---- 产能目标是公司披露的目标，不是估算：P4 → P1（分类纠正，非取代）----
    for rid in ('r040', 'r041'):
        for t in ('stg_observation', 'fct_quant'):
            m.set(t, rid, 'provenance', 'P1', basis='公司 8-K 明示目标 = 一手（obs_type=target 已表达其为目标而非实际），原标 P4 是把「目标」误当「估算」')
        m.set('fct_quant', rid, 'status', 'pass', basis='一手'); m.set('fct_quant', rid, 'owner', 'B', basis='目标值仍需人判')
    m.set('metric_registry', 'm_fcel_capacity', 'notes_assumption_ids', '目标值 = 公司披露（P1，obs_type target）；100 MW 10 月达成与否是验证点', basis='原「目标值为 P4」已纠正')
    # ---- registry ----
    KJ = {
      'm_fcel_rev': ('GAAP 总收入（产品 / 服务 / 发电 / 先进技术四段）；财年 11 月–10 月；另记毛亏（unit 区分）', 'USD M', f'["{SRC_OLD}","{SRC["q3"]}","{SRC["q2"]}"]', '[]'),
      'm_fcel_backlog': ('三层口径：committed backlog（已签合同，产品 / 服务 / 发电 / 先进技术）· awarded capacity backlog（客户期权，未签约）· sales pipeline（商谈中，不代表协议）；unit 区分', 'USD B', f'["{SRC_OLD}","{SRC["q3"]}","{SRC["q2"]}"]', '[]'),
      'm_fcel_dc_ppa': ('事件：数据中心供电协议 / 预留 / 合作（Fit Energy 380 MW、75 MW 德州预留、Siemens MOU）；对手方、金额、期权结构逐条记；本体 = D7 能源约束的一手交点', '—', f'["{SRC_OLD}","{SRC["q3"]}","{SRC["fit"]}"]', '[]'),
      'm_fcel_capacity': ('Torrington 年化产能率（MW）：当季实际运行率 vs 公司目标（10 月 100 MW、2028-06 500 MW）；目标 obs_type=target', 'MW', f'["{SRC_OLD}","{SRC["q3"]}","{SRC["q2"]}"]', '[]'),
      'm_fcel_cash': ('现金 = 现金 + 等价物 + 受限现金（8-K 口径）；净亏 = 归属普通股净亏损；融资事件与盈利目标另记', 'USD M', f'["{SRC_OLD}","{SRC["q3"]}","{SRC["q2"]}","{SRC["off"]}"]', '[]'),
    }
    for mid, (kj, unit, src, deps) in KJ.items():
        m.set('metric_registry', mid, 'track', TRACK, basis='entity_master.track'); m.set('metric_registry', mid, 'kou_jing', kj, basis='8-K 定义'); m.set('metric_registry', mid, 'unit', unit, basis='记录单位')
        m.set('metric_registry', mid, 'source_ids', src, basis='source_master'); m.set('metric_registry', mid, 'upstream_deps', deps, basis='计算依赖'); m.set('metric_registry', mid, 'last_validated', '2026-09-20', basis=V)
        m.set('metric_registry', mid, 'next_release_basis', '估计（上年 Q4 FY25 结果 12 月中旬发布节奏；IR 页无 upcoming）', basis='规则推定')
    # ---- fct_quant：期间 / 快照 / 置信 / 锚点 / 同比环比 ----
    P = {'Q3FY26': ('2026-05-01', '2026-07-31'), 'Q2FY26': ('2026-02-01', '2026-04-30'), 'Q3FY25': ('2025-05-01', '2025-07-31'), 'FY27Q4': ('2027-08-01', '2027-10-31')}
    Q = {  # rid: (period, snapshot, anchor, qoq, yoy)
      'r034': ('Q3FY26', S_Q3, 'Revenue of $33.0 million, compared to $46.7 million, a decrease of approximately 29%', -0.073, -0.29),
      'r035': ('Q3FY25', S_Q3, 'compared to $46.7 million', None, None),
      'r036': ('Q3FY26', S_Q3, 'Committed Backlog of $1.3 billion as of July 31, 2026, compared to $1.24 billion as of July 31, 2025, an increase of approximately 4.1%', None, 0.041),
      'r037': ('Q3FY26', S_Q3, 'Added $2.4 billion to Awarded Capacity Backlog related to Fit Energy’s option to purchase additional fuel cell systems representing generation capacity of up to 350 MW', None, None),
      'r039': ('Q3FY26', S_Q3, 'reflect the annualized production rate of approximately 37.1 MW at which we operated during the quarter', None, None),
      'r040': ('Q3FY26', S_Q3, 'the goal of achieving its targeted annualized production rate of 100 MW in October 2026', None, None),
      'r041': ('Q3FY26', S_Q3, 'The expansion to 500 MW of annualized manufacturing capacity is scheduled for completion by June 2028', None, None),
      'r042': ('Q3FY26', S_Q3, 'Net loss attributable to common stockholders was $(45.3) million in the third quarter of fiscal 2026, compared to net loss attributable to common stockholders of $(92.5) million', 0.425, 0.51),
      'r043': ('Q3FY26', S_Q3, 'Cash, cash equivalents, restricted cash and restricted cash equivalents totaled $737.3 million', 0.672, None),
      'r241': ('Q2FY26', S_Q2, None, None, -0.05), 'r242': ('Q2FY26', S_Q2, None, None, -0.099), 'r243': ('Q3FY26', S_Q3, None, None, None), 'r244': ('Q3FY26', S_Q3, None, 1.5, None), 'r245': ('Q2FY26', S_Q2, None, 2.67, None),
      'r248': ('Q2FY26', S_Q2, None, None, None), 'r250': ('Q2FY26', S_Q2, None, None, 1.03), 'r252': ('Q3FY26', S_Q3, None, None, 3.77),
    }
    for rid, (pk, snap, anchor, qoq, yoy) in Q.items():
        m.set('fct_quant', rid, 'period_start', P[pk][0], basis='财年 11 月–10 月，期间解析'); m.set('fct_quant', rid, 'period_end', P[pk][1], basis='期间解析')
        m.set('fct_quant', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_quant', rid, 'confidence', 1.0, basis='一手原文，人工核对')
        if anchor: m.set('fct_quant', rid, 'anchor', anchor, basis='原文短引')
        if qoq is not None: m.set('fct_quant', rid, 'qoq', qoq, basis='与 Q2 FY26 同口径（r241 / r248 / r250 / r245）；r042 净亏 qoq = 亏损收窄比例')
        if yoy is not None: m.set('fct_quant', rid, 'yoy', yoy, basis='原文 YoY；r042 为亏损收窄 51%')
    m.set('fct_quant', 'r042', 'unit', 'USD M 净亏（归属普通股）', basis='与 r250 同口径'); m.set('fct_quant', 'r042', 'note', '亏损收窄 51%（去年 −92.5，含减值与重组）；−45.3 = 归属普通股净亏', basis='原「收窄」补全')
    m.set('fct_quant', 'r251', 'period_start', P['FY27Q4'][0], basis='目标期间'); m.set('fct_quant', 'r251', 'period_end', P['FY27Q4'][1], basis='目标期间'); m.set('fct_quant', 'r251', 'snapshot_id', S_Q3, basis='快照'); m.set('fct_quant', 'r251', 'confidence', 1.0, basis='一手')
    # ---- fct_event ----
    m.set('fct_event', 'r038', 'snapshot_id', S_Q3, basis='快照'); m.set('fct_event', 'r038', 'confidence', 1.0, basis='一手'); m.set('fct_event', 'r038', 'event_type', 'contract', basis='容量预留协议（含预付）'); m.set('fct_event', 'r038', 'amount_text', '75 MW（六台 12.5 MW Block）；金额未披露', basis='原文'); m.set('fct_event', 'r038', 'event_date_text', '2026-08/09（Q3 结束后、9-02 披露前）', basis='原文「Subsequent to the third quarter」'); m.set('fct_event', 'r038', 'relation', 'customer', basis='—'); m.set('fct_event', 'r038', 'object_entity', '未具名「a major data center operator」', basis='原文')
    m.set('fct_event', 'r246', 'event_type', 'contract', basis='资本设备采购协议'); m.set('fct_event', 'r246', 'amount', 380, basis='MW 上限'); m.set('fct_event', 'r246', 'amount_type', 'multi_year_cap', basis='四期上限，仅 Phase 0 30 MW 已承诺'); m.set('fct_event', 'r246', 'object_entity', 'Fit Energy USA LP', basis='原文'); m.set('fct_event', 'r246', 'relation', 'customer', basis='—'); m.set('fct_event', 'r246', 'is_estimate', True, basis='350 MW 为期权，未签约'); m.set('fct_event', 'r246', 'snapshot_id', S_FIT, basis='快照'); m.set('fct_event', 'r246', 'confidence', 1.0, basis='一手')
    m.set('fct_event', 'r247', 'event_type', 'other', basis='MOU'); m.set('fct_event', 'r247', 'object_entity', 'Siemens', basis='原文'); m.set('fct_event', 'r247', 'relation', 'partner', basis='—'); m.set('fct_event', 'r247', 'snapshot_id', S_Q3, basis='快照'); m.set('fct_event', 'r247', 'confidence', 1.0, basis='一手')
    m.set('fct_event', 'r249', 'event_type', 'funding', basis='股权融资'); m.set('fct_event', 'r249', 'amount', 225, basis='毛募资'); m.set('fct_event', 'r249', 'currency', 'USD', basis='—'); m.set('fct_event', 'r249', 'amount_type', 'one_time', basis='—'); m.set('fct_event', 'r249', 'snapshot_id', S_OFF, basis='快照'); m.set('fct_event', 'r249', 'confidence', 1.0, basis='一手')
    # ---- 边：机制 / 证据 / owner ----
    m.set('edge_registry', 'e_dcppa_fcel', 'mechanism', '本体 0 跳：数据中心现场供电协议直接进 backlog → 收入；三层验证点 = Fit Phase 0 30 MW 本财年 Q4 交付、75 MW 对手方与金额披露、10 月 100 MW 产能率；证伪见 kf057', basis='doc25 / kf057 falsifier')
    m.set('edge_registry', 'e_dcppa_fcel', 'evidence_ids', '["r038","r246","r247"]', basis='库：m_fcel_dc_ppa 全部记录'); m.set('edge_registry', 'e_dcppa_fcel', 'evidence', 'Fit Energy 380 MW 分四期（r246）；75 MW 德州预留（r038）；Siemens MOU（r247）', basis='同上')
    # 本体边不手写分数：留空，呈现用 v_edge_calc 规则分并标「算」（避免再造一条与规则不一致的手写分）
    m.set('edge_registry', 'e_energy_fcel', 'mechanism', 'D7 能源 / 电网约束（并网排队、输电受限、审批）→ 现场基荷供电方案需求 → 燃料电池订单；2 跳，结构级；上游节点 m_energy_grid 仍为占位', basis='doc25')
    m.set('edge_registry', 'e_energy_fcel', 'evidence_ids', '[]', basis='上游 m_energy_grid 仅占位记录 r169，暂无证据'); m.set('edge_registry', 'e_energy_fcel', 'evidence', '待填：上游节点 m_energy_grid 为占位；FCEL 稿里「reduces dependence on constrained transmission systems, simplifies permitting」是本体侧陈述，不计上游证据', basis='诚实标注')
    m.set('edge_registry', 'e_dcbuild_fcel', 'mechanism', 'D1 算力建设 → 数据中心电力需求（IEA ~1000 TWh 2030）→ 现场供电订单；2 跳，结构 + backlog 真值对账', basis='doc25')
    m.set('edge_registry', 'e_dcbuild_fcel', 'evidence_ids', '["r105","r106"]', basis='库：m_dc_power_iea 全部记录'); m.set('edge_registry', 'e_dcbuild_fcel', 'evidence', 'IEA 数据中心用电 ≈1000 TWh 2030 指引（r105，P2）/ ~460 TWh 2024（r106）', basis='同上')
    for e in ('e_dcppa_fcel', 'e_energy_fcel', 'e_dcbuild_fcel'):
        m.set('edge_registry', e, 'owner', 'B', basis='B 初稿 D 复核'); m.set('edge_registry', e, 'last_validated', '2026-09-20', basis=V)
    # ---- 来源 ----
    for sid, pub, freq, note in (
        (SRC_OLD, 'SEC EDGAR / FuelCell Energy, Inc.', '季', 'P1；与 Q3 FY26 稿同一文件（早期登记用了日期命名）'),
        (SRC['q3'], 'SEC EDGAR / FuelCell Energy, Inc.', '季', 'P1 交易所归档，accession 0001104659-26-104498'),
        (SRC['q2'], 'SEC EDGAR / FuelCell Energy, Inc.', '季', 'P1 交易所归档，accession 0001104659-26-071181'),
        (SRC['fit'], 'SEC EDGAR / FuelCell Energy, Inc.', '事件', 'P1；GLOBE NEWSWIRE 稿随 8-K 归档'),
        (SRC['off'], 'SEC EDGAR / FuelCell Energy, Inc.', '事件', 'P1；增发定价稿'),
    ):
        m.set('source_master', sid, 'publisher', pub, basis='来源页'); m.set('source_master', sid, 'frequency', freq, basis='—'); m.set('source_master', sid, 'reliability_note', note, basis='—'); m.set('source_master', sid, 'last_validated', '2026-09-20', basis=V)
    m.set('source_master', SRC_OLD, 'superseded_by', SRC['q3'], basis='同一文件，归并到按季命名的来源 id')

    # ---- 拆：一个指标一种量（同一 knowledge_date 下「净亏 vs 现金」「committed vs awarded / 管线」抢标题值）----
    m.insert('metric_registry', dict(metric_id='m_fcel_awarded', name='FuelCell awarded capacity backlog / 管线（未签约需求）', entity_id='ent_fcel', ticker_or_entity='FCEL', entry='持仓', track=TRACK, layer='L1', dim='—', data_class='1', signal_role='predictor',
        source_ids=f'["{SRC["q3"]}","{SRC["q2"]}"]', source_family='FuelCell 8-K Ex.99.1', frequency='季', lead_time_est='1–2 季（期权 / 管线 → 签约）', kou_jing='awarded capacity backlog = 客户期权（未签约，Fit Energy 350 MW，$2.35B）；sales pipeline = 商谈中（GW，PR 脚注明示不代表协议）；committed + awarded 合计另记为 computed', unit='USD B', owner='B', upstream_deps='[]',
        availability='🟢', next_release='2026-12 中旬（待定）', next_release_basis='估计（上年 Q4 发布节奏）', status='testing', fill_status='已填', notes_assumption_ids='从 m_fcel_backlog 拆出：签约 vs 未签约必须分开看（合同质量判读 B）', last_validated='2026-09-20'), basis='一个指标一种量；签约与未签约是两种事实')
    m.insert('metric_registry', dict(metric_id='m_fcel_netloss', name='FuelCell 净亏 / 毛亏', entity_id='ent_fcel', ticker_or_entity='FCEL', entry='持仓', track=TRACK, layer='L1', dim='—', data_class='1', signal_role='expectation_base',
        source_ids=f'["{SRC["q3"]}","{SRC["q2"]}"]', source_family='FuelCell 8-K Ex.99.1', frequency='季', lead_time_est='—', kou_jing='净亏 = 归属普通股净亏损；毛亏 = 产品成本在低产能率下未吸收固定费用（unit 区分）；盈利目标记在 m_fcel_cash', unit='USD M', owner='A', upstream_deps='[]',
        availability='🟢', next_release='2026-12 中旬（待定）', next_release_basis='估计（上年 Q4 发布节奏）', status='testing', fill_status='已填', notes_assumption_ids='从 m_fcel_cash 拆出', last_validated='2026-09-20'), basis='一个指标一种量')
    for mid in ('m_fcel_awarded', 'm_fcel_netloss'):
        m.sql(f"INSERT INTO metric_entity VALUES ('{mid}','ent_fcel')", basis='指标挂实体')
        m.insert('metric_factor', dict(metric_id=mid, r=0.9, e=0.3, l=(0.6 if mid == 'm_fcel_awarded' else 0.3), s=0.9, phi=0.6, rationale='规则默认：r←P1；e=L 全公开；l 管线 / 期权领先签约 = M，损益 = L；s=H 结构化财报；φ=M 季', owner='B', status='draft'), basis='factors.py 规则')
    for rid, mid in (('r037', 'm_fcel_awarded'), ('r243', 'm_fcel_awarded'), ('r244', 'm_fcel_awarded'), ('r245', 'm_fcel_awarded'), ('r042', 'm_fcel_netloss'), ('r250', 'm_fcel_netloss'), ('r252', 'm_fcel_netloss')):
        m.set('stg_observation', rid, 'metric_id', mid, basis='拆指标：记录挪到对应量的指标'); m.set('fct_quant', rid, 'metric_id', mid, basis='同上')
    m.set('stg_observation', 'r243', 'obs_type', 'computed', basis='committed + awarded 合计是推导量'); m.set('fct_quant', 'r243', 'obs_type', 'computed', basis='同上')
    for rid, v, u, note in (('r036', 1.296, 'USD B committed backlog', '精确值 $1,296,010K（8-K 表）；产品 108.9 / 服务 263.6 / 发电 915.7 / 先进技术 7.8'), ('r037', 2.35, 'USD B awarded capacity backlog', '精确值 $2,350,250K；全部为 Fit Energy 350 MW 期权（Phase 1–3），未签约')):
        m.set('fct_quant', rid, 'value', v, basis='与上期 / 注册单位同口径（USD B），精确值进 note'); m.set('fct_quant', rid, 'unit', u, basis='同上'); m.set('fct_quant', rid, 'note', note, basis='精确值保留')
        m.set('stg_observation', rid, 'unit', u, basis='同上'); m.set('stg_observation', rid, 'value', str(v), basis='同上（登记层文本值同步）')
    m.set('metric_registry', 'm_fcel_backlog', 'name', 'FuelCell committed backlog（已签约）', basis='拆后只留签约口径')
    m.set('metric_registry', 'm_fcel_backlog', 'kou_jing', 'committed backlog = 已签合同（产品 / 服务 / 发电 / 先进技术四段之和）；未签约的期权与管线见 m_fcel_awarded', basis='拆后口径')
    m.set('metric_registry', 'm_fcel_cash', 'name', 'FuelCell 现金 / 融资 / 盈利目标', basis='拆后：损益见 m_fcel_netloss')
    m.set('metric_registry', 'm_fcel_cash', 'kou_jing', '现金 = 现金 + 等价物 + 受限现金（8-K 口径）；融资事件（增发）与盈利目标（Adj. EBITDA 转正）另记；净亏 / 毛亏见 m_fcel_netloss', basis='拆后口径')
    # ---- 实体 ----
    m.set('entity_master', 'ent_fcel', 'aliases', 'FuelCell Energy, Inc.; FCEL; NASDAQ: FCEL; Torrington 工厂', basis='PR 用名')
