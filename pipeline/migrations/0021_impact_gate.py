# -*- coding: utf-8 -*-
"""0021 · 影响力闸(d_impact_gate)起草 20 条活跃前沿记录 · owner B(起草)· 2026-09-20
承 TODO P0-1 / doc29 §四。对 fct_frontier 20 条活跃记录(r145/r154/r172 占位已取代,跳过)按五判据
(改算力需求结构 / 降本 / 被产业采用 / 落地路径 / 触瓶颈层)起草 industry_impact 高/中/低 + rationale,
落 decision_log(d_impact_gate,executor=B 起草,待 D 复核)并同步写回 fct_frontier.industry_impact。
两闸串联:外溢到票 = 影响高 AND 证伪过(third_party_verified / reproducible)。
本轮判定 6 条外溢(r500/r153/r504/r142/r143/r146),r501 影响高但 claimed_only → 留 watchlist 不外溢。"""
OWNER = 'B'
# (record_id, industry_impact, confidence, rationale)
GATE = [
    ('r500', '高', 'H', '合成数据(SynPro)把有效 token 放大 3.4–5.2×,直接缓解 D2 数据瓶颈并降训练成本;reproducible → 外溢'),
    ('r153', '高', 'H', '每任务推理成本 7.63/3.26/2.01,直接落 cost/token 降本主线;third_party → 外溢'),
    ('r504', '高', 'H', '稀疏注意力 DSA 降长上下文注意力算力、开放权重易被采用,触算力瓶颈;reproducible → 外溢'),
    ('r142', '高', 'H', '训练算力 5×/年 = D1 算力需求根驱动,定需求量级;third_party → 外溢'),
    ('r143', '高', 'H', '训练算力 4–5×/年(notable 口径),同上;third_party → 外溢'),
    ('r146', '高', 'H', '开源vs闭源差距(53 vs 45)决定自部署可行性→推理需求结构与模型层价值分配;third_party → 外溢'),
    ('r501', '高', 'M', 'long-horizon/agentic 论文 +510% = 推理需求结构主线;但源 claimed_only(博客汇总 arXiv 计数)→ 证伪未过,留 watchlist 不外溢'),
    ('r144', '中', 'M', 'AA 智能指数 = 能力前沿标尺,给方向,不直接改算力/成本'),
    ('r502', '中', 'M', 'SSM/Mamba 学术份额降温,对"SSM 取代 Transformer"叙事是反向证据,方向性'),
    ('r503', '中', 'M', 'Qwen 提及首超 Llama = 开源生态权力转移 + 中国侧信号,方向性'),
    ('r148', '中', 'M', 'SWE-bench 79.2%(提交方自报 claimed_only)agentic coding 进展,间接拉推理需求'),
    ('r149', '中', 'M', 'SWE-bench Bash Only 76.8%(团队统一环境),能力方向'),
    ('r150', '中', 'M', 'ARC-AGI-3 99.9%/62.7%,前沿推理能力标尺,方向'),
    ('r151', '中', 'M', 'ARC-AGI-2 95%,能力方向'),
    ('r152', '中', 'M', 'LMArena 1506(众包 Elo,噪声较大),能力方向'),
    ('r453', '中', 'M', 'Gemini Robotics 2 VLA 控制人形 = 具身新范式,长期重排 L6,对当前算力书间接'),
    ('r454', '中', 'M', 'AlphaGenome Atlas AI4S(1PB),科研影响大但对算力/票间接'),
    ('r455', '中', 'M', 'Cosmos 3 世界模型开放权重,拉仿真/推理算力需求,方向'),
    ('r505', '中', 'M', 'Mercury 2.5 扩散模型潜在冲击推理成本结构,但 vendor_pr/claimed_only 未第三方证 → 封顶中,待证升高'),
    ('r147', '中', 'M', '开源模型采用量(HF 下载),开源生态方向'),
]

def up(m):
    for rid, impact, conf, why in GATE:
        m.decide('d_impact_gate', impact, why, target=f'fct_frontier:{rid}.industry_impact',
                 confidence=conf, executor='B', executor_kind='human',
                 state_anchor={'record_id': rid, 'gate': 'doc29 影响力闸五判据', 'as_of': '2026-09-20'},
                 note='B 起草,待 D 复核(d_impact_gate owner=D)', sync=True)
        m.set('fct_frontier', rid, 'impact_rationale', why, basis='doc29 影响力闸 · B 起草待 D')
