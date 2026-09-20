# -*- coding: utf-8 -*-
"""四算子传播引擎(v2):结构取 graph_data(doc25 链),权重/方向/tier 运行时从库读。
输入一个 AI 发展事件 → REPRESENT(入口) → PROPOSE(可能空间) → PREDICT(方向/确定性) → SELECT(排序→ticker)。
用法:
  python3 propagate.py --list                # 列出可挂载入口(维 / 机制 / 源指标)
  python3 propagate.py --dim D1              # 一个 D1 新事件
  python3 propagate.py --at k_d1_subnode     # 从某机制进入
  python3 propagate.py --at m_gpu_ship       # 从某源指标进入
  python3 propagate.py --dim D5 --new "某前沿模型训练算力再翻倍"
  python3 propagate.py                        # 跑示例"""
import os, sys, argparse, collections, duckdb
from graph_data import MECH, CHAINS, TICKERS, DIMS

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anatole_ai_monitor.duckdb')
con = duckdb.connect(DB, read_only=True)
# 运行时权重:按 edge_id 从库读(v_edge_calc)+ 方向(v_signal_latest)+ 名称/领先因子
W = {r[0]: {'trad': r[1], 'warn': r[2], 'tier': r[3], 'dominant': r[4]}
     for r in con.execute("SELECT edge_id, round(tradable_calc,3), round(warning_calc,3), tier, dominant FROM v_edge_calc").fetchall()}
NAME = dict(con.execute("SELECT metric_id, name FROM metric_registry").fetchall())
DIRN = dict(con.execute("SELECT metric_id, direction FROM v_signal_latest").fetchall())
LEADF = dict(con.execute("SELECT metric_id, l FROM metric_factor").fetchall())

def mlabel(n):
    if n in MECH: return MECH[n][0]
    if n in DIMS: return f'{n} 维'
    if n in NAME: return NAME[n]
    return n

# 一条链的节点序列(源 → 机制… → ticker)+ 运行时权重
def chain_info(ch):
    eid, tk, fm, dim, mechs, hops, etype = ch
    w = W.get(eid, {})
    trad, warn = w.get('trad'), w.get('warn')
    score = max(trad or 0, warn or 0)
    return {'eid': eid, 'ticker': tk, 'from': fm, 'from_name': NAME.get(fm, fm), 'dim': dim,
            'mechs': mechs, 'hops': hops, 'etype': etype, 'trad': trad, 'warn': warn,
            'tier': w.get('tier'), 'dominant': w.get('dominant'), 'dir': DIRN.get(fm, '—'),
            'leadf': LEADF.get(fm), 'score': score,
            'nodes': [fm] + mechs + [tk]}

CI = [chain_info(c) for c in CHAINS]

# ---- REPRESENT ----
def represent(entry):
    if entry not in DIMS and entry not in MECH and entry not in NAME and entry not in TICKERS:
        raise SystemExit(f'入口 {entry} 未知;--list 看可挂载入口')
    kind = 'dim' if entry in DIMS else 'mech' if entry in MECH else 'metric'
    return {'entry': entry, 'kind': kind, 'label': mlabel(entry)}

# ---- PROPOSE:从入口可达哪些链(= 可能空间)----
def reachable(entry):
    hit = []
    for ci in CI:
        if entry == ci['dim'] or entry in ci['mechs'] or entry == ci['from']:
            # 入口在链上的位置 → 传播路径 = 从入口到 ticker 的后缀
            seq = ci['nodes']
            idx = 0
            if entry in seq: idx = seq.index(entry)
            elif entry == ci['dim']: idx = 0        # 维入口 = 从源头进
            hit.append({**ci, 'suffix': seq[idx:]})
    return hit

# ---- PREDICT + SELECT ----
def quad(ci):
    hard = ci['tier'] in ('T1', 'T2')
    longlead = (ci['leadf'] or 0) >= 0.6
    return 'act' if hard and longlead else 'watch' if longlead else 'priced' if hard else 'ignore'
QT = {'act': '现在动·早且可信', 'watch': '观察名单·早但待证', 'priced': '大概率已priced', 'ignore': '忽略'}

def run(entry, text=None):
    rep = represent(entry)
    hits = reachable(entry)
    reach = sorted({h['ticker'] for h in hits})
    print('=' * 74)
    print(f'输入事件:{text or "(未描述)"}')
    print(f'① REPRESENT  入口 = {entry}「{rep["label"]}」({rep["kind"]})')
    print(f'② PROPOSE    可能空间 = {len(hits)} 条路径,可达 {len(reach)} 个 ticker:{reach}')
    hits.sort(key=lambda h: -h['score'])
    print(f'③ PREDICT + ④ SELECT  (权重取库 v_edge_calc,非手填):')
    for h in hits[:8]:
        chain = ' → '.join(mlabel(n) for n in h['suffix'])
        print(f"   [{h['score']:.3f}] {h['dir']} {h['tier'] or '—':2} {h['etype']:13} [{QT[quad(h)]}]  {chain}")
    if len(hits) > 8: print(f'   …其余 {len(hits)-8} 条略')
    agg = collections.defaultdict(lambda: {'best': 0, 'n': 0, 'dir': set(), 'dom': set()})
    for h in hits:
        a = agg[h['ticker']]; a['best'] = max(a['best'], h['score']); a['n'] += 1
        a['dir'].add(h['dir']); a['dom'].add(h['dominant'] or '待定')
    print(f'\n  → 导向哪个 ticker(按最强路径分):')
    for tk, a in sorted(agg.items(), key=lambda x: -x[1]['best']):
        print(f"     {tk:5} 最强 {a['best']:.3f} · {a['n']} 路径 · 方向 {'/'.join(sorted(a['dir']))} · {'/'.join(sorted(a['dom']))}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true'); ap.add_argument('--dim'); ap.add_argument('--at'); ap.add_argument('--new')
    a = ap.parse_args()
    if a.list:
        print('维入口:', sorted(DIMS))
        print('机制入口:'); [print(f'  {k:24} {v[0]}  [{v[1]}]') for k, v in MECH.items()]
        print('源指标入口(部分):'); [print(f'  {m:28} {NAME.get(m, "")}') for m in sorted({c[2] for c in CHAINS})]
        return
    if a.dim or a.at: run(a.at or a.dim, text=a.new); return
    for e, t in [('D1', '示例:某季 hyperscaler capex 大超预期'), ('k_d1_subnode', '示例:HBM 供给紧张'),
                 ('D7', '示例:BIS 收紧对华算力出口'), ('D5', '示例:开源模型把推理成本砍半')]:
        run(e, text=t); print()

if __name__ == '__main__': main()
