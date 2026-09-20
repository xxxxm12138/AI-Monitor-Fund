# -*- coding: utf-8 -*-
"""基础数据:AI 发展传播图【结构】——照抄 doc25 §1.2 逐票链式图(A1 交叉引用 edge_registry 核对)。
设计:结构(本文件,稳定,源自 doc25)与 权重(运行时从库 v_edge_calc 读,不手填)分离。
每条 CHAIN = 一条 doc25 映射链,对到一个真实 edge_id;中间机制用共享词表 MECH,同名合并 → 传播时扇出。
维护:doc25 §1.2 改了才改这里;权重/方向/tier 全部 propagate.py 按 edge_id 从库取。B 据 A1 报告落稿,待 D 复核。"""

# ---- 共享机制节点(A1 去重词表:同义合并,使传播可扇出)----
MECH = {
    'k_cluster_build':      ('全球 AI 集群在建强度', 'D1'),
    'k_neocloud_env':       ('neocloud 扩张环境', 'D1'),
    'k_nbis_capacity_exec': ('NBIS 产能执行 / 上电', 'D1'),
    'k_lab_buypower':       ('lab 算力采购力', 'D3'),
    'k_infer_train_demand': ('推理 / 训练需求', 'D5/D6'),
    'k_infer_elasticity':   ('推理需求弹性(cost/token)', 'D6'),
    'k_gpu_supply_cost':    ('GPU 供给 / 成本', 'D7/D1'),
    'k_dc_power_approval':  ('数据中心用电审批 / 上电节奏', 'D7'),
    'k_dc_power_solution':  ('数据中心供电方案(基荷/共址)', 'D7'),
    'k_dc_power_demand':    ('数据中心电力需求(建设驱动)', 'D1'),
    'k_gov_budget':         ('企业数据治理 / 合规预算', 'D2/D6/D7'),
    'k_enterprise_data_ready': ('企业需备好 / 护住 AI 数据', 'D6'),
    'k_d1_subnode':         ('D1 算力子节点(HBM/存储/光/加速器/整机)', 'D1'),
}

# ---- 链:(edge_id, ticker, from_metric, dim, [中间机制 id 有序], hops, edge_type) ----
# hops / edge_type 照 doc25 §1.2;from_metric / edge_id 经 A1 核库;NBIS 前 13 条 = doc25 七条链(含库内并置代理),后 6 条 = 库比 doc25 多出的边(E4/E6 等)。
CHAINS = [
    # ===== NBIS · doc25 §1.2 七条链 =====
    ('e_optics_nbis',      'NBIS', 'm_cn_optics_zte',        'D1', ['k_cluster_build', 'k_neocloud_env'], 3, 'E2_supplier'),   # 链1 光互连(旭创)
    ('e_eoptolink_nbis',   'NBIS', 'm_cn_optics_eoptolink',  'D1', ['k_cluster_build', 'k_neocloud_env'], 3, 'E2_supplier'),   # 链1 光互连(新易盛)
    ('e_capex_nbis',       'NBIS', 'm_hyperscaler_capex',    'D1', ['k_cluster_build'],                    2, 'E5_theme'),      # 链1 在建强度(capex 代理)
    ('e_backlog_nbis',     'NBIS', 'm_nbis_backlog',         'D1', [],                                     0, 'E1_self'),       # 链2 本体
    ('e_power_nbis',       'NBIS', 'm_nbis_capacity',        'D1', ['k_nbis_capacity_exec'],               1, 'E2_supplier'),   # 链3 电力上电 ★
    ('e_labfund_nbis',     'NBIS', 'm_lab_funding_reflection','D3',['k_lab_buypower'],                     2, 'E3_customer'),   # 链4 lab 融资
    ('e_frontierfund_nbis','NBIS', 'm_lab_funding_frontier', 'D3', ['k_lab_buypower'],                     2, 'E3_customer'),   # 链4 其他 lab 融资
    ('e_capability_nbis',  'NBIS', 'm_train_compute_epoch',  'D5', ['k_infer_train_demand', 'k_lab_buypower'], 3, 'E3_customer'), # 链5 能力→需求
    ('e_aa_nbis',          'NBIS', 'm_aa_intel_index',       'D5', ['k_infer_train_demand', 'k_lab_buypower'], 3, 'E3_customer'), # 链5 代理
    ('e_bench_nbis',       'NBIS', 'm_bench_frontier',       'D5', ['k_infer_train_demand', 'k_lab_buypower'], 3, 'E3_customer'), # 链5 代理
    ('e_power_reg_nbis',   'NBIS', 'm_dc_power_iea',         'D7', ['k_dc_power_approval'],                2, 'E5_theme'),      # 链6 电力政策
    ('e_export_nbis',      'NBIS', 'm_export_ctrl_bis',      'D7', ['k_gpu_supply_cost'],                  2, 'E5_theme'),      # 链7 出口管制
    ('e_token_nbis',       'NBIS', 'm_token_usage',          'D6', ['k_infer_train_demand'],               2, 'E3_customer'),   # §二额外 token 用量
    # ===== NBIS · 库比 doc25 §1.2 多出的边(A1 §②;E4/E6 新边型,建议回填 doc25)=====
    ('e_gpu_nbis',         'NBIS', 'm_gpu_ship',             'D1', ['k_gpu_supply_cost'],                  1, 'E2_supplier'),
    ('e_crwv_nbis',        'NBIS', 'm_crwv_peer',            'D1', [],                                     1, 'E4_competitor'),  # 同业 read-through
    ('e_circular_nbis',    'NBIS', 'm_circular_financing',   'D3', [],                                     1, 'E6_flow'),        # 循环融资 regime
    ('e_costtoken_nbis',   'NBIS', 'm_cost_per_token',       'D6', ['k_infer_elasticity'],                 2, 'E3_customer'),
    ('e_openclosed_nbis',  'NBIS', 'm_open_vs_closed',       'D5', ['k_infer_elasticity'],                 2, 'E3_customer'),
    ('e_priceperf_nbis',   'NBIS', 'm_infer_price_perf',     'D5', ['k_infer_elasticity'],                 2, 'E3_customer'),
    ('e_infer_arch_nbis',  'NBIS', 'm_infer_arch',           'D5', ['k_infer_elasticity', 'k_neocloud_env'], 3, 'E3_customer'),   # 0023 议题①:DSA 类架构降本→用量↑→NBIS(T3 弱利好,收入弹性 caveat 见边 note)
    # ===== RBRK · doc25 四条链 =====
    ('e_adoption_rbrk',    'RBRK', 'm_enterprise_adoption',  'D6', ['k_enterprise_data_ready'],            2, 'E3_customer'),
    ('e_datagov_rbrk',     'RBRK', 'm_copyright_lit',        'D2', ['k_gov_budget'],                       2, 'E3_customer'),
    ('e_reg_rbrk',         'RBRK', 'm_ai_regulation',        'D7', ['k_gov_budget'],                       2, 'E5_theme'),
    ('e_challenger_rbrk',  'RBRK', 'm_new_paradigm',         'D5', [],                                     1, 'E4_competitor'),  # 做空侧
    # ===== FCEL · doc25 两条链 + 库本体 =====
    ('e_energy_fcel',      'FCEL', 'm_energy_grid',          'D7', ['k_dc_power_solution'],                2, 'E5_theme'),
    ('e_dcbuild_fcel',     'FCEL', 'm_dc_power_iea',         'D1', ['k_dc_power_demand'],                  2, 'E3_customer'),
    ('e_dcppa_fcel',       'FCEL', 'm_fcel_dc_ppa',          'D1', [],                                     0, 'E1_self'),
    # ===== 算力尾仓 · 各 1 跳 E2 到 D1 子节点(共享 k_d1_subnode → 扇出)=====
    ('e_d1_mu',            'MU',   'm_hbm_cowos',            'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_d1_sndk',          'SNDK', 'm_hbm_cowos',            'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_d1_cien',          'CIEN', 'm_800g_shipment',        'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_d1_poet',          'POET', 'm_800g_shipment',        'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_d1_mrvl',          'MRVL', 'm_gpu_ship',             'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_d1_intc',          'INTC', 'm_gpu_ship',             'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_d1_supx',          'SUPX', 'm_gpu_ship',             'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_d1_amd',           'AMD',  'm_gpu_ship',             'D1', ['k_d1_subnode'],                       1, 'E2_supplier'),
    ('e_anthropic_amd',    'AMD',  'm_lab_funding_frontier', 'D3', [],                                     1, 'E3_customer'),   # 需求侧多出边
]

TICKERS = sorted({c[1] for c in CHAINS})
DIMS = {'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'}
# STAA:doc25 标 out-of-AI-scope,库中 0 边,故不入图(按设计缺席)。
