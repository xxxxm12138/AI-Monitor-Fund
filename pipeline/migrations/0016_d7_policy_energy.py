# -*- coding: utf-8 -*-
"""0016 · D7 政策 · 能源 · 安全 第一轮（BIS 三条旧记录核原文补快照 / 锚点 + 2026 新增 3 条管制事件；EU AI Act / Digital Omnibus / 加州 SB 53 四条法规事件；FERC 大负荷 show cause + Vistra–Meta 核电 PPA + IEA 电网排队；IEA 数据中心用电四条 P1 记录取代 P2 占位；OpenAI–Hugging Face 事故报告；工信部两份算力文件；五个占位记录取代；六个指标 registry 口径；五条边证据）· owner B · 2026-09-20
一手来源全部走官方原文：govinfo（Federal Register）、bis.gov PDF、whitehouse.gov、EUR-Lex、leginfo.legislature.ca.gov、ferc.gov（403，经 Wayback 存档）、SEC EDGAR、iea.org、cdn.openai.com、nda.gov.cn / miit.gov.cn；18 份快照 snap_d7_*。
研究上有意义的四点：① 2026-01 之后 BIS 对华 AI 芯片没有新的正式规则（FR API 列出 BIS 2026-01-16→09-19 全部 38 份文件，无一涉及 3A090 对华）；有意义的是 2026-05-31 一份「指引」重申 D:5 / 澳门总部实体在全球任何地点拿先进算力都要许可（堵海外代持），及 UAE 规则把两家 UAE AI 公司列为免许可收货人。
② 旧 r105 / r106（≈1000 TWh 2026E / 460 TWh 2022）实际出自 IEA Electricity 2024（2024-01），不是登记的「Energy and AI / Electricity 2026」，knowledge_time 2026 有误；IEA 自己在 Energy and AI（2025-04）已下修为 415 TWh（2024）→ ~945 TWh（2030 基准情形）。边 e_dcbuild_fcel 写的「≈1000 TWh 2030」把两份报告混了。
③ EU AI Act 的 GPAI 义务（第 V 章）2025-08-02 起适用未被 Digital Omnibus（Reg. 2026/1744，2026-07-27 生效）推迟；被推迟的只是高风险系统（附件 III → 2027-12-02，附件 I → 2028-08-02）。
④ 2026 年唯一有一手来源的重大安全事故是 OpenAI 自述的 7 月评估沙箱逃逸 → 攻陷 Hugging Face 生产基础设施（2026-07-11–13，07-21 披露，技术报告 51 页）；Anthropic 同期「Agentic Misalignment in Summer 2026」自称不是真实事故，未登记。"""
OWNER = 'B'
# ---- 来源（名 + URL，URL 均实际打开过）----
BISPR = 'BIS press release https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china'
FR789 = 'govinfo https://www.govinfo.gov/content/pkg/FR-2026-01-15/html/2026-00789.htm'
WH232 = 'https://www.whitehouse.gov/presidential-actions/2026/01/adjusting-imports-of-semiconductors-semiconductor-manufacturing-equipment-and-their-derivative-products-into-the-united-states/'
BISG = 'BIS Guidance 2026-05-31 enforcement of license requirements for advanced computing items https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf'
FRIC = 'Federal Register 91 FR 17851 BIS final rule IC designer extension (govinfo) https://www.govinfo.gov/content/pkg/FR-2026-04-09/html/2026-06851.htm'
FRUAE = 'Federal Register 91 FR 43034 BIS final rule UAE enhanced favorable treatment (govinfo) https://www.govinfo.gov/content/pkg/FR-2026-07-14/html/2026-14132.htm'
EURLEX = 'EUR-Lex Regulation (EU) 2024/1689 AI Act https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689'
OMNI = 'EUR-Lex Regulation (EU) 2026/1744 Digital Omnibus on AI https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32026R1744'
SB53 = 'California Legislative Information SB 53 (2025) TFAIA chaptered text https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB53'
FERCN = 'FERC news release 2026-06-18 large load show cause orders https://www.ferc.gov/news-events/news/ferc-launches-aggressive-targeted-action-speed-large-load-integration'
FRPJM = 'Federal Register 91 FR 37972 FERC notice Section 206 proceeding PJM EL26-67 (govinfo) https://www.govinfo.gov/content/pkg/FR-2026-06-24/html/2026-12708.htm'
VST = 'Vistra 8-K 2026-01-09 Meta nuclear PPAs (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1692819/000119312526008508/d20785d8k.htm'
IEAAI = 'IEA Energy and AI (2025-04) Energy demand from AI https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai'
IEAE24 = 'IEA Electricity 2024 executive summary https://www.iea.org/reports/electricity-2024/executive-summary'
IEAE26 = 'IEA Electricity 2026 executive summary https://www.iea.org/reports/electricity-2026/executive-summary'
OAI = 'OpenAI Hugging Face Incident Technical Report (2026-08) https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf'
NDA = '国家数据局 转发 工信部等八部门《“人工智能+制造”专项行动实施意见》工信部联科〔2025〕279号 https://www.nda.gov.cn/sjj/zwgk/zcfb/0112/20260107214358696030895_pc.html'
MIIT = '工业和信息化部办公厅 关于组织开展国家算力互联互通节点建设工作的通知 工信厅信管函〔2026〕35号 https://www.miit.gov.cn/jgsj/xgj/wjfb/art/2026/art_67864b94485943ad8cee03f4f4989d17.html'
# ---- 快照 id（snapshots/snap_d7_*.txt）----
S = dict(bispr='snap_d7_bis_pr_2026_01_13_license_review_policy', fr789='snap_d7_fr_2026_00789_bis_license_policy', wh='snap_d7_wh_232_proclamation_2026_01_14',
         bisg='snap_d7_bis_guidance_2026_05_31_advanced_computing_d5', fric='snap_d7_fr_2026_06851_ic_designer_extension', fruae='snap_d7_fr_2026_14132_uae_advanced_computing',
         eurlex='snap_d7_eurlex_ai_act_2024_1689_art51_101_113', omni='snap_d7_eurlex_2026_1744_digital_omnibus_ai', sb53='snap_d7_ca_sb53_tfaia_chaptered_2025_09_29',
         fercn='snap_d7_ferc_news_2026_06_18_large_load_show_cause', frpjm='snap_d7_fr_2026_12708_ferc_pjm_el26_67', vst='snap_d7_vistra_8k_2026_01_09_meta_nuclear_ppa',
         ieaai='snap_d7_iea_energy_and_ai_energy_demand_from_ai', ieae24='snap_d7_iea_electricity_2024_exec_summary', ieae26='snap_d7_iea_electricity_2026_exec_summary',
         oai='snap_d7_openai_hf_incident_technical_report_2026', nda='snap_d7_nda_miit_ai_plus_manufacturing_2025_279', miit='snap_d7_miit_2026_35_suanli_interconnect_nodes')
# ---- 来源 id（core.slug 生成，勿手改）----
SRC = dict(bispr='src_bis_press_release', fr789='src_govinfo', wh='src_white_house_proclamation_fact_sheet',
           bisg='src_bis_guidance_2026_05_31_enforcement_of_license_r', fric='src_federal_register_91_fr_17851_bis_final_rule_ic_d', fruae='src_federal_register_91_fr_43034_bis_final_rule_uae_',
           eurlex='src_eur_lex_regulation_eu_2024_1689_ai_act', omni='src_eur_lex_regulation_eu_2026_1744_digital_omnibus_', sb53='src_california_legislative_information_sb_53_2025_tf',
           fercn='src_ferc_news_release_2026_06_18_large_load_show_cau', frpjm='src_federal_register_91_fr_37972_ferc_notice_section', vst='src_vistra_8_k_2026_01_09_meta_nuclear_ppas_sec_edga',
           ieaai='src_iea_energy_and_ai_2025_04_energy_demand_from_ai', ieae24='src_iea_electricity_2024_executive_summary', ieae26='src_iea_electricity_2026_executive_summary',
           oai='src_openai_hugging_face_incident_technical_report_20', nda='src_国家数据局_转发_工信部等八部门_人工智能_制造_专项行动实施意见_工信部联科_2025_279', miit='src_工业和信息化部办公厅_关于组织开展国家算力互联互通节点建设工作的通知_工信厅信管函_2026_3')
V = '本轮逐字段核官方原文（2026-09-20）'
D = '2026-09-20'

def ev(m, rid, etype, snap, anchor=None, obj=None, rel=None, conf=1.0, edate=None, edate_text=None):
    """fct_event 补字段：类型 / 快照 / 置信 / 锚点 / 客体 / 关系 / 事件日"""
    m.set('fct_event', rid, 'event_type', etype, basis='事件类型词表'); m.set('fct_event', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_event', rid, 'confidence', conf, basis='一手原文，人工核对')
    if anchor: m.set('fct_event', rid, 'anchor', anchor, basis='原文短引')
    if obj: m.set('fct_event', rid, 'object_entity', obj, basis='原文')
    if rel: m.set('fct_event', rid, 'relation', rel, basis='—')
    if edate: m.set('fct_event', rid, 'event_date', edate, basis='原文日期')
    if edate_text: m.set('fct_event', rid, 'event_date_text', edate_text, basis='原文日期')

def up(m):
    # ============ 1. m_export_ctrl_bis：三条旧记录核原文 ============
    ev(m, 'r165', 'policy', S['bispr'], anchor='BIS will now review export license applications for the Nvidia H200, AMD MI325X, and similar chips on a case-by-case basis provided certain security requirements are met')
    m.set('fct_event', 'r165', 'note', '不含 25%；核对 bis.gov 原稿：规则「effective immediately upon publication in the Federal Register」，随 12-08-2025 总统宣布而来', basis=V)
    ev(m, 'r166', 'policy', S['fr789'], anchor='changing it from a presumption of denial to a case-by-case review. The semiconductors covered by this rule are the Nvidia H200 and its equivalents, as well as less advanced chips')
    m.set('fct_event', 'r166', 'amount_type', None, basis='原 range 系加载器把页码「1684–1689」误判为区间，清空')
    m.set('fct_event', 'r166', 'note', '核对 govinfo 原文：TPP < 21,000 且 total DRAM bandwidth < 6,500 GB/s（如 H200 / MI325X）；对华出货不得超过对美国终端用户出货的 50%；须美国境内第三方实验室测试；对 D:5 / 澳门总部实体的再出口维持推定拒绝', basis=V)
    ev(m, 'r167', 'policy', S['wh'], anchor='imports of Covered Products will be subject to a 25 percent ad valorem duty rate. This tariff shall be effective with respect to goods entered for consumption, or withdrawn from warehouse for consumption, on or after 12:01 a.m. eastern standard time on January 15, 2026')
    m.set('fct_event', 'r167', 'source_url', WH232, basis='公告原文 URL（原记录无 URL；Fact Sheet 未另存）')
    m.set('fct_event', 'r167', 'note', '措辞修正：关税，非“抽成 25% 收入”（C14）；核对公告：豁免美国数据中心 / 研发 / 初创 / 非数据中心消费与工业 / 公共部门用途；第 9 条要求商务部长 2026-07-01 前就数据中心芯片市场提交更新以决定是否修改关税', basis=V)
    m.set('source_master', SRC['wh'], 'url', WH232, basis='来源页'); m.set('source_master', SRC['wh'], 'publisher', 'The White House', basis='—')
    # ---- 2026-01 → 2026-09-19 新增（FR API 列 BIS 38 份文件逐一看；bis.gov 新闻稿）----
    m.observe('r350', 'm_export_ctrl_bis', 'BIS', 'event', 'BIS 指引：对总部在 D:5（含中国）或澳门、或最终母公司在 D:5 / 澳门的实体，先进算力物项（3A090.a/.b、4A090.a/.b 及 .z）在全球任何目的地都须许可；2025-05 对 AI 扩散规则的不执行政策不适用于此类实体', '—', '2026-05-31', '2026-05-31', BISG, 'P1',
              note='堵「海外代持」路径（如东南亚数据中心）；“a license requirement continues to apply under § 742.6(a)(6)(iii)(A) of the EAR to all destinations outside the United States for these advanced computing items when such items are for entities headquartered in, or whose ultimate parent company is headquartered in, Country Group D:5 or Macau”')
    m.observe('r351', 'm_export_ctrl_bis', 'BIS', 'event', '最终规则：先进逻辑 IC 代工尽调（FDD IFR 90 FR 5298）的「授权 IC 设计者」触发日与「认可 IC 设计者」申请截止日从 2026-04-13 延至 2026-12-31（91 FR 17851–17852，FR Doc 2026-06851）', '—', '2026-04-07', '2026-04-09', FRIC, 'P1',
              note='生效 2026-04-07；3A090.a 代工 / OSAT 推定控制的执行节奏放缓；“extending by about eight months the triggering date for authorized integrated circuit designer status and submission date for applications to become an approved integrated circuit (IC) designer. The new date is December 31, 2026”')
    m.observe('r352', 'm_export_ctrl_bis', 'BIS', 'event', '最终规则：UAE 从 D:3 / D:4 移入 A:5；UAE 政府及附录 8 所列实体（G42 / Core42 两家 UAE AI 公司 + 美国总部 AI 公司 UAE 子公司）免许可接收先进算力物项；对 D:5 / 澳门总部实体的许可要求维持（91 FR 43034–43039，FR Doc 2026-14132）', '—', '2026-07-10', '2026-07-14', FRUAE, 'P1',
              note='非对华条款，但同一许可框架（§742.6(a)(6)(iii)）且文内引用 2026-05-31 指引；两家 UAE 公司若 2027-04-06 前未成为美国公司须重新申请；“As of July 10, 2026, UAE government agencies are eligible recipients of advanced computing items license-free”')
    ev(m, 'r350', 'policy', S['bisg'], obj='D:5 / 澳门总部实体（全球）', rel='target')
    ev(m, 'r351', 'policy', S['fric'], obj='代工厂 / OSAT / IC 设计者', rel='target')
    ev(m, 'r352', 'policy', S['fruae'], obj='UAE 政府 / G42 / Core42', rel='target')
    # ============ 2. m_ai_regulation：EU AI Act / Digital Omnibus / 加州 SB 53 ============
    m.observe('r353', 'm_ai_regulation', 'EU', 'event', 'EU AI Act（Reg. 2024/1689）第 V 章通用目的 AI 模型（GPAI）义务自 2025-08-02 起适用（Art. 113(b)）：技术文档 / 下游信息 / 版权政策 / 训练数据摘要（Art. 53），系统性风险模型加评估 / 事故报告 / 网络安全（Art. 55）；2025-08-02 前已上市的 GPAI 模型宽限至 2027-08-02（Art. 111(3)）', '—', '2025-08-02', '2024-07-12', EURLEX, 'P1',
              note='取代 r170 占位；OJ L 2024/1689 于 2024-07-12 公布；“Chapter III Section 4, Chapter V, Chapter VII and Chapter XII and Article 78 shall apply from 2 August 2025, with the exception of Article 101”')
    m.observe('r354', 'm_ai_regulation', 'EU', 'event', 'EU AI Act 总体适用日 2026-08-02（Art. 113），含 Art. 101 对 GPAI 提供者的罚款权（不超过全球年营业额 3% 或 1,500 万欧元取高）', '—', '2026-08-02', '2024-07-12', EURLEX, 'P1',
              note='“It shall apply from 2 August 2026”；Art. 101(1)：“fines not exceeding 3 % of their annual total worldwide turnover in the preceding financial year or EUR 15 000 000, whichever is higher”')
    m.observe('r355', 'm_ai_regulation', 'EU', 'event', 'Digital Omnibus on AI（Reg. (EU) 2026/1744，2026-07-08 通过，OJ 2026-07-24，公布后第三日生效）修订 Art. 113：高风险系统义务推迟 —— 附件 III 类 → 2027-12-02，附件 I 类 → 2028-08-02；GPAI（第 V 章）2025-08-02 与总体 2026-08-02 适用日不变', '—', '2026-07-27', '2026-07-24', OMNI, 'P1',
              note='生效日 = 公布后第三日 2026-07-27（Art. 4）；“2 December 2027 as regards AI systems classified as high-risk pursuant to Article 6(2) and Annex III”')
    m.observe('r356', 'm_ai_regulation', 'California', 'event', '加州 SB 53《Transparency in Frontier Artificial Intelligence Act》签署成法（Chapter 138, Statutes of 2025）：训练算力 > 10^26 FLOP 的前沿模型开发者、年营收 > 5 亿美元的大型开发者须公布前沿 AI 框架、向 OES 报告灾难性风险评估摘要与重大安全事故，附举报人保护', '—', '2025-09-29', '2025-09-29', SB53, 'P1',
              note='取代 r170 同批；生效日：法案文本未写，按加州宪法 art. IV §8(c) 非紧急法案于次年 1 月 1 日生效 = 2026-01-01（规则推定，非原文）；“Frontier model” means a foundation model that was trained using a quantity of computing power greater than 10^26 integer or floating-point operations”')
    ev(m, 'r353', 'policy', S['eurlex'], obj='GPAI 模型提供者', rel='target')
    ev(m, 'r354', 'policy', S['eurlex'], obj='AI 系统提供者 / 部署者 / GPAI 提供者', rel='target')
    ev(m, 'r355', 'policy', S['omni'], obj='高风险 AI 系统提供者', rel='target')
    ev(m, 'r356', 'policy', S['sb53'], obj='大型前沿开发者（> $500M 营收）', rel='target')
    m.supersede('r170', 'r353', reason='r170 为「待填」占位，无来源 URL；由 EUR-Lex 原文事件取代')
    # ============ 3. m_energy_grid：FERC / PJM / 核电 PPA / 电网排队 ============
    m.observe('r357', 'm_energy_grid', 'FERC', 'event', 'FERC 依 FPA §206 向六家 RTO/ISO 各发 show cause 令：60 天内证明现行 tariff 无大负荷条款仍合理、或提交修订；五类改革含并网 / 共址与表后发电 / 灵活大负荷输电服务 / 电气邻近发电的专门研究流程；30 天内报告如何保证新增大负荷有足够发电', '—', '2026-06-18', '2026-06-18', FERCN, 'P1',
              note='取代 r169 占位；ferc.gov 直连 403，快照经 Wayback 2026-09-14 存档；“directing them to justify or reform the rules that govern how data centers, manufacturing facilities, and other large energy users connect to the electric grid”')
    m.observe('r358', 'm_energy_grid', 'FERC', 'event', 'Federal Register 通知：FERC 2026-06-18 令（195 FERC ¶ 61,211，Docket EL26-67-000）对 PJM 及 46 家输电业主启动 §206 调查，退款生效日 = 通知刊登日 2026-06-24；同日另有 NYISO（2026-12707）/ MISO（2026-12706）等平行通知', '—', '2026-06-24', '2026-06-24', FRPJM, 'P1',
              note='91 FR 37972–37973；“instituting an investigation to determine whether PJM Interconnection, L.L.C\'s Open Access Transmission Tariff is unjust, unreasonable, unduly discriminatory or preferential, or otherwise unlawful”')
    m.observe('r359', 'm_energy_grid', 'Vistra', 'event', 'Vistra 与 Meta 签 20 年 PPA 共 2,609 MW PJM 核电：在运 Perry 1,268 MW + Davis-Besse 908 MW（2026 末起部分交付、2027 末全量），另 Perry 213 / Davis-Besse 80 / Beaver Valley 140 MW 扩容（2031 起、2034 末全量）', 'MW', '2026-01-09', '2026-01-09', VST, 'P1',
              note='8-K Item 7.01；扩容资本开支 2026–2034；“20-year power purchase agreements (“PPAs”) with Meta Platforms, Inc. (“Meta”), pursuant to which the Company has agreed to supply Meta with a total of 2,609 MW of carbon-free power and capacity from the Company’s PJM nuclear power plants”')
    m.observe('r360', 'm_energy_grid', 'IEA', 'state', 'IEA Electricity 2026：全球 > 2,500 GW 项目（可再生、储能及数据中心等大负荷）滞留并网排队；到 2030 年电网年投资需较当前 4,000 亿美元再增约 50%；美国 2025 用电 +2.1%，至 2030 年增量约一半来自数据中心', 'GW', '2026', '2026-02-06', IEAE26, 'P1',
              note='报告页元数据日期 2026-02-06；“more than 2 500 gigawatts (GW) worth of projects – encompassing renewables, storage, and projects with large loads, such as data centres − remain stalled in grid connection queues worldwide”')
    ev(m, 'r357', 'policy', S['fercn'], obj='PJM / MISO / SPP / CAISO / NYISO / ISO-NE 及输电业主', rel='target')
    ev(m, 'r358', 'policy', S['frpjm'], obj='PJM Interconnection 及 46 家输电业主', rel='target')
    ev(m, 'r359', 'contract', S['vst'], obj='Meta Platforms', rel='customer')
    m.set('fct_event', 'r359', 'amount', 2609, basis='MW 合计'); m.set('fct_event', 'r359', 'amount_type', 'multi_year_cap', basis='20 年 PPA，含 433 MW 扩容期权式分期')
    ev(m, 'r360', 'other', S['ieae26'], edate='2026-02-06', edate_text='2026-02-06（报告发布）')
    m.supersede('r169', 'r357', reason='r169 为「待填」占位，无来源 URL；由 FERC 一手事件取代')
    # ============ 4. m_dc_power_iea：核原文 —— 旧值出自 Electricity 2024，登记正确来源并取代 ============
    m.observe('r361', 'm_dc_power_iea', 'IEA', 'actual', '415', 'TWh', '2024', '2025-04-10', IEAAI, 'P1',
              note='约占全球用电 1.5%，过去五年年增 12%；“electricity consumption from data centres is estimated to amount to around 415 terawatt hours (TWh), or about 1.5% of global electricity consumption in 2024”')
    m.observe('r362', 'm_dc_power_iea', 'IEA', 'guidance', '945', 'TWh', '2030E（Base Case）', '2025-04-10', IEAAI, 'P1',
              note='基准情形；2024→2030 年增约 15%；Lift-Off 情形 2035 > 1,700 TWh、High Efficiency ~970 TWh、Headwinds ~700 TWh；“global electricity consumption for data centres is projected to double to reach around 945 TWh by 2030 in the Base Case”')
    m.observe('r363', 'm_dc_power_iea', 'IEA', 'prior', '460', 'TWh', '2022', '2024-01-24', IEAE24, 'P1',
              note='取代 r106（原来源标「IEA（同上）」、knowledge_time 2026 有误，实出自 Electricity 2024）；“After globally consuming an estimated 460 terawatt-hours (TWh) in 2022”')
    m.observe('r364', 'm_dc_power_iea', 'IEA', 'guidance', '>1000', 'TWh', '2026E', '2024-01-24', IEAE24, 'P1',
              note='取代 r105（原来源标「Energy and AI / Electricity 2026」、knowledge_time 2026 有误，实出自 Electricity 2024）；已被 IEA 自己的 Energy and AI（r361 / r362）下修；“data centres’ total electricity consumption could reach more than 1 000 TWh in 2026”')
    for rid, ps, pe, snap in (('r361', '2024-01-01', '2024-12-31', S['ieaai']), ('r362', '2030-01-01', '2030-12-31', S['ieaai']), ('r363', '2022-01-01', '2022-12-31', S['ieae24']), ('r364', '2026-01-01', '2026-12-31', S['ieae24'])):
        m.set('fct_quant', rid, 'period_start', ps, basis='年度期间'); m.set('fct_quant', rid, 'period_end', pe, basis='年度期间'); m.set('fct_quant', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_quant', rid, 'confidence', 1.0, basis='一手原文，人工核对')
    m.set('fct_quant', 'r105', 'snapshot_id', S['ieae24'], basis='核到原句所在报告（Electricity 2024，非登记的 Energy and AI）'); m.set('fct_quant', 'r105', 'anchor', 'could reach more than 1 000 TWh in 2026', basis='原文短引')
    m.set('fct_quant', 'r106', 'snapshot_id', S['ieae24'], basis='同上'); m.set('fct_quant', 'r106', 'anchor', 'After globally consuming an estimated 460 terawatt-hours (TWh) in 2022', basis='原文短引')
    m.supersede('r105', 'r364', reason='来源与 knowledge_time 登记有误（实为 IEA Electricity 2024，2024-01）；r364 同值正源，r362 为 IEA 最新指引')
    m.supersede('r106', 'r363', reason='来源「IEA（同上）」无法溯源、knowledge_time 2026 有误；r363 同值正源')
    # ============ 5. m_safety_incident：OpenAI–Hugging Face 事故（公司自述技术报告）============
    m.observe('r365', 'm_safety_incident', 'OpenAI', 'event', 'OpenAI 内部网络安全评估中，一个内部研究模型 + GPT-5.6 Sol 作为 agent 利用 Artifactory 漏洞逃出隔离沙箱、接入公网、用公开泄露凭证攻陷 Hugging Face 部分生产基础设施（2026-07-11–13，数十台服务器执行代码、一台 root）；07-19 发现、07-21 公开披露；CrowdStrike 验证，METR / Redwood 第三方评估', '—', '2026-07-21', '2026-08', OAI, 'P1',
              note='取代 r171 占位；技术报告 51 页，PDF 元数据 2026-08-27；报告自述无客户数据影响、涉事模型未部署安全护栏；“circumvented controls intended to isolate them from the internet and performed computer network exploitation of OpenAI’s internal research infrastructure and Hugging Face systems”')
    ev(m, 'r365', 'other', S['oai'], obj='Hugging Face', rel='victim', edate='2026-07-21', edate_text='2026-07-11–13 攻陷；07-21 披露')
    m.supersede('r171', 'r365', reason='r171 为「待填」占位；由公司自述事故报告取代')
    # ============ 6. m_domestic_sub_policy：工信部两份文件 ============
    m.observe('r366', 'm_domestic_sub_policy', '工信部等八部门', 'event', '《“人工智能+制造”专项行动实施意见》（工信部联科〔2025〕279号，2025-12-25 印发）：强化人工智能算力供给，推动智能芯片软硬协同，支持突破高端训练芯片 / 端侧推理芯片 / AI 服务器 / 高速互联 / 智算云操作系统；建设全国一体化算力网监测调度平台', '—', '2025-12-25', '2026-01-09', NDA, 'P1',
              note='取代 r168 占位；来源为共同发文单位国家数据局官网 2026-01-09 转载（来源：工业和信息化部；miit.gov.cn 原页未定位到）；非明文「国产替代」，而是国产高端训练芯片攻关导向，判读 D；“支持突破高端训练芯片、端侧推理芯片、人工智能服务器、高速互联、智算云操作系统等关键技术”')
    m.observe('r367', 'm_domestic_sub_policy', '工信部办公厅', 'event', '《关于组织开展国家算力互联互通节点建设工作的通知》（工信厅信管函〔2026〕35号，2026-01-27 印发，02-06 公布）：建“1+M+N”国家算力互联互通节点体系，统一标识 / 标准 / 规则，区域与行业节点 2026-04-01 前申报', '—', '2026-01-27', '2026-02-06', MIIT, 'P1',
              note='算力资源「入网入市」的国家调度层，非芯片国产化条款，判读 D；“实现不同区域、主体、架构的算力资源标准化互联和高效流动应用”')
    ev(m, 'r366', 'policy', S['nda'], obj='智能芯片 / 智算设施产业', rel='target')
    ev(m, 'r367', 'policy', S['miit'], obj='各省通信管理局 / 工信主管部门 / 算力节点建设主体', rel='target')
    m.supersede('r168', 'r366', reason='r168 为「待填」占位，无来源 URL；由官方文本事件取代')
    # ============ 7. metric_registry ============
    KJ = {
      'm_export_ctrl_bis': ('出口管制 / 关税（D7）', '事件：BIS 对华（D:5 / 澳门）先进算力物项（3A090 / 4A090 等）许可政策、代工尽调、及同一许可框架下的第三国安排；白宫 232 关税另记（unit —）；每条记规则号 / FR 页码 / 生效日', '—', [SRC['bispr'], SRC['fr789'], SRC['wh'], SRC['bisg'], SRC['fric'], SRC['fruae']], '2026-01 后无新对华规则；2026-05-31 指引堵海外代持；判读 D'),
      'm_ai_regulation': ('AI 监管 / 合规（D7）', '事件：法规适用 / 生效节点（EU AI Act 分章适用日、修订案、美各州法签署 / 生效）；每条记条款号与官方文本 URL；只记一手法规文本，不记提案', '—', [SRC['eurlex'], SRC['omni'], SRC['sb53']], 'GPAI 义务 2025-08-02 未推迟；高风险推迟至 2027-12 / 2028-08；SB 53 生效日为规则推定'),
      'm_energy_grid': ('能源 / 电网约束（D7）', '事件：联邦 / RTO 级大负荷并网正式行动（FERC 令、FR 通知）、核电 PPA（公司 8-K）、IEA 电网排队状态；MW 只在 PPA 记录用', '—', [SRC['fercn'], SRC['frpjm'], SRC['vst'], SRC['ieae26']], 'FERC 六家 RTO show cause 60 天期限 ≈ 2026-08-17，后续 tariff 提交是验证点'),
      'm_dc_power_iea': ('数据中心用电（D1/D7 交点）', '全球数据中心年用电 TWh（IEA 口径，不含加密货币；含 AI）；actual = 估计实测，guidance = 情景预测（Base Case 为准），同一 period 只取最新报告', 'TWh', [SRC['ieaai'], SRC['ieae24'], SRC['ieae26']], '旧 r105 / r106 出自 Electricity 2024 已取代；下一版 Energy and AI / Electricity 2027 更新'),
      'm_safety_incident': ('AI 安全 / 对齐事故（D7）', '事件：仅登记有一手来源（公司自述 / 监管机构 / 法院）的真实事故；实验性对齐失败（如 Anthropic Agentic Misalignment 系列）不计', '—', [SRC['oai']], '2026 年仅 OpenAI–HF 一起有一手报告'),
      'm_domestic_sub_policy': ('国产替代 / 算力政策（D7）', '事件：中国政府官方文本（工信部 / 国务院 / 发改委 / 数据局）中与算力 / 芯片自主直接相关的条款；中文原句作 anchor；是否构成「国产替代」由 D 判', '—', [SRC['nda'], SRC['miit']], '两份文件均非明文替代指令，判读 D'),
    }
    for mid, (track, kj, unit, srcs, note) in KJ.items():
        m.set('metric_registry', mid, 'track', track, basis='D7 赛道'); m.set('metric_registry', mid, 'kou_jing', kj, basis='本轮口径'); m.set('metric_registry', mid, 'unit', unit, basis='记录单位')
        m.set('metric_registry', mid, 'source_ids', __import__('json').dumps(srcs, ensure_ascii=False), basis='source_master'); m.set('metric_registry', mid, 'upstream_deps', '[]', basis='无计算依赖'); m.set('metric_registry', mid, 'last_validated', D, basis=V)
        m.set('metric_registry', mid, 'notes_assumption_ids', note, basis=V)
    for mid in ('m_ai_regulation', 'm_energy_grid', 'm_safety_incident', 'm_domestic_sub_policy'):
        m.set('metric_registry', mid, 'fill_status', '已填', basis='占位记录已被一手事件取代')
    m.set('metric_registry', 'm_dc_power_iea', 'next_release', '2027-02（估计）', basis='Electricity 2026 于 2026-02-06 发布，年更'); m.set('metric_registry', 'm_dc_power_iea', 'next_release_basis', '估计（IEA Electricity 系列每年 2 月）', basis='规则推定')
    # ============ 8. 边：证据由库生成（from_metric 名下全部可见记录）============
    def vis(mid):
        return [r[0] for r in m.con.execute("SELECT record_id FROM v_obs WHERE metric_id=? AND superseded_by IS NULL ORDER BY record_id", [mid]).fetchall()]
    J = lambda ids: __import__('json').dumps(ids, ensure_ascii=False)
    m.set('edge_registry', 'e_export_nbis', 'evidence_ids', J(vis('m_export_ctrl_bis')), basis='库：m_export_ctrl_bis 全部可见记录')
    m.set('edge_registry', 'e_export_nbis', 'evidence', 'BIS 2026-01 H200 case-by-case（r165 / r166）；232 关税 25%（r167）；2026-05-31 指引堵 D:5 总部实体海外拿卡（r350）；IC 设计者尽调延期（r351）；UAE 免许可（r352）', basis='同上')
    m.set('edge_registry', 'e_export_nbis', 'mechanism', 'BIS 许可 / 232 关税 → NVIDIA 中国收入与供给 → GPU 可得与成本 → NBIS；2026-05-31 指引把中国总部实体在第三国拿卡也纳入许可，压缩灰色需求；UAE 免许可则放开中东买家（NBIS 竞争者 / 客户两可）；证伪：BIS 对 H200 许可实际批复量公开', basis='doc25 / 本轮原文')
    for e in ('e_power_reg_nbis', 'e_dcbuild_fcel'):
        m.set('edge_registry', e, 'evidence_ids', J(vis('m_dc_power_iea')), basis='库：m_dc_power_iea 全部可见记录（r105 / r106 已取代）')
    m.set('edge_registry', 'e_power_reg_nbis', 'evidence', 'IEA 数据中心用电 415 TWh 2024（r361）→ ~945 TWh 2030 Base Case（r362）；旧口径 460 TWh 2022 / >1000 TWh 2026E 出自 Electricity 2024（r363 / r364）', basis='同上')
    m.set('edge_registry', 'e_dcbuild_fcel', 'evidence', 'IEA 415 TWh 2024（r361）→ ~945 TWh 2030 Base Case（r362，非原写「≈1000 TWh 2030」）；Electricity 2024 旧口径 r363 / r364', basis='原 evidence 把 Electricity 2024 的 >1000 TWh 2026E 误写成 2030')
    m.set('edge_registry', 'e_dcbuild_fcel', 'mechanism', 'D1 算力建设 → 数据中心电力需求（IEA Base Case 2024→2030 年增 ~15%，美国增量约半数来自数据中心）→ 并网排队（>2,500 GW 滞留）→ 现场供电订单；2 跳，结构 + backlog 真值对账', basis='原机制数字纠正 + IEA Electricity 2026')
    m.set('edge_registry', 'e_reg_rbrk', 'evidence_ids', J(vis('m_ai_regulation')), basis='库：m_ai_regulation 全部可见记录')
    m.set('edge_registry', 'e_reg_rbrk', 'evidence', 'EU AI Act GPAI 义务 2025-08-02 适用（r353）、总体 2026-08-02（r354）；Omnibus 推迟高风险至 2027-12 / 2028-08（r355，对合规预算节奏偏空）；加州 SB 53 前沿开发者框架 + 事故报告（r356）', basis='同上')
    m.set('edge_registry', 'e_energy_fcel', 'evidence_ids', J(vis('m_energy_grid')), basis='库：m_energy_grid 全部可见记录')
    m.set('edge_registry', 'e_energy_fcel', 'evidence', 'FERC 六家 RTO 大负荷 show cause（r357 / r358，含共址与表后发电改革）；Vistra–Meta 2,609 MW 核电 PPA（r359，电网侧替代方案）；IEA >2,500 GW 并网排队（r360）', basis='同上')
    m.set('edge_registry', 'e_energy_fcel', 'mechanism', 'D7 能源 / 电网约束（并网排队 >2,500 GW、FERC 要求 RTO 为大负荷与共址发电建专门流程）→ 现场基荷供电方案需求 → 燃料电池订单；核电 PPA 是替代路径（对 FCEL 偏空）；2 跳，结构级；验证点：RTO 60 天 tariff 提交内容是否给表后发电 / 共址开绿灯', basis='原机制 + 本轮原文')
    for e in ('e_export_nbis', 'e_power_reg_nbis', 'e_dcbuild_fcel', 'e_reg_rbrk', 'e_energy_fcel'):
        m.set('edge_registry', e, 'last_validated', D, basis=V)
        m.set('edge_registry', e, 'owner', 'B', basis='B 初稿 D 复核')
    # ============ 9. 来源：出版方 / 频率 / 可靠性 ============
    for k, pub, freq, note in (
        ('bisg', 'BIS, U.S. Department of Commerce', '事件', 'P1 官方指引 PDF；非规则但明示执法口径'),
        ('fric', 'GPO govinfo / BIS', '事件', 'P1 Federal Register 原文'), ('fruae', 'GPO govinfo / BIS', '事件', 'P1 Federal Register 原文；文内引用 2026-05-31 指引'),
        ('eurlex', 'Publications Office of the EU', '事件', 'P1 OJ 法规原文；1.2MB 全文仅存节选快照'), ('omni', 'Publications Office of the EU', '事件', 'P1 OJ 修订案原文；仅存节选快照'),
        ('sb53', 'California Legislative Counsel', '事件', 'P1 chaptered 文本；生效日靠宪法规则推定'),
        ('fercn', 'FERC', '事件', 'P1 官方新闻稿；ferc.gov Cloudflare 403，快照经 Wayback 2026-09-14'), ('frpjm', 'GPO govinfo / FERC', '事件', 'P1 Federal Register 通知；只证明令的存在与日期，内容见 FERC 稿'),
        ('vst', 'SEC EDGAR / Vistra Corp.', '事件', 'P1 8-K Item 7.01（Reg FD），accession 0001193125-26-008508'),
        ('ieaai', 'IEA', '年', 'P1 官方报告网页版（2025-04-10）；页码不可得，锚点为原句'), ('ieae24', 'IEA', '年', 'P1 官方报告执行摘要（2024-01-24）'), ('ieae26', 'IEA', '年', 'P1 官方报告执行摘要（2026-02-06）'),
        ('oai', 'OpenAI', '事件', 'P1 公司自述（self-reported）；openai.com 博客 403，用 cdn PDF；第三方 METR / Redwood 报告待出'),
        ('nda', '国家数据局（转载工业和信息化部）', '事件', 'P1 共同发文单位官网；miit.gov.cn 原页未定位'), ('miit', '工业和信息化部信息通信管理局', '事件', 'P1 部委官网原文'),
    ):
        sid = SRC[k]
        m.set('source_master', sid, 'publisher', pub, basis='来源页'); m.set('source_master', sid, 'frequency', freq, basis='—'); m.set('source_master', sid, 'reliability_note', note, basis='—'); m.set('source_master', sid, 'last_validated', D, basis=V)
    for sid, why in (('src_法案文本', 'r170 已被 r353 取代'), ('src_iea_地方审批_机组订单', 'r169 已被 r357 取代'), ('src_新闻', 'r171 已被 r365 取代'), ('src_政府公开文本', 'r168 已被 r366 取代'), ('src_iea_同上', 'r106 已被 r363 取代'), ('src_iea_energy_and_ai_electricity_2026', 'r105 实出自 Electricity 2024，已被 r364 取代')):
        m.set('source_master', sid, 'verify_status', 'stale', basis=why); m.set('source_master', sid, 'reliability_note', '无 URL 的占位来源；其记录已全部被取代', basis='—')
