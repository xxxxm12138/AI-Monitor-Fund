# -*- coding: utf-8 -*-
"""0029 · 修 decision_registry.freq_est 里硬编码的会漂移计数 · owner D · 2026-09-21
freq_est 本该只描述「判断发生的频率量级」,但 7 行嵌了会过期的实时计数——
d_route「现 231 条」实为 317、d_source_tier「现 123 源」实为 176、d_factor「现 82 节点」实为 84、
d_falsify_gate「现 14 条填 8」实为 fct_frontier 23、d_edge_tier「现 35 条边」实为 36、
d_calendar_scope「现 58 行」、d_divergence_explain「v_divergence 现 3 条」。
硬编码计数长在「自描述、无漂移」的卖点上,尽调一眼看穿。此迁移剥离括号里的实时计数、只留频率描述;
实时吞吐一律看 v_decision_health(视图动态算),不再写死在字段里。"""
OWNER = 'D'

FIX = {
    'd_route':             '每条观测一次',
    'd_source_tier':       '每新源一次',
    'd_falsify_gate':      '每条前沿记录一次',
    'd_factor':            '每节点 5 次(r/e/l/s/φ)',
    'd_edge_tier':         '每边一次 + 复验时重判',
    'd_calendar_scope':    '每排期行一次',
    'd_divergence_explain':'每背离一次',
}

def up(m):
    for did, val in FIX.items():
        m.set('decision_registry', did, 'freq_est', val,
              basis='剥离硬编码实时计数(会漂移);实时吞吐见 v_decision_health')
