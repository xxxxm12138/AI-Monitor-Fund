# -*- coding: utf-8 -*-
import json, duckdb
import evidence_structure as E
from graph_data import CHAINS, MECH

con = duckdb.connect(E.DB, read_only=True)
ec = E.load_edge_calc(con)
pos = E.load_positions(con)
est = E.load_ticker_edge_stats(con)
G = E.build_graph(ec)
tickers = sorted({c[1] for c in CHAINS})

# metric label map
mcols = [c[0] for c in con.execute("select column_name from information_schema.columns where table_name='metric_registry'").fetchall()]
namecol = next((c for c in ['label','name','metric_name','short_name','title','short'] if c in mcols), None)
mlab = {}
if namecol:
    for mid, nm in con.execute(f"select metric_id, {namecol} from metric_registry").fetchall():
        mlab[mid] = nm or mid

# key_fact headlines
kf = {}
for r in con.execute("select target, status_line, falsifier, brief, watch from key_fact where target in ('NBIS','RBRK','FCEL')").fetchall():
    t = r[0]
    if t not in kf: kf[t] = dict(status_line=r[1], falsifier=r[2], brief=r[3], watch=r[4])
    else:
        for i,k in enumerate(['status_line','falsifier','brief','watch']):
            if not kf[t].get(k) and r[i+1]: kf[t][k]=r[i+1]

# divergence
div = [dict(subject=r[0].replace('record:',''), type=r[1], metric=r[2], detail=(r[3] or '').strip(), date=str(r[4])) for r in con.execute("select div_key,div_type,subject,detail,knowledge_date from v_divergence").fetchall()]

SIDEFAM = {'supply':'f1','demand':'f2','regime':'f5'}
def perpath(tk):
    rows=[]
    for (eid, t, frm, dim, mechs, hops, etype) in CHAINS:
        if t!=tk: continue
        e=ec.get(eid,{})
        rows.append(dict(edge=eid, src=frm, src_label=mlab.get(frm,frm), dim=dim,
            mechs=[MECH.get(m,(m,))[0] for m in mechs], hops=hops, etype=etype,
            side=e.get('side'), tier=e.get('tier'),
            tradable=round(e.get('tradable') or 0,3), warning=round(e.get('warning') or 0,3),
            dominant=e.get('dominant')))
    return rows

out=dict(positions=pos, tickers={}, book=[], divergence=div, keyfact=kf)
for tk in tickers:
    r=E.per_ticker(G,tk)
    if not r: continue
    sv=E.sizing_verdict(r,pos.get(tk,0),est.get(tk))
    out['tickers'][tk]=dict(
        weight=pos.get(tk,0), raw=r['raw'], independent=r['independent'],
        mincut=sorted(r['mincut']), fam={k:[v[0],sorted(v[1])] for k,v in r['fam'].items()},
        sizing=sv, paths=perpath(tk))
for m,d in E.book_cut(G,pos,tickers).items():
    out['book'].append(dict(node=m, weight=d['weight'], n_tk=d['n_tk'],
        tickers=[[t,round(w,2),b,a] for (t,b,a,w) in d['tickers']], disconnected=d['disconnected']))

p='/Users/adminzt/Desktop/Anatole/pipeline/result_layer_data.json'
json.dump(out, open(p,'w'), ensure_ascii=False, indent=1)
print('wrote',p)
print('metric name col:',namecol,'| keyfact keys:',list(kf.keys()))
print('NBIS:',out['tickers']['NBIS']['raw'],'→',out['tickers']['NBIS']['independent'],'paths',len(out['tickers']['NBIS']['paths']))
print('book top3:',[(b['node'],b['weight'],b['n_tk']) for b in out['book'][:3]])
