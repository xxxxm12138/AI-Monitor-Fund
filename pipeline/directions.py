# -*- coding: utf-8 -*-
# 方向判断（B 初稿 · D 复核）。语义：相对「这个节点所喂的持仓票的 thesis」——
# ↑ 增强 · ↓ 削弱 · → 中性 / 未变 · ! regime 冲击或双向，需人判 · — 不适用（上期 / 仓位 / 计算值 / 纯指引）
# 登记为假设 A11：方向是判断不是数据；未复核前只用于排序与状态显示，不进阈值。
import re
DEFAULT_BY_METRIC = {
 # 持仓本体
 'm_nbis_rev':'↑','m_nbis_ebitda':'↑','m_nbis_arr':'↑','m_nbis_backlog':'↑','m_nbis_capacity':'↑','m_nbis_calltone':'↑','m_reconcile_nbis':'↑',
 'm_rbrk_rev':'↑','m_rbrk_sub_arr':'↑','m_rbrk_cloud_arr':'↑','m_rbrk_nn_arr':'↑','m_rbrk_fcf':'↑','m_rbrk_ai_product':'↑',
 'm_staa_sales':'↑','m_staa_china':'↑','m_staa_units':'↑','m_staa_ni':'↑','m_staa_event':'!',
 'm_fcel_rev':'↓','m_fcel_backlog':'↑','m_fcel_dc_ppa':'↑','m_fcel_capacity':'→','m_fcel_cash':'→',
 'm_tail_supx':'↑','m_tail_sndk':'↑','m_tail_mu':'↑','m_tail_intc':'↑','m_tail_cien':'↑','m_tail_mrvl':'↑','m_tail_poet':'↑','m_tail_amd':'↑',
 'm_slmt':'—','m_13f_book':'→','m_hkex_0679':'→',
 # D1
 'm_cn_optics_zte':'↑','m_cn_optics_eoptolink':'↑','m_cn_optics_customs':'—','m_800g_shipment':'↑','m_hbm_cowos':'↑','m_gpu_ship':'↑',
 'm_capex_msft':'↑','m_capex_googl':'↑','m_capex_amzn':'↑','m_capex_meta':'↑','m_hyperscaler_capex':'↑','m_gpu_rental_price':'—','m_dc_power_iea':'↑',
 # D2
 'm_data_wall':'—','m_data_labeling':'→','m_copyright_lit':'→',
 # D3
 'm_lab_funding_reflection':'↑','m_lab_contract_reflection_nbis':'↑','m_lab_funding_cohere':'→','m_lab_funding_frontier':'↑','m_vc_flow':'—','m_circular_financing':'!','m_crwv_peer':'↑','m_preipo_pool':'—',
 # D4
 'm_talent_flow':'—',
 # D5
 'm_train_compute_epoch':'↑','m_aa_intel_index':'→','m_arxiv_topic_slope':'—','m_open_vs_closed':'→','m_bench_frontier':'→','m_infer_price_perf':'↑','m_new_paradigm':'—',
 # D6
 'm_enterprise_adoption':'↑','m_cost_per_token':'↑','m_token_usage':'↑','m_app_retention_cn':'—',
 # D7
 'm_export_ctrl_bis':'!','m_domestic_sub_policy':'—','m_energy_grid':'—','m_ai_regulation':'—','m_safety_incident':'—',
}
# 记录级覆盖：(metric_id, 实体片段, 值片段) → (方向, 一句理由)
OVERRIDES = [
 ('m_nbis_calltone','NBIS','20–25 USD B',('→','capex 指引重申，无增量')),
 ('m_nbis_calltone','NBIS','~50%',('↑','AI 分部利润率口径 P2，待钉')),
 ('m_fcel_cash','FCEL','−45.3',('↑','净亏收窄')),
 ('m_fcel_capacity','FCEL','~37.1',('→','产能现值，对目标 100MW 仍差 63MW')),
 ('m_tail_supx','SUPX','AI 基础设施板块',('↓','AI 板块无收入，叙事未兑现')),
 ('m_hkex_0679','0679','423.9',('→','收入增但亏损，非 AI')),
 ('m_hkex_0679','0679','盈利警告',('↓','公允值亏损致亏')),
 ('m_gpu_ship','NVDA','108.0',('!','指引 +12% 但明确不含中国 DC compute：供给强、D7 未兑现')),
 ('m_data_labeling','Scale AI','CEO',('→','管理层变动，方向不明')),
 ('m_copyright_lit','NYT','DOJ',('!','DOJ 支持 fair use：对 RBRK 数据治理顺风偏空，非裁定')),
 ('m_copyright_lit','NYT','summary',('→','程序性')),
 ('m_copyright_lit','Reddit','43',('↑','数据授权收入 +24%')),
 ('m_copyright_lit','Wiley','49',('↑','AI 授权收入 +23%')),
 ('m_copyright_lit','Meta','内容协议',('↑','授权而非诉讼')),
 ('m_lab_funding_cohere','Cohere','240',('→','ARR 稳，2026 无更新')),
 ('m_lab_funding_cohere','Cohere','Schwarz',('↑','拿到结构化融资')),
 ('m_lab_funding_cohere','Cohere','Series E 在谈',('→','在谈未完成')),
 ('m_lab_funding_frontier','OpenAI','员工要约',('→','二级流动性，非新增资本')),
 ('m_lab_funding_frontier','xAI','估值',('→','媒体口径')),
 ('m_circular_financing','NVIDIA','18.6',('!','10-Q 一手：私营投资规模，循环融资敞口基数')),
 ('m_aa_intel_index','Artificial Analysis','53',('→','榜首并列，无拐点')),
 ('m_open_vs_closed','Artificial Analysis','53 vs 45',('→','差距 8 分，开源追赶中')),
 ('m_open_vs_closed','Hugging Face','22,967,391',('↑','开源下载量高位')),
 ('m_bench_frontier','ARC-AGI-3','99.9%',('↑','新纪录')),
 ('m_bench_frontier','ARC-AGI-2','95.0%',('↑','新纪录')),
 ('m_cost_per_token','OpenAI GPT-6 Astra','10 / 50',('→','前沿档一年未降')),
 ('m_cost_per_token','Anthropic Claude Fable 5.1','10 / 50',('→','前沿档一年未降')),
 ('m_cost_per_token','Google Gemini 3.8 Flash','0.75',('!','已公告 2027-01-01 涨价一倍，cost/token 非单调下行')),
 ('m_cost_per_token','OpenAI GPT-5.6 Luna','Luna',('↑','中低档降价 80%，需求弹性')),
 ('m_cost_per_token','OpenAI GPT-5.6 Sol','促销',('→','促销非永久')),
 ('m_cost_per_token','Anthropic Claude Sonnet 5','取消',('→','取消涨价，持平')),
 ('m_export_ctrl_bis','BIS','case-by-case',('!','许可放宽 = 供给可得 ↑；同日 25% 关税 = 成本 ↑；NVDA 指引未计入')),
 ('m_export_ctrl_bis','BIS','最终规则',('!','同上，法律生效')),
 ('m_export_ctrl_bis','White House','232',('!','关税，非抽成')),
 ('m_reconcile_nbis','NBIS','信念',('↑','供需同向；背离风险挂账 C18')),
]
NA_TYPES = {'prior','position','computed'}
def assign(r):
    if r['obs_type'] in NA_TYPES: return '—',''
    if r['obs_type']=='guidance' and r['metric_id'] not in ('m_nbis_capacity','m_800g_shipment'):
        # 指引本身不判方向，除非是被上调 / 目标（在 target 里处理）
        return '—',''
    for mid, ent, val, (d, why) in OVERRIDES:
        if r['metric_id']==mid and ent in r['entity'] and val in (r['value']+' '+r['unit']):
            return d, why
    d = DEFAULT_BY_METRIC.get(r['metric_id'],'—')
    return d, ''
