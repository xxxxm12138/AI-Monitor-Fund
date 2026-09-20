# -*- coding: utf-8 -*-
"""0003 · RBRK 第一轮逐字段填充（registry 口径 / fct 期间与快照 / 上期与旧版指引 / 10-Q 差分 / 事件钉日期 / 边机制与证据 / 来源 / 实体 / 13F 仓位）· owner B · 2026-09-20
一手来源全部走 SEC EDGAR（8-K Ex.99.1 Q2 / Q1 FY27，10-Q Q2 / Q1 FY27 关键业务指标节）+ Rubrik IR / newsroom 稿；每份有 snapshots/ 快照。
新增 18 条记录、1 个新指标（m_rbrk_calltone，对称 m_nbis_calltone）、2 条取代（r026 / r027 原无 URL、日期未钉）。
研究上有意义的三点：① Q2 收入 427.3 vs Q1 版指引 395–397，FY27 三项指引全部上调（revision_flag=revised，旧版指引留为记录）；
② net new Sub-ARR 绝对值 = 10-Q 差分 95.8M（上年 71.2M，+34.6%，与 PR +35% 对上）；③ 未调整 net new Cloud ARR 88.8M 同比 −4%，PR 口径「adjusted +20%」剔除了迁移 —— 口径差异本身是信号。"""
OWNER = 'B'
Q2PR = 'Rubrik 8-K Ex.99.1 Q2 FY27 press release (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1943896/000194389626000055/rubrikinc-991pressrelease7.htm'
Q1PR = 'Rubrik 8-K Ex.99.1 Q1 FY27 press release (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1943896/000194389626000041/rubrikinc-991pressrelease4.htm'
Q2TQ = 'Rubrik 10-Q Q2 FY27 key business metrics (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1943896/000194389626000060/rbrk-20260731.htm'
Q1TQ = 'Rubrik 10-Q Q1 FY27 key business metrics (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1943896/000194389626000047/rbrk-20260430.htm'
IRAI = 'Rubrik IR press release 2026-06-09 Rubrik Now Available as AI Agent https://ir.rubrik.com/news-events/press-releases/news-details/2026/Rubrik-Now-Available-as-AI-Agent/default.aspx'
NRUK = 'Rubrik newsroom press release 2026-07-09 UK investment https://www.rubrik.com/company/newsroom/press-releases/26/rubrik-announces-375-million-uk-investment-and-names-london-as-emea-headquarters'
F13 = 'SEC 13F-HR 2026Q2（Anatole_13F_2023Q2-2026Q2_1.xlsx sheet 01 / 05）'
S_Q2PR, S_Q1PR, S_Q2TQ, S_Q1TQ, S_IRAI, S_NRUK = 'snap_rbrk_8k_ex991_q2_fy27', 'snap_rbrk_8k_ex991_q1_fy27', 'snap_rbrk_10q_q2_fy27_kbm', 'snap_rbrk_10q_q1_fy27_kbm', 'snap_rbrk_ir_pr_2026_06_09_rubrik_ai', 'snap_rbrk_newsroom_2026_07_09_uk_investment'
V = '本轮逐字段核 EDGAR 原文'
TRACK = '数据安全 / AI 治理'

def up(m):
    # ---- 新指标：管理层措辞（对称 m_nbis_calltone；类 3 观点）----
    m.insert('metric_registry', dict(metric_id='m_rbrk_calltone', name='RBRK 管理层措辞（AI 需求叙事）', entity_id='ent_rbrk', ticker_or_entity='RBRK', entry='持仓', track=TRACK, layer='L4', dim='D6', data_class='3', signal_role='arbiter',
        source_ids='["src_rubrik_8_k_ex_99_1_q2_fy27_press_release_sec_edg"]', source_family='Rubrik IR PR / 8-K Ex.99.1 / 电话会', frequency='季', lead_time_est='—',
        kou_jing='管理层表述抽取：AI 需求叙事（前沿模型 = 威胁 + 需求）、agentic 产品节奏、指引措辞；codebook icl-v1', unit='—', owner='B', upstream_deps='[]', availability='🟢',
        next_release='2026-12-03（估计）', next_release_basis='估计（P3）', status='testing', fill_status='已填', notes_assumption_ids='对称 m_nbis_calltone；A11 方向为判断', last_validated='2026-09-20'), basis='NBIS 有 calltone 节点，RBRK 缺；D6 企业 adoption 的管理层叙事需可抽取')
    m.sql("INSERT INTO metric_entity VALUES ('m_rbrk_calltone','ent_rbrk')", basis='指标挂实体')
    m.insert('metric_factor', dict(metric_id='m_rbrk_calltone', r=0.9, e=0.3, l=0.3, s=0.6, phi=0.6, rationale='对称 m_nbis_calltone 规则：r←P1；e=L 全公开；l=L 财报同步；s=M 表述抽取；φ=M 季', owner='B', status='draft'), basis='factors.py 规则')

    # ---- 新增记录 ----
    m.observe('r219', 'm_rbrk_ai_product', 'RBRK', 'event', '推出 Rubrik AI（agentic-first 层，横跨 Rubrik Security Cloud 与 Rubrik Agent Cloud）；同日推出 Rubrik Agent Cloud for Anthropic Claude Code / Claude Cowork；FORWARD 2026 拉斯维加斯', '—', '2026-06-09', '2026-06-09', IRAI, 'P1',
              note='取代 r026（原无 URL、日期未钉）；“today announced the launch of Rubrik AI, which transforms its platform with agentic-first experiences to operate at AI speed”')
    m.observe('r220', 'm_rbrk_ai_product', 'RBRK', 'event', '£375M（$500M）英国五年投资，伦敦设 EMEA 总部；CEO 点名 European data sovereignty 与 safely scale AI', 'USD M', '2026-07-09', '2026-07-09', NRUK, 'P1',
              note='取代 r027（原无 URL、日期未钉）；“plans to invest more than £375 million ($500 million USD) in the UK over the next five years”')
    m.observe('r221', 'm_rbrk_rev', 'RBRK', 'prior', '387.1', 'USD M', 'Q1 FY27（期末 2026-04-30）', '2026-06-04', Q1PR, 'P1',
              note='YoY +39%；“Total revenue was $387.1 million, a 39% increase compared to $278.5 million in the first quarter of fiscal 2026”')
    m.observe('r222', 'm_rbrk_sub_arr', 'RBRK', 'prior', '1.57', 'USD B', '2026-04-30', '2026-06-04', Q1PR, 'P1',
              note='YoY +32%；10-Q 精确值 $1,565,141K；“Subscription ARR was up 32% year-over-year, growing to $1.57 billion as of April 30, 2026”')
    m.observe('r223', 'm_rbrk_cloud_arr', 'RBRK', 'prior', '1.39', 'USD B', '2026-04-30', '2026-06-05', Q1TQ, 'P1',
              note='YoY +43%；10-Q 精确值 $1,393,920K（上年同期 $971,546K）；PR 未单列 Cloud ARR，取 10-Q 关键业务指标表')
    m.observe('r224', 'm_rbrk_fcf', 'RBRK', 'prior', '73.6', 'USD M', 'Q1 FY27（期末 2026-04-30）', '2026-06-04', Q1PR, 'P1',
              note='FCF 利润率 19%；“Free cash flow was $73.6 million, compared to $33.3 million in the first quarter of fiscal 2026”')
    m.observe('r225', 'm_rbrk_rev', 'RBRK', 'guidance', '395–397', 'USD M', 'Q2 FY27（Q1 版指引）', '2026-06-04', Q1PR, 'P1',
              note='预期基准：Q2 实际 427.3 高出指引上沿 7.7%；“Revenue of $395 million to $397 million”')
    m.observe('r226', 'm_rbrk_rev', 'RBRK', 'guidance', '1,638–1,648', 'USD M', 'FY27（Q1 版指引）', '2026-06-04', Q1PR, 'P1',
              note='Q2 上调至 1,685–1,693（r018）；“Revenue of $1,638 million to $1,648 million”')
    m.observe('r227', 'm_rbrk_sub_arr', 'RBRK', 'guidance', '1,854–1,862', 'USD M', 'FY27 末（Q1 版指引）', '2026-06-04', Q1PR, 'P1',
              note='Q2 上调至 1,880–1,885（r020）；“Subscription ARR between $1,854 million and $1,862 million”')
    m.observe('r228', 'm_rbrk_fcf', 'RBRK', 'guidance', '293–303', 'USD M', 'FY27（Q1 版指引）', '2026-06-04', Q1PR, 'P1',
              note='Q2 上调至 323–333（r025）；“Free cash flow of $293 million to $303 million”')
    m.observe('r229', 'm_rbrk_nn_arr', 'RBRK', 'computed', '95.8', 'USD M', 'Q2 FY27', '2026-09-01', Q2TQ, 'P1',
              note='= Sub-ARR 2026-07-31 $1,660,903K − 2026-04-30 $1,565,141K = $95,762K；上年同期 $71,154K → +34.6%，与 PR「net new Subscription ARR up 35%」对上；r022 的绝对值在此')
    m.observe('r230', 'm_rbrk_nn_arr', 'RBRK', 'computed', '71.2', 'USD M', 'Q2 FY26', '2026-09-01', Q2TQ, 'P1',
              note='上年同期 net new Sub-ARR = $1,252,423K − $1,181,269K = $71,154K（10-Q Q2 / Q1 FY27 上年列）')
    m.observe('r231', 'm_rbrk_cloud_arr', 'RBRK', 'computed', '88.8', 'USD M 未调整 net new Cloud ARR', 'Q2 FY27', '2026-09-01', Q2TQ, 'P1',
              note='= $1,482,674K − $1,393,920K；上年同期 $1,064,114K − $971,546K = $92,568K → 未调整口径同比 −4.1%；PR 口径「Adjusted net new Cloud ARR grew 20%」剔除迁移（老客户转云、维护转订阅）。两口径差 = 迁移贡献在缩小，需在电话会追问')
    m.observe('r232', 'm_enterprise_adoption', 'RBRK', 'actual', 'over 119', '% 平均订阅美元净留存（trailing 4Q）', '2026-07-31', '2026-09-01', Q2TQ, 'P1',
              note='2026-04-30 approximately 120%；2025-07-31 over 120% → 微降；“Average subscription dollar-based net retention rate | over 119 | %”')
    m.observe('r233', 'm_enterprise_adoption', 'RBRK', 'actual', '3084', '客户数（Sub-ARR ≥ $100K）', '2026-07-31', '2026-08-27', Q2PR, 'P1',
              note='YoY +23%（上年 2,505）；“Rubrik had 3,084 customers with Subscription ARR of $100,000 or more, up 23% year-over-year”')
    m.observe('r234', 'm_enterprise_adoption', 'RBRK', 'prior', '2946', '客户数（Sub-ARR ≥ $100K）', '2026-04-30', '2026-06-04', Q1PR, 'P1',
              note='YoY +24%；“Rubrik had 2,946 customers with Subscription ARR of $100,000 or more, up 24% year-over-year”')
    m.observe('r235', 'm_rbrk_calltone', 'RBRK 管理层（CEO Bipul Sinha）', 'state', 'Mythos and frontier AI models have fundamentally changed the cybersecurity landscape. This new reality demands not only machine speed cyber recovery but also autonomous runtime AI agent security … We are more confident than ever that we are in the early innings of the AI acceleration opportunity', 'AI 需求叙事', 'Q2 FY27', '2026-08-27', Q2PR, 'P1',
              note='前沿模型被同时定义为威胁与需求；Q1 稿已有「early innings of the AI acceleration opportunity」同句 → 叙事连续；“Mythos and frontier AI models have fundamentally changed the cybersecurity landscape”')
    m.observe('r236', 'm_rbrk_rev', 'RBRK', 'position', '29.80%', '13F 权重', '2026Q2（截止 2026-06-30）', '2026-08-14', F13, 'P1',
              note='市值 $175,753,552；2,189,257 股；新建仓；组合第二大；13F 申报 2026-08-14')
    # ---- 取代：旧事件行不删 ----
    m.supersede('r026', 'r219', reason='原记录来源「新闻 / 公司公告」无 URL、日期 2026-08 未钉；IR 稿钉为 2026-06-09')
    m.supersede('r027', 'r220', reason='原记录来源「新闻 / 公司公告」无 URL、日期 2026-08 未钉；newsroom 稿钉为 2026-07-09')

    # ---- metric_registry：口径 / 单位 / 来源 / 依赖 / 复验日 ----
    SRC_Q = '["src_rubrik_ir_press_release_2026_08_27","src_rubrik_8_k_ex_99_1_q2_fy27_press_release_sec_edg","src_rubrik_8_k_ex_99_1_q1_fy27_press_release_sec_edg"]'
    SRC_TQ = '["src_rubrik_ir_press_release_2026_08_27","src_rubrik_8_k_ex_99_1_q2_fy27_press_release_sec_edg","src_rubrik_10_q_q2_fy27_key_business_metrics_sec_edg","src_rubrik_10_q_q1_fy27_key_business_metrics_sec_edg"]'
    KJ = {
      'm_rbrk_rev': ('GAAP 总收入，含 material rights 收入（Q2 FY27 $4.7M / Q2 FY26 $14.2M，剔除后 +43%）；财年 2 月–次年 1 月，Q2 = 5–7 月', 'USD M', SRC_Q, '[]'),
      'm_rbrk_sub_arr': ('Subscription ARR = 期末活跃订阅按客户 TCV 年化，假设 12 个月内到期合同按原条款续约；含 RSC 套件 / RSC-Private 期限许可 / CDM 订阅 / SaaS 单品；不含永久许可维护（10-Q 定义）', 'USD B', SRC_TQ, '[]'),
      'm_rbrk_cloud_arr': ('Cloud ARR = 云订阅（RSC / RSC-Government + SaaS 单品）年化；不含 RSC-Private 与遗留 CDM；「adjusted net new Cloud ARR」剔除迁移（老客户转托管、维护客户买云订阅）', 'USD B', SRC_TQ, '[]'),
      'm_rbrk_nn_arr': ('Net new Subscription ARR = 本季 Sub-ARR − 上季 Sub-ARR（新 logo + 扩张 − 收缩 − 流失，10-Q 定义）；PR 只给 YoY %，绝对值由 10-Q 差分（r229）', 'USD M', SRC_TQ, '["m_rbrk_sub_arr"]'),
      'm_rbrk_fcf': ('FCF = 经营现金流 − 资本开支（含资本化内部软件），non-GAAP；Q2 FY27 经营现金流 $76.8M', 'USD M', SRC_Q, '[]'),
      'm_rbrk_ai_product': ('事件：AI / agent 产品与战略动作（Rubrik AI、Agent Cloud、投资、并购）；一手 = IR / newsroom 稿，日期取稿件日', '—', '["src_rubrik_ir_press_release_2026_06_09_rubrik_now_av","src_rubrik_newsroom_press_release_2026_07_09_uk_inve","src_rubrik_8_k_ex_99_1_q2_fy27_press_release_sec_edg"]', '[]'),
    }
    for mid, (kj, unit, src, deps) in KJ.items():
        m.set('metric_registry', mid, 'track', TRACK, basis='entity_master.track')
        m.set('metric_registry', mid, 'kou_jing', kj, basis='10-Q / PR 定义')
        m.set('metric_registry', mid, 'unit', unit, basis='记录单位')
        m.set('metric_registry', mid, 'source_ids', src, basis='source_master')
        m.set('metric_registry', mid, 'upstream_deps', deps, basis='计算依赖')
        m.set('metric_registry', mid, 'last_validated', '2026-09-20', basis=V)
    m.set('metric_registry', 'm_rbrk_nn_arr', 'notes_assumption_ids', '绝对值 = 10-Q 差分（r229 / r230）', basis='原「绝对值待回 IR 原文」已解决')
    m.set('metric_registry', 'm_rbrk_ai_product', 'notes_assumption_ids', '已钉：r219 2026-06-09 / r220 2026-07-09', basis='原「事件日期待钉」已解决')

    # ---- fct_quant：期间 / 快照 / 置信 / 锚点 / 同比环比 / 指引修订 ----
    P = {'Q2FY27': ('2026-05-01', '2026-07-31'), 'Q1FY27': ('2026-02-01', '2026-04-30'), 'Q2FY26': ('2025-05-01', '2025-07-31'), 'Q3FY27': ('2026-08-01', '2026-10-31'), 'FY27': ('2026-02-01', '2027-01-31')}
    Q = {  # record → (period key, snapshot, anchor, qoq, yoy, revision_flag)
      'r015': ('Q2FY27', S_Q2PR, 'Total revenue was $427.3 million, a 38% increase compared to $309.9 million in the second quarter of fiscal 2026', 0.1038, None, None),
      'r016': ('Q2FY26', S_Q2PR, 'compared to $309.9 million in the second quarter of fiscal 2026', None, None, None),
      'r017': ('Q3FY27', S_Q2PR, 'Revenue of $429 million to $431 million', None, None, 'initial'),
      'r018': ('FY27', S_Q2PR, 'Revenue of $1,685 million to $1,693 million', None, None, 'revised'),
      'r019': ('Q2FY27', S_Q2PR, 'Subscription ARR grew 33% year-over-year to $1.66 billion as of July 31, 2026', 0.0612, 0.326, None),
      'r020': ('FY27', S_Q2PR, 'Subscription ARR between $1,880 million and $1,885 million', None, None, 'revised'),
      'r021': ('Q2FY27', S_Q2PR, 'Cloud ARR grew 39% year-over-year to $1.48 billion as of July 31, 2026', 0.0637, 0.393, None),
      'r022': ('Q2FY27', S_Q2PR, 'with net new Subscription ARR up 35% year-over-year', None, 0.35, None),
      'r023': ('Q2FY27', S_Q2PR, 'Free cash flow was $65.7 million, compared to $57.5 million in the second quarter of fiscal 2026', -0.1073, 0.143, None),
      'r024': ('Q2FY26', S_Q2PR, 'compared to $57.5 million in the second quarter of fiscal 2026', None, None, None),
      'r025': ('FY27', S_Q2PR, 'Free cash flow of $323 million to $333 million', None, None, 'revised'),
      'r221': ('Q1FY27', S_Q1PR, None, None, 0.39, None), 'r222': ('Q1FY27', S_Q1PR, None, None, 0.32, None), 'r223': ('Q1FY27', S_Q1TQ, 'Cloud ARR | $ | 1,393,920 | $ | 971,546', None, 0.435, None),
      'r224': ('Q1FY27', S_Q1PR, None, None, None, None), 'r225': ('Q2FY27', S_Q1PR, None, None, None, 'initial'), 'r226': ('FY27', S_Q1PR, None, None, None, 'initial'), 'r227': ('FY27', S_Q1PR, None, None, None, 'initial'), 'r228': ('FY27', S_Q1PR, None, None, None, 'initial'),
      'r229': ('Q2FY27', S_Q2TQ, 'Subscription ARR | $ | 1,660,903 | $ | 1,252,423', None, 0.346, None), 'r230': ('Q2FY26', S_Q2TQ, None, None, None, None), 'r231': ('Q2FY27', S_Q2TQ, 'Cloud ARR | $ | 1,482,674 | $ | 1,064,114', None, -0.041, None),
      'r232': ('Q2FY27', S_Q2TQ, None, None, None, None), 'r233': ('Q2FY27', S_Q2PR, None, None, 0.23, None), 'r234': ('Q1FY27', S_Q1PR, None, None, 0.24, None),
    }
    for rid, (pk, snap, anchor, qoq, yoy, rev) in Q.items():
        m.set('fct_quant', rid, 'period_start', P[pk][0], basis='财年 2 月–1 月，期间解析'); m.set('fct_quant', rid, 'period_end', P[pk][1], basis='期间解析')
        m.set('fct_quant', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_quant', rid, 'confidence', 1.0, basis='一手原文，人工核对')
        if anchor: m.set('fct_quant', rid, 'anchor', anchor, basis='原文短引')
        if qoq is not None: m.set('fct_quant', rid, 'qoq', qoq, basis='与 Q1 FY27 同口径（r221 / r222 / r223 / r224）')
        if yoy is not None: m.set('fct_quant', rid, 'yoy', yoy, basis='原文 YoY 或 10-Q 上年列计算')
        if rev: m.set('fct_quant', rid, 'revision_flag', rev, basis='对照 Q1 版指引（r225–r228）：FY27 三项全部上调')
    for rid in ('r229', 'r230', 'r231'):
        m.set('fct_quant', rid, 'conversion_assumption', '期末余额差分：本季 ARR − 上季 ARR；10-Q 千美元 → 百万美元，四舍五入 0.1', basis='10-Q 对 net new 的定义')
        m.set('fct_quant', rid, 'assumption_source', '10-Q「Net new Subscription ARR refers to the difference between Subscription ARR in the reported period and Subscription ARR in the prior quarter」', basis='原文')
    m.set('fct_quant', 'r022', 'note', '绝对值见 r229（10-Q 差分 $95.8M，上年 $71.2M）', basis='原「绝对值待回 IR 原文」已解决')
    m.set('fct_quant', 'r232', 'period_start', None, basis='时点值无期间'); m.set('fct_quant', 'r232', 'period_end', '2026-07-31', basis='as-of')

    # ---- fct_event：新事件的类型 / 金额 / 对手方 / 快照 ----
    m.set('fct_event', 'r219', 'event_type', 'launch', basis='产品发布'); m.set('fct_event', 'r219', 'object_entity', 'Anthropic', basis='Agent Cloud for Claude Code'); m.set('fct_event', 'r219', 'relation', 'partner', basis='—')
    m.set('fct_event', 'r219', 'snapshot_id', S_IRAI, basis='快照'); m.set('fct_event', 'r219', 'confidence', 1.0, basis='一手')
    m.set('fct_event', 'r220', 'event_type', 'investment', basis='对外投资'); m.set('fct_event', 'r220', 'amount', 500, basis='$500M（£375M）'); m.set('fct_event', 'r220', 'currency', 'USD', basis='—'); m.set('fct_event', 'r220', 'amount_type', 'multi_year_cap', basis='五年累计'); m.set('fct_event', 'r220', 'object_entity', 'UK / London EMEA HQ', basis='—')
    m.set('fct_event', 'r220', 'snapshot_id', S_NRUK, basis='快照'); m.set('fct_event', 'r220', 'confidence', 1.0, basis='一手')

    # ---- fct_opinion：codebook 字段 ----
    for c, v, b in (('variable', 'AI 需求叙事', 'codebook icl-v1'), ('direction', 'up', '相对 thesis'), ('strength', 'strong', '「more confident than ever」'), ('level', '2', '—'), ('codebook_version', 'icl-codebook-v1', 'doc22'), ('speaker', 'Bipul Sinha（CEO）', 'PR'), ('speaker_role', 'management', '—'), ('snapshot_id', S_Q2PR, '快照')):
        m.set('fct_opinion', 'r235', c, v, basis=b)

    # ---- 边：机制 / 证据（由库按上游指标生成）/ owner / 复验 ----
    m.set('edge_registry', 'e_adoption_rbrk', 'mechanism', '企业部署 AI agent 前要先备份 / 治理 / 可恢复数据与身份 → Sub-ARR、NRR、≥$100K 客户数是 adoption 的一手读数（本体样本，0 跳）；证伪：Sub-ARR 增速连续两季低于指引节奏或 NRR 转弱', basis='doc25 §四 / kf056 falsifier')
    m.set('edge_registry', 'e_adoption_rbrk', 'evidence_ids', '["r155","r232","r233","r234"]', basis='库：m_enterprise_adoption 全部记录'); m.set('edge_registry', 'e_adoption_rbrk', 'evidence', 'RBRK Sub-ARR $1.66B +33%（r155）；NRR over 119%（r232，微降）；≥$100K 客户 3,084 +23%（r233 / r234）', basis='同上')
    m.set('edge_registry', 'e_challenger_rbrk', 'mechanism', 'AI-native 安全挑战者 / 云厂自带 agent 治理（如云平台原生 guardrails）→ 价格与份额压力；信号多为 PR / 融资传闻，r=L s=L；只做预警', basis='doc25')
    m.set('edge_registry', 'e_challenger_rbrk', 'evidence_ids', '[]', basis='上游 m_new_paradigm 仅占位记录 r154，暂无证据'); m.set('edge_registry', 'e_challenger_rbrk', 'evidence', '待填：上游节点 m_new_paradigm 为占位', basis='诚实标注')
    m.set('edge_registry', 'e_datagov_rbrk', 'mechanism', '版权 / 数据授权诉讼与协议 → 企业数据治理与合规预算 → 数据安全平台需求（2 跳，方向级）；DOJ 支持 fair use 对治理预算偏空', basis='doc25 / kf056 status_line')
    m.set('edge_registry', 'e_datagov_rbrk', 'evidence_ids', '["r110","r111","r112","r113","r114"]', basis='库：m_copyright_lit 全部记录'); m.set('edge_registry', 'e_datagov_rbrk', 'evidence', 'DOJ SOI 主张 fair use（r110）；SJ 动议解封（r111）；Reddit / Wiley 授权收入（r112 / r113）；Meta 内容协议（r114）', basis='同上')
    m.set('edge_registry', 'e_reg_rbrk', 'mechanism', 'AI 监管（EU AI Act / 美各州）与数据主权要求 → 合规与恢复能力预算 → RBRK 顺风（2 跳）；r220 UK 投资稿点名 European data sovereignty 为佐证但属本体事件，不计入上游证据', basis='doc25')
    m.set('edge_registry', 'e_reg_rbrk', 'evidence_ids', '[]', basis='上游 m_ai_regulation 仅占位记录 r170，暂无证据'); m.set('edge_registry', 'e_reg_rbrk', 'evidence', '待填：上游节点 m_ai_regulation 为占位', basis='诚实标注')
    for e in ('e_adoption_rbrk', 'e_challenger_rbrk', 'e_datagov_rbrk', 'e_reg_rbrk'):
        m.set('edge_registry', e, 'owner', 'B', basis='B 初稿 D 复核'); m.set('edge_registry', e, 'last_validated', '2026-09-20', basis=V)

    # ---- 来源：出版方 / 频率 / 可靠性 ----
    for sid, pub, freq, note in (
        ('src_rubrik_ir_press_release_2026_08_27', 'Rubrik, Inc.（IR）', '季', 'P1；与 8-K Ex.99.1 同稿，快照取 EDGAR 版（IR 站 curl 403）'),
        ('src_rubrik_8_k_ex_99_1_q2_fy27_press_release_sec_edg', 'SEC EDGAR / Rubrik, Inc.', '季', 'P1 交易所归档，accession 0001943896-26-000055'),
        ('src_rubrik_8_k_ex_99_1_q1_fy27_press_release_sec_edg', 'SEC EDGAR / Rubrik, Inc.', '季', 'P1 交易所归档，accession 0001943896-26-000041'),
        ('src_rubrik_10_q_q2_fy27_key_business_metrics_sec_edg', 'SEC EDGAR / Rubrik, Inc.', '季', 'P1；关键业务指标表给千美元精度与上年列，可做差分'),
        ('src_rubrik_10_q_q1_fy27_key_business_metrics_sec_edg', 'SEC EDGAR / Rubrik, Inc.', '季', 'P1；同上'),
        ('src_rubrik_ir_press_release_2026_06_09_rubrik_now_av', 'Rubrik, Inc.（IR / Business Wire）', '事件', 'P1 公司稿；浏览器抓取快照'),
        ('src_rubrik_newsroom_press_release_2026_07_09_uk_inve', 'Rubrik, Inc.（newsroom）', '事件', 'P1 公司稿；浏览器抓取快照'),
    ):
        m.set('source_master', sid, 'publisher', pub, basis='来源页'); m.set('source_master', sid, 'frequency', freq, basis='—'); m.set('source_master', sid, 'reliability_note', note, basis='—'); m.set('source_master', sid, 'last_validated', '2026-09-20', basis=V)
    m.set('source_master', 'src_新闻_公司公告', 'verify_status', 'stale', basis='r026 / r027 已被带 URL 的 r219 / r220 取代'); m.set('source_master', 'src_新闻_公司公告', 'reliability_note', '无 URL 的占位来源；其记录已全部被取代', basis='—')

    # ---- 实体 ----
    m.set('entity_master', 'ent_rbrk', 'aliases', 'Rubrik, Inc.; RBRK; NYSE: RBRK; Rubrik Security Cloud (RSC); Rubrik Agent Cloud (RAC)', basis='PR 用名')
