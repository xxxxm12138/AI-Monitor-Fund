# -*- coding: utf-8 -*-
"""0004 · 指引记录的 period 只写目标期间，版本靠 knowledge_time 区分 · owner B · 2026-09-20
0003 把「Q1 版指引」写进了 period 文本，导致同一目标期间的新旧指引无法按期间分组；改回目标期间，版本信息移到 note。
配合 views.sql v_metric_guidance 改为「每个目标期间只取最新一版」。"""
OWNER = 'B'
def up(m):
    for rid, per, tbl in (('r225', 'Q2 FY27', 'fct_quant'), ('r226', 'FY27', 'fct_quant'), ('r227', 'FY27 末', 'fct_quant'), ('r228', 'FY27', 'fct_quant')):
        old = m.con.execute('SELECT period, note FROM fct_quant WHERE record_id=?', [rid]).fetchone()
        m.set('stg_observation', rid, 'period', per, basis='period = 目标期间；版本由 knowledge_time 区分')
        m.set('fct_quant', rid, 'period', per, basis='同上')
        m.set('fct_quant', rid, 'note', f'Q1 版指引（2026-06-04）；{old[1]}', basis='版本信息移到 note')
