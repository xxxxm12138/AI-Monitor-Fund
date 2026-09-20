# -*- coding: utf-8 -*-
"""0018 · D5 能力前沿 / D6 token 经济逐字段填充（AA / SWE-bench / ARC / LMArena / Epoch 复核 + 快照 + doc29 两道闸；定价页与 changelog 重抓；OpenRouter 复核；新范式与中国 AI 应用占位落地；registry 口径；边机制与证据）· owner B · 2026-09-20
18 份快照（snap_d56_*）。复核结论：AA v4.3 榜首 53（Fable 5.1 max = GPT-6 Astra max）、开源榜首 GLM-5.3 45、每任务成本 7.63 / 3.26 / 2.01、ARC-AGI-3 99.9% / 62.7%（generatedAt 2026-09-04）、ARC-AGI-2 95.0%、SWE-bench Verified 79.2%（最新提交 2026-02-26）/ Bash Only 76.8%、LMArena 1506 ±5、Epoch 5×/年（Updated 2026-02-05）、三家定价页 —— 与库内值全部一致，只填 snapshot / anchor / 闸门字段（fct_frontier 无 confidence 列），不新记录。
新记录 8 条（r450–r457）+ 新指标 1 个（m_token_share_openrouter）：OpenRouter 榜单已滚动到「Usage data through Sep 19, 2026」，旧 r162 / r163（through Sep 18，我方抽核截断）不可复核 → 取代；新范式 3 条一手（Gemini Robotics 2 具身 / AlphaGenome Atlas AI4S / NVIDIA Cosmos 3 世界模型，均 vendor_pr · claimed_only）取代占位 r154；QuestMobile 2026Q1 公开摘要（P3）取代占位 r164；GPT-6 Astra 发布定价事件（2026-09-03）。
研究上有意义的四点：① SWE-bench Verified 榜首两条 checked=false（提交方自报，SWE-bench 团队未复跑）→ verifiability 由 third_party_verified 纠为 claimed_only；Bash Only 视图才是团队统一环境跑的；② OpenRouter 7 天榜首一天内从 GPT-5.6 Luna 换成 DeepSeek V4.1 Flash（14.6T，+300%），前五中四席中国开源模型，按作者请求份额 openai 23.6% / deepseek 22.6% / google 18.6%，anthropic 仅 2.5% —— 只代表 OpenRouter 路由；③ r159「serving costs −20% via GPU kernel improvements」归因句在 changelog 页未见，价格变动本身已核；④ GPT-6 Astra 短上下文 $10/$50、长上下文（>272K）$20/$75 —— 定价页已出现「上下文分档」，cost/token 口径需带上下文长度。
industry_impact / impact_rationale 一律不填（D 判）。"""
OWNER = 'B'
V = '本轮重抓来源页复核（2026-09-20）'
# ---- 来源字符串（URL 均本轮实际打开）----
AA_LB = 'AA 榜单 https://artificialanalysis.ai/leaderboards/models'
AA_V43 = 'AA v4.3 https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3'
OR_RANK = 'OpenRouter rankings https://openrouter.ai/rankings'
OAI_CL = 'OpenAI changelog https://platform.openai.com/docs/changelog'
GDM_ROBO = 'Google DeepMind blog Gemini Robotics 2 https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/'
GDM_AG = 'Google DeepMind blog AlphaGenome Atlas https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/'
NV_COSMOS = 'NVIDIA blog Cosmos 3 open world models https://blogs.nvidia.com/blog/open-world-models-physical-ai/'
QM_Q1 = 'QuestMobile 研究院 2026年一季度AI应用洞察 https://www.questmobile.com.cn/research/report/2046482337382842370/'
# ---- 快照 id ----
S = dict(aa_lb='snap_d56_aa_leaderboard_models', aa_v43='snap_d56_aa_v4_3_article', hf='snap_d56_hf_api_models_downloads',
         arc3='snap_d56_arcprize_leaderboard_v3_json', arc2='snap_d56_arcprize_leaderboard_v2_json', swe='snap_d56_swebench_com', arena='snap_d56_arena_leaderboard_text',
         epoch='snap_d56_epoch_trends', oai_p='snap_d56_openai_pricing', oai_cl='snap_d56_openai_changelog', ant_p='snap_d56_anthropic_pricing', goog_p='snap_d56_google_gemini_pricing',
         orr='snap_d56_openrouter_rankings', gdm_robo='snap_d56_deepmind_gemini_robotics_2', gdm_ag='snap_d56_deepmind_alphagenome_atlas', nv='snap_d56_nvidia_blog_open_world_models',
         qm_q1='snap_d56_questmobile_2026q1_ai_app', qm_plat='snap_d56_questmobile_2026_ai_platform')
SRC = dict(aa_lb='src_aa_榜单', aa_v43='src_aa_v4_3', aa_json='src_aa_首页内嵌_json', hf='src_hf_api', swe_json='src_swebench_com_内嵌_leaderboard_json', swe='src_swebench_com',
           arc3='src_arc_prize_json_博客', arc2='src_arc_prize_json_v2', arena='src_arena_ai_leaderboard_text', epoch='src_epoch_ai_trends', epoch_blog='src_epoch_ai_博客',
           oai_p='src_openai_定价页', oai_cl='src_openai_changelog', oai_cl2='src_openai_changelog_同上', ant_p='src_anthropic_定价', ant_p2='src_anthropic_定价页_同上', goog_p='src_google_定价',
           orr='src_openrouter_rankings', orr2='src_openrouter_rankings_同上', gdm_robo='src_google_deepmind_blog_gemini_robotics_2', gdm_ag='src_google_deepmind_blog_alphagenome_atlas',
           nv='src_nvidia_blog_cosmos_3_open_world_models', qm='src_questmobile_研究院_2026年一季度ai应用洞察', para_old='src_顶会主题_lab_博客', app_old='src_第三方_app_数据')

def up(m):
    # ======== 新指标：OpenRouter 模型作者请求份额（与 token 量是两种量，不塞同一指标）========
    m.insert('metric_registry', dict(metric_id='m_token_share_openrouter', name='OpenRouter 模型作者请求份额（周）', entity_id='ent_openrouter', ticker_or_entity='OpenRouter', entry='AI', track='推理路由 / token 经济', layer='L4', dim='D6', data_class='1', signal_role='predictor',
        source_ids=f'["{SRC["orr"]}"]', source_family='OpenRouter rankings「Market Share」节（按模型作者的文本请求份额）', frequency='周', lead_time_est='—',
        kou_jing='OpenRouter 最近完整一周文本请求数按模型作者的份额（%），含免费 / 付费变体，用户设为私密的请求在聚合前剔除；只代表经 OpenRouter 路由的流量，不代表全市场；与 m_token_usage（token 量）分开记', unit='% 请求份额', owner='B', upstream_deps='[]',
        availability='🟢', next_release='周更（页面按日滚动）', next_release_basis='规则推定', status='testing', fill_status='已填', notes_assumption_ids='P3 聚合站；anthropic 份额低是因其流量多走一方 API，不能读成需求弱', last_validated='2026-09-20'), basis='一个指标一种量：份额 ≠ token 量（从 m_token_usage 拆出）')
    m.sql("INSERT INTO metric_entity VALUES ('m_token_share_openrouter','ent_openrouter')", basis='指标挂实体')
    m.insert('metric_factor', dict(metric_id='m_token_share_openrouter', r=0.6, e=0.3, l=0.6, s=0.9, phi=0.9, rationale='对称 m_token_usage 规则，r←P3（聚合站，非一手）；e=L 全公开；l=M；s=H 结构化榜单；φ=H 周', owner='B', status='draft'), basis='factors.py 规则')

    # ======== 新记录 ========
    # D6 OpenRouter：榜单已滚动到 Sep 19，旧 r162 / r163 不可复核 → 取代
    m.observe('r450', 'm_token_usage', 'OpenRouter 周榜', 'actual', '14.6T', 'tokens（#1 DeepSeek V4.1 Flash，7 天）', '7 天至 2026-09-19', '2026-09-19', OR_RANK, 'P3',
              note='取代 r162（through Sep 18，我方抽核截断未复核；窗口已滚动无法复核）。“Usage data through Sep 19, 2026”；#2 GLM 5.3 Flash 13T · #3 GPT-5.6 Luna 12.4T · #4 Hy4 preview 11.9T · #5 DeepSeek V4 Flash 0731 9.77T；#1 周环比 +300%；只代表 OpenRouter 路由，不代表全市场用量')
    m.observe('r451', 'm_token_usage', 'OpenRouter 月榜', 'actual', '49.2T', 'tokens（#1 DeepSeek V4 Flash 0731，30 天）', '30 天至 2026-09-19', '2026-09-19', OR_RANK, 'P3',
              note='取代 r163（through Sep 18，未复核）。“Models ranked by tokens processed on OpenRouter over the trailing thirty days”：#1 DeepSeek V4 Flash 0731 49.2T（+74%）· #2 GPT-5.6 Luna 48.8T（+215%）· #3 Hy4 preview 45.1T（new）· #4 GLM 5.3 Flash 42T（new）· #5 MiMo-V2.5 30T；只代表 OpenRouter 路由')
    m.observe('r452', 'm_token_share_openrouter', 'OpenRouter 作者份额', 'actual', '23.6', '% 文本请求份额（#1 openai，按模型作者）', '2026-09-07 起一周', '2026-09-19', OR_RANK, 'P3',
              note='“Share of text requests made on OpenRouter in the week beginning Sep 7, 2026”：openai 23.6%（+28%）· deepseek 22.6% · google 18.6% · tencent 7.2%（+105%）· z-ai 7.0%（−22%）· qwen 5.2% · anthropic 2.5%（−5%）· mistralai 2.3% · meta-llama 2.2%；只代表 OpenRouter 路由，Anthropic 流量多走一方 API')
    # D5 新范式：三条一手（lab 官方博客），vendor 自述，不下产业影响判断
    m.observe('r453', 'm_new_paradigm', 'Google DeepMind', 'state', 'Gemini Robotics 2：VLA 首次控制全身人形（Apptronik Apollo 2）、22 自由度五指手、多机器人协作；同一 checkpoint 跨三种本体；On-Device 2 数小时 / <200 样本适配新本体', '—', '2026-07-30', '2026-07-30', GDM_ROBO, 'P1',
              note='取代占位 r154。vendor 自述，成功率图为自评；“For the first time, our model can now control entire humanoid robots, translating intent into intelligent whole-body control”；同稿承认 “the multi-finger dexterous manipulation remains challenging”')
    m.observe('r454', 'm_new_paradigm', 'Google DeepMind', 'state', 'AlphaGenome Atlas：预计算 90 亿个人类基因组单核苷酸变异的分子效应（1 PB，AlphaFold DB 30 倍），发布 AVI 评分；外部合作者（Broad / GREGoR、Exeter UK Biobank 5.4 万人）已用其定位并实验验证致病变异', '—', '2026-09-08', '2026-09-08', GDM_AG, 'P1',
              note='vendor 自述；论文为 DeepMind 自托管 PDF（非同行评审刊物）；“a platform containing predictions for the effects of 9 billion single-nucleotide variants — every single-letter change possible — in the human genome”')
    m.observe('r455', 'm_new_paradigm', 'NVIDIA', 'state', 'Cosmos 3：开放权重物理 AI 世界模型族（Super 64B / Nano 16B / Edge 4B，mixture-of-transformers，OpenMDW 1.1 许可），一个模型族覆盖视觉推理 + 世界生成 + 动作预测；自称在 Artificial Analysis 开源 t2i / i2v、PAI-Bench、Physics-IQ i2v、RoboLab 排第一', '—', '2026-08-06', '2026-08-06', NV_COSMOS, 'P1',
              note='vendor 自述，榜单排名为 NVIDIA 转述（AA / PAI-Bench 可第三方复核，本轮未复核）；“NVIDIA Cosmos 3 — a frontier open physical AI foundation omni-model built on a mixture-of-transformers architecture — combines vision reasoning, world generation and action prediction”')
    # D6 中国 AI 应用：免费公开摘要（付费全文）
    m.observe('r456', 'm_app_retention_cn', 'QuestMobile（中国 AI 原生 App）', 'actual', '4.46', '亿 MAU（AI 原生 App 整体，中国）', '2026-03', '2026-04-21', QM_Q1, 'P3',
              note='取代占位 r164。“截止到2026年3月，AI原生APP月活用户规模已达到4.4亿，其中，豆包、千问、DeepSeek位居前三位，月活用户规模分别为3.45亿、1.66亿和1.27亿”；正文精确值 4.46 亿，较 2025-11 +13495 万（+43.4%）；一季度平均活跃率 豆包 33.5% / 千问 17.1% / DeepSeek 21%；春节后豆包 DAU 约 1.4 亿、千问 3000 万、元宝 900 万；月人均使用 87.1 次 / 173.3 分钟。第三方监测口径（QuestMobile TRUTH），全文付费；2026-09-01 同源报告只给 AI 办公赛道 7 月 MAU 1.02 亿，无整体口径')
    # D6 定价：GPT-6 Astra 发布定价（changelog + 定价页）
    m.observe('r457', 'm_cost_per_token', 'OpenAI GPT-6 Astra', 'event', 'GPT-6 Astra 发布，API 定价 $10 / $50（短上下文，缓存输入 $1）；长上下文（>272K）$20 / $75；Batch / Flex 半价；Fast mode 2 倍价', 'USD per 1M tokens 输入 / 输出', '2026-09-03', '2026-09-03', OAI_CL, 'P1',
              note='changelog “Released GPT-6 Astra, our most capable model, built for the hardest end-to-end work”；定价见定价页 gpt-6-astra 行；定价页已按 Short / Long context 分档 —— cost/token 口径需带上下文长度；无 2026-08-21 之后的降价 / 涨价公告（复核至 Sep 20）',
              direction='→', direction_note='新前沿档定价 $10/$50（r156 同值），无降价；长上下文加价')

    # ======== 取代 ========
    m.supersede('r162', 'r450', reason='OpenRouter 榜单已滚动到 through Sep 19；r162（through Sep 18）「我方抽核截断未复核」不可复核，以 Sep 19 新值取代')
    m.supersede('r163', 'r451', reason='同上（30 天窗口滚动）')
    m.supersede('r154', 'r453', reason='占位「待填」被 2026 年三条一手新范式记录（r453 / r454 / r455）取代')
    m.supersede('r164', 'r456', reason='占位「待填」被 QuestMobile 2026Q1 公开摘要（P3）取代；全文付费')

    # ======== 新记录字段 ========
    for rid in ('r450', 'r451', 'r452'):
        m.set('fct_quant', rid, 'snapshot_id', S['orr'], basis='快照'); m.set('fct_quant', rid, 'confidence', 1.0, basis='本轮抓页面文本节「as text」表读出，非截断')
        m.set('fct_quant', rid, 'period_end', '2026-09-19', basis='Usage data through Sep 19, 2026')
    m.set('fct_quant', 'r450', 'period_start', '2026-09-13', basis='trailing 7 days'); m.set('fct_quant', 'r451', 'period_start', '2026-08-21', basis='trailing 30 days')
    m.set('fct_quant', 'r452', 'period_start', '2026-09-07', basis='week beginning Sep 7'); m.set('fct_quant', 'r452', 'period_end', '2026-09-13', basis='most recent complete week')
    m.set('fct_quant', 'r452', 'anchor', 'openai | 23.6% | +28% | deepseek | 22.6% | +3% | google | 18.6% | +2%', basis='原文表')
    m.set('fct_quant', 'r456', 'snapshot_id', S['qm_q1'], basis='快照'); m.set('fct_quant', 'r456', 'confidence', 0.9, basis='公开摘要页原文；全文 PDF 付费未核'); m.set('fct_quant', 'r456', 'period_start', '2026-03-01', basis='月'); m.set('fct_quant', 'r456', 'period_end', '2026-03-31', basis='月')
    for rid, snap, tc, meth in (('r453', S['gdm_robo'], '具身 / VLA', 'VLA 全身控制 + ER 推理层 + On-Device 多本体适配'), ('r454', S['gdm_ag'], 'AI4S / 基因组', 'AlphaGenome 全基因组预计算 + AVI 评分（AlphaGenome + AlphaMissense）'), ('r455', S['nv'], '世界模型 / 物理 AI', 'mixture-of-transformers 开放权重世界模型族（视觉推理 + 世界生成 + 动作预测）')):
        m.set('fct_frontier', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_frontier', rid, 'topic_cluster', tc, basis='新范式分类'); m.set('fct_frontier', rid, 'method', meth, basis='原文')
        m.set('fct_frontier', rid, 'source_stance', 'vendor_pr', basis='lab 官方博客 = vendor 自述'); m.set('fct_frontier', rid, 'verifiability', 'claimed_only', basis='self_reported：无第三方复现 / 同行评审刊物；r454 有自托管论文与外部合作者验证但未过评审；r455 榜单排名可第三方复核但本轮未复核')
    m.set('fct_frontier', 'r454', 'doc_id', 'https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/alphagenome-atlas.pdf', basis='博客「Read our paper」链接（自托管 PDF）')
    m.set('fct_frontier', 'r453', 'doc_id', 'https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf', basis='博客「Safety Technical Report」链接')
    m.set('fct_event', 'r457', 'event_type', 'pricing', basis='定价事件'); m.set('fct_event', 'r457', 'snapshot_id', S['oai_cl'], basis='快照'); m.set('fct_event', 'r457', 'confidence', 1.0, basis='一手'); m.set('fct_event', 'r457', 'amount_text', '$10 / $50 短上下文；$20 / $75 长上下文', basis='定价页')

    # ======== 现有记录：快照 / 锚点 / 闸门 / 置信（值全部与本轮抓取一致）========
    F = {  # fct_frontier: rid → (snapshot, anchor, stance, verifiability, basis for verifiability)
      'r144': (S['aa_v43'], 'Both Claude Fable 5.1 (max with fallback) and GPT-6 Astra (max) score 53 on Intelligence Index v4.3, followed by Claude Opus 5 (max, 51), Claude Fable 5 (with fallback, 50), Muse Spark 1.3 (max, 48) and GPT-5.6 Sol (max, 47)', 'neutral', 'third_party_verified', 'AA 独立跑评测（10 项，含私有测试集）'),
      'r146': (S['aa_lb'], 'The top open weights models by Intelligence Index are: 1. GLM-5.3 (max) (45), 2. Kimi K3 (max) (44), 3. GLM 5.3 Flash (42)', 'neutral', 'third_party_verified', 'AA 独立跑评测'),
      'r147': (S['hf'], '"id":"Qwen/Qwen3-0.6B" … "downloads":22967391', 'neutral', 'reproducible', 'HF 公开 API 任何人可复现同一计数（平台自报下载量）'),
      'r148': (S['swe'], '79.2 | Sonar Foundation Agent + Claude 4.5 Opus | date=2025-12-05 | checked=False；79.2 | live-SWE-agent + Claude 4.5 Opus medium (20251101) | date=2025-12-15 | checked=False', 'neutral', 'claimed_only', '纠正：榜首两条 checked=false = 提交方自报，SWE-bench 团队未复跑（页面「Run performed or directly checked by the SWE-bench team」标记缺失）；榜单最新提交日 2026-02-26 与 knowledge_time 一致'),
      'r149': (S['swe'], '76.8 | Claude 4.5 Opus (high) | agent=mini-SWE-agent | date=2026-02-17', 'neutral', 'third_party_verified', 'Bash Only = SWE-bench 团队在统一 mini-SWE-agent 环境自跑'),
      'r150': (S['arc3'], '"modelDisplayName": "GPT-6 Astra - Provider Adapter (High)" … "score": 0.99945712321257, "cost": 18816.63138；"GPT-6 Astra (Max)" … "score": 0.6271280210060628, "cost": 26097.501720000007', 'neutral', 'third_party_verified', 'ARC Prize 半私有集官方跑；generatedAt 2026-09-04T14:38:06Z 与库一致'),
      'r151': (S['arc2'], '"modelDisplayName": "GPT-6 Astra (Max)" … "score": 0.95, "costPerTask": 1.1194680833333335', 'neutral', 'third_party_verified', 'ARC Prize 半私有集官方跑；generatedAt 2026-09-04 与库一致'),
      'r152': (S['arena'], 'claude-fable-5-high | 1506 ±5 | 30,057 | $10 / $50；Sep 13, 2026 · 8,146,274 votes · 402 models', 'neutral', 'third_party_verified', '众包盲测 Elo，页面日期 2026-09-13 与库一致'),
      'r153': (S['aa_lb'], 'Claude Fable 5.1 (max with fallback) … 53 | $7.63；GPT-6 Astra (max) … 53 | $3.26；GLM-5.3 (max) … 45 | $2.01', 'neutral', 'third_party_verified', 'AA 按其 Intelligence Index 跑量 × 官方 API 价计算；内嵌 JSON price1mInputTokens/Output：Astra 10/50、GLM-5.3 1.4/4.4（3:1 blended 2.15 与库注一致）'),
      'r142': (S['epoch'], 'Training compute for frontier language models has been growing at 5× per year since 2020', 'neutral', 'third_party_verified', 'Epoch 独立数据库，页面 Updated Feb. 5, 2026 与库一致；口径 = top-5 前沿语言模型训练算力'),
    }
    for rid, (snap, anchor, st, vf, vb) in F.items():
        m.set('fct_frontier', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_frontier', rid, 'anchor', anchor, basis='原文短引 / JSON 字段')
        m.set('fct_frontier', rid, 'source_stance', st, basis='第三方榜单 / 平台 API'); m.set('fct_frontier', rid, 'verifiability', vf, basis=vb)
    m.set('fct_frontier', 'r143', 'note', '旧口径（2010 起全部 notable 模型 4–5×/年）；博客未重抓，trends 页同句「Training compute of frontier AI models grows by 4-5× per year」在 snap_d56_epoch_trends 内', basis='本轮 trends 页复核')
    m.set('fct_frontier', 'r146', 'note', '开源榜首 GLM-5.3 (max)；次 Kimi K3 44、GLM 5.3 Flash 42；差距 8 分为计算值。2026-09-20 复核：榜单「Status: Current」口径 147 模型中 66 个开源（原记 162 / 80 为含 deprecated 口径）', basis='本轮页面 FAQ 节原文')
    m.set('fct_frontier', 'r148', 'note', '并列：Sonar Foundation Agent + Claude 4.5 Opus（2025-12-05）/ live-SWE-agent + Claude 4.5 Opus（2025-12-15）；均 checked=false（提交方自报）；#3 TRAE + Doubao-Seed-Code 78.8；knowledge_time 取榜单最新提交日 2026-02-26', basis='本轮 JSON 复核补日期')
    for rid, snap, anchor in (('r156', S['oai_p'], 'gpt-6-astra | $10.00 | $1.00 | $12.50 | $50.00 | $20.00 | $2.00 | $25.00 | $75.00'), ('r157', S['ant_p'], 'Claude Fable 5.1 | $10 / MTok | $12.50 / MTok | $20 / MTok | $0.25 / MTok 1 | $50 / MTok'), ('r158', S['goog_p'], '$0.75 through December 31, 2026. $1.50 starting January 1, 2027.')):
        m.set('fct_quant', rid, 'snapshot_id', snap, basis='快照'); m.set('fct_quant', rid, 'anchor', anchor, basis='定价表原文行'); m.set('fct_quant', rid, 'confidence', 1.0, basis='本轮重抓核对，值一致')
    m.set('fct_quant', 'r156', 'note', '缓存输入 $1；长上下文（>272K）$20 / $75、Batch / Flex $5 / $25、Fast mode $20 / $100 —— 定价页按上下文分档', basis='本轮定价页补口径')
    m.set('fct_quant', 'r158', 'period_start', '2026-09-19', basis='抓取日起'); m.set('fct_quant', 'r158', 'period_end', '2026-12-31', basis='through December 31, 2026')
    m.set('fct_quant', 'r158', 'note', '2027-01-01 起 $1.50 / $7.50（涨价，C16）；Gemini 3.7 / 3.6 Flash 同样 2027-01-01 翻倍；缓存 $0.075 → $0.15', basis='本轮定价页复核')
    m.set('fct_event', 'r159', 'snapshot_id', S['oai_cl'], basis='快照'); m.set('fct_event', 'r159', 'anchor', 'Starting July 30, GPT-5.6 Luna costs 80% less, while GPT-5.6 Terra costs 20% less', basis='changelog 原句（原锚点「serving costs −20% via GPU kernel improvements」在 changelog 页未见，替换为可核句）')
    m.set('fct_event', 'r159', 'note', '归因 “serving costs −20% via GPU kernel improvements” —— 2026-09-20 复核：该句不在 changelog 页，来源待钉；价格变动本身已核（Luna $0.20/$1.20、Terra $2/$12 与定价页一致）；同日 Fast mode 取代 Priority（2 倍价）', basis='诚实标注')
    m.set('fct_event', 'r159', 'confidence', 0.9, basis='价格已核，归因句未核'); m.set('fct_event', 'r159', 'event_type', 'pricing', basis='降价事件')
    m.set('fct_event', 'r160', 'snapshot_id', S['oai_cl'], basis='快照'); m.set('fct_event', 'r160', 'anchor', 'GPT-5.6 Sol now costs $4 per million input tokens and $20 per million output tokens, representing 20% lower input pricing and 33% lower output pricing', basis='changelog 原句'); m.set('fct_event', 'r160', 'confidence', 1.0, basis='一手核对')
    m.set('fct_event', 'r161', 'snapshot_id', S['ant_p'], basis='快照'); m.set('fct_event', 'r161', 'anchor', 'The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur', basis='定价页原句'); m.set('fct_event', 'r161', 'confidence', 1.0, basis='一手核对'); m.set('fct_event', 'r161', 'event_type', 'pricing', basis='取消涨价 = 定价事件')

    # ======== metric_registry：赛道 / 口径 / 单位 / 来源 / 依赖 / 复验 ========
    TRK = {'D5': '前沿模型能力（第三方榜单）', 'D6': '推理定价 / token 经济', 'APP': '中国 AI 应用（第三方监测）'}
    KJ = {
      'm_aa_intel_index': (TRK['D5'], 'Artificial Analysis Intelligence Index v4.3.2（10 项：AA-Briefcase v1.1、GDPval-AA v2.1、AutomationBench-AA、Terminal-Bench 4.0、SciCode、HLE、GDP.pdf、CritPt、AA-Omniscience、AA-LCR v1.1）榜首分；AA 自跑（第三方复现），含私有测试集；版本升级会重排（v4.2→v4.3 换 τ³-Banking 为 AutomationBench）；knowledge_time 取版本文章日', '分（0–100）', f'["{SRC["aa_v43"]}","{SRC["aa_lb"]}"]', '[]'),
      'm_infer_price_perf': (TRK['D5'], 'AA「Cost per Task」= 跑完 Intelligence Index 全套的 API 成本（按官方标价，Blended 3:1 输入:输出）；同分模型间比较；开源 vs 闭源同榜；随榜单版本与定价变动重算', 'USD per Intelligence Index task', f'["{SRC["aa_lb"]}","{SRC["aa_json"]}"]', '["m_aa_intel_index","m_cost_per_token"]'),
      'm_open_vs_closed': (TRK['D5'], '两种量 unit 区分：① AA Intelligence Index 闭源最高 vs 开源最高（第三方复现），差距为计算值；② HF API text-generation 30 天下载榜首（平台自报计数，可复现）；HF 下载 ≠ 用量', '分 / 30 天下载', f'["{SRC["aa_lb"]}","{SRC["hf"]}"]', '["m_aa_intel_index"]'),
      'm_bench_frontier': (TRK['D5'], '四榜 unit / benchmark 区分：SWE-bench Verified 全部提交榜首（提交方自报，checked 标记看 verifiability）与 Bash Only（团队统一环境自跑）；ARC-AGI-3 / ARC-AGI-2 半私有集官方 JSON（score 0–1 × 100，附单任务成本）；LMArena Text 众包 Elo（Style Control 默认）；knowledge_time 取榜单 generatedAt / 最新提交日 / 页面日期', '% / Elo', f'["{SRC["swe"]}","{SRC["swe_json"]}","{SRC["arc3"]}","{SRC["arc2"]}","{SRC["arena"]}"]', '[]'),
      'm_train_compute_epoch': (TRK['D5'], 'Epoch AI trends：top-5 前沿语言模型训练算力（FLOP）年增速拟合，2020 起 5×/年（0.7 OOM，5.2 个月翻倍）；旧口径 2010 起全部 notable 模型 4–5×/年（博客 2024-05）；第三方独立数据库，页面 Updated 日为 knowledge_time', '× / 年', f'["{SRC["epoch"]}","{SRC["epoch_blog"]}"]', '[]'),
      'm_new_paradigm': (TRK['D5'], '事件型：lab 官方博客 / arXiv / 顶会一手的「新范式」信号（世界模型 / 具身 / AI4S / 新架构），每条记 institution、source_stance（vendor_pr / neutral）、verifiability（claimed_only = 自报 / third_party_verified / reproducible）；industry_impact 由 D 判', '—', f'["{SRC["gdm_robo"]}","{SRC["gdm_ag"]}","{SRC["nv"]}"]', '[]'),
      'm_cost_per_token': (TRK['D6'], '三家官方定价页前沿档标价（USD / 1M tokens，输入 / 输出，短上下文；缓存、长上下文、Batch / Fast 档在 note）+ 官方 changelog 的降价 / 涨价 / 促销事件；不是实际成交价；Gemini 3.8 Flash 2027-01-01 翻倍是反例', 'USD per 1M tokens', f'["{SRC["oai_p"]}","{SRC["oai_cl"]}","{SRC["ant_p"]}","{SRC["goog_p"]}"]', '[]'),
      'm_token_usage': (TRK['D6'], 'OpenRouter rankings：按模型变体统计经 OpenRouter API 处理的 token（prompt + completion），UTC 日桶，私密请求剔除；7 天 / 30 天 trailing 窗口 unit 区分；「Usage data through …」为 knowledge_time；只代表 OpenRouter 路由（一方 API 流量不在内），不代表全市场；作者份额见 m_token_share_openrouter', 'tokens（T）', f'["{SRC["orr"]}"]', '[]'),
      'm_app_retention_cn': (TRK['APP'], 'QuestMobile 公开摘要：中国 AI 原生 App 整体 MAU（月），头部 App MAU / 平均活跃率 / DAU 在 note；第三方监测（TRUTH 数据库），全文付费，P3；留存率全文才有', '亿 MAU', f'["{SRC["qm"]}"]', '[]'),
    }
    for mid, (trk, kj, unit, src, deps) in KJ.items():
        m.set('metric_registry', mid, 'track', trk, basis='赛道'); m.set('metric_registry', mid, 'kou_jing', kj, basis='来源页方法说明'); m.set('metric_registry', mid, 'unit', unit, basis='记录单位')
        m.set('metric_registry', mid, 'source_ids', src, basis='source_master'); m.set('metric_registry', mid, 'upstream_deps', deps, basis='计算依赖'); m.set('metric_registry', mid, 'last_validated', '2026-09-20', basis=V)
    m.set('metric_registry', 'm_new_paradigm', 'fill_status', '已填', basis='r453–r455'); m.set('metric_registry', 'm_new_paradigm', 'source_family', 'lab 官方博客（DeepMind / NVIDIA）；顶会 / arXiv 待补', basis='本轮来源')
    m.set('metric_registry', 'm_new_paradigm', 'notes_assumption_ids', '过证伪闸（source_stance / verifiability 已填）；影响力闸 industry_impact 待 D；C8 占位', basis='闸门状态')
    m.set('metric_registry', 'm_app_retention_cn', 'fill_status', '已填', basis='r456（P3 公开摘要）'); m.set('metric_registry', 'm_app_retention_cn', 'availability', '🔵', basis='全文付费，摘要免费'); m.set('metric_registry', 'm_app_retention_cn', 'source_family', 'QuestMobile 研究院公开摘要（季度 AI 应用洞察 / AI 平台报告）', basis='本轮来源')
    m.set('metric_registry', 'm_app_retention_cn', 'frequency', '季（QuestMobile 季度报告）', basis='来源节奏'); m.set('metric_registry', 'm_app_retention_cn', 'next_release', '2026-10 下旬（Q3 报告，估计）', basis='Q1 报告 04-21 发布节奏'); m.set('metric_registry', 'm_app_retention_cn', 'next_release_basis', '估计', basis='规则推定')
    m.set('metric_registry', 'm_token_usage', 'fill_status', '已填', basis='r450 / r451 已复核（原「已填（待复核）」）')
    m.set('metric_registry', 'm_token_usage', 'notes_assumption_ids', 'OpenRouter 只是聚合路由的一角，不代表全市场用量；前五中四席为中国开源模型（DeepSeek / GLM / 腾讯 Hy4），是 D5 开源追赶的需求侧印证；记录 P3（聚合站），metric_factor r=0.9 按 P1 推，待 D 复核', basis='更新')
    m.set('metric_registry', 'm_bench_frontier', 'notes_assumption_ids', 'T_a 中立第三方；SWE-bench 榜首两条 checked=false → verifiability=claimed_only；ARC-AGI-3 榜单页只显示 <$10K 系统，99.9% 取自官方 JSON', basis='更新')
    m.set('metric_registry', 'm_cost_per_token', 'source_family', 'OpenAI 定价页 + changelog；Anthropic 定价页；Google Gemini API 定价页（均 P1，2026-09-20 重抓）', basis='更新')

    # ======== 边：机制 / 证据（该 from_metric 名下全部可见记录）/ owner / 复验 ========
    E = {
      'e_aa_nbis': ('能力前沿抬升（AA 榜首分）→ 前沿 lab 训练 / 推理算力需求 → lab 向 neocloud 采购 → NBIS 用量；3 跳只方向；证伪：榜首分停滞两个版本且 lab 资本开支指引下修', '["r144"]', 'AA v4.3 榜首 53：Fable 5.1 (max) = GPT-6 Astra (max)（r144，2026-09-07，第三方复现）'),
      'e_bench_nbis': ('前沿 benchmark 新纪录（ARC / SWE-bench / Arena）→ 推理侧 test-time compute 与训练需求 → lab 采购 → NBIS；评测本身即算力消耗（ARC-AGI-3 单次 $18.8K–$26.1K）；3 跳只方向', '["r148","r149","r150","r151","r152"]', 'ARC-AGI-3 99.9% / 62.7%（r150）、ARC-AGI-2 95.0%（r151）、SWE-bench Verified 79.2%（r148，自报）/ Bash Only 76.8%（r149）、LMArena 1506（r152）'),
      'e_openclosed_nbis': ('开源 vs 闭源差距收窄 → 推理从一方 API 向自托管 / neocloud 迁移（对 NBIS 偏多）；但开源模型更便宜也压低单位推理收入（偏空）→ 双向需人判；2 跳', '["r146","r147"]', 'AA 开源 45 vs 闭源 53（r146，差 8 分）；HF 30 天下载榜首 Qwen3-0.6B 2,297 万（r147）'),
      'e_priceperf_nbis': ('每任务成本下降（同分更便宜）→ 推理需求弹性释放 → 用量上升 → neocloud 需求；2 跳；开源 GLM-5.3 $2.01/task 是性价比曲线压低者', '["r153"]', 'Fable 5.1 $7.63 / Astra $3.26 / GLM-5.3 $2.01 per task（r153，2026-09-19）'),
      'e_costtoken_nbis': (None, '["r156","r157","r158","r159","r160","r161","r457"]', '前沿档 $10/$50 三家一致（r156 / r157 / r457 Astra 发布同价）；Gemini 3.8 Flash 2027-01-01 翻倍（r158）；Luna −80% / Terra −20%（r159）、Sol 促销 −20%/−33%（r160）、Sonnet 5 取消涨价（r161）'),
      'e_token_nbis': ('推理用量 → 推理需求 → neocloud 用量；OpenRouter 只是一角（一方 API 流量不在内）；2 跳', '["r450","r451"]', 'OpenRouter 7 天榜首 DeepSeek V4.1 Flash 14.6T（r450）、30 天榜首 DeepSeek V4 Flash 0731 49.2T（r451）；through Sep 19, 2026；P3'),
      'e_challenger_rbrk': (None, '["r453","r454","r455"]', '上游新范式信号已落地：Gemini Robotics 2（r453）、AlphaGenome Atlas（r454）、NVIDIA Cosmos 3（r455）—— 均为 vendor 自述，与 RBRK 数据安全挑战者关系为间接（具身 / 物理 AI 扩大受保护数据面），产业影响待 D'),
      'e_capability_nbis': (None, None, None),
    }
    for eid, (mech, ev_ids, ev) in E.items():
        if mech: m.set('edge_registry', eid, 'mechanism', mech, basis='doc25 §四；同 e_capability_nbis 机制族')
        if ev_ids: m.set('edge_registry', eid, 'evidence_ids', ev_ids, basis='库：from_metric 名下全部可见记录（取代后）')
        if ev: m.set('edge_registry', eid, 'evidence', ev, basis='同上')
        m.set('edge_registry', eid, 'owner', 'B', basis='B 初稿 D 复核'); m.set('edge_registry', eid, 'last_validated', '2026-09-20', basis=V)

    # ======== 来源：出版方 / 频率 / 可靠性 / URL / 归并 ========
    SM = (
        (SRC['aa_lb'], 'Artificial Analysis', '周', 'P1 第三方评测（自跑，含私有集）；数据以 vendor API 标价计成本；页面无显式更新日', None),
        (SRC['aa_v43'], 'Artificial Analysis', '版本事件', 'P1；版本文章日 = 榜单口径日', None),
        (SRC['aa_json'], 'Artificial Analysis', '周', 'P1；页面内嵌 JSON（price1mInputTokens / price1mOutputTokens / intelligenceIndexCostPerTask）', 'https://artificialanalysis.ai/leaderboards/models'),
        (SRC['hf'], 'Hugging Face', '日', 'P1 平台自报下载计数，可复现；下载 ≠ 用量', None),
        (SRC['swe'], 'SWE-bench（Princeton / Stanford）', '事件', 'P1 官方榜单页；「checked」标记区分团队复跑与自报', 'https://www.swebench.com/'),
        (SRC['swe_json'], 'SWE-bench（Princeton / Stanford）', '事件', 'P1；页面 <script id="leaderboard-data"> 内嵌 JSON（Verified 180 条），快照附前 25 条抽取', 'https://www.swebench.com/'),
        (SRC['arc3'], 'ARC Prize Foundation', '事件', 'P1 官方 JSON，generatedAt 2026-09-04；半私有集官方跑', None),
        (SRC['arc2'], 'ARC Prize Foundation', '事件', 'P1 官方 JSON，generatedAt 2026-09-04', 'https://arcprize.org/media/data/leaderboard/v2.json'),
        (SRC['arena'], 'LMArena', '周', 'P1 众包盲测 Elo；页面日期 2026-09-13，8.1M 票 402 模型', 'https://arena.ai/leaderboard/text'),
        (SRC['epoch'], 'Epoch AI', '持续', 'P1 独立研究机构数据库；Updated 2026-02-05', None),
        (SRC['oai_p'], 'OpenAI', '事件', 'P1 官方定价页；按 Short / Long context 与 Standard / Batch / Flex / Fast 分档', None),
        (SRC['oai_cl'], 'OpenAI', '事件', 'P1 官方 changelog；r159 归因句不在此页', None),
        (SRC['ant_p'], 'Anthropic', '事件', 'P1 官方定价页；含 Sonnet 5 取消涨价声明', None),
        (SRC['goog_p'], 'Google', '事件', 'P1 官方定价页；3.8 / 3.7 / 3.6 Flash 均标 2027-01-01 翻倍', None),
        (SRC['orr'], 'OpenRouter', '日（页面）/ 周（口径）', 'P3 聚合站（本轮改标 P3）；只代表 OpenRouter 路由；「as text」表节可完整读出，2026-09-20 复核通过', None),
        (SRC['gdm_robo'], 'Google DeepMind', '事件', 'P1 lab 官方博客，vendor 自述', None),
        (SRC['gdm_ag'], 'Google DeepMind', '事件', 'P1 lab 官方博客，vendor 自述；论文自托管 PDF', None),
        (SRC['nv'], 'NVIDIA', '事件', 'P1 公司官方博客，vendor 自述；榜单排名为转述', None),
        (SRC['qm'], 'QuestMobile 研究院', '季', 'P3 第三方监测，公开摘要免费、全文付费；官方页有防伪声明', None),
    )
    for sid, pub, freq, note, url in SM:
        m.set('source_master', sid, 'publisher', pub, basis='来源页'); m.set('source_master', sid, 'frequency', freq, basis='—'); m.set('source_master', sid, 'reliability_note', note, basis='—'); m.set('source_master', sid, 'last_validated', '2026-09-20', basis=V)
        if url: m.set('source_master', sid, 'url', url, basis='本轮实际打开的 URL')
    m.set('source_master', SRC['orr'], 'verify_status', 'confirmed', basis='2026-09-20 复核：页面「as text」表完整读出'); m.set('source_master', SRC['orr'], 'source_tier', 'P3', basis='聚合站，非一手')
    m.set('source_master', SRC['qm'], 'source_kind', 'data_aggregator', basis='第三方监测机构'); m.set('source_master', SRC['qm'], 'access', 'paywall', basis='摘要免费、全文付费')
    for old, new in ((SRC['orr2'], SRC['orr']), (SRC['oai_cl2'], SRC['oai_cl']), (SRC['ant_p2'], SRC['ant_p'])):
        m.set('source_master', old, 'superseded_by', new, basis='「同上」占位来源归并到带 URL 的正源'); m.set('source_master', old, 'verify_status', 'stale', basis='同上')
    for old, why in ((SRC['para_old'], 'r154 已被 r453–r455 取代'), (SRC['app_old'], 'r164 已被 r456 取代')):
        m.set('source_master', old, 'verify_status', 'stale', basis=why); m.set('source_master', old, 'reliability_note', '无 URL 的占位来源；其记录已被取代', basis='—')
