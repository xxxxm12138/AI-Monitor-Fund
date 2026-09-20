# -*- coding: utf-8 -*-
"""0015 · D1 算力供给第一轮逐字段填充（四家 hyperscaler capex 统一现金口径 + 上季 / 上年同期 / 指引 · 合计重算 · NVDA DC 收入分项与上季 · 中际旭创 / 新易盛回巨潮原文补一季报与 Q2 计算值 · GPU 按需租价两家云厂价格页 · registry 口径 · 边证据）· owner B · 2026-09-20
一手来源：SEC EDGAR 8-K Ex.99.1（MSFT FY26 Q4 / Q3，AMZN Q2 / Q1 2026，META Q2 / Q1 2026）+ AMZN 10-Q Q2 2026 + Alphabet IR 稿 PDF（Q2 / Q1 2026）+ Microsoft IR 页内嵌电话会 transcript（P2）+ NVIDIA 官方稿 / CFO commentary + 巨潮 static.cninfo.com.cn 原 PDF（带研究 UA 可抓，浏览器 UA 反而 403）+ Nebius / Lambda 官方价格页；19 份新快照，复用 snap_nvda_cfo_q2fy27 / snap_eoptolink_h1_2026（后者与巨潮原 PDF 逐字节一致）。
研究上有意义的四点：① C11 口径统一：四家「现金流量表 purchases of property and equipment 毛额、不含融资租赁」2026Q2 合计 165.05B（上季 129.75B +27.2%，上年同期 88.25B +87.0%），取代原口径混合的 ≈166；
② MSFT FY27 起数据中心折旧年限 15→25 年，更多租赁由融资租赁转经营租赁 → 公司口径 capex（含融资租赁）被压低（CY2026 指引由此调至 ≈175B），现金口径不受影响 —— 跨期比较必须用现金口径；
③ AMZN 10-Q「net additions to PP&E」（含融资租赁与已购未付）63.9B，比现金流量表 54.2B 高 18%，其中 AWS 48.6B（上年 16.0B，+203%）—— 应计口径领先现金口径，是 D1 更早的读数；
④ NVDA DC 收入分项：ACIE（AI clouds / 企业 / 主权，neocloud 所在）40.3B 环比 +25%，快于 Hyperscale 48.7B 的 +13%；中际旭创 / 新易盛 Q2 单季（H1−Q1）分别 222.8 亿（+174.6% / 环比 +14.3%）与 125.7 亿（+96.9% / 环比 +50.8%）。
未找到：AMZN 官方 capex 指引（8-K / 10-Q 均无数字，r101 维持 Motley Fool 转述 P2）；GOOGL 电话会官方 transcript（r098 维持 P2）；NVDA 数据中心分项指引（只有总收入 ±2%）。"""
OWNER = 'B'
V = '本轮逐字段核原文（EDGAR / IR / 巨潮 / 价格页）'
# ---- 来源字符串（URL 均本轮实际抓取）----
MSFT_Q4 = 'Microsoft FY26 Q4 press release https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast'   # 既有来源（r093），快照取 EDGAR 8-K Ex.99.1 同文
MSFT_Q4E = 'Microsoft 8-K Ex.99.1 FY26 Q4 press release (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/789019/000119312526323632/msft-ex99_1.htm'
MSFT_Q3E = 'Microsoft 8-K Ex.99.1 FY26 Q3 press release (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/789019/000119312526191457/msft-ex99_1.htm'
MSFT_CALL = 'Microsoft FY26 Q4 earnings call transcript (IR event page) https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4'
GOOGL_Q2 = 'Alphabet Q2 2026 earnings release https://s206.q4cdn.com/479360582/files/doc_financials/2026/q2/2026q2-alphabet-earnings-release.pdf'   # 既有来源（r096）
GOOGL_Q1 = 'Alphabet Q1 2026 earnings release https://s206.q4cdn.com/479360582/files/doc_financials/2026/q1/2026q1-alphabet-earnings-release.pdf'
AMZN_Q2 = 'Amazon 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/1018724/000101872426000024/amzn-20260630xex991.htm'   # 既有来源（r099）
AMZN_Q1 = 'Amazon 8-K Ex.99.1 Q1 2026 (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm'
AMZN_10Q = 'Amazon 10-Q Q2 2026 net additions to property and equipment (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm'
META_Q2 = 'Meta 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/1326801/000162828026050596/meta-06302026xexhibit991.htm'   # 既有来源（r102）
META_Q1 = 'Meta 8-K Ex.99.1 Q1 2026 (SEC EDGAR) https://www.sec.gov/Archives/edgar/data/1326801/000162828026028364/meta-03312026xexhibit991.htm'
NVDA_Q2PR = 'NVIDIA press release 2026-08-26 https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027'   # 既有来源（r091）
NVDA_Q1PR = 'NVIDIA press release 2026-05-20 Q1 FY27 results https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2027'
NVDA_CFO = 'NVIDIA CFO Commentary Q2 FY27 https://s201.q4cdn.com/141608511/files/doc_financials/2027/Q227/Q2FY27-CFO-Commentary.pdf'
ZJXC_H1 = '中际旭创 2026 半年报摘要（公告 2026-082）https://static.cninfo.com.cn/finalpage/2026-08-22/1225491752.PDF'   # 既有来源（r078–r080）
ZJXC_Q1 = '中际旭创 2026 年一季度报告（公告 2026-042，巨潮）https://static.cninfo.com.cn/finalpage/2026-04-17/1225111941.PDF'
ZJXC_FY = '中际旭创 2025 年年度报告摘要（公告 2026-019，巨潮）https://static.cninfo.com.cn/finalpage/2026-03-31/1225056458.PDF'
EOP_H1 = '新易盛 2026 年半年度报告全文（公告 2026-044，巨潮）https://static.cninfo.com.cn/finalpage/2026-08-25/1225499406.PDF'
EOP_Q1 = '新易盛 2026 年第一季度报告（公告 2026-011，巨潮）https://static.cninfo.com.cn/finalpage/2026-04-24/1225172606.PDF'
EOP_FY = '新易盛 2025 年年度报告摘要（公告 2026-008，巨潮）https://static.cninfo.com.cn/finalpage/2026-04-24/1225172597.PDF'
NEBIUS = 'Nebius AI Cloud pricing page https://nebius.com/prices'
LAMBDA = 'Lambda AI cloud pricing page https://lambda.ai/pricing'
SUM = '计算：四家现金流量表 purchases of property and equipment 毛额之和（分项记录见 note）'
# ---- 快照 ----
S = dict(msft_q4='snap_d1_msft_8k_ex991_q4_fy26', msft_q3='snap_d1_msft_8k_ex991_q3_fy26', msft_call='snap_d1_msft_call_fy26_q4',
         googl_q2='snap_d1_googl_er_2026q2', googl_q1='snap_d1_googl_er_2026q1', amzn_q2='snap_d1_amzn_8k_ex991_2026q2', amzn_q1='snap_d1_amzn_8k_ex991_2026q1', amzn_10q='snap_d1_amzn_10q_2026q2_ppe',
         meta_q2='snap_d1_meta_8k_ex991_2026q2', meta_q1='snap_d1_meta_8k_ex991_2026q1', nvda_q2='snap_d1_nvda_pr_q2_fy27', nvda_q1='snap_d1_nvda_pr_q1_fy27', nvda_cfo='snap_nvda_cfo_q2fy27',
         zjxc_h1='snap_d1_zjxc_h1_2026_summary', zjxc_q1='snap_d1_zjxc_q1_2026', zjxc_fy='snap_d1_zjxc_fy2025_summary', eop_h1='snap_eoptolink_h1_2026', eop_q1='snap_d1_eop_q1_2026', eop_fy='snap_d1_eop_fy2025_summary',
         nebius='snap_d1_nebius_prices', lambda_='snap_d1_lambda_pricing')
# ---- 来源 id（core.slug）----
SRC = dict(msft_q4='src_microsoft_fy26_q4_press_release', msft_q4e='src_microsoft_8_k_ex_99_1_fy26_q4_press_release_sec_', msft_q3e='src_microsoft_8_k_ex_99_1_fy26_q3_press_release_sec_', msft_call='src_microsoft_fy26_q4_earnings_call_transcript_ir_ev', msft_call_old='src_microsoft_电话会',
           googl_q2='src_alphabet_q2_2026_earnings_release', googl_q1='src_alphabet_q1_2026_earnings_release', googl_call='src_alphabet_电话会',
           amzn_q2='src_amazon_8_k_ex_99_1', amzn_q1='src_amazon_8_k_ex_99_1_q1_2026_sec_edgar', amzn_10q='src_amazon_10_q_q2_2026_net_additions_to_property_an', amzn_call='src_amazon_电话会_transcript_motley_fool_转载',
           meta_q2='src_meta_8_k_ex_99_1', meta_q1='src_meta_8_k_ex_99_1_q1_2026_sec_edgar',
           nvda_q2='src_nvidia_press_release_2026_08_26', nvda_q1='src_nvidia_press_release_2026_05_20_q1_fy27_results', nvda_cfo='src_nvidia_cfo_commentary_q2_fy27',
           zjxc_h1='src_中际旭创_2026_半年报摘要_公告_2026_082', zjxc_q1='src_中际旭创_2026_年一季度报告_公告_2026_042_巨潮', zjxc_fy='src_中际旭创_2025_年年度报告摘要_公告_2026_019_巨潮',
           eop_h1='src_新易盛_2026_年半年度报告全文_公告_2026_044_巨潮', eop_q1='src_新易盛_2026_年第一季度报告_公告_2026_011_巨潮', eop_fy='src_新易盛_2025_年年度报告摘要_公告_2026_008_巨潮',
           nebius='src_nebius_ai_cloud_pricing_page', lambda_='src_lambda_ai_cloud_pricing_page')
def J(*ids): return '[' + ', '.join(f'"{i}"' for i in ids) + ']'
def pct(a, b): return round(a / b - 1, 4)

def up(m):
    # ============ 1. 四家 capex：统一现金口径的 actual / prior / guidance ============
    # MSFT（财年 7–6 月；FY26 Q4 = 2026 年 4–6 月）
    m.observe('r300', 'm_capex_msft', 'MSFT', 'prior', '30.876', 'USD B 现金 capex', 'FY26 Q3（截止 2026-03-31）', '2026-04-29', MSFT_Q3E, 'P1',
              note='YoY +84.4%（上年同期 16,745）；现金流量表“Additions to property and equipment | (30,876) | (16,745)”')
    m.observe('r311', 'm_capex_msft', 'MSFT', 'prior', '17.079', 'USD B 现金 capex', 'FY25 Q4（截止 2025-06-30）', '2026-07-29', MSFT_Q4E, 'P1',
              note='FY26 Q4 稿上年同期列；FY25 全年 64,551 / FY26 全年 115,948（+79.6%）；“Additions to property and equipment | (35,802) | (17,079) | (115,948) | (64,551)”')
    m.observe('r301', 'm_capex_msft', 'MSFT', 'guidance', 'over 50', 'USD B capex 含融资租赁', 'FY27 Q1（截止 2026-09-30）', '2026-07-29', MSFT_CALL, 'P2',
              note='CFO Amy Hood 电话会口径，含融资租赁并含折旧年限调整引起的租赁重分类影响；FY27 全年“capital expenditures will grow year-over-year”；“We expect CapEx spend will be over $50 billion including the lease reclassification impact from the useful life update”')
    # GOOGL（自然季度；只有现金口径）
    m.observe('r302', 'm_capex_googl', 'GOOGL', 'prior', '35.674', 'USD B', '2026Q1', '2026-04-29', GOOGL_Q1, 'P1',
              note='YoY +107.4%（上年同期 17,197）；现金流量表“Purchases of property and equipment | (17,197) | (35,674)”')
    # AMZN（三口径：毛额 / 净额 cash capex / 10-Q 应计净增）
    m.observe('r303', 'm_capex_amzn', 'AMZN', 'prior', '44.203', 'USD B PP&E 购置', '2026Q1', '2026-04-29', AMZN_Q1, 'P1',
              note='YoY +76.7%（上年同期 25,019）；净额 cash capex = 44,203 − 969 = 43,234；“Purchases of property and equipment | (25,019) | (44,203)”')
    m.observe('r306', 'm_capex_amzn', 'AMZN', 'prior', '32.183', 'USD B PP&E 购置', '2025Q2', '2026-07-30', AMZN_Q2, 'P1',
              note='Q2 2026 稿上年同期列；净额 = 32,183 − 815 = 31,368；“Purchases of property and equipment | (32,183) | (54,208)”')
    m.observe('r304', 'm_capex_amzn', 'AMZN', 'actual', '53.076', 'USD B cash capex（净额）', '2026Q2', '2026-07-30', AMZN_Q2, 'P1',
              note='取代 r100（Motley Fool 转述 53.1，P2）：= 54,208 − 1,132 = 53,076，即 8-K FCF 定义的“Purchases of property and equipment, net of proceeds from sales and incentives”；YoY +69.2%（上年 31,368）、QoQ +22.8%（上季 43,234）；TTM 169,007（+64%）')
    m.observe('r305', 'm_capex_amzn', 'AMZN', 'actual', '63.891', 'USD B 净增 PP&E（10-Q 应计口径，含融资租赁与已购未付）', '2026Q2', '2026-07-30', AMZN_10Q, 'P1',
              note='YoY +107.7%（上年 30,761）；其中 AWS 48,604（上年 16,043，+203%）、北美 12,139、国际 2,540；比现金流量表毛额 54,208 高 17.9% → 应计口径领先现金口径；“Total net additions to property and equipment include technology infrastructure assets and the effect of non-cash activity such as property and equipment acquired but not yet paid”')
    # META（公司口径 = PP&E + 融资租赁本金；C11 统一口径只取 PP&E）
    m.observe('r310', 'm_capex_meta', 'META', 'actual', '30.116', 'USD B 现金 PP&E 购置（不含融资租赁本金）', '2026Q2', '2026-07-29', META_Q2, 'P1',
              note='YoY +82.1%（上年 16,538）、QoQ +58.5%（上季 18,997）；公司自报 capex 31.078 = 30,116 + 融资租赁本金 962（r102）；“Purchases of property and equipment | (30,116) | (16,538) | (49,113) | (29,479)”')
    m.observe('r307', 'm_capex_meta', 'META', 'prior', '18.997', 'USD B 现金 PP&E 购置（不含融资租赁本金）', '2026Q1', '2026-04-29', META_Q1, 'P1',
              note='YoY +46.8%（上年 12,941）；含融资租赁本金 843 后 = 19,840（公司口径）；“Purchases of property and equipment | (18,997) | (12,941)”')
    m.observe('r308', 'm_capex_meta', 'META', 'prior', '16.538', 'USD B 现金 PP&E 购置（不含融资租赁本金）', '2025Q2', '2026-07-29', META_Q2, 'P1',
              note='Q2 2026 稿上年同期列；含融资租赁本金 474 后 = 17,012；“Principal payments on finance leases | (962) | (474) | (1,805) | (1,225)”')
    m.observe('r309', 'm_capex_meta', 'META', 'guidance', '125–145', 'USD B', 'FY2026（Q1 版指引）', '2026-04-29', META_Q1, 'P1',
              note='预期基准：Q2 收窄至 130–145（r103）；Q1 版自 115–135 上调，理由为元件涨价；“We anticipate 2026 capital expenditures, including principal payments on finance leases, to be in the range of $125-145 billion, increased from our prior range of $115-135 billion”')
    # ============ 2. 四家合计：同口径重算（现金流量表 PP&E 毛额，不含融资租赁）============
    m.observe('r312', 'm_hyperscaler_capex', 'MSFT / GOOGL / AMZN / META', 'computed', '165.050', 'USD B 现金 PP&E 购置合计（不含融资租赁）', '2026Q2', '2026-07-30', SUM, 'P1',
              note='= MSFT 35.802（r093）+ GOOGL 44.924（r096）+ AMZN 54.208（r099）+ META 30.116（r310）= 165.050；取代 r104（≈166 口径混合：MSFT 现金 + META 含融资租赁）；YoY +87.0%（r314）、QoQ +27.2%（r313）；C11 统一口径')
    m.observe('r313', 'm_hyperscaler_capex', 'MSFT / GOOGL / AMZN / META', 'computed', '129.750', 'USD B 现金 PP&E 购置合计（不含融资租赁）', '2026Q1', '2026-04-29', SUM, 'P1',
              note='= MSFT FY26 Q3 30.876（r300）+ GOOGL 35.674（r302）+ AMZN 44.203（r303）+ META 18.997（r307）= 129.750')
    m.observe('r314', 'm_hyperscaler_capex', 'MSFT / GOOGL / AMZN / META', 'computed', '88.246', 'USD B 现金 PP&E 购置合计（不含融资租赁）', '2025Q2', '2026-07-30', SUM, 'P1',
              note='= MSFT FY25 Q4 17.079（r311）+ GOOGL 22.446（r097）+ AMZN 32.183（r306）+ META 16.538（r308）= 88.246')
    # ============ 3. NVDA 数据中心收入：上季 / 上年 / 分项 / Q1 版指引 ============
    m.observe('r315', 'm_gpu_ship', 'NVDA', 'prior', '75.2', 'USD B 数据中心收入', 'Q1 FY27（截止 2026-04-26）', '2026-05-20', NVDA_Q1PR, 'P1',
              note='YoY +92%；CFO commentary Q2 FY27 重列精确值 75,246（含分类调整）；“Record Data Center revenue of $75.2 billion, up 92% from a year ago”')
    m.observe('r319', 'm_gpu_ship', 'NVDA', 'prior', '41.096', 'USD B 数据中心收入', 'Q2 FY26（截止 2025-07-27）', '2026-08-26', NVDA_CFO, 'P1',
              note='Q2 FY27 CFO commentary 上年同期列（经 Hyperscale / ACIE 分类重列）；“Data Center | $89,023 | $75,246 | $41,096 | 18 % | 117 %”')
    m.observe('r316', 'm_gpu_ship', 'NVDA', 'actual', '40.313', 'USD B 数据中心 ACIE 收入（AI clouds / 工业 / 企业 / 主权）', 'Q2 FY27（截止 2026-07-26）', '2026-08-26', NVDA_CFO, 'P1',
              note='YoY +138%、QoQ +25%（上季 32,196、上年 16,928）；neocloud 客户所在分项，增速快于 Hyperscale；本季有一家客户由 ACIE 重分类至 Hyperscale 并重列前期；“ACIE revenue increased 138% from a year ago and 25% sequentially driven by end-demand from AI natives, enterprises, and sovereign customers, as well as hyperscalers utilizing AI clouds”')
    m.observe('r317', 'm_gpu_ship', 'NVDA', 'actual', '48.710', 'USD B 数据中心 Hyperscale 收入', 'Q2 FY27（截止 2026-07-26）', '2026-08-26', NVDA_CFO, 'P1',
              note='YoY +102%、QoQ +13%（上季 43,050、上年 24,168）；“Hyperscale revenue more than doubled from a year ago and increased 13% sequentially on the strength of Blackwell Ultra”')
    m.observe('r318', 'm_gpu_ship', 'NVDA', 'guidance', '91.0 ± 2%', 'USD B 总收入', 'Q2 FY27（Q1 版指引）', '2026-05-20', NVDA_Q1PR, 'P1',
              note='预期基准：Q2 实际 96.2 高出指引中值 5.7%；同样不含中国 DC compute；“Revenue is expected to be $91.0 billion, plus or minus 2%. NVIDIA is not assuming any Data Center compute revenue from China in its outlook”')
    # ============ 4. 中际旭创：巨潮原文 一季报 / 年报摘要 / Q2 计算值 ============
    m.observe('r320', 'm_cn_optics_zte', '中际旭创', 'actual', '19,496,398,083.95', 'CNY 营收', '2026Q1', '2026-04-17', ZJXC_Q1, 'P1',
              note='取代 r081（同值、无 URL）；YoY +192.12%；“营业收入（元） | 19,496,398,083.95 | 6,674,176,487.23 | 192.12%”')
    m.observe('r321', 'm_cn_optics_zte', '中际旭创', 'actual', '5,734,501,526.83', 'CNY 归母净利', '2026Q1', '2026-04-17', ZJXC_Q1, 'P1',
              note='YoY +262.28%（上年 1,582,876,128.67）；扣非 5,717,748,340.78（+264.56%）；“归属于上市公司股东的净利润（元） 5,734,501,526.83 1,582,876,128.67 262.28%”')
    m.observe('r322', 'm_cn_optics_zte', '中际旭创', 'prior', '38,239,935,640.67', 'CNY 营收', '2025 全年', '2026-03-31', ZJXC_FY, 'P1',
              note='取代 r082（新浪转述 382 亿）；YoY +60.25%；归母净利 10,797,254,300.45（+108.78%）；“报告期内，公司实现营业收入 382.40 亿元，同比增长 60.25%”')
    m.observe('r324', 'm_cn_optics_zte', '中际旭创', 'prior', '8,114,898,350.57', 'CNY 营收', '2025Q2', '2026-03-31', ZJXC_FY, 'P1',
              note='年报摘要分季度表第二季度列；2025 四季分别 6,674.18 / 8,114.90 / 10,215.73 / 13,235.13（百万）；“营业收入 6,674,176,487.23 8,114,898,350.57 10,215,726,013.52 13,235,134,789.35”')
    m.observe('r323', 'm_cn_optics_zte', '中际旭创', 'computed', '22,281,463,711.08', 'CNY 营收', '2026Q2', '2026-08-22', ZJXC_H1, 'P1',
              note='= H1 41,777,861,795.03（r078）− Q1 19,496,398,083.95（r320）；YoY +174.6%（上年 Q2 8,114,898,350.57，r324）、QoQ +14.3%；单季环比增速明显放缓（Q1 环比 2025Q4 为 +47.3%）')
    # ============ 5. 新易盛：巨潮原链取代新浪镜像 + 一季报 / 年报摘要 / Q2 计算值 ============
    m.observe('r325', 'm_cn_optics_eoptolink', '新易盛', 'actual', '20,909,746,962.20', 'CNY 营收', '2026H1', '2026-08-25', EOP_H1, 'P1',
              note='取代 r083（同值，来源为新浪镜像链路）：巨潮原 PDF 与既有快照逐字节一致；YoY +100.34%；境外收入 20,474,923,217.01（占 97.9%）；“营业收入（元） 20,909,746,962.20 10,437,170,265.50 10,437,170,265.50 100.34%”')
    m.observe('r326', 'm_cn_optics_eoptolink', '新易盛', 'actual', '7,529,168,039.39', 'CNY 归母净利', '2026H1', '2026-08-25', EOP_H1, 'P1',
              note='取代 r084（同值，镜像链路）；YoY +90.98%（上年 3,942,294,268.37）')
    m.observe('r327', 'm_cn_optics_eoptolink', '新易盛', 'prior', '10,437,170,265.50', 'CNY 营收', '2025H1', '2026-08-25', EOP_H1, 'P1',
              note='取代 r085（同值，镜像链路）；半年报上年同期列（调整前 / 后一致）')
    m.observe('r328', 'm_cn_optics_eoptolink', '新易盛', 'actual', '8,337,902,040.74', 'CNY 营收', '2026Q1', '2026-04-24', EOP_Q1, 'P1',
              note='YoY +105.76%；“营业收入（元） 8,337,902,040.74 4,052,256,538.37 105.76%”')
    m.observe('r329', 'm_cn_optics_eoptolink', '新易盛', 'actual', '2,780,222,960.23', 'CNY 归母净利', '2026Q1', '2026-04-24', EOP_Q1, 'P1',
              note='YoY +76.80%（上年 1,572,525,789.22）；扣非 2,767,975,248.13（+76.44%）；净利增速显著低于营收增速')
    m.observe('r330', 'm_cn_optics_eoptolink', '新易盛', 'prior', '24,841,854,840.22', 'CNY 营收', '2025 全年', '2026-04-24', EOP_FY, 'P1',
              note='取代 r086（semisino 转述 248 亿）；YoY +187.29%；归母净利 9,531,922,730.17（+235.89%）')
    m.observe('r332', 'm_cn_optics_eoptolink', '新易盛', 'prior', '6,384,913,727.13', 'CNY 营收', '2025Q2', '2026-04-24', EOP_FY, 'P1',
              note='年报摘要分季度表第二季度列；2025 四季分别 4,052.26 / 6,384.91 / 6,067.62 / 8,337.06（百万）；“营业收入 4,052,256,538.37 6,384,913,727.13 6,067,620,945.86 8,337,063,628.86”')
    m.observe('r331', 'm_cn_optics_eoptolink', '新易盛', 'computed', '12,571,844,921.46', 'CNY 营收', '2026Q2', '2026-08-25', EOP_H1, 'P1',
              note='= H1 20,909,746,962.20（r325）− Q1 8,337,902,040.74（r328）；YoY +96.9%（上年 Q2 6,384,913,727.13，r332）、QoQ +50.8%；与中际旭创 Q2 环比 +14.3% 形成反差')
    # ============ 6. GPU 按需租价：两家云厂官方价格页（P1；页面无日期 → 抓取日）============
    m.observe('r333', 'm_gpu_rental_price', 'Nebius（NBIS）', 'actual', '3.85', 'USD/GPU-hr H100 按需（Nebius HGX H100，16 vCPU / 200 GB）', '2026-09-20', '2026-09-20', NEBIUS, 'P1',
              note='取代 r173 占位；抢占式 2.15；同页 H200 4.50 / 2.45、B200 7.15 / 3.95、B300 7.85 / 4.30（按需 / 抢占式）；承诺折扣“up to 35% less than on-demand rates”；不含税、出口流量免费；“NVIDIA HGX H100 | 16 | 200 | $2.15 | $3.85”')
    m.observe('r334', 'm_gpu_rental_price', 'Nebius（NBIS）', 'actual', '7.15', 'USD/GPU-hr B200 按需（Nebius HGX B200，20 vCPU / 224 GB）', '2026-09-20', '2026-09-20', NEBIUS, 'P1',
              note='抢占式 3.95；B200 / H100 按需价比 1.86×；“NVIDIA HGX B200 | 20 | 224 | $3.95 | $7.15”')
    m.observe('r335', 'm_gpu_rental_price', 'Lambda', 'actual', '3.99', 'USD/GPU-hr H100 SXM 按需（Lambda 8x 实例，含 22 TiB 本地 SSD）', '2026-09-20', '2026-09-20', LAMBDA, 'P1',
              note='1x–4x 实例 4.09–4.29；1-Click Clusters（2 周–1 年，16–256 GPU）5.54–6.16 反而更贵（含集群网络）；不含税；“NVIDIA H100 SXM | 80 GB | 208 | 1800 GiB | 22 TiB SSD | $3.99”')
    m.observe('r336', 'm_gpu_rental_price', 'Lambda', 'actual', '6.69', 'USD/GPU-hr B200 SXM6 按需（Lambda 8x 实例，含 22 TiB 本地 SSD）', '2026-09-20', '2026-09-20', LAMBDA, 'P1',
              note='1-Click Clusters B200 8.87–9.86；B200 / H100 按需价比 1.68×；“NVIDIA B200 SXM6 | 180 GB | 208 | 2900 GiB | 22 TiB SSD | $6.69”')
    # ============ 取代（旧行不删）============
    m.supersede('r100', 'r304', reason='Motley Fool 转述 P2 → 8-K 现金流量表可直接算出净额 53,076（P1）')
    m.supersede('r104', 'r312', reason='原合计口径混合（MSFT 现金 / META 含融资租赁，P5）→ 四家统一现金流量表 PP&E 毛额重算 165.050（C11）')
    m.supersede('r081', 'r320', reason='原记录无 URL / 无快照；巨潮原 PDF 钉为公告 2026-042，日期 2026-04-17')
    m.supersede('r082', 'r322', reason='新浪转述 P3 → 巨潮年报摘要原文 P1（382.40 亿精确值 38,239,935,640.67）')
    m.supersede('r083', 'r325', reason='新浪镜像链路 P3 → 巨潮原链（同文，快照已逐字节核对）')
    m.supersede('r084', 'r326', reason='同上')
    m.supersede('r085', 'r327', reason='同上')
    m.supersede('r086', 'r330', reason='semisino 转述 P3 → 巨潮年报摘要原文 P1')
    m.supersede('r173', 'r333', reason='「待填」占位 → Nebius / Lambda 官方价格页 P1')

    # ============ 7. fct_quant：期间 / 快照 / 置信 / 锚点 / 同比环比 ============
    P = {'2026Q2': ('2026-04-01', '2026-06-30'), '2026Q1': ('2026-01-01', '2026-03-31'), '2025Q2': ('2025-04-01', '2025-06-30'), '2026H1': ('2026-01-01', '2026-06-30'), '2025H1': ('2025-01-01', '2025-06-30'),
         'FY2025': ('2025-01-01', '2025-12-31'), 'FY2026': ('2026-01-01', '2026-12-31'), 'FY27Q1': ('2026-07-01', '2026-09-30'), 'FY27': ('2026-07-01', '2027-06-30'),
         'NQ2FY27': ('2026-04-27', '2026-07-26'), 'NQ1FY27': ('2026-01-26', '2026-04-26'), 'NQ2FY26': ('2025-04-28', '2025-07-27'), 'NQ3FY27': ('2026-07-27', '2026-10-25'), 'DAY': (None, '2026-09-20')}
    Q = {  # rid: (period key, snapshot, anchor(None=note 已抽), qoq, yoy, basis for qoq)
      # 既有 actual / guidance 补字段
      'r093': ('2026Q2', S['msft_q4'], 'Additions to property and equipment | (35,802) | (17,079) | (115,948) | (64,551)', pct(35802, 30876), pct(35802, 17079)),
      'r094': ('2026Q2', S['msft_call'], 'Capital expenditures were $41 billion including the impact from higher component pricing as noted in our guide … total finance leases were $5.6 billion … And cash paid for P, P, and E was $35.8 billion', None, None),
      'r095': ('FY2026', S['msft_call'], 'the shift from finance to operating leases adjusts our expectation to approximately $175 billion', None, None),
      'r096': ('2026Q2', S['googl_q2'], 'Purchases of property and equipment | (22,446) | (44,924) | (39,643) | (80,598)', pct(44924, 35674), pct(44924, 22446)),
      'r097': ('2025Q2', S['googl_q2'], None, None, None),
      'r099': ('2026Q2', S['amzn_q2'], 'Purchases of property and equipment | (32,183) | (54,208) | (57,202) | (98,411) | (107,656) | (173,028)', pct(54208, 44203), pct(54208, 32183)),
      'r102': ('2026Q2', S['meta_q2'], 'Purchases of property and equipment | (30,116) | (16,538) … Principal payments on finance leases | (962) | (474)', pct(31078, 19840), pct(31078, 17012)),
      'r103': ('FY2026', S['meta_q2'], 'We anticipate 2026 capital expenditures, including principal payments on finance leases, to be in the range of $130-145 billion, narrowed from our prior outlook of $125-145 billion', None, None),
      'r091': ('NQ2FY27', S['nvda_q2'], 'Data Center revenue of $89.0 billion, up 117% from a year ago', pct(89023, 75246), pct(89023, 41096)),
      'r092': ('NQ3FY27', S['nvda_q2'], None, None, None),
      'r078': ('2026H1', S['zjxc_h1'], '营业收入（元） 41,777,861,795.03 14,789,074,837.80 182.49%', None, 1.8249),
      'r079': ('2026H1', S['zjxc_h1'], '归属于上市公司股东的净利润（元） 13,651,149,693.27 3,995,115,384.70 241.70%', None, 2.4170),
      'r080': ('2026H1', S['zjxc_h1'], None, None, 2.099),
      # 新记录
      'r300': ('2026Q1', S['msft_q3'], None, None, pct(30876, 16745)), 'r311': ('2025Q2', S['msft_q4'], None, None, None), 'r301': ('FY27Q1', S['msft_call'], None, None, None),
      'r302': ('2026Q1', S['googl_q1'], None, None, pct(35674, 17197)),
      'r303': ('2026Q1', S['amzn_q1'], None, None, pct(44203, 25019)), 'r306': ('2025Q2', S['amzn_q2'], None, None, None),
      'r304': ('2026Q2', S['amzn_q2'], 'Purchases of property and equipment, net of proceeds from sales and incentives', pct(53076, 43234), pct(53076, 31368)),
      'r305': ('2026Q2', S['amzn_10q'], 'AWS (2) | 16,043 | 48,604 | 36,507 | 90,120 … Consolidated | $ | 30,761 | $ | 63,891', None, pct(63891, 30761)),
      'r310': ('2026Q2', S['meta_q2'], None, pct(30116, 18997), pct(30116, 16538)), 'r307': ('2026Q1', S['meta_q1'], None, None, pct(18997, 12941)), 'r308': ('2025Q2', S['meta_q2'], None, None, None), 'r309': ('FY2026', S['meta_q1'], None, None, None),
      'r312': ('2026Q2', None, None, pct(165.050, 129.750), pct(165.050, 88.246)), 'r313': ('2026Q1', None, None, None, None), 'r314': ('2025Q2', None, None, None, None),
      'r315': ('NQ1FY27', S['nvda_q1'], None, None, 0.92), 'r319': ('NQ2FY26', S['nvda_cfo'], None, None, None),
      'r316': ('NQ2FY27', S['nvda_cfo'], None, pct(40313, 32196), pct(40313, 16928)), 'r317': ('NQ2FY27', S['nvda_cfo'], None, pct(48710, 43050), pct(48710, 24168)), 'r318': ('NQ2FY27', S['nvda_q1'], None, None, None),
      'r320': ('2026Q1', S['zjxc_q1'], None, None, 1.9212), 'r321': ('2026Q1', S['zjxc_q1'], None, None, 2.6228), 'r322': ('FY2025', S['zjxc_fy'], None, None, 0.6025), 'r324': ('2025Q2', S['zjxc_fy'], None, None, None),
      'r323': ('2026Q2', S['zjxc_h1'], None, pct(22281463711.08, 19496398083.95), pct(22281463711.08, 8114898350.57)),
      'r325': ('2026H1', S['eop_h1'], None, None, 1.0034), 'r326': ('2026H1', S['eop_h1'], None, None, 0.9098), 'r327': ('2025H1', S['eop_h1'], None, None, None),
      'r328': ('2026Q1', S['eop_q1'], None, None, 1.0576), 'r329': ('2026Q1', S['eop_q1'], None, None, 0.7680), 'r330': ('FY2025', S['eop_fy'], None, None, 1.8729), 'r332': ('2025Q2', S['eop_fy'], None, None, None),
      'r331': ('2026Q2', S['eop_h1'], None, pct(12571844921.46, 8337902040.74), pct(12571844921.46, 6384913727.13)),
      'r333': ('DAY', S['nebius'], None, None, None), 'r334': ('DAY', S['nebius'], None, None, None), 'r335': ('DAY', S['lambda_'], None, None, None), 'r336': ('DAY', S['lambda_'], None, None, None),
    }
    for rid, (pk, snap, anchor, qoq, yoy) in Q.items():
        if P[pk][0]: m.set('fct_quant', rid, 'period_start', P[pk][0], basis='期间解析（MSFT 财年季 → 自然季；NVDA 财季按 10-Q 期末日）')
        m.set('fct_quant', rid, 'period_end', P[pk][1], basis='期间解析')
        if snap: m.set('fct_quant', rid, 'snapshot_id', snap, basis='快照（r093 取 EDGAR 8-K Ex.99.1 同文；r078–r080 巨潮 PDF 本轮 curl 重抓，与既有 snap_zjxc_h1_2026_summary 一致）')
        if anchor: m.set('fct_quant', rid, 'anchor', anchor, basis='原文短引')
        if qoq is not None: m.set('fct_quant', rid, 'qoq', qoq, basis='与上季同口径记录计算（见 note）')
        if yoy is not None: m.set('fct_quant', rid, 'yoy', yoy, basis='原文 YoY 或上年同期列计算')
    for rid in Q:
        prov = m.con.execute('SELECT provenance FROM fct_quant WHERE record_id=?', [rid]).fetchone()[0]
        m.set('fct_quant', rid, 'confidence', 1.0 if prov == 'P1' else 0.9, basis='一手原文人工核对 1.0；官方 transcript 口径 0.9')
    for rid in ('r312', 'r313', 'r314'):
        m.set('fct_quant', rid, 'conversion_assumption', '四家现金流量表「purchases of / additions to property and equipment」毛额直接相加，不扣 AMZN 处置与激励收入、不加 META / MSFT 融资租赁；MSFT 财年季映射到自然季', basis='C11 统一口径')
        m.set('fct_quant', rid, 'assumption_source', '假设 C11；各家 8-K / earnings release 现金流量表（r093 r096 r099 r310 / r300 r302 r303 r307 / r311 r097 r306 r308）', basis='—')
    for rid in ('r323', 'r331'):
        m.set('fct_quant', rid, 'conversion_assumption', '单季 = 半年报累计 − 一季报累计（元，未审 / 未审）', basis='中国上市公司季报为累计披露')
        m.set('fct_quant', rid, 'assumption_source', '半年报摘要 + 一季度报告原文', basis='—')
    m.set('fct_quant', 'r309', 'revision_flag', 'revised', basis='Q1 版自 115–135 上调'); m.set('fct_quant', 'r103', 'revision_flag', 'revised', basis='对照 Q1 版 125–145（r309）：下限上调')
    m.set('fct_quant', 'r318', 'revision_flag', 'initial', basis='Q1 版指引'); m.set('fct_quant', 'r301', 'revision_flag', 'initial', basis='首版')

    # ============ 8. metric_registry：赛道 / 口径 / 单位 / 来源 / 依赖 / 复验 ============
    TRK = {'capex': 'hyperscaler 云基础设施 capex（D1 算力供给）', 'gpu': 'AI 加速器（D1 算力供给）', 'optics': '高速光模块（D1 算力供给，中国供应链）', 'rent': 'GPU 云租赁价（D1 算力供给 / 供需价格）'}
    KJ = {
      'm_capex_msft': (TRK['capex'], 'capex 两口径：① 现金 capex = 现金流量表「Additions to property and equipment」（FY26 Q4 35.802B）；② 公司电话会口径 = ① + 融资租赁新增（41B，融资租赁 5.6B）。财年 7–6 月，FY26 Q4 = 2026 年 4–6 月。FY27 起数据中心 / 办公楼折旧年限 15→25 年，更多租赁由融资租赁转经营租赁 → ②被压低（CY2026 指引由此调至 ≈175B），①不受影响 —— C11 合计用 ①', 'USD B',
                       J(SRC['msft_q4'], SRC['msft_q4e'], SRC['msft_q3e'], SRC['msft_call']), '[]'),
      'm_capex_googl': (TRK['capex'], '现金流量表「Purchases of property and equipment」= 现金 capex（Alphabet 定义 FCF 用同一行）；财报不单列融资租赁新增，故只有现金口径；自然季度；FY 指引为电话会口径（r098，含租赁与否未明示）', 'USD B',
                        J(SRC['googl_q2'], SRC['googl_q1'], SRC['googl_call']), '[]'),
      'm_capex_amzn': (TRK['capex'], '三口径：① 现金流量表「Purchases of property and equipment」毛额（Q2 54.208B）；② cash capex = ① − 「Proceeds from property and equipment sales and incentives」（53.076B，= 8-K FCF 定义与管理层口径）；③ 10-Q「Total net additions to property and equipment」应计口径，含融资租赁与已购未付（63.891B，AWS 48.604B）。C11 合计用 ①；③ 领先 ①', 'USD B',
                       J(SRC['amzn_q2'], SRC['amzn_q1'], SRC['amzn_10q'], SRC['amzn_call']), '[]'),
      'm_capex_meta': (TRK['capex'], 'Meta 自报 capex = 「Purchases of property and equipment」+「Principal payments on finance leases」（Q2 31.078 = 30.116 + 0.962）；FY 指引为该含融资租赁本金口径；C11 合计只取 PP&E 行（r310 / r307 / r308）', 'USD B',
                       J(SRC['meta_q2'], SRC['meta_q1']), '[]'),
      'm_hyperscaler_capex': (TRK['capex'], '四家现金流量表 purchases of property and equipment 毛额之和（均不含融资租赁；MSFT 财年季映射自然季）；含融资租赁的合计无法统一（GOOGL 不披露）→ C11 按现金口径统一；2026Q2 165.050 / 2026Q1 129.750 / 2025Q2 88.246', 'USD B',
                              J(SRC['msft_q4'], SRC['googl_q2'], SRC['amzn_q2'], SRC['meta_q2']), '["m_capex_msft", "m_capex_googl", "m_capex_amzn", "m_capex_meta"]'),
      'm_gpu_ship': (TRK['gpu'], 'NVIDIA 数据中心收入（Market Platform 口径，含 compute + networking；unit 区分总额 / Hyperscale / ACIE 分项）；ACIE = AI clouds, industrial & enterprise（neocloud、企业、主权）；指引只给公司总收入 ±2%，不给 DC 分项；财季期末约 1 月底 / 4 月底 / 7 月底 / 10 月底', 'USD B',
                     J(SRC['nvda_q2'], SRC['nvda_cfo'], SRC['nvda_q1']), '[]'),
      'm_cn_optics_zte': (TRK['optics'], '公司口径营业收入 / 归母净利润（元，中国会计准则，季报累计披露）；半年报 / 一季报 / 年报摘要取巨潮 static.cninfo.com.cn 原 PDF；Q2 单季 = H1 − Q1 计算值；海外业务收入取半年报经营讨论段', 'CNY',
                          J(SRC['zjxc_h1'], SRC['zjxc_q1'], SRC['zjxc_fy']), '[]'),
      'm_cn_optics_eoptolink': (TRK['optics'], '公司口径营业收入 / 归母净利润（元，中国会计准则，季报累计披露）；半年报全文 / 一季报 / 年报摘要取巨潮原 PDF（新浪镜像已弃用）；Q2 单季 = H1 − Q1 计算值；境外收入取半年报分地区表', 'CNY',
                                J(SRC['eop_h1'], SRC['eop_q1'], SRC['eop_fy']), '[]'),
      'm_gpu_rental_price': (TRK['rent'], 'GPU 云按需（on-demand）每 GPU 小时挂牌价：不含税；不含独立存储 / 网络计费（Nebius 出口流量免费；Lambda 实例价含本地 SSD）；抢占式与承诺 / 预留折扣写在 note；来源页无日期 → knowledge_time = 抓取日；各家实例配置不同，只做同源同型号时间序列比较（H100 / B200 分 unit）', 'USD/GPU-hr',
                             J(SRC['nebius'], SRC['lambda_']), '[]'),
    }
    for mid, (trk, kj, unit, src, deps) in KJ.items():
        m.set('metric_registry', mid, 'track', trk, basis='D1 赛道'); m.set('metric_registry', mid, 'kou_jing', kj, basis='原文定义'); m.set('metric_registry', mid, 'unit', unit, basis='记录单位')
        m.set('metric_registry', mid, 'source_ids', src, basis='source_master'); m.set('metric_registry', mid, 'upstream_deps', deps, basis='计算依赖'); m.set('metric_registry', mid, 'last_validated', '2026-09-20', basis=V)
    m.set('metric_registry', 'm_cn_optics_zte', 'source_family', '深交所 / 巨潮 static.cninfo.com.cn 原 PDF（带研究 UA 可抓）：2026 半年报摘要 1225491752（2026-082）· 2026 一季报 1225111941（2026-042）· 2025 年报摘要 1225056458（2026-019）', basis='巨潮 URL 本轮 curl 200，已存快照')
    m.set('metric_registry', 'm_cn_optics_eoptolink', 'source_family', '巨潮 static.cninfo.com.cn 原 PDF：2026 半年报全文 1225499406（2026-044）· 摘要 1225499405（2026-043）· 2026 一季报 1225172606（2026-011）· 2025 年报摘要 1225172597（2026-008）', basis='原「巨潮接口 403，原链待补」已解决')
    m.set('metric_registry', 'm_cn_optics_eoptolink', 'fill_status', '已填', basis='巨潮原链已补'); m.set('metric_registry', 'm_cn_optics_eoptolink', 'notes_assumption_ids', '巨潮原链已回（r325–r327 取代镜像链路记录）；假设 B1 / C3', basis='原「待补巨潮静态 URL」已解决')
    m.set('metric_registry', 'm_cn_optics_zte', 'notes_assumption_ids', 'H1 / Q1 / 年报均巨潮原文 P1；Q2 单季为计算值（r323）；假设 B1 / C3 / C10', basis='原备注更新')
    m.set('metric_registry', 'm_gpu_rental_price', 'source_family', 'Nebius 价格页 https://nebius.com/prices · Lambda 价格页 https://lambda.ai/pricing（均官方，P1；页面无日期，按抓取日登记）', basis='原「云价格页 / 专家访谈」占位')
    m.set('metric_registry', 'm_gpu_rental_price', 'fill_status', '已填', basis='r333–r336'); m.set('metric_registry', 'm_gpu_rental_price', 'notes_assumption_ids', '按需挂牌价 ≠ 大客户合同价（承诺折扣可达 35%）；metric_factor r 仍为 P3 默认 0.6，待 D 复核提级', basis='诚实标注')
    m.set('metric_registry', 'm_hyperscaler_capex', 'notes_assumption_ids', '假设 C11 已按现金口径统一（r312–r314 取代 r104）；C4 作 e_optics_nbis 回测的下游代理。分项：m_capex_msft / googl / amzn / meta', basis='原「🟠 若用于回归须统一口径」已解决')
    m.set('metric_registry', 'm_capex_amzn', 'notes_assumption_ids', 'C11：毛额 / 净额 / 10-Q 应计三口径见 kou_jing；官方 capex 指引仅电话会口径（r101，P2）', basis='原备注更新')
    m.set('metric_registry', 'm_capex_msft', 'notes_assumption_ids', 'C11 口径：现金 capex 不含融资租赁；FY27 折旧年限调整使含租赁口径不可跨期比较', basis='原备注更新')

    # ============ 9. 边：证据（SQL 生成，from_metric 名下全部可见记录）/ 机制 / 复验 ============
    def vis(*mids):
        rows = m.con.execute(f"SELECT record_id FROM v_obs WHERE metric_id IN ({','.join(['?']*len(mids))}) ORDER BY record_id", list(mids)).fetchall()
        return J(*[r[0] for r in rows])
    m.set('edge_registry', 'e_optics_nbis', 'evidence_ids', vis('m_cn_optics_zte'), basis='库：m_cn_optics_zte 全部可见记录（SQL 生成）')
    m.set('edge_registry', 'e_optics_nbis', 'evidence', '中际旭创 H1 营收 417.8 亿 +182%、Q2 单季 222.8 亿 +175%（环比仅 +14%）、海外占比 ≈95%（r078–r080 / r320–r324）', basis='同上')
    m.set('edge_registry', 'e_eoptolink_nbis', 'evidence_ids', vis('m_cn_optics_eoptolink'), basis='库：m_cn_optics_eoptolink 全部可见记录（SQL 生成）')
    m.set('edge_registry', 'e_eoptolink_nbis', 'evidence', '新易盛 H1 营收 209.1 亿 +100%、Q2 单季 125.7 亿 +97%（环比 +51%）、境外 97.9%（r325–r332）', basis='同上')
    m.set('edge_registry', 'e_eoptolink_nbis', 'mechanism', '新易盛 800G / 1.6T 光模块出货 ≈ 全球 AI 集群在建强度（境外 97.9%，Google / 北美云厂敞口高）→ neocloud 扩张环境 → NBIS 产能骑乘（赛道 beta，3 跳）；证伪：单季营收环比转负而 hyperscaler capex 仍增', basis='对称 e_optics_nbis；doc25 §四')
    m.set('edge_registry', 'e_capex_nbis', 'evidence_ids', vis('m_hyperscaler_capex', 'm_capex_msft', 'm_capex_googl', 'm_capex_amzn', 'm_capex_meta'), basis='库：m_hyperscaler_capex + 四个分项指标全部可见记录（checks 7e EXTRA 允许）')
    m.set('edge_registry', 'e_capex_nbis', 'evidence', '四家现金 capex 2026Q2 合计 165.05B（+87% YoY / +27% QoQ，r312）；MSFT FY27 Q1 指引 >50B、META FY26 130–145B、AMZN ≈220B、GOOGL 195–205B；AMZN 10-Q 应计口径 63.9B（AWS 48.6B）领先现金口径', basis='同上')
    m.set('edge_registry', 'e_gpu_nbis', 'evidence_ids', vis('m_gpu_ship'), basis='库：m_gpu_ship 全部可见记录（SQL 生成）')
    m.set('edge_registry', 'e_gpu_nbis', 'evidence', 'NVDA Q2 FY27 DC 89.0B（+117% / 环比 +18%），其中 ACIE（neocloud 所在）40.3B 环比 +25% 快于 Hyperscale +13%；Q3 总收入指引 108B ±2% 不含中国（r091 / r092 / r315–r319）', basis='同上')
    m.set('edge_registry', 'e_gpu_nbis', 'mechanism', 'NVDA 数据中心出货 / 代际（Blackwell Ultra → Vera Rubin）→ NBIS 的 GPU 采购成本、可得性与折旧节奏；ACIE 分项直接含 neocloud 采购（1 跳本体供应商）；证伪：ACIE 环比转负或代际切换致旧卡租价崩', basis='doc25 §四；CFO commentary 分项')
    D1SUB = {'e_d1_supx': '中国 AI 服务器整机（SUPX）：NVDA DC 出货代际与出口管制（Q3 指引不含中国 DC compute）→ 中国整机厂可得芯片与订单（1 跳）', 'e_d1_intc': 'AI 服务器 CPU / 代工（INTC）：每台 GPU 服务器带 CPU 头节点，DC 出货量 → CPU 配套需求（1 跳）',
             'e_d1_mrvl': '定制芯片 / 光 DSP（MRVL）：hyperscaler 自研加速器与 800G / 1.6T 光互联随 DC 出货同增（1 跳）', 'e_d1_amd': '加速器竞争者（AMD）：NVDA DC 收入是市场总盘子读数，AMD 份额 = 盘子 × 份额（1 跳，方向同向）'}
    for e, mech in D1SUB.items():
        m.set('edge_registry', e, 'mechanism', mech, basis='doc25 §四；D1 子节点机制补句'); m.set('edge_registry', e, 'evidence_ids', vis('m_gpu_ship'), basis='库：m_gpu_ship 全部可见记录（SQL 生成）')
        m.set('edge_registry', e, 'evidence', 'NVDA Q2 FY27 DC 89.0B（r091），分项 Hyperscale 48.7B / ACIE 40.3B（r316 / r317）', basis='同上'); m.set('edge_registry', e, 'owner', 'B', basis='B 初稿 D 复核')
    for e in ('e_optics_nbis', 'e_eoptolink_nbis', 'e_capex_nbis', 'e_gpu_nbis', 'e_d1_supx', 'e_d1_intc', 'e_d1_mrvl', 'e_d1_amd'):
        m.set('edge_registry', e, 'last_validated', '2026-09-20', basis=V)

    # ============ 10. 来源：出版方 / 频率 / 可靠性 / 旧源标 stale ============
    for sid, pub, freq, note in (
        (SRC['msft_q4e'], 'SEC EDGAR / Microsoft Corp.', '季', 'P1 交易所归档，accession 0001193125-26-323632；与 IR 页 press release 同文'),
        (SRC['msft_q3e'], 'SEC EDGAR / Microsoft Corp.', '季', 'P1 交易所归档，accession 0001193125-26-191457'),
        (SRC['msft_call'], 'Microsoft Corp.（IR 事件页内嵌 transcript）', '季', 'P2 电话会口径（官方 transcript，非第三方转录）；capex 含融资租赁口径与指引只在此'),
        (SRC['msft_q4'], 'Microsoft Corp.（IR）', '季', 'P1；与 8-K Ex.99.1 同文，快照取 EDGAR 版'),
        (SRC['googl_q1'], 'Alphabet Inc.（IR，q4cdn PDF）', '季', 'P1 公司稿 PDF；无 8-K Ex.99.1 版差异'),
        (SRC['googl_q2'], 'Alphabet Inc.（IR，q4cdn PDF）', '季', 'P1 公司稿 PDF；含 TTM FCF 表可核季度序列'),
        (SRC['amzn_q1'], 'SEC EDGAR / Amazon.com, Inc.', '季', 'P1 交易所归档，accession 0001018724-26-000012'),
        (SRC['amzn_q2'], 'SEC EDGAR / Amazon.com, Inc.', '季', 'P1 交易所归档，accession 0001018724-26-000024；现金流量表给毛额与处置收入，可算 cash capex 净额'),
        (SRC['amzn_10q'], 'SEC EDGAR / Amazon.com, Inc.', '季', 'P1；分部「net additions to PP&E」应计口径（含融资租赁与未付款），AWS 单列 —— 领先现金口径'),
        (SRC['meta_q1'], 'SEC EDGAR / Meta Platforms, Inc.', '季', 'P1 交易所归档，accession 0001628280-26-028364'),
        (SRC['meta_q2'], 'SEC EDGAR / Meta Platforms, Inc.', '季', 'P1 交易所归档，accession 0001628280-26-050596；capex 指引在稿内（P1）'),
        (SRC['nvda_q1'], 'NVIDIA Corp.（newsroom）', '季', 'P1 公司稿；DC 收入只到 0.1B，精确值见 CFO commentary'),
        (SRC['nvda_q2'], 'NVIDIA Corp.（newsroom）', '季', 'P1 公司稿'),
        (SRC['nvda_cfo'], 'NVIDIA Corp.（IR，q4cdn PDF）', '季', 'P1；Market Platform 分项（Hyperscale / ACIE）与三期对比表只在此'),
        (SRC['zjxc_q1'], '深交所 / 巨潮资讯（中际旭创）', '季', 'P1 交易所公告原 PDF；static.cninfo.com.cn 带研究 UA curl 200（浏览器 UA 403）'),
        (SRC['zjxc_fy'], '深交所 / 巨潮资讯（中际旭创）', '年', 'P1；含分季度表，可得 2025 各季'),
        (SRC['zjxc_h1'], '深交所 / 巨潮资讯（中际旭创）', '半年', 'P1；本轮 curl 重抓 200，快照与既有一致'),
        (SRC['eop_h1'], '深交所 / 巨潮资讯（新易盛）', '半年', 'P1 原链；与新浪镜像逐字节一致'),
        (SRC['eop_q1'], '深交所 / 巨潮资讯（新易盛）', '季', 'P1'),
        (SRC['eop_fy'], '深交所 / 巨潮资讯（新易盛）', '年', 'P1；含分季度表'),
        (SRC['nebius'], 'Nebius Group N.V.（官方价格页）', '持续', 'P1 云厂自家挂牌价；页面无日期与历史，需定期抓取成序列；不含税，承诺折扣另议'),
        (SRC['lambda_'], 'Lambda（官方价格页）', '持续', 'P1 云厂自家挂牌价；页面无日期；实例价含本地 SSD，1-Click Clusters 为 2 周–1 年预留价'),
    ):
        m.set('source_master', sid, 'publisher', pub, basis='来源页'); m.set('source_master', sid, 'frequency', freq, basis='—'); m.set('source_master', sid, 'reliability_note', note, basis='—'); m.set('source_master', sid, 'last_validated', '2026-09-20', basis=V)
    for sid, new, why in (('src_深交所_300308_一季报公告', SRC['zjxc_q1'], 'r081 已被带 URL 的 r320 取代'), ('src_年报_新浪转述_待回原文', SRC['zjxc_fy'], 'r082 已被巨潮原文 r322 取代'),
                          ('src_新易盛_2026_半年报全文_公告_2026_044_新浪镜像', SRC['eop_h1'], '镜像链路已被巨潮原链取代（r325–r327）'), ('src_semisino_待回年报', SRC['eop_fy'], 'r086 已被巨潮原文 r330 取代'),
                          (SRC['amzn_call'], SRC['amzn_q2'], 'r100 已被 8-K 计算值 r304 取代；r101（FY 指引）仍引用，来源保留'), ('src_计算_35_8_44_9_54_2_31_1', None, 'r104 已被统一口径 r312 取代'), ('src_云价格页_专家访谈', SRC['nebius'], 'r173 占位已被 r333 取代')):
        m.set('source_master', sid, 'verify_status', 'stale', basis=why)
        if new: m.set('source_master', sid, 'superseded_by', new, basis=why)
