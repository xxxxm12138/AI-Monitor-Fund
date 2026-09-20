# -*- coding: utf-8 -*-
"""节点五因子的规则默认（doc21 §6.1 锚点：H .9 / M .6 / L .3）。规则默认 = B 初稿；OVERRIDE 为逐点判断；全部 status=draft 待 D 复核。
r 由最佳 provenance 映射（A8）：P1→H、P2/P3→M、P4/P5/—→L。"""
H, M, L = 0.9, 0.6, 0.3
def r_from_prov(p):
    return H if p == 'P1' else (M if p in ('P2', 'P3', 'P3–P5') else L)
def e_rule(m):   # 独家性：中国侧一手 / 自建对账 = H；半公开（电话会、付费源、聚合） = M；全公开财报 / 官方 = L
    if m['metric_id'] == 'm_reconcile_nbis': return H
    if m['availability'] in ('🔵',): return M
    if any(k in (m['ticker_or_entity'] + m['name']) for k in ('300308', '300502', '海关', '中际', '新易盛')): return M   # 中国侧但公开披露
    if m['availability'] == '🟡': return M
    return L
def l_rule(m):   # 固有领先性：一级融资 / 前沿 = H；供应链月季 / 事件 = M；财报同步 / 仓位 = L
    dim = (m['dim'] or ''); role = (m['signal_role'] or ''); dc = (m['data_class'] or '')
    if m['entry'] == '持仓': return L
    if dim.startswith('D3') or dim.startswith('D5') or dim.startswith('D4'): return H
    if 'regime' in role: return M
    if dc.startswith('4'): return H
    return M
def s_rule(m):   # 可观测 / 信噪：结构化财报量价 = H；事件 / 电话会 = M；前沿 / 舆情 / 未标定 = L
    dc = (m['data_class'] or '')
    if m['status'].startswith('placeholder') or m['status'].startswith('合规'): return L
    if dc.startswith('1') and m['availability'] == '🟢': return H
    if dc.startswith('4'): return L
    return M
def phi_rule(m): # 频率适配：日 / 周 = H；月 / 季 = M；事件 / 年 = L
    f = (m['frequency'] or '')
    if any(k in f for k in ('日', '周')): return H
    if any(k in f for k in ('月', '季', '半年')): return M
    return L
OVERRIDE = {   # metric_id: (r, e, l, s, phi, rationale)
    'm_hyperscaler_capex': (H, L, M, H, M, '合计为计算值 P5，但分项四行均 P1 → r 继承分项；口径混合见 C11'),
    'm_reconcile_nbis': (M, H, M, M, L, '对账节点：独家交叉判断 e=H；规则人定 s=M；P5 r=M'),
    'm_cn_optics_customs': (L, H, M, L, M, '海关反推：中国侧独家 e=H，但系数未标定 s=L、r=L'),
    'm_talent_flow': (L, H, H, L, L, '人才流向：最领先 l=H、独家 e=H，但合规受限 s=L r=L'),
    'm_lab_contract_reflection_nbis': (H, M, M, M, L, '合同事实 P1；已确认客户，半独家'),
}
def assign(m, best_prov):
    if m['metric_id'] in OVERRIDE:
        r, e, l, s, phi, why = OVERRIDE[m['metric_id']]; return r, e, l, s, phi, why
    return r_from_prov(best_prov), e_rule(m), l_rule(m), s_rule(m), phi_rule(m), f'规则默认：r←{best_prov or "—"}；e/l/s/φ 按 doc21 §6.1 锚点由可得性 / 维度 / 数据类 / 频率推'
