# -*- coding: utf-8 -*-
"""0019 · 尾仓 8 只口径 + 9 条 E2/E3 边机制 + D2 数据供给（版权诉讼 / 数据标注 / 数据枯竭）逐字段填充 · owner B · 2026-09-20
尾仓（SUPX / SNDK / MU / INTC / CIEN / MRVL / POET / AMD）：只填 registry 口径与 fct 期间 / 快照 / 锚点 / 置信，**不扩 KPI**；13 份来源全部重抓存快照（Ciena IR 站 403 → EDGAR 8-K Ex.99.1 同稿）。
边：8 条 e_d1_* + e_anthropic_amd 各写一句机制，evidence_ids 由库按 from_metric 现有可见记录生成；不改 cert_tier / 分数。
D2：m_copyright_lit 5 条中 4 条有 URL 且可抓（DOJ SOI 用已有快照）→ 快照 / 锚点 / 事件字段；r111（TechCrunch / 404 Media，无 URL）不动；m_data_labeling Scale 两条 P1 快照 + 锚点；
m_data_wall 占位 r172 → r500（arXiv:2605.17849，CMU，COLM 2026：预训练进入 data-bound 体制，SynPro 让有限人类数据发挥 3.4–5.2× 有效 token）取代；Epoch AI 2026 无「数据枯竭」主题新稿（查证于 2026-09-20）。
研究上有意义的三点：① 尾仓 KPI 全部 P1 且原文核对无误，但 m_hbm_cowos（SNDK / MU 上游）只有一条定性 P3「紧」——两只存储票的边证据最弱，与其 KPI 强度反差最大；
② AMD 稿原文为「up to 2 gigawatts of MI450 Series GPUs in AMD Helios racks」+ Helios 客户名单含 Anthropic / OpenAI / Meta / Microsoft，e_anthropic_amd 的对手方与规模有一手锚点；
③ D2「数据枯竭」的一手证据形态已从 Epoch 预测（2024）转为 2026 学术界的 data-bound 训练方法论（合成 rephrase / megadoc / 正则化）——「墙」本身不再是新闻，绕墙的方法才是。"""
import json
OWNER = 'B'
V = '本轮逐字段核原文（snapshots/snap_tail_*）'
D = '2026-09-20'
# ---- 快照 ----
S = dict(supx='snap_tail_supx_6k_ex991_2026_06_22', sndk='snap_tail_sndk_8k_ex991_q4_fy26', mu='snap_tail_mu_8k_ex991_q3_fy26', intc='snap_tail_intc_8k_ex991_q2_2026',
         cien='snap_tail_cien_8k_ex991_q3_fy26', mrvl='snap_tail_mrvl_ir_q2_fy27', poet='snap_tail_poet_news_q2_2026', amd='snap_tail_amd_ir_q2_2026',
         reddit='snap_tail_reddit_8k_ex991_q2_2026', wiley='snap_tail_wiley_8k_ex991_q4_fy26', meta='snap_tail_meta_newsroom_2026_03_13',
         scale1='snap_tail_scale_blog_2026_01_22_next_era', scale2='snap_tail_scale_blog_2026_07_30_new_ceo', doj='snap_doj_soi_2026_09_01',
         arxiv='snap_tail_arxiv_2605_17849_synpro_data_bound')
# ---- 来源 id（core.slug 算自现有记录的 source 字符串）----
F13 = 'src_sec_13f_hr_2026q2_xlsx_sheet_01'
SRC = dict(supx=['src_superx_6_k_ex_99_1', 'src_superx_6_k_同上'], sndk=['src_sandisk_8_k_ex_99_1_2026_08_05'], mu=['src_micron_8_k_ex_99_1_2026_06_24'], intc=['src_intel_8_k_2026_07_23'],
           cien=['src_ciena_ir_2026_09_03'], mrvl=['src_marvell_ir_2026_08_27'], poet=['src_poet_新闻稿_2026_08_13'], amd=['src_amd_ir_2026_08_04'])
ARXIV = 'arXiv:2605.17849 Generating Pretraining Tokens from Organic Data for Data-Bound Scaling (Yu & Xiong, CMU, COLM 2026) https://arxiv.org/abs/2605.17849'
SRC_ARXIV = 'src_arxiv_2605_17849_generating_pretraining_tokens_f'

# ---- A. 尾仓 registry：track（D1 子节点）/ 口径 / 单位 ----
TAIL = {  # metric: (D1 子节点 track, 口径, unit)
  'm_tail_supx': ('D1 加速器链 · 服务器 / 整机（中国 AI 服务器）', '仓位 = 13F 权重（2026Q2，sheet 01）；KPI = 6-K 半年报总收入（USD，FY 7 月–6 月，FY26 H1 = 2025-07-01–12-31），全部来自遗留设计装修业务，AI 基础设施板块报告期内无收入（state 记录单列）', 'USD'),
  'm_tail_sndk': ('D1 加速器链 · 存储（NAND）', '仓位 = 13F 权重；KPI = 8-K Ex.99.1 季度总收入（USD B，52/53 周财年，FY26 Q4 期末 2026-07-03）；指引 = 下季收入区间（unit 同）；GM / EPS 只进 note', 'USD B'),
  'm_tail_mu': ('D1 加速器链 · HBM', '仓位 = 13F 权重；KPI = 8-K Ex.99.1 季度总收入（USD B，财年 9 月–8 月，FY26 Q3 期末 2026-05-28）；HBM 单独收入未披露，HBM4 出货进度记 state；指引 = 下季收入中值 ± 区间', 'USD B'),
  'm_tail_intc': ('D1 加速器链 · CPU / 代工', '仓位 = 13F 权重；KPI = 8-K Ex.99.1 季度总净收入（USD B，52/53 周财年，Q2 2026 期末 2026-06-27）；分部（DCAI / Foundry / CCG）只进 note；指引 = 下季收入区间', 'USD B'),
  'm_tail_cien': ('D1 加速器链 · 光互连（DCI / 相干光）', '仓位 = 13F 权重；KPI = 8-K Ex.99.1 季度总收入（USD B，财年 11 月–10 月，FY26 Q3 期末 2026-08-01）；指引 = 下季收入 ± $50M；全年指引进 note', 'USD B'),
  'm_tail_mrvl': ('D1 加速器链 · 定制芯片（ASIC）/ 光 DSP', '仓位 = 13F 权重；KPI = IR 稿数据中心分部净收入（USD M，财年 2 月–1 月，FY27 Q2 期末 2026-08-01；unit 标明分部）；指引 = 下季总净收入 ± 5%（unit 区分）', 'USD M 数据中心收入'),
  'm_tail_poet': ('D1 加速器链 · 光互连（光引擎 / 光互连基板）', '仓位 = 13F 权重；KPI = 公司新闻稿季度 NRE + 产品收入（USD，日历季）；订单事件（PO 金额）另记 event，PO ≠ 收入', 'USD'),
  'm_tail_amd': ('D1 加速器链 · 加速器（GPU）', '仓位 = 13F 权重；KPI = IR 稿数据中心分部收入（USD B，52/53 周财年，Q2 2026 期末 2026-06-27；unit 标明分部）；指引 = 下季总收入 ≈ 中值 ± $300M（unit 区分）；产品 / 合作事件另记', 'USD B 数据中心收入'),
}
# ---- fct_quant：期间 / 快照 / 锚点 ----  (period_start, period_end, period_basis, snap, anchor)
Q = {
  'r045': ('2025-07-01', '2025-12-31', '6-K「six months ended December 31, 2025」', 'supx', 'Revenue increased by $2,094,286, or 283.8%, from $737,981 for the six months ended December 31, 2024 to $2,832,267 for the six months ended December 31, 2025'),
  'r046': ('2024-07-01', '2024-12-31', '同上，上年同期', 'supx', 'from $737,981 for the six months ended December 31, 2024'),
  'r049': ('2026-04-04', '2026-07-03', '8-K 表头 Q3 末 April 3, 2026 / Q4 末 July 3, 2026', 'sndk', 'Fiscal fourth quarter revenue was $8.97 billion, up 51% sequentially'),
  'r050': ('2026-07-04', '2026-10-02', '起 = Q4 末次日（原文）；止 = 52/53 周财历 13 周推定', 'sndk', 'Expect first quarter 2027 revenue to be in the range of $10.30 billion to $10.80 billion'),
  'r052': ('2026-02-27', '2026-05-28', '8-K「ended May 28, 2026」；起 = Q2 末（10-Q 报告期 2026-02-26，EDGAR 元数据）次日', 'mu', 'Revenue of $41.46 billion versus $23.86 billion for the prior quarter and $9.30 billion for the same period last year'),
  'r053': ('2025-11-28', '2026-02-26', 'Q2 FY26 末 = 10-Q mu-20260226 报告期；起 = 美光财历 Q1 末（2025-11-27）次日', 'mu', 'versus $23.86 billion for the prior quarter'),
  'r055': ('2026-05-29', '2026-09-03', '起 = Q3 末次日（原文）；止 = 美光财年末（最接近 8/31 的周四）规则推定，与公司公告 9-30 财报日一致', 'mu', '$50.0 billion ± $1.0 billion'),
  'r057': ('2026-03-29', '2026-06-27', '8-K 表头 Three Months Ended Jun 27, 2026 / Mar 28, 2026', 'intc', 'Second-quarter revenue was $16.1 billion, up 25% year-over-year (YoY)'),
  'r058': ('2026-06-28', '2026-09-26', '起 = Q2 末次日（原文）；止 = 52/53 周财历 13 周推定', 'intc', 'Forecasting third-quarter 2026 revenue of $15.8 billion to $16.8 billion'),
  'r060': ('2026-05-03', '2026-08-01', '8-K「fiscal third quarter ended August 1, 2026」；起 = Q2 末（2026-05-02）次日', 'cien', 'Fiscal third quarter 2026 revenue was $1.67 billion, up 37% year-over-year'),
  'r061': ('2026-08-02', '2026-10-31', '起 = Q3 末次日（原文）；止 = Ciena 财年末 10 月底（规则推定）', 'cien', 'Providing revenue guidance for fiscal fourth quarter 2026 of $1.75 billion plus or minus $50 million'),
  'r063': ('2026-05-03', '2026-08-01', 'IR 稿表头 August 1, 2026 / May 2, 2026', 'mrvl', 'driven by continued strong demand across our Data Center portfolio, where revenue growth accelerated to 46% year over year'),
  'r064': ('2026-08-02', '2026-10-31', '起 = Q2 末次日；止 = 原文「October 31, 2026」', 'mrvl', 'Net revenue is expected to be $3.150 billion +/- 5%'),
  'r066': ('2026-04-01', '2026-06-30', '新闻稿「second quarter ended June 30, 2026」', 'poet', 'Revenue was $569,925, up 13% from the first quarter and 112% from the second quarter of 2025 — the Company’s sixth consecutive quarter of sequential revenue growth'),
  'r069': ('2026-03-29', '2026-06-27', 'IR 稿表头 Three Months Ended June 27, 2026 / March 28, 2026', 'amd', 'Data Center segment revenue was $6.7 billion, up 107% year-over-year, driven by strong demand for AMD EPYC™ processors and AMD Instinct™ GPUs'),
  'r070': ('2026-06-28', '2026-09-26', '起 = Q2 末次日（原文）；止 = 52/53 周财历 13 周推定', 'amd', 'For the third quarter of 2026, AMD expects revenue to be approximately $13 billion, plus or minus $300 million'),
  'r112': ('2026-04-01', '2026-06-30', '8-K「June 30, 2026」日历季', 'reddit', 'Other revenue increased 24% year-over-year to $43 million'),
  'r113': ('2025-05-01', '2026-04-30', '8-K 财年末 April 30, 2026', 'wiley', 'Delivered $49 million of AI revenue (+23%) with recurring revenue rapidly scaling'),
}
# ---- fct_event：快照 / 锚点 / 类型 / 对手方 ----  rid: (snap, anchor, {col: (val, basis)})
E = {
  'r047': ('supx', 'No revenue was generated from the AI infrastructure segment during the reporting period for the six months ended December 31, 2025 amid capacity building and customer development', {'event_date': ('2025-12-31', '报告期末（state 描述的是 FY26 H1）'), 'event_date_text': ('FY26 H1（截至 2025-12-31）', '原文')}),
  'r054': ('mu', 'HBM4, built on 1-beta DRAM technology, is in high-volume shipments for our lead customer\'s platform, and qualification samples have been shipped to multiple end-customers', {'event_type': ('launch', '产品出货 / 认证进度'), 'event_date_text': ('FY26 Q3（截至 2026-05-28）', '原文')}),
  'r067': ('poet', 'Lumilens has placed an initial purchase order with the Company for the manufacturing of POET Optical Interposer-based engines valued at $50 million', {'object_entity': ('Lumilens（$50M 首批 PO）；另一 $2.4M PO 来自未具名既有客户', '原文'), 'relation': ('customer', '—'), 'amount_text': ('$2.4M 新 PO（季后）+ $50M Lumilens 首批 PO；PO ≠ 收入，五年累计「could scale to $500+ million」为前瞻', '原文'), 'is_estimate': (False, '两笔 PO 金额为公司披露；$500M+ 只进 amount_text')}),
  'r071': ('amd', 'Announced a strategic partnership with Anthropic to deploy up to 2 gigawatts of MI450 Series GPUs in AMD Helios racks and a multiyear collaboration to optimize AMD Instinct GPUs and ROCm software development using Claude', {'object_entity': ('Anthropic', '原文'), 'relation': ('customer', '—'), 'amount_text': ('最多 2 GW MI450（金额未披露）；Helios 客户另含 Cirrascale / HUMAIN / Meta / Microsoft / OpenAI / Oracle / Tensorwave / Vultr', '原文')}),
  'r110': ('doj', 'The United States thus has a strong interest in the question whether training AI models on written works constitutes “fair use” under copyright law', {'object_entity': ('S.D.N.Y. 25-md-3143（NYT v. OpenAI / Microsoft MDL）', '文件页眉'), 'relation': ('amicus（Statement of Interest, 28 U.S.C. § 517）', '原文脚注 1'), 'event_date_text': ('Filed 09/01/26', '页眉')}),
  'r114': ('meta', 'Today, we’re pleased to announce that we’re partnering with a variety of outlets – News Corp, Le Figaro, Prisa and Süddeutsche Zeitung', {'object_entity': ('News Corp / Le Figaro / Prisa / Süddeutsche Zeitung', '原文'), 'relation': ('licensor（内容合作，金额未披露）', '原文未披露金额；WSJ 的 $50M/yr 为 P3 只留 note')}),
  'r107': ('scale1', '2025 was Scale’s strongest financial year ever, ending the year with well over $1B in new business, with nearly half of all new bookings coming in Q4 alone', {'event_type': ('other', '经营状态陈述（新签 / 盈利 / 展望），非单一合同'), 'amount_text': ('新签 well over $1B（2025，bookings 非收入）；Department of War 两项合同 nearly $200M；收入绝对值未披露', '原文'), 'object_entity': ('Department of War（两项合同）；Mayo Clinic / BP / Allianz（Q4 新客）', '原文'), 'event_date_text': ('2025 全年（博客 2026-01-22）', '原文')}),
  'r108': ('scale2', 'Scale AI today announced that its Board of Directors has appointed Francis deSouza as Chief Executive Officer, effective August 10, 2026', {'object_entity': ('Francis deSouza（前 Google Cloud COO / Illumina CEO）；接替 interim CEO Jason Droege', '原文'), 'relation': ('personnel', '—'), 'amount_type': (None, '原 range 为误填，人事事件无金额'), 'event_date_text': ('公告 2026-07-30；生效 2026-08-10', '原文')}),
}

def up(m):
    # ===== A. 尾仓 8 只：registry 口径 =====
    for mid, (track, kj, unit) in TAIL.items():
        k = mid.split('_')[-1]
        m.set('metric_registry', mid, 'track', track, basis='D1 加速器链子节点（entity_master.track + 边 notes）')
        m.set('metric_registry', mid, 'kou_jing', kj, basis='原文口径（快照 ' + S[k] + '）')
        m.set('metric_registry', mid, 'unit', unit, basis='KPI 记录单位')
        m.set('metric_registry', mid, 'source_ids', json.dumps([F13] + SRC[k], ensure_ascii=False), basis='core.slug 算自现有记录 source')
        m.set('metric_registry', mid, 'upstream_deps', '[]', basis='无计算依赖')
        m.set('metric_registry', mid, 'last_validated', D, basis=V)
    # ===== A. fct_quant：期间 / 快照 / 锚点 / 置信 =====
    for rid, (ps, pe, pb, sk, anchor) in Q.items():
        m.set('fct_quant', rid, 'period_start', ps, basis=pb); m.set('fct_quant', rid, 'period_end', pe, basis=pb)
        m.set('fct_quant', rid, 'snapshot_id', S[sk], basis='快照'); m.set('fct_quant', rid, 'anchor', anchor, basis='原文短引')
        m.set('fct_quant', rid, 'confidence', 1.0, basis='P1 一手原文，人工核对值一致')
    m.set('fct_quant', 'r063', 'qoq', 0.185, basis='原文表 2,171.5 vs 1,832.7（May 2, 2026）= +18.5%；note 已写 +18%'); m.set('fct_quant', 'r063', 'yoy', 0.46, basis='原文「accelerated to 46% year over year」')
    m.set('fct_quant', 'r049', 'qoq', 0.51, basis='原文「up 51% sequentially」'); m.set('fct_quant', 'r045', 'yoy', 2.838, basis='原文「283.8%」')
    m.set('fct_quant', 'r057', 'yoy', 0.25, basis='原文「up 25% year-over-year」'); m.set('fct_quant', 'r060', 'yoy', 0.37, basis='原文「up 37% year-over-year」')
    m.set('fct_quant', 'r066', 'yoy', 1.12, basis='原文「112% from the second quarter of 2025」'); m.set('fct_quant', 'r066', 'qoq', 0.13, basis='原文「up 13% from the first quarter」')
    m.set('fct_quant', 'r069', 'yoy', 1.07, basis='原文「up 107% year-over-year」'); m.set('fct_quant', 'r112', 'yoy', 0.24, basis='原文「increased 24% year-over-year」'); m.set('fct_quant', 'r113', 'yoy', 0.23, basis='原文「+23%」')
    # ===== A/C. fct_event：快照 / 锚点 / 类型 / 对手方 =====
    for rid, (sk, anchor, cols) in E.items():
        m.set('fct_event', rid, 'snapshot_id', S[sk], basis='快照'); m.set('fct_event', rid, 'anchor', anchor, basis='原文短引'); m.set('fct_event', rid, 'confidence', 1.0, basis='P1 一手原文，人工核对')
        for c, (v, b) in cols.items(): m.set('fct_event', rid, c, v, basis=b)
    # ===== B. 九条边：机制一句 + 证据（库按 from_metric 现有可见记录生成）=====
    MECH = {
      'e_d1_supx': 'NVDA 数据中心收入（GPU 出货代理）↑ → 中国 / 亚太 AI 服务器整机集成需求 → SUPX AI 基础设施板块收入（当前为 0，FY26 H1 全部为遗留业务）；1 跳，票本身尚未验证传导',
      'e_d1_intc': 'GPU 出货 ↑ → 每机架配套 x86 主机 CPU（DCAI）与代工 / 先进封装需求 → INTC DCAI + Foundry 收入；1 跳，但 CPU 附着率与 18A 外部客户是两个独立变量',
      'e_d1_mrvl': 'GPU 出货 ↑ → 超大规模客户定制 ASIC / 光 DSP / 互连配套 → MRVL 数据中心分部收入（Q2 FY27 +46%，Custom 下半年加速）；1 跳',
      'e_d1_amd': 'GPU 出货 ↑（NVDA 代理）→ 加速器总盘子扩张 + 客户多源化 → AMD Instinct / Helios 出货 → 数据中心分部收入；1 跳，同时含 compete 成分（份额 vs 盘子）',
      'e_d1_sndk': 'HBM / CoWoS 紧 → DRAM / NAND 产能与资本开支向 HBM 倾斜、企业级 SSD 随 AI 服务器放量 → NAND 量价齐升 → SNDK 收入与毛利率；1 跳，上游节点目前只有定性 P3',
      'e_d1_mu': 'HBM / CoWoS 紧 → HBM3E/HBM4 供不应求、定价权 → MU 收入与毛利率（HBM 单独收入未披露，以总收入 + HBM4 出货 state 代理）；1 跳',
      'e_d1_cien': '800G+ 光模块出货 ↑ → 数据中心间互连（DCI）与相干光带宽需求 → CIEN 收入与订单；1 跳，上游为 P3/P4 出货估计',
      'e_d1_poet': '800G+ 光模块出货 ↑ → 光引擎 / 光互连基板需求 → POET PO 与 NRE / 产品收入（体量 <$1M/季，PO 领先收入）；1 跳，期权型',
      'e_anthropic_amd': '前沿 lab 大额融资（Anthropic Series H $65B 等）→ lab 资本开支 / 算力采购承诺 → AMD 最多 2 GW MI450 Helios 部署 → AMD 数据中心收入；1 跳，E3 需求边，验证点 = Helios 放量与 Anthropic 部署进度',
    }
    for eid, mech in MECH.items():
        fm = m.con.execute('SELECT from_metric FROM edge_registry WHERE edge_id=?', [eid]).fetchone()[0]
        ids = [r[0] for r in m.con.execute('SELECT record_id FROM v_obs WHERE metric_id=? ORDER BY record_id', [fm]).fetchall()]
        m.set('edge_registry', eid, 'mechanism', mech, basis='doc25 §四 一跳供应边；原文快照')
        if ids:
            m.set('edge_registry', eid, 'evidence_ids', json.dumps(ids), basis=f'库：{fm} 全部可见记录')
            m.set('edge_registry', eid, 'evidence', f'{fm} 现有记录 {"/".join(ids)}；' + m.con.execute('SELECT string_agg(record_id || \' \' || obs_type || \' \' || value || \' \' || COALESCE(unit,\'\') || \'（\' || provenance || \'）\', \'；\' ORDER BY record_id) FROM v_obs WHERE metric_id=?', [fm]).fetchone()[0], basis='同上')
        else:
            m.set('edge_registry', eid, 'evidence_ids', '[]', basis=f'上游 {fm} 名下尚无记录'); m.set('edge_registry', eid, 'evidence', f'上游节点 {fm} 尚无记录', basis='诚实标注')
        m.set('edge_registry', eid, 'owner', 'B', basis='B 初稿 D 复核'); m.set('edge_registry', eid, 'last_validated', D, basis=V)
    # ===== C. D2 数据供给 =====
    # m_data_wall：占位 r172 → r500（2026 arXiv 一手）
    m.observe('r500', 'm_data_wall', '前沿数据', 'state',
              'LLM 预训练进入 data-bound 体制（人类文本远不够 scaling 需求）；SynPro（RL 优化的 rephrase + reformat 合成）在 10% Chinchilla 数据下解锁 3.4–5.2× 有效 token，1.1B / 2B 规模超过等量唯一数据的 oracle；无分布坍塌',
              'x 有效 token（vs 重复）', '2026-05（v1）/ 2026-09-05（v2）', '2026-05-18', ARXIV, 'P1',
              note='取代 r172 占位；COLM 2026；CMU LTI（Zichun Yu, Chenyan Xiong）；“LLM pretraining is shifting from a compute-bound to a data-bound regime, where available human (organic) text falls far short of scaling demands”；Epoch AI 2026 Data Insights 无数据枯竭 / 合成数据主题新稿（查证 2026-09-20，epoch.ai/data-insights）')
    m.supersede('r172', 'r500', reason='r172 为「待填」占位；r500 为 2026 年 arXiv 一手（同题：数据枯竭 → 合成数据）')
    m.set('fct_frontier', 'r500', 'benchmark', 'DCLM-Baseline 子集，400M / 1.1B / 2B 模型，10% Chinchilla-optimal tokens（0.8B / 2.2B / 4B）', basis='摘要')
    m.set('fct_frontier', 'r500', 'score_text', '3.4–5.2× effective tokens of repetition', basis='摘要'); m.set('fct_frontier', 'r500', 'institution', 'Carnegie Mellon University（LTI）', basis='arXiv HTML v2 作者栏')
    m.set('fct_frontier', 'r500', 'authors', '["Zichun Yu","Chenyan Xiong"]', basis='arXiv'); m.set('fct_frontier', 'r500', 'doc_id', 'arXiv:2605.17849', basis='arXiv'); m.set('fct_frontier', 'r500', 'topic_cluster', '数据枯竭 / 合成数据（data-bound pretraining）', basis='—'); m.set('fct_frontier', 'r500', 'method', 'SynPro：RL 优化的 rephrasing + reformatting 生成器（quality / faithfulness / data influence 奖励），随预训练平台期持续更新', basis='摘要')
    m.set('fct_frontier', 'r500', 'source_stance', 'neutral', basis='学术论文，非厂商 PR'); m.set('fct_frontier', 'r500', 'verifiability', 'reproducible', basis='代码开源 github.com/cxcscmu/SynPro；COLM 2026 同行评审；未见第三方复现')
    m.set('fct_frontier', 'r500', 'snapshot_id', S['arxiv'], basis='快照'); m.set('fct_frontier', 'r500', 'anchor', 'SynPro unlocks 3.4--5.2x the effective tokens of repetition, even surpassing the non-data-bound oracle that trains on equivalent unique data at the 1.1B and 2B scales', basis='摘要原文')
    m.set('metric_registry', 'm_data_wall', 'fill_status', '已填', basis='r500'); m.set('metric_registry', 'm_data_wall', 'notes_assumption_ids', 'r172 占位已由 r500 取代；Epoch AI 2026 Data Insights 无本主题新稿（查证 2026-09-20）；2026 同题 arXiv 另有 2603.18534（Stanford，synthetic megadocs 1.80× 数据效率）、2606.06888（Michigan，data-constrained scaling law）可续填；industry_impact 留 D', basis='本轮查证')
    # D2 三个指标 registry 口径
    D2 = {
      'm_copyright_lit': ('D2 数据供给 · 版权诉讼 / 内容授权', '事件流 + 授权收入量：① 诉讼节点（DOJ SOI / SJ 动议 / 裁定 / 和解，event，非裁定要注明）② 内容 / 数据授权协议（event，金额多为未披露）③ 授权收入代理 = Reddit「Other revenue」（季，含数据授权但不单列）与 Wiley「AI revenue」（财年 5 月–4 月，unit 区分）；量价记录不可跨公司相加', 'USD M（授权收入代理）/ —（事件）',
                          '["src_s_d_n_y_25_md_3143_doc_316","src_techcrunch_404_media","src_reddit_8_k_ex_99_1","src_wiley_8_k_ex_99_1","src_meta_newsroom"]'),
      'm_data_labeling': ('D2 数据供给 · 数据标注 / RLHF 数据', '事件 + 状态：Scale 官方博客的 bookings / 盈利 / 合同 / 人事表述（P1，无收入绝对值与估值）；收入绝对值仅有 P3 转引（2024 $1.2B）；Surge 2026 无一手。口径：bookings ≠ revenue，「new business」按公司原话', 'USD B 收入（仅 P3）/ —（事件）',
                          '["src_scale_ai_博客","src_wikipedia_sacra_转引_bloomberg"]'),
      'm_data_wall': ('D2 数据供给 · 数据枯竭 / 合成数据', '前沿记录（类 4）：Epoch AI 数据存量 / 枯竭预测更新 + arXiv / 顶会关于 data-bound 预训练与合成数据有效性的一手论文；score = 论文自报的数据效率倍数（相对重复 / 唯一数据），benchmark 写清模型规模与数据预算；industry_impact 由 D 判', 'x 有效 token / 数据效率倍数',
                      f'["src_arxiv_epoch_ai","{SRC_ARXIV}"]'),
    }
    for mid, (track, kj, unit, src) in D2.items():
        m.set('metric_registry', mid, 'track', track, basis='D2 子节点'); m.set('metric_registry', mid, 'kou_jing', kj, basis='现有记录口径归纳 + 原文快照')
        m.set('metric_registry', mid, 'unit', unit, basis='记录单位'); m.set('metric_registry', mid, 'source_ids', src, basis='core.slug 算自记录 source')
        m.set('metric_registry', mid, 'upstream_deps', '[]', basis='无计算依赖'); m.set('metric_registry', mid, 'last_validated', D, basis=V)
    # ===== D. e_datagov_rbrk：m_copyright_lit 记录未增减，证据不变；只更新复验日 =====
    m.set('edge_registry', 'e_datagov_rbrk', 'last_validated', D, basis='本轮核对 m_copyright_lit 5 条来源（4 条快照 + 锚点；r111 无 URL 未动），记录集未变，evidence_ids 保持')
    # ===== 来源：出版方 / 频率 / 可靠性 =====
    SM = {
      'src_superx_6_k_ex_99_1': ('SEC EDGAR / SuperX AI Technology Ltd', '半年', 'P1 交易所归档（6-K 半年报，accession 0001213900-26-070389）'),
      'src_superx_6_k_同上': ('SEC EDGAR / SuperX AI Technology Ltd', '半年', 'P1；与 src_superx_6_k_ex_99_1 同一文件（登记时写「同上」）'),
      'src_sec_13f_hr_2026q2_xlsx_sheet_01': ('SEC 13F-HR（基金申报，xlsx 整理）', '季', 'P1 交易所归档；权重为 xlsx 计算'),
      'src_sandisk_8_k_ex_99_1_2026_08_05': ('SEC EDGAR / Sandisk Corp', '季', 'P1 交易所归档，accession 0001628280-26-053346'),
      'src_micron_8_k_ex_99_1_2026_06_24': ('SEC EDGAR / Micron Technology', '季', 'P1 交易所归档，accession 0000723125-26-000013'),
      'src_intel_8_k_2026_07_23': ('SEC EDGAR / Intel Corp', '季', 'P1 交易所归档，accession 0000050863-26-000155'),
      'src_ciena_ir_2026_09_03': ('Ciena Corp（IR）', '季', 'P1；IR 站 curl 403，快照取 EDGAR 8-K Ex.99.1 同稿（accession 0001628280-26-060245）'),
      'src_marvell_ir_2026_08_27': ('Marvell Technology（IR）', '季', 'P1 公司稿；IR 站可抓'),
      'src_poet_新闻稿_2026_08_13': ('POET Technologies（公司新闻稿）', '季', 'P1 公司稿；财报正文在 SEDAR+'),
      'src_amd_ir_2026_08_04': ('AMD（IR / GlobeNewswire）', '季', 'P1 公司稿；IR 站可抓'),
      'src_reddit_8_k_ex_99_1': ('SEC EDGAR / Reddit Inc', '季', 'P1 交易所归档；「Other revenue」含数据授权但不单列'),
      'src_wiley_8_k_ex_99_1': ('SEC EDGAR / John Wiley & Sons', '季', 'P1 交易所归档；「AI revenue」为公司自定义口径'),
      'src_meta_newsroom': ('Meta Platforms（Newsroom）', '事件', 'P1 公司稿；协议金额未披露'),
      'src_scale_ai_博客': ('Scale AI（官方博客）', '事件', 'P1 公司博客；只给 bookings / 定性，无收入绝对值'),
      'src_s_d_n_y_25_md_3143_doc_316': ('U.S. DOJ（S.D.N.Y. 25-md-3143 Doc. 316，Reuters 镜像 PDF）', '事件', 'P1 法院文件；本地快照 snap_doj_soi_2026_09_01 已存（pdftotext），PDF 镜像可访问性以快照为准'),
    }
    for sid, (pub, freq, note) in SM.items():
        m.set('source_master', sid, 'publisher', pub, basis='来源页'); m.set('source_master', sid, 'frequency', freq, basis='—'); m.set('source_master', sid, 'reliability_note', note, basis='—'); m.set('source_master', sid, 'last_validated', D, basis=V)
    m.set('source_master', 'src_s_d_n_y_25_md_3143_doc_316', 'verify_status', 'confirmed', basis='快照在库，r110 已挂 snapshot_id')
    m.set('source_master', SRC_ARXIV, 'publisher', 'arXiv（CMU LTI 作者自存）', basis='来源页'); m.set('source_master', SRC_ARXIV, 'frequency', '事件', basis='—')
    m.set('source_master', SRC_ARXIV, 'reliability_note', 'P1 一手论文（COLM 2026）；自报结果，代码开源，未见第三方复现', basis='—'); m.set('source_master', SRC_ARXIV, 'last_validated', D, basis=V)
