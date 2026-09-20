# -*- coding: utf-8 -*-
"""0022 · 影响力闸按新框架重判 20 条(取代 0021 旧 doc29 5 条清单)· owner B(起草)· 2026-09-20
新框架(D 2026-09-20 定,PLAN-graph-refactor §11.3):影响力 = likelihood(被采用×落地×可验证) × magnitude(经渠道:需求/成本/供给瓶颈/竞争替代) × target_KPI(动哪个可观测量)。
外溢 = 影响高 ∧ 证伪过(third_party/reproducible) ∧ target_KPI 可 nowcast(T1/T2,待②清单)。
每条 impact_rationale 结构化前缀 [L·渠道·落点·M·外溢]。0021 判断留在 decision_log(append-only),本轮新判断为最新(checks 7k 取最新)。
本轮相对 0021 的实质变化:①引入"渠道"→ 竞争替代渠道显式化(r146/r147/r502/r503);②引入"落点KPI"→ r500 落纯KPI、r504 暴露应加 NBIS 边(现错接 RBRK 竞对);③方向双向的 r146 标需人判。"""
OWNER = 'B'
# (rid, impact, conf, L, 渠道, 落点KPI, M, 外溢, 理由)
G = [
 ('r142','高','H','高','需求','AI算力总需求→NBIS云需求','高','外溢✓','训练算力5×/年=算力需求根驱动,third_party'),
 ('r143','高','H','高','需求','同r142','高','旁证·不重复外溢','r142旧口径(2024),同一事实,留旁证不重复外溢'),
 ('r146','高','H','高','需求+竞争替代','自部署推理需求↑ / 前沿闭源租用↓(双向)','中','外溢✓·方向需人判','开源追近53vs45:利好自部署推理 vs 利空前沿租用,方向双向,third_party'),
 ('r153','高','H','高','成本','推理 cost/token','高','外溢✓·待补URL','每任务成本=cost/token降本直接读数,third_party(source_url 待补)'),
 ('r500','高','H','中','供给瓶颈','有效token供给(纯KPI)','高','外溢✓·纯KPI落点','合成数据放大有效token 3.4–5.2×缓解D2数据墙,落纯KPI不落票,reproducible'),
 ('r504','高','H','高','成本+供给瓶颈','长上下文推理成本→NBIS','高','外溢✓·应加NBIS边','DSA降长上下文推理算力/成本,开放权重易采用;现边错接e_challenger_rbrk竞对,应加打NBIS的边,reproducible'),
 ('r501','高','M','高','需求','推理调用量/test-time compute','高','watchlist·证伪未过','long-horizon/agentic+510%=推理需求主线,但源claimed_only(博客汇总)未过证伪闸'),
 ('r144','中','M','高','能力标尺','能力前沿方向','低','雷达','AA智能指数=能力标尺,给方向不经具体渠道'),
 ('r147','中','M','中','竞争替代','开源生态份额','中','雷达','开源模型采用量(HF下载),开源vs闭源权力分配'),
 ('r148','中','M','中','需求','推理需求(agentic coding)','中','雷达','SWE-bench 79.2%(自报claimed_only),间接拉推理'),
 ('r149','中','M','中','需求','推理需求','中','雷达','SWE-bench Bash Only 76.8%(团队环境),能力方向'),
 ('r150','中','M','中','能力标尺','能力前沿方向','中','雷达','ARC-AGI-3,前沿推理能力标尺'),
 ('r151','中','M','中','能力标尺','能力前沿方向','中','雷达','ARC-AGI-2 95%,能力方向'),
 ('r152','中','M','低','能力标尺','能力前沿方向','低','雷达','LMArena 1506(众包Elo噪声大)'),
 ('r453','中','M','中','需求','具身算力需求(远)','中','雷达','Gemini Robotics 2 VLA控人形,具身长期需求,对当前书间接'),
 ('r454','中','M','中','科研','AI4S(远)','低','雷达','AlphaGenome Atlas AI4S,科研影响大对算力/票间接'),
 ('r455','中','M','中','需求','仿真/推理需求','中','雷达','Cosmos 3世界模型开放权重,拉仿真/推理需求'),
 ('r502','中','M','中','竞争替代','架构叙事(反向)','中','雷达','SSM/Mamba学术降温,"SSM取代Transformer"反证'),
 ('r503','中','M','中','竞争替代','开源份额/中国侧','中','雷达','Qwen提及首超Llama,开源权力转移+中国侧'),
 ('r505','中','M','中','成本','推理成本(潜在)','高(潜在)','雷达·待证升','Mercury 2.5扩散潜在冲击推理成本,但vendor_pr/claimed_only封顶中'),
]

def up(m):
    for rid, impact, conf, L, ch, kpi, M, out, why in G:
        rationale = f'[L:{L}·渠道:{ch}·落点:{kpi}·M:{M}·{out}] {why}'
        m.decide('d_impact_gate', impact, rationale, target=f'fct_frontier:{rid}.industry_impact',
                 confidence=conf, executor='B', executor_kind='human',
                 state_anchor={'record_id': rid, 'framework': 'likelihood×渠道×KPI(取代 doc29 5条)', 'as_of': '2026-09-20'},
                 note='新框架重判,取代 0021;待 D 复核', sync=True)
        m.set('fct_frontier', rid, 'impact_rationale', rationale, basis='影响力闸新框架 · B 起草待 D')
