# -*- coding: utf-8 -*-
"""0023 · 影响力闸新框架暴露的修正(① DSA 拆节点+加边 · ② 开源追近 regime watch · 纯B口径修正)· owner B/D · 2026-09-20
D 2026-09-20 拍板:
议题①:拆 m_infer_arch(推理架构效率:DSA/MoE调度/KV-cache),r504 移入;加 m_infer_arch→NBIS 边,方向 T3 弱利好↑,
  edge note 必带收入弹性 caveat(token 用量↑为强假设;净收入取决于 计费模式/成本红利去向/价格弹性;按卡时计费时单卡吞吐↑反可能压缩卡时收入;T3 不量化)。理由=Jevons 效应下总用量方向稳、但收入端弹性存疑。
议题②:e_open_vs_closed 维持 watchlist 不定向(regime watch),加三观察信号(签约量/利用率、毛利率、自托管份额);r146 方向标 →。
纯 B 口径:r153 补 AA 来源 URL;光模块 T1 标海关系数未校准占位(C1);RBRK/尾仓上游标 T2-only/P3 定性。"""
import json
OWNER = 'D'
CAVEAT = ('token 用量↑为强假设;NBIS 总收入净方向取决于:(a)计费按 token 还是 GPU 卡时;(b)成本红利留毛利端还是转化为降价;'
          '(c)需求价格弹性。按卡时计费时,单卡吞吐提升反而可能压缩卡时收入。T3 不量化量级。(Jevons:单位成本↓→总 token 通常指数↑,方向稳)')

def up(m):
    # ===== 议题① 拆 m_infer_arch + 移 r504 + 加 NBIS 边 =====
    m.insert('metric_registry', dict(
        metric_id='m_infer_arch', name='推理架构效率(DSA/MoE调度/KV-cache)', entity_id='ent_frontier_cap',
        ticker_or_entity='前沿模型能力（赛道）', entry='AI', dim='D5', data_class='4', signal_role='predictor',
        source_family='arXiv/lab 技术报告', frequency='事件', owner='D', availability='🟢',
        status='testing', fill_status='已填'), basis='议题① D 拍板:从 m_new_paradigm 拆出推理降本架构一类,避免具身/世界模型误外溢')
    m.sql("INSERT INTO metric_entity VALUES ('m_infer_arch','ent_frontier_cap')", basis='新指标挂实体')
    m.sql("INSERT INTO metric_factor VALUES ('m_infer_arch',0.9,0.3,0.9,0.3,0.3,'D5 前沿架构:r←P1/可复现;l 高(能力供给侧领先);s/e/φ 低(前沿信号)','D','draft')",
          basis='新指标因子(v_edge_calc 需要);待 D 复核')
    # r504 从 m_new_paradigm 移入 m_infer_arch(两表同改,同 0007 先例)
    m.set('stg_observation', 'r504', 'metric_id', 'm_infer_arch', basis='议题①:DSA 归推理架构效率,非泛新范式')
    m.set('fct_frontier', 'r504', 'metric_id', 'm_infer_arch', basis='同上')
    m.set('observation_direction', 'r504', 'direction', '↑', basis='议题①:对 NBIS 弱利好(见边 caveat)')
    m.set('observation_direction', 'r504', 'direction_note', 'DSA 降推理成本→Jevons 用量↑,弱利好;收入弹性见边 caveat', basis='议题①')
    # 加边 m_infer_arch → NBIS(T3 方向,弱利好,带 caveat)
    m.insert('edge_registry', dict(
        edge_id='e_infer_arch_nbis', from_metric='m_infer_arch', to_ticker='NBIS', side='demand',
        edge_type='E3_customer', hops=3, map_path='推理成本↓ → neocloud 用量↑',
        mechanism='推理架构降本(DSA/MoE调度/KV-cache)→ 单位推理成本↓ → Jevons 总 token 用量↑ → neocloud 需求',
        cert_tier='T3', cert_method='方向级,不量化(收入弹性存疑)', is_key='★', evidence_ids=json.dumps(['r504']),
        owner='D', status='testing', notes=CAVEAT), basis='议题① D 拍板:T3 弱利好边 + 收入弹性 caveat')

    # ===== 议题② 开源追近:regime watch 不定向 =====
    m.set('edge_registry', 'e_openclosed_nbis', 'notes',
          'regime watch,不定向(开源追近对 NBIS 双向:利好自部署推理需求↑ vs 利空前沿闭源租用↓)。观察三信号:①开源模型发布后 1-2 季 neocloud 签约量/利用率变化 ②头部 neocloud 毛利率走势 ③企业自托管 vs 闭源 API 份额切换。当前倾斜(仅参考不入边):近 1-2 年偏短期利好(自部署上量),中长期单价 commoditize 压利润率,正负对冲,证据不足以定向。',
          basis='议题② D 拍板')
    m.set('observation_direction', 'r146', 'direction', '→', basis='议题②:regime watch 不定向')
    m.set('observation_direction', 'r146', 'direction_note', '开源追近双向,不下注方向;跟踪签约量/毛利率/自托管份额', basis='议题②')

    # ===== 纯 B 口径修正 =====
    m.set('fct_frontier', 'r153', 'source_url', 'https://artificialanalysis.ai/leaderboards/models', basis='补 AA 来源 URL(每任务成本读数)')
    for eid in ('e_optics_nbis', 'e_eoptolink_nbis'):
        m.set('edge_registry', eid, 'notes',
              'T1 结构成立但"未校准":海关 HS8517→光模块占比系数为 placeholder(C1),标定前领先读数只作方向、不下注量级。', basis='KPI-NOWCAST-TIERS 缺口③')
    m.set('edge_registry', 'e_adoption_rbrk', 'notes',
          'T2-only:RBRK 链无另类地面数据,doc24v2 列的 JD/招聘/支出调查未接入,只能事后结构对账(Sub/NN-ARR 互校),不能真 nowcast。', basis='KPI-NOWCAST-TIERS 缺口①')
    for eid in ('e_d1_mu', 'e_d1_sndk'):
        m.set('edge_registry', eid, 'notes', '上游 m_hbm_cowos 付费定性 P3、未标定 → 终点缺量级 nowcast(T1 候选实为 P3 定性)。', basis='KPI-NOWCAST-TIERS 缺口②')
