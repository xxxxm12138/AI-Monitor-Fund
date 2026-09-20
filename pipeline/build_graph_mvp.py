# -*- coding: utf-8 -*-
"""MVP: 库 → 事件传播图（Cytoscape + dagre 左→右流向图，单文件 HTML）。只做 NBIS 主链。
map_path 文本在此临时拆并【合并同名】中间节点（不动库）；正式版走 PLAN-graph-refactor.md Phase 1 升一等节点。
用法: python3 build_graph_mvp.py → graph_mvp.html"""
import duckdb, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
con = duckdb.connect(os.path.join(HERE, 'anatole_ai_monitor.duckdb'), read_only=True)

Q = """
SELECT e.edge_id, e.from_metric, m.name AS from_name, m.dim, e.map_path, e.hops, e.edge_type, e.side,
       c.tier, round(c.tradable_calc,3) AS tradable, round(c.warning_calc,3) AS warning, c.dominant,
       m.lead_time_est, s.direction, l.provenance, l.headline_value, l.headline_unit, l.knowledge_date,
       e.mechanism, e.cert_method, mf.l AS lead_factor
FROM edge_registry e
JOIN metric_registry m ON m.metric_id = e.from_metric
LEFT JOIN v_edge_calc c ON c.edge_id = e.edge_id
LEFT JOIN v_signal_latest s ON s.metric_id = e.from_metric
LEFT JOIN v_metric_latest l ON l.metric_id = e.from_metric
LEFT JOIN metric_factor mf ON mf.metric_id = e.from_metric
WHERE e.to_ticker = 'NBIS'
ORDER BY greatest(coalesce(c.tradable_calc,0), coalesce(c.warning_calc,0)) DESC
"""
E = [dict(zip([d[0] for d in con.description], r)) for r in con.execute(Q).fetchall()]
nbis = con.execute("SELECT name, layer, maturity FROM entity_master WHERE ticker='NBIS' LIMIT 1").fetchone()
nbis_kf = con.execute("SELECT status_line, falsifier FROM key_fact WHERE target='NBIS' AND status_line IS NOT NULL LIMIT 1").fetchone()

def norm(s): return re.sub(r'\s+', ' ', (s or '').strip())
def short(s, n=15):
    s = norm(s); return s if len(s) <= n else s[:n] + '…'
def dim1(d): return (d or '').split('/')[0].strip()[:2]   # 主维 D1..D7

nodes, cy_edges, EDGE_META = {}, [], {}
def add(nid, label, kind, meta):
    if nid not in nodes: nodes[nid] = {'data': {'id': nid, 'label': label, 'kind': kind, **meta}}
    return nid

add('NBIS', 'NBIS', 'sink', {'full': f'NBIS · {norm(nbis[0]) if nbis else ""}', 'dim': '',
    'status_line': norm(nbis_kf[0]) if nbis_kf else '', 'falsifier': norm(nbis_kf[1]) if nbis_kf else '',
    'sink_type': '持仓 51.22%', 'sal': 0})

for e in E:
    w = max(e['tradable'] or 0, e['warning'] or 0)
    src = 'm:' + e['from_metric']
    hv = f"{e['headline_value']} {e['headline_unit'] or ''}".strip() if e['headline_value'] is not None else ''
    add(src, short(e['from_name']), 'source', {'full': norm(e['from_name']), 'dim': dim1(e['dim']),
        'direction': e['direction'] or '—', 'provenance': e['provenance'] or '', 'headline': hv,
        'lead': norm(e['lead_time_est']), 'sal': 0})
    chain = [c for c in re.split(r'\s*→\s*', e['map_path'] or '') if c.strip()]
    prev = src
    for i, seg in enumerate(chain):
        mid = 'mid:' + re.sub(r'\W+', '', norm(seg))[:24]        # 同名机制合并
        add(mid, short(seg, 14), 'transit', {'full': norm(seg), 'dim': '', 'sal': 0})
        cy_edges.append({'data': {'id': f'{e["edge_id"]}_{i}', 'source': prev, 'target': mid,
            'edge_id': e['edge_id'], 'w': w, 'dir': e['direction'] or '—', 'tier': e['tier'] or 'T3'}})
        prev = mid
    cy_edges.append({'data': {'id': f'{e["edge_id"]}_z', 'source': prev, 'target': 'NBIS',
        'edge_id': e['edge_id'], 'w': w, 'dir': e['direction'] or '—', 'tier': e['tier'] or 'T3'}})
    hard = e['tier'] in ('T1', 'T2'); longlead = (e['lead_factor'] or 0) >= 0.6
    quad = 'act' if hard and longlead else 'watch' if longlead else 'priced' if hard else 'ignore'
    EDGE_META[e['edge_id']] = {'from_name': norm(e['from_name']), 'dim': e['dim'] or '',
        'chain': [norm(x) for x in ([e['from_name']] + chain + ['NBIS'])], 'hops': e['hops'],
        'edge_type': e['edge_type'], 'tier': e['tier'], 'cert_method': norm(e['cert_method']),
        'tradable': e['tradable'], 'warning': e['warning'], 'dominant': e['dominant'],
        'direction': e['direction'] or '—', 'lead': norm(e['lead_time_est']), 'mechanism': norm(e['mechanism']),
        'provenance': e['provenance'] or '', 'headline': f"{e['headline_value']} {e['headline_unit'] or ''}".strip() if e['headline_value'] is not None else '',
        'kdate': str(e['knowledge_date']) if e['knowledge_date'] else '', 'quad': quad, 'w': w}

for ce in cy_edges:
    for p in (ce['data']['source'], ce['data']['target']):
        nodes[p]['data']['sal'] = round(nodes[p]['data'].get('sal', 0) + ce['data']['w'], 3)

# ---- 自算坐标：x 按「到 NBIS 的跳数距离」(NBIS 最右)，y 按同列 salience 排布 ----
import collections
dist = {'NBIS': 0}
for _ in range(20):
    changed = False
    for ce in cy_edges:
        s, t = ce['data']['source'], ce['data']['target']
        d = dist.get(t, 0) + 1
        if d > dist.get(s, 0): dist[s] = d; changed = True
    if not changed: break
maxd = max(dist.values()) if dist else 0
bycol = collections.defaultdict(list)
for nid in nodes: bycol[maxd - dist.get(nid, 0)].append(nid)   # col0 最左…maxd 最右(NBIS)
COLW, ROWH = 250, 70
for col, ids in bycol.items():
    ids.sort(key=lambda i: -nodes[i]['data'].get('sal', 0))
    y0 = -(len(ids) - 1) * ROWH / 2
    for j, i in enumerate(ids):
        nodes[i]['pos'] = {'x': col * COLW, 'y': y0 + j * ROWH}

node_elems = [{'data': nd['data'], **({'position': nd['pos']} if 'pos' in nd else {})} for nd in nodes.values()]
qc = {'act': 0, 'watch': 0, 'priced': 0, 'ignore': 0}
for m in EDGE_META.values(): qc[m['quad']] += 1
DATA = {'nodes': node_elems, 'edges': cy_edges, 'edgeMeta': EDGE_META, 'quad': qc}

HTML = r"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 事件传播图 · NBIS</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.2/cytoscape.min.js"></script>
<style>
:root{--bg:#fbfbfd;--panel:#fff;--fg:#1a1d24;--mut:#7a828f;--line:#e8eaee;--card:#f6f7f9;--accent:#2563eb;
 --d1:#2563eb;--d2:#0891b2;--d3:#7c3aed;--d4:#db2777;--d5:#0d9488;--d6:#059669;--d7:#e11d48;--nbis:#f59e0b}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0e1014;--panel:#14171d;--fg:#e6e8ec;--mut:#8b93a1;--line:#242832;--card:#181c23;--accent:#60a5fa}}
:root[data-theme=dark]{--bg:#0e1014;--panel:#14171d;--fg:#e6e8ec;--mut:#8b93a1;--line:#242832;--card:#181c23;--accent:#60a5fa}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:var(--bg);color:var(--fg);
 font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
header{padding:14px 20px;display:flex;align-items:baseline;gap:12px;border-bottom:1px solid var(--line);background:var(--panel)}
h1{font-size:16px;font-weight:650;margin:0}.sub{color:var(--mut);font-size:12.5px}
.theme{margin-left:auto;background:var(--card);border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:5px 10px;cursor:pointer;font-size:13px}
.grid{display:grid;grid-template-columns:1fr 360px;height:calc(100% - 118px)}
@media(max-width:760px){.grid{grid-template-columns:1fr;height:auto}#cy{height:60vh}}
#cy{background:radial-gradient(circle at 30% 20%,rgba(37,99,235,.04),transparent 60%),var(--bg)}
#side{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:18px}
.quadbar{display:flex;gap:10px;padding:12px 20px;background:var(--panel);border-bottom:1px solid var(--line);flex-wrap:wrap}
.qb{flex:1;min-width:150px;border:1px solid var(--line);border-radius:10px;padding:9px 12px;display:flex;align-items:center;gap:10px}
.qb .n{font-size:20px;font-weight:700;line-height:1}.qb .t{font-size:12px;color:var(--mut)}
.qb.act{background:linear-gradient(0deg,rgba(5,150,105,.10),transparent)}.qb.act .n{color:#059669}
.qb.watch{background:linear-gradient(0deg,rgba(217,119,6,.10),transparent)}.qb.watch .n{color:#d97706}
.qb.priced{background:linear-gradient(0deg,rgba(107,114,128,.10),transparent)}.qb.priced .n{color:#6b7280}
.qb.ignore .n{color:#9ca3af}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:11.5px;color:var(--mut);padding:10px 20px;border-top:1px solid var(--line);background:var(--panel)}
.legend b{color:var(--fg);font-weight:600}.sw{display:inline-block;width:22px;height:0;border-top-width:3px;border-top-style:solid;vertical-align:middle;margin-right:4px}
.hint{color:var(--mut);font-size:13px;margin-top:8px}
.card h2{font-size:14px;margin:0 0 4px;color:var(--fg)}.card .tag{font-size:11px;color:var(--mut);margin-bottom:12px}
.k{color:var(--mut);font-size:11px;margin-top:13px;font-weight:600;letter-spacing:.03em}
.v{font-size:13px;margin-top:3px}
.chain{display:flex;flex-wrap:wrap;gap:5px;align-items:center;margin-top:4px}
.chain .n{background:var(--card);border:1px solid var(--line);border-radius:7px;padding:4px 8px;font-size:12px}
.chain .n.src{border-color:var(--accent)}.chain .n.dst{border-color:var(--nbis);font-weight:600}
.chain .ar{color:var(--mut);font-size:11px}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11.5px;border:1px solid var(--line);margin:2px 4px 2px 0;background:var(--card)}
.pill.up{color:#059669;border-color:#05966955}.pill.dn{color:#dc2626;border-color:#dc262655}.pill.shock{color:#d97706;border-color:#d9770655}
.pill.q-act{background:rgba(5,150,105,.14);border-color:#05966955;color:#059669;font-weight:600}
.pill.q-watch{background:rgba(217,119,6,.14);border-color:#d9770655;color:#b45309;font-weight:600}
.pill.q-priced{background:rgba(107,114,128,.14);color:#6b7280;font-weight:600}
.fold{margin-top:16px;font-size:11.5px;color:var(--mut);border-top:1px dashed var(--line);padding-top:10px}
</style></head><body>
<header><h1>AI 事件传播图</h1><span class="sub">NBIS 主链 · 事件 → 传播路径 → 影响</span>
<button class="theme" onclick="var r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'light':'dark'">◐ 主题</button></header>
<div class="quadbar" id="quadbar"></div>
<div class="grid"><div id="cy"></div><div id="side"><div class="card"><h2>点图上的节点或边</h2><div class="hint">点 <b>源</b>(左) 看信号卡 · 点 <b>边</b> 看路径卡 · 点 <b>NBIS</b>(右) 看节点档案。滚轮缩放、拖拽平移。</div></div></div></div>
<div class="legend">
<span><b>源</b> AI 事件(按维着色)</span><span><b>○</b> 传导机制(同名已合并)</span><span><b>◆ NBIS</b> 影响落点</span>
<span>边宽 = 权重</span><span><span class="sw" style="border-top-color:#059669"></span>↑增强 <span class="sw" style="border-top-color:#dc2626"></span>↓削弱 <span class="sw" style="border-top-color:#d97706"></span>!冲击</span>
<span>线型 <span class="sw" style="border-top-style:solid;border-top-color:var(--mut)"></span>T1 <span class="sw" style="border-top-style:dashed;border-top-color:var(--mut)"></span>T2 <span class="sw" style="border-top-style:dotted;border-top-color:var(--mut)"></span>T3</span>
</div>
<script>
const DATA=__DATA__;
const q=DATA.quad;
document.getElementById('quadbar').innerHTML=
 '<div class="qb act"><span class="n">'+q.act+'</span><span class="t">现在动<br>早 + 可信</span></div>'+
 '<div class="qb watch"><span class="n">'+q.watch+'</span><span class="t">观察名单<br>早 + 待证</span></div>'+
 '<div class="qb priced"><span class="n">'+q.priced+'</span><span class="t">大概率已 priced<br>可信 + 同步</span></div>'+
 '<div class="qb ignore"><span class="n">'+q.ignore+'</span><span class="t">忽略<br>待证 + 同步</span></div>';
const DIM={'D1':'#2563eb','D2':'#0891b2','D3':'#7c3aed','D4':'#db2777','D5':'#0d9488','D6':'#059669','D7':'#e11d48'};
const DIR={'↑':'#059669','↓':'#dc2626','→':'#94a3b8','!':'#d97706','—':'#cbd5e1'};
const TIER={'T1':'solid','T2':'dashed','T3':'dotted'};
const cy=cytoscape({container:document.getElementById('cy'),elements:{nodes:DATA.nodes,edges:DATA.edges},
 minZoom:.3,maxZoom:2.5,wheelSensitivity:.25,
 layout:{name:'preset',fit:true,padding:36},
 style:[
  {selector:'node',style:{'label':'data(label)','font-size':'10.5px','font-weight':500,'color':'var(--fg)',
    'text-wrap':'wrap','text-max-width':'100px','text-valign':'center','text-halign':'center',
    'background-color':'#e5e7eb','border-width':1.5,'border-color':'#cbd5e1','width':'label','height':'label',
    'padding':'8px','shape':'round-rectangle','background-opacity':.9}},
  {selector:'node[kind="source"]',style:{'background-color':ele=>DIM[ele.data('dim')]||'#64748b','background-opacity':.16,
    'border-color':ele=>DIM[ele.data('dim')]||'#64748b','border-width':2,'color':'var(--fg)'}},
  {selector:'node[kind="transit"]',style:{'background-color':'#f1f5f9','border-color':'#cbd5e1','border-width':1,
    'font-size':'9.5px','color':'var(--mut)','shape':'round-rectangle'}},
  {selector:'node[kind="sink"]',style:{'background-color':'#f59e0b','background-opacity':.22,'border-color':'#f59e0b',
    'border-width':3,'shape':'round-rectangle','font-size':'15px','font-weight':700,'padding':'14px','color':'var(--fg)'}},
  {selector:'edge',style:{'width':'mapData(w,0,0.4,1.2,7)','line-color':ele=>DIR[ele.data('dir')]||'#cbd5e1',
    'target-arrow-color':ele=>DIR[ele.data('dir')]||'#cbd5e1','target-arrow-shape':'triangle','arrow-scale':.8,
    'curve-style':'bezier','line-style':ele=>TIER[ele.data('tier')]||'dotted','opacity':.55}},
  {selector:'.dim',style:{'opacity':.12}},
  {selector:'.hi',style:{'opacity':1,'width':'mapData(w,0,0.4,2,8)'}},
  {selector:'node.hi',style:{'opacity':1,'border-width':3}},
  {selector:':selected',style:{'border-width':3,'border-color':'#2563eb','line-color':'#2563eb','target-arrow-color':'#2563eb','opacity':1}}
 ]});
cy.ready(()=>cy.fit(undefined,30));
const side=document.getElementById('side');
const esc=s=>(s==null?'':(''+s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const dcls=d=>d==='↑'?'up':d==='↓'?'dn':d==='!'?'shock':'';
function focus(ele){cy.elements().addClass('dim').removeClass('hi');const nb=ele.closedNeighborhood?ele.closedNeighborhood():ele.connectedNodes().add(ele);nb.removeClass('dim').addClass('hi');}
function clearFocus(){cy.elements().removeClass('dim hi');}
function nodeCard(d){
 if(d.kind==='sink')return '<div class="card"><h2>◆ '+esc(d.full)+'</h2><div class="tag">节点档案 · 影响落点</div>'+
   '<div class="k">头</div><div class="v"><span class="pill">'+esc(d.sink_type)+'</span></div>'+
   '<div class="k">入边(什么在推动它)</div><div class="v hint" style="margin-top:4px">点任一条打到它的边 → 路径卡</div>'+
   '<div class="k">当前 regime / 现状</div><div class="v">'+esc(d.status_line||'—')+'</div>'+
   '<div class="k">falsifier(什么推翻)</div><div class="v">'+esc(d.falsifier||'—')+'</div>'+
   '<div class="fold">出信号(自身财报事件)与本体读数(营收/PE)默认折叠——正式版展开;基金已有的不占版面</div></div>';
 if(d.kind==='source')return '<div class="card"><h2>'+esc(d.full)+'</h2><div class="tag">信号卡 · AI 事件源</div>'+
   '<div class="k">维 / 方向</div><div class="v"><span class="pill">'+esc(d.dim||'—')+'</span><span class="pill '+dcls(d.direction)+'">方向 '+esc(d.direction||'—')+'</span></div>'+
   '<div class="k">最新读数</div><div class="v">'+esc(d.headline||'—')+'</div>'+
   '<div class="k">证据级</div><div class="v"><span class="pill">'+esc(d.provenance||'—')+'</span></div>'+
   '<div class="fold">点它连出的边 → 看它点燃的传播路径</div></div>';
 return '<div class="card"><h2>○ '+esc(d.full)+'</h2><div class="tag">传导机制节点</div>'+
   '<div class="hint">多条路径共用此机制。正式版升一等:含义 / 所属维 / 指标 / 来源可点开。</div></div>';
}
function edgeCard(eid){const m=DATA.edgeMeta[eid];if(!m)return;
 const chain=m.chain.map((n,i)=>'<span class="n '+(i===0?'src':i===m.chain.length-1?'dst':'')+'">'+esc(n)+'</span>'+(i<m.chain.length-1?'<span class="ar">→</span>':'')).join('');
 const qt={act:'现在动 · 早且可信',watch:'观察名单 · 早但待证',priced:'大概率已 priced',ignore:'忽略'}[m.quad];
 side.innerHTML='<div class="card"><h2>'+esc(m.from_name)+' → NBIS</h2><div class="tag">路径卡 · '+esc(m.edge_type)+' · '+m.hops+' 跳</div>'+
  '<div class="k">拆解链</div><div class="chain">'+chain+'</div>'+
  '<div class="k">机制</div><div class="v">'+esc(m.mechanism||'—')+'</div>'+
  '<div class="k">领先期(P&amp;L 何时显现)</div><div class="v">'+esc(m.lead||'—')+'</div>'+
  '<div class="k">确定性</div><div class="v"><span class="pill">'+esc(m.tier)+'</span>'+esc(m.cert_method||'')+'</div>'+
  '<div class="k">方向 × 权重(= 因子算出的边宽)</div><div class="v"><span class="pill '+dcls(m.direction)+'">'+esc(m.direction)+'</span><span class="pill">可交易 '+(m.tradable??'—')+'</span><span class="pill">预警 '+(m.warning??'—')+'</span><span class="pill">'+esc(m.dominant||'')+'</span></div>'+
  '<div class="k">可测量检查点 / 最近读数</div><div class="v">'+esc(m.headline||'—')+(m.kdate?' <span class="hint">('+esc(m.kdate)+')</span>':'')+'</div>'+
  '<div class="k">2×2 定位(领先期 × 证据级)</div><div class="v"><span class="pill q-'+m.quad+'">'+esc(qt)+'</span></div></div>';
}
cy.on('tap','node',e=>{focus(e.target);side.innerHTML=nodeCard(e.target.data());});
cy.on('tap','edge',e=>{const ed=e.target;cy.elements().addClass('dim').removeClass('hi');ed.removeClass('dim').addClass('hi');ed.connectedNodes().removeClass('dim').addClass('hi');edgeCard(ed.data('edge_id'));});
cy.on('tap',e=>{if(e.target===cy){clearFocus();side.innerHTML='<div class="card"><h2>点图上的节点或边</h2><div class="hint">点 <b>源</b>(左) 信号卡 · 点 <b>边</b> 路径卡 · 点 <b>NBIS</b>(右) 节点档案。</div></div>';}});
</script></body></html>"""

open(os.path.join(HERE, 'graph_mvp.html'), 'w', encoding='utf-8').write(HTML.replace('__DATA__', json.dumps(DATA, ensure_ascii=False)))
print('nodes', len(DATA['nodes']), '(源', sum(1 for n in DATA['nodes'] if n['data']['kind']=='source'),
      '传导', sum(1 for n in DATA['nodes'] if n['data']['kind']=='transit'), ') edges', len(DATA['edges']), '2x2', qc)
