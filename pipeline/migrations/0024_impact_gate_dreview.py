# -*- coding: utf-8 -*-
"""0024 · 影响力闸 20 条 D 复核留痕 · owner D · 2026-09-20
D 2026-09-20 复核 0022 起草的 20 条影响力闸评级(IMPACT-GATE-REVIEW.md):
除 r147 外全部维持起草评级;r147 评级不变(中),渠道修正为「需求+竞争替代(双向)」(下载≠生产部署:部分转自部署=需求↑、部分替代闭源API=竞争替代,占比无法拆→净方向不定)。
结论确认:6 高外溢(r142/r143旁证/r146单向不下注/r153/r500纯KPI/r504收入弹性caveat)· r501 高但证伪未过锁 watchlist · 13 雷达(中/低,不外溢)。
r150/r453 不升高(远期/学术标尺,缺近中期落地算力转化链)· r505 不升高(潜力高但 vendor_pr,待第三方复测再评)。
本迁移 = D 复核的入库留痕(B 起草 0022 → D 复核 0024)。"""
OWNER = 'D'
R147 = '[L:中·渠道:需求+竞争替代(双向)·落点:开源生态份额/自部署推理需求·M:中·雷达] 开源下载≠生产部署:部分转自部署(需求↑)、部分替代闭源API(竞争替代),两效应占比无法拆→净方向不定;生态活跃度代理,对NBIS间接。'

def up(m):
    # r147:评级不变(中),渠道修正为双向
    m.set('fct_frontier', 'r147', 'impact_rationale', R147, basis='D 复核:渠道改需求+竞争替代双向')
    m.decide('d_impact_gate', '中', 'D 复核:r147 渠道修正为需求+竞争替代(双向),评级维持中', target='fct_frontier:r147.industry_impact',
             confidence='M', executor='D', executor_kind='human',
             state_anchor={'record_id': 'r147', 'review': 'D 2026-09-20', 'framework': 'likelihood×渠道×KPI'},
             note='D 复核留痕:渠道改双向,级不变')
    # 20 条整体 D 复核留痕(其余 19 条维持 0022 起草评级,不逐条重记;本条为批次确认)
    m.decide('d_impact_gate', '中', 'D 复核 20 条影响力闸(IMPACT-GATE-REVIEW.md):除 r147 渠道改双向外全部维持起草评级;'
             '外溢集(r142/r146/r153/r500/r504)+ r143旁证 确认,r501 锁 watchlist,r150/r453/r505 不升高。批次确认。',
             target='fct_frontier:r144.industry_impact', confidence='H', executor='D', executor_kind='human',
             state_anchor={'batch': '20 条', 'review': 'D 2026-09-20', 'verdict': '维持起草,仅 r147 渠道改'},
             note='D 复核批次留痕(挂 r144 作锚,不改其值);逐条评级见 0022 + 本条备注')
