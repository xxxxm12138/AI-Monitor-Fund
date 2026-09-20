# -*- coding: utf-8 -*-
"""0017 · D3 资本（前沿 lab 融资 / 循环融资 / 一级资金流）第一轮：二手回一手、占位换真值、registry / fct_event / 边字段逐项填 · owner B · 2026-09-20
一手新增：软银官方稿（OpenAI 轮 pre-money $730B、软银 $30B 三期，第二期 2026-07-01 已执行）· Reflection 官方博客（$2B）· Cohere 官方博客（Schwarz €500M Series E 领投意向；2026-09-16 definitive agreement 稿未提融资完成）· Nebius newsroom（NVIDIA $2B）
· NVIDIA 10-Q Q2 FY27（非上市股权净增 $13.1B / 余额 $47.9B；对 OpenAI 俄亥俄租约担保上限 $105B；股权投资承诺 $25B）· SpaceX 10-Q Q2 2026 + x.ai 官方（xAI 2026-02-02 换股并入 SpaceX）· Nebius Q2 SHL 原句（Reflection 多年期协议、四笔 >$1B TCV）。
未拿到：OpenAI 官方页 openai.com/index/accelerating-the-next-phase-ai（curl / WebFetch 均 403，查证于 2026-09-20），$122B @ $852B 仍 P2；Reflection 2026 轮官方稿不存在（reflection.ai/news 只转列 CNBC 视频），保持 P2；Cohere Series E 截至 2026-09-20 无完成公告。
研究上有意义的三点：① OpenAI 轮 pre-money $730B（软银官方）+ $122B = $852B post，与媒体一致，且软银三期打款到 10 月才完，「已融 $122B」≠「已到账」；② NVIDIA 半年非上市股权净增 $31.0B、另承诺 $25B 股权投资 + $105B OpenAI 租约担保，循环融资敞口从「个案」变成 10-Q 可追踪的季度序列；
③ xAI 已于 2026-02-02 并入 SpaceX（同一控制换股，10-Q 未披露作价），xAI 独立融资序列终止，$230–250B 估值仍只有媒体口径；Crunchbase 口径 OpenAI+Anthropic H1 2026 $217B（43%），与库内三 lab ≈$207B 计算值口径不同（不调和，留 D）。"""
OWNER = 'B'
V = '本轮逐字段核官方 / EDGAR 原文（2026-09-20）'
SB0227 = 'SoftBank Group press release 2026-02-27 Follow-on Investments in OpenAI https://group.softbank/en/news/press/20260227'
SB0701 = 'SoftBank Group press release 2026-07-01 Execution of Follow-on Investment (Second Tranche) in OpenAI https://group.softbank/en/news/press/20260701'
RBLOG = 'Reflection AI blog 2025-10-09 Building Frontier Open Intelligence https://reflection.ai/blog/frontier-open-intelligence'
RNEWS = 'Reflection AI news page https://reflection.ai/news'
TCR14 = 'TechCrunch 2026-07-14 Reflection inks $1B compute deal with Nebius https://techcrunch.com/2026/07/14/reflection-inks-1b-compute-deal-with-nebius/'
SHL = 'Nebius Q2 2026 Shareholder Letter https://assets.nebius.com/assets/a6ecfd85-a6cb-4967-8ef7-9a25bd261f9c/SHLQ226.pdf'
CO424 = 'Cohere blog 2026-04-24 Cohere and Aleph Alpha join forces https://cohere.com/blog/cohere-alephalpha-join-forces'
CO916 = 'Cohere newsroom 2026-09-16 Cohere and Aleph Alpha sign agreement https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement'
NVQ2 = 'NVIDIA 10-Q Q2 FY27 (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm'
SPCX = 'SpaceX 10-Q Q2 2026 (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm'
CB = 'Crunchbase News H1 2026 global funding report https://news.crunchbase.com/venture/global-startup-exits-ipo-ma-soar-ai-q2-h1-2026/'
S = dict(sb0227='snap_d3_softbank_pr_2026_02_27_openai_followon', sb0701='snap_d3_softbank_pr_2026_07_01_openai_tranche2', tcoai='snap_d3_techcrunch_2026_03_31_openai_122b',
         rblog='snap_d3_reflection_blog_2025_10_09_frontier_open_intelligence', tcr2b='snap_d3_techcrunch_2025_10_09_reflection_2b', rnews='snap_d3_reflection_news_index_2026_09_20',
         tcr14='snap_d3_techcrunch_2026_07_14_reflection_nebius', shl='snap_nebius_shl_q2_2026', co424='snap_d3_cohere_blog_2026_04_24_aleph_alpha_series_e', co916='snap_d3_cohere_blog_2026_09_16_aleph_alpha_definitive',
         conr='snap_d3_cohere_newsroom_index_2026_09_20', nbnr='snap_d3_nebius_newsroom_2026_03_11_nvidia_partnership', nvq2='snap_d3_nvda_10q_q2fy27_investments_notes', xai='snap_d3_xai_news_2026_02_02_joins_spacex',
         spcx='snap_d3_spcx_10q_q2_2026_xai_merger', cb='snap_d3_crunchbase_news_h1_2026_global_funding')
SRC = dict(sb0227='src_softbank_group_press_release_2026_02_27_follow_o', sb0701='src_softbank_group_press_release_2026_07_01_executio', tc='src_techcrunch', rblog='src_reflection_ai_blog_2025_10_09_building_frontier_',
           rnews='src_reflection_ai_news_page', tcr14='src_techcrunch_2026_07_14_reflection_inks_1b_compute', shl='src_nebius_q2_2026_shareholder_letter', co424='src_cohere_blog_2026_04_24_cohere_and_aleph_alpha_jo',
           co916='src_cohere_newsroom_2026_09_16_cohere_and_aleph_alph', nbnr='src_nebius_newsroom', nvq2='src_nvidia_10_q_q2_fy27_sec_edgar', spcx='src_spacex_10_q_q2_2026_sec_edgar', cb='src_crunchbase_news_h1_2026_global_funding_report',
           anth='src_anthropic_官方', xai='src_xai_官方', nvq1='src_nvidia_10_q', nvnr='src_nvidia_newsroom', cnbc='src_cnbc_视频_reflection_ai_news_转列')
TRACK = '前沿 lab 一级资本 / 循环融资（D3）'

def ev(m, rid, **kw):
    for c, v in kw.items(): m.set('fct_event', rid, c, v, basis=V)

def up(m):
    # ================= 1. m_lab_funding_frontier =================
    m.observe('r400', 'm_lab_funding_frontier', 'OpenAI', 'event', '软银参与 OpenAI 融资轮：追加投资 $30.0B（三期各 $10B：2026-04-01 / 07-01 / 10-01），pre-money $730B；完成后软银累计 $64.6B ≈13%', 'USD B', '2026-02-27', '2026-02-27', SB0227, 'P1',
              note='OpenAI 官方页 403，软银官方稿是本轮唯一可得一手：pre-money $730B + 轮次 $122B = $852B post（与 r122 媒体口径一致）；优先股，IPO 自动转普通股；“to participate in OpenAI’s fundraising round, and to make follow-on investments of USD 30.0 billion (JPY 4,674.3 billion*1) via SoftBank Vision Fund 2”')
    ev(m, 'r400', event_type='funding', amount=30, currency='USD', amount_type='multi_year_cap', object_entity='OpenAI Group PBC', relation='investor（SoftBank Vision Fund 2 → OpenAI）', round='2026 轮（pre-money $730B）', event_date='2026-02-27', snapshot_id=S['sb0227'], confidence=1.0, entity_id='ent_openai')
    m.observe('r401', 'm_lab_funding_frontier', 'OpenAI', 'event', '软银第二期 $10.0B 于 2026-07-01 执行（第一期 04-01 已执行；第三期 $10B 计划 10-01，IPO 可提前）；资金来自 2026-03-27 过桥贷款', 'USD B', '2026-07-01', '2026-07-01', SB0701, 'P1',
              note='2026-06 至 09-19 三家 lab 唯一有一手的资金事件：「已融 $122B」的到账节奏拉到 10 月；“it executed the follow-on investment (second tranche) of USD 10.0 billion (JPY 1,627.3 billion*1) (the “Follow-on Investment”) in OpenAI Group PBC via SoftBank Vision Fund 2”')
    ev(m, 'r401', event_type='funding', amount=10, currency='USD', amount_type='one_time', object_entity='OpenAI Group PBC', relation='investor（tranche 2 of 3）', round='2026 轮（pre-money $730B）', event_date='2026-07-01', snapshot_id=S['sb0701'], confidence=1.0, entity_id='ent_openai')
    m.observe('r402', 'm_lab_funding_frontier', 'xAI', 'state', 'xAI 于 2026-02-02 换股并入 SpaceX（X.AI Holdings Corp. 成为全资子公司，同一控制合并；10-Q 未披露作价）；SpaceX 2026-06-12 IPO（424B4）；xAI 独立融资序列终止', '—', '2026-02-02', '2026-08-04', SPCX, 'P1',
              note='x.ai 官方 2026-02-02 稿仅一句「SpaceX announced today that it has acquired xAI」（快照 snap_d3_xai_news_2026_02_02_joins_spacex）；$230B / $250B 作价仍只有媒体口径（r125 保留 P3）；xAI 员工股回购 $2,413M；“the Company completed its acquisition of X.AI Holdings Corp. (“xAI”), pursuant to which xAI became a wholly-owned subsidiary of the Company (“xAI Merger”)”')
    ev(m, 'r402', event_type='other', object_entity='SpaceX（Space Exploration Technologies Corp，CIK 1181412）', relation='acquired_by（换股，同一控制）', event_date='2026-02-02', snapshot_id=S['spcx'], confidence=1.0, entity_id='ent_xai')
    # 既有记录：r122 保持 P2，note 写明官方页 403；钉快照 / 实体
    m.set('fct_event', 'r122', 'note', 'SoftBank + a16z 共同领投；含 Nvidia $30B；官方页 https://openai.com/index/accelerating-the-next-phase-ai/ 403（curl + WebFetch，查证于 2026-09-20），保持 P2；pre-money $730B 由软银官方稿证实（r400），$730B + $122B = $852B post 对得上', basis='官方页 403 查证 + 软银稿交叉')
    ev(m, 'r122', snapshot_id=S['tcoai'], amount=122, amount_type='one_time', object_entity='OpenAI Group PBC', relation='round（SoftBank / a16z / D.E. Shaw / MGX / TPG / T. Rowe 领投；Amazon / Nvidia / Microsoft 参与）', round='2026 轮（post $852B）', entity_id='ent_openai', confidence=0.6)
    ev(m, 'r123', entity_id='ent_openai', amount=7, amount_type='one_time', relation='tender offer（公司回购）')
    ev(m, 'r121', amount=65, amount_type='one_time', object_entity='Anthropic', relation='round（Altimeter / Dragoneer / Greenoaks / Sequoia 领投）', round='Series H（post $965B）', confidence=1.0)
    ev(m, 'r124', amount=20, amount_type='one_time', object_entity='xAI', relation='round（NVIDIA / Cisco 战略）', round='Series E', entity_id='ent_xai', confidence=1.0)
    ev(m, 'r125', entity_id='ent_xai', event_type='other', amount_type='range')
    m.set('fct_event', 'r125', 'note', '并入 SpaceX 已由 SpaceX 10-Q 证实（r402，P1），但作价未披露，$230B / $250B 仍为媒体口径', basis='与 r402 交叉')

    # ================= 2. m_lab_funding_reflection =================
    m.observe('r404', 'm_lab_funding_reflection', 'Reflection AI', 'event', '融资 $2B（官方博客；投资方 B Capital / Citi / CRV / Disruptive / DST / Eric Schmidt / Zoom Ventures / Lightspeed / NVIDIA / Sequoia / 1789 等；官方未披露估值与领投方）', 'USD B', '2025-10-09', '2025-10-09', RBLOG, 'P1',
              note='取代 r115（原 TechCrunch 无 URL、标 P1 实为媒体）；$8B 估值仅 TechCrunch 口径（快照 snap_d3_techcrunch_2025_10_09_reflection_2b，投资方列表亦未称 Nvidia 领投）；“We’ve assembled an extraordinary AI team, built a frontier LLM training stack, and raised $2 billion.”')
    ev(m, 'r404', event_type='funding', amount=2, currency='USD', amount_type='one_time', object_entity='Reflection AI', relation='round（领投方官方未指明）', round='2025-10 轮（媒体：$8B 估值）', event_date='2025-10-09', snapshot_id=S['rblog'], confidence=1.0)
    m.supersede('r115', 'r404', reason='官方博客取代无 URL 的媒体转述；估值口径保留在 r404 note')
    m.observe('r405', 'm_lab_funding_reflection', 'Reflection AI', 'state', '截至 2026-09-20 reflection.ai/news 与 /blog 无 2026 年融资官方稿：news 页仅转列 CNBC 2026-04-23 视频（$25B pre-money）、FT 2026-03-02（$20bn+ 在谈）；官方博客最后一篇为 2025-10-09', '—', '截至 2026-09-20', '2026-09-20', RNEWS, 'P1',
              note='2026 轮金额 / 领投方仍无一手，r116（CEO 口径 P2）保持不取代；TechCrunch 2026-07-14 称累计已融「close to $2.6 billion」（媒体，不推算轮次）；“CNBC SquawkboxReflection CEO confirms latest funding round closed at $25 billion pre-money valuationApril 23, 2026”')
    ev(m, 'r405', event_type='other', object_entity='—', relation='—', snapshot_id=S['rnews'], confidence=1.0)
    m.set('fct_event', 'r116', 'source_url', 'https://www.cnbc.com/video/2026/04/23/reflection-ceo-on-ai-race-the-best-open-models-are-coming-from-china.html', basis='reflection.ai/news 页外链（快照 snap_d3_reflection_news_index_2026_09_20）')
    ev(m, 'r116', snapshot_id=S['rnews'], round='2026 轮（pre-money $25B，金额未披露）', object_entity='Reflection AI', relation='round（领投方未披露）')

    # ================= 3. m_lab_contract_reflection_nbis =================
    m.observe('r406', 'm_lab_contract_reflection_nbis', 'Reflection AI ↔ NBIS', 'event', '$1B 算力合同：Nebius 向 Reflection 提供 NVIDIA 最新芯片算力（Bloomberg 原报道：>$1B、至 2029、GB300）', 'USD B', '2026-07-14', '2026-07-14', TCR14, 'P3',
              note='取代 r117（原「TechCrunch / Bloomberg / Reuters」无 URL、标 P1 实为媒体）；Bloomberg 原文 https://www.bloomberg.com/news/articles/2026-07-14/nebius-to-sell-1-billion-in-ai-capacity-to-startup-reflection 403，reflection.ai/news 转列；公司确认见 r407；“has signed a $1 billion compute deal with European AI infrastructure company Nebius”')
    ev(m, 'r406', event_type='contract', amount=1, currency='USD', amount_type='multi_year_cap', object_entity='Reflection AI', relation='customer（Reflection → Nebius）', event_date='2026-07-14', snapshot_id=S['tcr14'], confidence=0.6)
    m.supersede('r117', 'r406', reason='补具体 URL 与快照；媒体来源按规则降为 P3，一手确认另记 r407')
    m.observe('r407', 'm_lab_contract_reflection_nbis', 'Reflection AI ↔ NBIS', 'event', 'Nebius Q2 股东信确认：Reflection 选择 Nebius 签多年期协议（训练 + 运行开源模型）；Q2 四笔 landmark deals 平均 TCV >$1B，点名 Reflection 与 Cohere；ACV $20–25M/MW，≈70% 含预付', 'USD B', '2026Q2', '2026-08-12', SHL, 'P1',
              note='金额未单独披露，只给「四笔平均 >$1B」；证边 e_labfund_nbis（融资 → 采购）一次；“Reflection selected Nebius for a multi-year agreement to train and run its open-source models on our platform”')
    ev(m, 'r407', event_type='contract', object_entity='Reflection AI', relation='customer（Reflection → Nebius）', event_date='2026-08-12', snapshot_id=S['shl'], confidence=1.0)
    m.set('fct_event', 'r407', 'amount_text', '四笔 landmark deals 平均 TCV >$1B（含 Reflection、Cohere）；Reflection 单笔金额未披露', basis='SHL 原文')

    # ================= 4. m_lab_funding_cohere =================
    m.observe('r408', 'm_lab_funding_cohere', 'Cohere', 'event', 'Schwarz Group 拟以 $600M（€500M）结构化融资领投即将进行的 Series E；同日宣布与 Aleph Alpha 合并计划（STACKIT 主权云）', 'EUR M', '2026-04-24', '2026-04-24', CO424, 'P1',
              note='取代 r119（原 TechCrunch P3）；是「意向」不是完成：“the companies of Schwarz Group intend to back our upcoming Series E funding as lead investor with a $600M (€500M) structured financing commitment”')
    ev(m, 'r408', event_type='funding', amount=500, currency='EUR', amount_type='one_time', is_estimate=True, object_entity='Cohere', relation='lead investor（Schwarz Group → Cohere，意向）', round='Series E（拟）', event_date='2026-04-24', snapshot_id=S['co424'], confidence=1.0)
    m.supersede('r119', 'r408', reason='官方博客取代媒体转述；官方口径为「intend to back」，标 is_estimate')
    m.observe('r409', 'm_lab_funding_cohere', 'Cohere', 'state', '截至 2026-09-20 Cohere newsroom（2026-03-04 至 09-16 共 17 篇）无 Series E 完成公告；2026-09-16「与 Aleph Alpha 签 definitive business combination agreement」稿只提 Schwarz 合作，未提融资完成或估值', '—', '截至 2026-09-20', '2026-09-20', CO916, 'P1',
              note='C7 时效：$7B 估值 stale、$20B 为在谈（r120 P3 保留）；合并预计年内完成、待监管批准；“We are announcing the signing of a definitive business combination agreement with Aleph Alpha, following the release of our planned partnership in April of this year.”')
    ev(m, 'r409', event_type='other', object_entity='Aleph Alpha', relation='merger（definitive agreement，待监管）', event_date='2026-09-16', snapshot_id=S['co916'], confidence=1.0)
    ev(m, 'r120', is_estimate=True, object_entity='Cohere', relation='round（在谈，含加拿大政府）', round='Series E（在谈）')

    # ================= 5. m_circular_financing =================
    ev(m, 'r128', event_type='investment', amount=2, currency='USD', amount_type='one_time', object_entity='Nebius Group N.V.（NASDAQ: NBIS）', relation='investor + supplier（NVIDIA → Nebius；同为 NBIS 客户 Reflection 的投资方）', event_date='2026-03-11', snapshot_id=S['nbnr'], confidence=1.0, entity_id='ent_nbis',
       anchor='NVIDIA will invest $2 billion in Nebius, reflecting NVIDIA’s confidence in Nebius’s business and unique depth of engineering expertise across the full AI technology stack.')
    m.set('fct_event', 'r128', 'note', 'NBIS 循环融资敞口一手证据（C18）；我方抽核；nebius.com 稿 2026-09-20 可抓（200），快照已存；股份类别 / 每股价未在稿内披露', basis='快照核对')
    ev(m, 'r127', amount=2, currency='USD', amount_type='one_time', object_entity='CoreWeave', relation='investor + supplier', confidence=1.0)
    m.observe('r410', 'm_circular_financing', 'NVIDIA', 'actual', '13.1', 'USD B 非上市股权净增（non-marketable equity net additions）', 'Q2 FY27（截至 2026-07-26）', '2026-08-26', NVQ2, 'P1',
              note='上半年净增 $31.0B；期末余额 $47.9B（期初 $42.3B；重分类 −$12.3B 为已上市）；累计未实现收益 $9.1B；权益法「infrastructure financiers」$3.3B；“Net additions | 13,106 | 299 | 31,005 | 948”')
    m.observe('r411', 'm_circular_financing', 'NVIDIA', 'state', '10-Q 承诺表：股权投资承诺 $25B（FY27 余下 $18B / FY28 $3B / FY29 $2B / FY30 $2B），对象为 AI model makers、infrastructure financiers 与其他私营公司；另 AI cloud agreements 承诺 $36B、供应承诺 $279B', 'USD B', '截至 2026-07-26', '2026-08-26', NVQ2, 'P1',
              note='循环融资的「未来敞口」一手读数：投 lab（股权）+ 买回云（AI cloud agreements）+ 担保（r412）同表；“We committed to make certain equity investments in AI model makers, infrastructure financiers, and other private companies, subject to certain contingencies.”')
    ev(m, 'r411', event_type='investment', amount=25, currency='USD', amount_type='multi_year_cap', object_entity='AI model makers / infrastructure financiers / 其他私营公司（未具名）', relation='committed equity investments', event_date='2026-07-26', snapshot_id=S['nvq2'], confidence=1.0, entity_id='ent_nvda')
    m.observe('r412', 'm_circular_financing', 'NVIDIA ↔ OpenAI', 'event', '2026-08 为 OpenAI 关联方在 SB Energy 俄亥俄 PORTS 园区（≈4.25 GW，九期 20 年租约）提供土地 / 电力 / 厂房担保，上限 $105B；条件：园区独家部署 NVIDIA 算力；另有 ≈3.8 GW 追加期权', 'USD B', '2026-08', '2026-08-26', NVQ2, 'P1',
              note='取代 r132（Fortune P3）；担保自各期租约起租生效（预计 FY2029 起），OpenAI 取得满意信用评级即终止；“we entered into guarantees, capped at a total of $105 billion, to provide credit support on a land, power, and shell buildout with affiliates of SB Energy Corp. (SB Energy) on behalf of a customer, an affiliate of OpenAI Group PBC (OpenAI)”')
    ev(m, 'r412', event_type='other', amount=105, currency='USD', amount_type='multi_year_cap', object_entity='OpenAI Group PBC 关联方（承租人）/ SB Energy Corp.（出租人）', relation='guarantor（NVIDIA 为 OpenAI 租约担保，换园区独家部署 NVIDIA）', event_date='2026-08-15', snapshot_id=S['nvq2'], confidence=1.0, entity_id='ent_nvda')
    m.supersede('r132', 'r412', reason='10-Q 原文取代 Fortune 转述')
    m.set('fct_quant', 'r131', 'note', '非上市证券余额 $42.3B（= Q2 FY27 10-Q 期初余额 $42,336M，口径对上）；Q2 净增见 r410', basis='与 Q2 10-Q 交叉'); m.set('fct_quant', 'r131', 'period_end', '2026-04-26', basis='as-of')

    # ================= 6. m_preipo_pool / m_vc_flow（付费源，免费定性）=================
    m.observe('r413', 'm_preipo_pool', 'pre-IPO 池', 'state', 'Crunchbase 免费报告（数据截至 2026-07-01）：Q2 2026 有 32 家公司以 >$1B 估值 IPO（最大 SpaceX：$1.77T 估值募 $75B；其次 Cerebras、Quantinuum）；24 起 ≥$1B 并购合计 $113B（单季纪录）；SpaceX 拟 $60B 收购 Anysphere（Cursor）', '—', '2026Q2', '2026-07-02', CB, 'P3',
              note='取代 r140 占位；付费一级库（PitchBook 等）仍未接，只定性；“A total of 32 companies went public at values above $1 billion in Q2. After SpaceX, the next two largest listings were inference chipmaker Cerebras Systems and quantum company Quantinuum.”')
    ev(m, 'r413', event_type='other', object_entity='—', relation='—', event_date='2026-07-01', snapshot_id=S['cb'], confidence=0.6)
    m.supersede('r140', 'r413', reason='占位换成免费可得的定性来源（P3）')
    m.observe('r414', 'm_vc_flow', 'AI 赛道一级', 'state', 'Crunchbase 免费报告：H1 2026 全球风险投资 $510B（Q1 $305B / Q2 $205B），超 2025 全年 $440B；Q2 >70% 流向 AI（上年同期 <50%）；OpenAI + Anthropic 合计 $217B = H1 的 43%；Q2 16 笔 ≥$1B 轮合计 $108.6B（53%），其中 7 家为前沿 lab（DeepSeek、StepFun、Moonshot、Ineffable、Prometheus、Isomorphic）', 'USD B', '2026H1', '2026-07-02', CB, 'P3',
              note='取代 r126 占位；Crunchbase「OpenAI + Anthropic $217B」与库内三 lab ≈$207B（含 xAI $20B）口径不同，不调和；“OpenAI and Anthropic alone accounted for $217 billion — 43% of all startup funding in H1”')
    ev(m, 'r414', event_type='other', amount=510, currency='USD', amount_type='one_time', object_entity='—', relation='—', event_date='2026-07-01', snapshot_id=S['cb'], confidence=0.6)
    m.set('fct_event', 'r414', 'amount_text', 'H1 2026 全球 VC $510B（AI 份额 >70%；OpenAI + Anthropic $217B）', basis='原文')
    m.supersede('r126', 'r414', reason='占位换成免费可得的定性来源（P3）')

    # ================= 7. metric_registry =================
    R = {  # metric: (kou_jing, unit, source_ids, upstream_deps, fill_status)
      'm_lab_funding_frontier': ('事件：OpenAI / Anthropic / xAI 大额一级融资与结构性事件；每条记轮次、post / pre-money、领投方、到账节奏（tranche）；估值只记披露口径不推算；xAI 2026-02 起并入 SpaceX，其后资金事件归 SpaceX', 'USD B',
                                 f'["{SRC["anth"]}","{SRC["xai"]}","{SRC["sb0227"]}","{SRC["sb0701"]}","{SRC["spcx"]}","{SRC["tc"]}"]', '[]', '已填（OpenAI 官方页 403，轮次总额 P2）'),
      'm_lab_funding_reflection': ('事件：Reflection AI 各轮融资金额 / 估值 / 投资方；2025-10 $2B 官方证实，2026 轮仅 CEO 口径 pre-money $25B（P2），金额无一手', 'USD B',
                                   f'["{SRC["rblog"]}","{SRC["rnews"]}","{SRC["cnbc"]}"]', '[]', '已填（2026 轮金额待一手，截至 2026-09-20 无官方稿）'),
      'm_lab_contract_reflection_nbis': ('事件：Reflection ↔ Nebius 算力合同；金额取媒体（$1B，P3），公司确认取 Nebius 股东信（多年期、四笔平均 TCV >$1B，P1）；单笔金额未披露', 'USD B',
                                         f'["{SRC["tcr14"]}","{SRC["shl"]}"]', '["m_lab_funding_reflection"]', '已填'),
      'm_lab_funding_cohere': ('事件：Cohere 融资（Series E 意向 / 在谈 / 完成分开记，obs_type state = 在谈或未完成）、合并 Aleph Alpha、ARR（P2 备忘录）；估值只记披露口径', 'USD B',
                               f'["{SRC["co424"]}","{SRC["co916"]}","{SRC["tc"]}"]', '[]', '已填（Series E 截至 2026-09-20 未见完成公告）'),
      'm_circular_financing': ('NVIDIA 系「投 lab / 云 → 卖芯片 / 买回云 / 担保租约」三类敞口：个案（newsroom / 10-Q 附注，event）+ 季度序列（10-Q 非上市股权净增、承诺表 Equity investments / AI cloud agreements / 担保上限，quant / state）；「循环」判读 D', 'USD B',
                               f'["{SRC["nvnr"]}","{SRC["nbnr"]}","{SRC["nvq1"]}","{SRC["nvq2"]}"]', '["m_lab_funding_frontier"]', '已填'),
      'm_preipo_pool': ('pre-IPO 池 / 打新：>$1B IPO 数与规模、≥$1B 并购；付费一级库未接，暂用 Crunchbase 免费季报定性（P3）；人定口径 C 待补', '—', f'["{SRC["cb"]}"]', '[]', '付费定性'),
      'm_vc_flow': ('AI 赛道一级资金流：全球 VC 总额、AI 份额、前沿 lab 集中度（Crunchbase 免费季报，P3）；付费库（PitchBook / IT桔子 / 烯牛）未接', 'USD B', f'["{SRC["cb"]}"]', '[]', '付费定性'),
    }
    for mid, (kj, unit, src, deps, fs) in R.items():
        m.set('metric_registry', mid, 'track', TRACK, basis='D3 一级资本赛道'); m.set('metric_registry', mid, 'kou_jing', kj, basis='本轮口径'); m.set('metric_registry', mid, 'unit', unit, basis='记录单位')
        m.set('metric_registry', mid, 'source_ids', src, basis='source_master'); m.set('metric_registry', mid, 'upstream_deps', deps, basis='依赖'); m.set('metric_registry', mid, 'last_validated', '2026-09-20', basis=V)
        m.set('metric_registry', mid, 'fill_status', fs, basis=V)
    m.set('metric_registry', 'm_lab_funding_frontier', 'notes_assumption_ids', 'D3 一级资本流 2026 年内三大 lab 合计 ≈$207B 融资（计算值；Crunchbase 口径 OpenAI + Anthropic H1 $217B，口径不同，D 判）；xAI 2026-02-02 并入 SpaceX（P1）；Anthropic Series H 之后至 2026-09-20 未见新轮；软银三期打款至 2026-10-01', basis='本轮')
    m.set('metric_registry', 'm_circular_financing', 'notes_assumption_ids', 'NBIS 头号风险论据。**NVIDIA 投 Nebius $2B 是 NBIS 本体的循环融资敞口一手证据**（供芯方 = 股东 = 客户 Reflection 的投资方）；10-Q Q2 FY27：股权承诺 $25B + OpenAI 租约担保 $105B + AI cloud 承诺 $36B（P1）；判读 D', basis='本轮')
    m.set('metric_registry', 'm_preipo_pool', 'fill_status', '付费定性', basis='r140 占位已取代为 P3 定性')

    # ================= 8. 边 =================
    E = {
      'e_labfund_nbis': ('lab 拿到融资 → 有算力采购力 → 与 NBIS 签约；Reflection 2025-10 融 $2B（官方）→ 2026-07 签 Nebius 多年期协议（股东信确认，媒体 $1B）证过一次；禁止回归自己（NVIDIA 同为 Reflection 投资方与 NBIS 股东，见 e_circular_nbis）',
                         '["r404","r116","r405","r406","r407"]', 'Reflection $2B（r404，官方 P1）→ 2026 轮 $25B pre（r116，P2）→ Nebius 多年期协议（r407，SHL P1；r406 媒体 $1B）；2026 轮金额无一手（r405）'),
      'e_frontierfund_nbis': ('前沿 lab 融资总量 → neocloud 需求；非确认客户，只给方向；到账节奏（软银三期）与 lab 并购（xAI → SpaceX）改变「可采购资金」的时间分布',
                              '["r121","r122","r123","r124","r125","r400","r401","r402"]', 'Anthropic $65B（r121 P1）；OpenAI $122B（r122 P2；软银 $30B 三期 r400 / r401 P1）；xAI $20B（r124 P1）后并入 SpaceX（r402 P1）；员工要约 / 估值为 P3（r123 / r125）'),
      'e_anthropic_amd': ('D3 lab 资本 → D1 加速器采购的直接实例：Anthropic 融资（Series H $65B）→ 与 AMD 的算力采购；AMD 侧 PR 属本体事件不计上游证据；因子 r=H',
                          '["r121"]', 'Anthropic Series H $65B @ $965B（r121，P1）；AMD Q2 2026 PR（P1）为下游侧'),
      'e_circular_nbis': ('供芯方 NVIDIA 入股 $2B，同时是客户 Reflection 投资方 → 采购与融资条件相互依赖；10-Q 层面 NVIDIA 对 AI 云 / lab 的股权承诺 $25B、担保 $105B 说明是系统性做法而非个案；「循环」判读 D',
                          '["r128","r410","r411","r412"]', 'NVIDIA 投 Nebius $2B（r128，2026-03-11，P1，快照已存）；NVIDIA Q2 FY27 非上市股权净增 $13.1B（r410）、股权承诺 $25B（r411）、OpenAI 租约担保 $105B（r412）均 P1'),
    }
    for eid, (mech, ids, evid) in E.items():
        m.set('edge_registry', eid, 'mechanism', mech, basis='doc25 / 本轮'); m.set('edge_registry', eid, 'evidence_ids', ids, basis='库：from_metric 名下可见记录（e_labfund_nbis 按 checks EXTRA 含 m_lab_contract_reflection_nbis）')
        m.set('edge_registry', eid, 'evidence', evid, basis='同上'); m.set('edge_registry', eid, 'last_validated', '2026-09-20', basis=V)
        m.set('edge_registry', eid, 'owner', ('D' if eid == 'e_circular_nbis' else 'B'), basis='B 初稿 D 复核；循环判读 D')

    # ================= 来源 =================
    for sid, pub, freq, note in (
        (SRC['sb0227'], 'SoftBank Group Corp.（IR press release）', '事件', 'P1 投资方官方稿；OpenAI 官方页 403 时的一手替代，给 pre-money $730B'),
        (SRC['sb0701'], 'SoftBank Group Corp.（IR press release）', '事件', 'P1；tranche 执行公告'),
        (SRC['rblog'], 'Reflection AI（company blog）', '事件', 'P1 官方稿；只给金额与投资方列表，无估值 / 领投方'),
        (SRC['rnews'], 'Reflection AI（官方 news 页，转列媒体）', '事件', '官方页但内容为媒体转列；用作「无官方稿」的证据'),
        (SRC['tcr14'], 'TechCrunch', '事件', 'P3 媒体；Bloomberg 原报道 403'),
        (SRC['co424'], 'Cohere（company blog）', '事件', 'P1 官方稿；Series E 为「intend to back」意向'),
        (SRC['co916'], 'Cohere（newsroom）', '事件', 'P1 官方稿；未提融资完成'),
        (SRC['nbnr'], 'Nebius Group newsroom', '事件', 'P1 一手新闻稿；2026-09-20 curl 200，快照已存'),
        (SRC['nvq2'], 'SEC EDGAR / NVIDIA Corporation', '季', 'P1 交易所归档，accession 0001045810-26-000075；Note 6 / 8 / 10 + MD&A 担保段'),
        (SRC['spcx'], 'SEC EDGAR / Space Exploration Technologies Corp.', '季', 'P1 交易所归档，accession 0001628280-26-052535；xAI 合并为同一控制换股，未披露作价'),
        (SRC['cb'], 'Crunchbase News（免费报告）', '季', 'P3 聚合站免费季报；付费一级库未接'),
    ):
        m.set('source_master', sid, 'publisher', pub, basis='来源页'); m.set('source_master', sid, 'frequency', freq, basis='—'); m.set('source_master', sid, 'reliability_note', note, basis='—'); m.set('source_master', sid, 'last_validated', '2026-09-20', basis=V)
    m.set('source_master', 'src_techcrunch_2025_10_09_reflection_raises_2b_url_待', 'verify_status', 'stale', basis='r115 已被官方博客 r404 取代'); m.set('source_master', 'src_techcrunch_2025_10_09_reflection_raises_2b_url_待', 'url', 'https://techcrunch.com/2025/10/09/reflection-raises-2b-to-be-americas-open-frontier-ai-lab-challenging-deepseek/', basis='URL 补齐（快照 snap_d3_techcrunch_2025_10_09_reflection_2b）')
    m.set('source_master', 'src_techcrunch_bloomberg_reuters', 'verify_status', 'stale', basis='r117 已被带 URL 的 r406 / r407 取代'); m.set('source_master', 'src_techcrunch_bloomberg_reuters', 'source_tier', 'P3', basis='媒体按规则 P3')
    m.set('source_master', 'src_一级_db_招股书', 'verify_status', 'placeholder', basis='r140 占位已取代'); m.set('source_master', 'src_pitchbook_it桔子_烯牛_付费', 'reliability_note', '付费未接；免费定性改用 Crunchbase News（r414）', basis='—')
    for sid, kind in ((SRC['sb0227'], 'ir_release'), (SRC['sb0701'], 'ir_release'), (SRC['rnews'], 'company_blog'), (SRC['cb'], 'data_aggregator')):
        m.set('source_master', sid, 'source_kind', kind, basis='doc23 kind')
    for rid in ('r402', 'r405', 'r409', 'r413'):
        m.set('fct_event', rid, 'amount_type', None, basis='state 记录无金额，规则误判 range 清空')
    m.set('source_master', SRC['cnbc'], 'url', 'https://www.cnbc.com/video/2026/04/23/reflection-ceo-on-ai-race-the-best-open-models-are-coming-from-china.html', basis='reflection.ai/news 外链'); m.set('source_master', SRC['cnbc'], 'access', 'blocked', basis='cnbc.com 403（视频未抓）')
