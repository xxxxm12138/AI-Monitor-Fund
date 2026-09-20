# -*- coding: utf-8 -*-
"""0020 · D5/D6 能力前沿 + D2 数据供给 联网采集补缺(REPRESENT/COLLECT)· owner B · 2026-09-20
两个只读联网子 agent 实际打开页面采集,已与库比对去重(NYT/DOJ SOI r110/r111、Wiley $49M r113、Scale/Surge r107/109、合成数据 SynPro r500 均已在库,不重复)。
只落库中 0 命中的真新记录 8 条 + 新指标 m_rl_environments;证伪闸(source_stance/verifiability)按采集标注填,影响力闸(industry_impact)一律留空给 D 判。
取代 r145(m_arxiv_topic_slope 占位「待建」)。所有数值带实际打开的来源 URL;vendor_pr/未核一手者标 claimed_only。搜索摘要未打开一手页的(Kimi K3/TEMPO/RLVR 等)本轮不入库,待逐条 fetch。"""
OWNER = 'B'
EF = 'ent_frontier_cap'
# 来源(子 agent 实际打开)
S_TREND = 'AI Papers Academy · AI Research Trends 2026 H1 https://aipapersacademy.com/ai-research-trends-2026-h1/'
S_DSA   = 'DeepSeek-AI · DeepSeek Sparse Attention arXiv 2512.02556 https://arxiv.org/abs/2512.02556'
S_MERC  = 'Inception · Mercury 2.5 新闻稿(Yahoo Finance 镜像) https://sg.finance.yahoo.com/news/inception-launches-mercury-2-5-163000864.html'
S_RLENV = 'Epoch AI Gradient Updates · State of RL Envs https://epoch.ai/gradient-updates/state-of-rl-envs'
S_MERCOR= 'Value Add VC(转引 Bloomberg/Forbes) https://valueaddvc.com/pulse/mercor-20b-valuation-talks-2026'
S_ANTH  = 'Authors Guild · 法院终审批准 Anthropic 版权和解 https://authorsguild.org/news/court-grants-final-approval-anthropic-copyright-settlement/'

def up(m):
    # ---- 新指标:RL 环境作为数据供给新形态(D2)----
    m.insert('metric_registry', dict(
        metric_id='m_rl_environments', name='RL 环境(数据供给新形态)', entity_id=EF, ticker_or_entity='前沿 lab',
        entry='AI', dim='D2', data_class='2', signal_role='predictor', source_family='Epoch / The Information',
        frequency='事件', owner='B', availability='🟢', status='testing', fill_status='已填'),
        basis='E51 · 采集:RL 环境成为前沿 lab 数据供给约束(Epoch)')
    m.sql("INSERT INTO metric_entity VALUES ('m_rl_environments', 'ent_frontier_cap')", basis='新指标挂实体')

    # ---- D5 能力前沿:arXiv 主题斜率(填空白)----
    m.observe('r501', 'm_arxiv_topic_slope', '前沿模型能力（赛道）', 'actual',
              'long-horizon planning 提及 +510%（264→1,611，2026H1 arXiv 增长最快主题）；agentic workflows 4,585→10,496',
              '17万篇 arXiv 主题计数', '2026H1', '2026-06-30', S_TREND, 'P3',
              note='“long-horizon planning … the fastest-growing topic”；底层为 170,927 篇 arXiv(2025初–2026-06)计数')
    m.observe('r502', 'm_arxiv_topic_slope', '前沿模型能力（赛道）', 'actual',
              'SSM/Mamba 论文份额 −20%（495→492 绝对持平）；扩散模型份额 −15%（绝对增至 1,774）；合成数据份额 −24% —— 与扩散商用落地(r505)形成张力',
              '份额变化', '2026H1', '2026-06-30', S_TREND, 'P3', note='学术份额降温 vs 工程落地推进的背离')
    m.observe('r503', 'm_arxiv_topic_slope', '前沿模型能力（赛道）', 'actual',
              'Reasoning/CoT 绝对量第一 11,636 篇；Qwen 提及 +98%（752→1,489）首超 Llama；Gemma +147%；Claude +130%',
              '提及计数', '2026H1', '2026-06-30', S_TREND, 'P3', note='开源生态权力转移:Qwen 反超 Llama')

    # ---- D5 能力前沿:架构/方法范式 ----
    m.observe('r504', 'm_new_paradigm', '前沿模型能力（赛道）', 'actual',
              'DeepSeek-V3.2 提出 Sparse Attention（DSA：lightning indexer + 细粒度 token 选择），长上下文大幅降注意力复杂度、性能基本不退；开放权重',
              '架构/方法', '2025-12', '2025-12-02', S_DSA, 'P1',
              note='“DeepSeek Sparse Attention”；开放权重可第三方复现;“超 GPT-5”/IMO 金牌属自述')
    m.observe('r505', 'm_new_paradigm', '前沿模型能力（赛道）', 'actual',
              'Inception 发布 Mercury 2.5 扩散语言模型（dLLM），宣称 >1,100 tokens/s、260K 上下文，定价 $0.20/$0.75（促销 $0.04/$0.15）',
              '方法/架构', '2026-09', '2026-09-08', S_MERC, 'P1',
              note='“more than 1,100 tokens per second”；吞吐/质量均厂商自述,未见第三方复测')

    # ---- D2 数据供给:RL 环境 / Mercor / Anthropic 和解(库中 0 命中)----
    m.observe('r506', 'm_rl_environments', '前沿模型能力（赛道）', 'event',
              'Anthropic 讨论未来一年在 RL 环境支出 >$1B（截至 2025-09，转引 The Information）；任务定价 $200–2,000/任务（复杂 SWE 偶达 $20,000）；独占溢价 4–5x；高保真网站副本(如 Slack)达 $300,000',
              'USD', '2026-01', '2026-01-12', S_RLENV, 'P2',
              note='数据供给从静态语料→可验证交互环境;>$1B 为 claimed_only(转引),定价区间访谈汇总')
    m.observe('r507', 'm_data_labeling', 'Scale AI（标注/数据）', 'event',
              'Mercor 2026-07 洽谈以 ~$20B 估值募 ~$500M（较 2025-09 的 $10B 四个月翻倍）；CEO 称年化营收破 $2B；~30,000 承包商（日付 >$150万）',
              'USD B', '2026-07', '2026-07-09', S_MERCOR, 'P3',
              note='“$20 billion valuation”洽谈中(claimed_only);印证约束从算力→专家验证型高质量数据')
    m.observe('r508', 'm_copyright_lit', 'NYT × OpenAI 案', 'event',
              'Bartz v. Anthropic $15亿版权和解 2026-07-20 终审批准（全美最大版权和解）；约 $3,000/作品（法定最低 $750 的 4x）；Anthropic 须销毁 LibGen/PLM 盗版文件',
              'USD B', '2026-07', '2026-07-20', S_ANTH, 'P2',
              note='“final approval”;为「盗版语料」路径定价基准,影响数据获取成本预期')

    # ---- 取代占位 ----
    m.supersede('r145', 'r501', 'm_arxiv_topic_slope 占位「待建」→ 真采集(2026H1 主题斜率)')

    # ---- 证伪闸(fct_frontier 类4 记录):按采集标注;影响力闸留空给 D ----
    for rid, stance, verif in [('r501', 'neutral', 'claimed_only'), ('r502', 'neutral', 'claimed_only'),
                               ('r503', 'neutral', 'claimed_only'), ('r504', 'neutral', 'reproducible'),
                               ('r505', 'vendor_pr', 'claimed_only')]:
        m.set('fct_frontier', rid, 'source_stance', stance, basis='doc29 证伪闸 · 采集标注')
        m.set('fct_frontier', rid, 'verifiability', verif, basis='doc29 证伪闸 · 采集标注')
