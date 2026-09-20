# -*- coding: utf-8 -*-
"""③ 面板:AI 事件传播图 + 三卡 + KPI-sink 两类呈现(量级 nowcast / 方向 regime)。
结构取 graph_data(doc25 链),权重/方向/tier/闸门 运行时从库读。单文件 Cytoscape,输出 graph_panel.html。
用法:python3 build_panel.py"""
import duckdb, os, json, re
from graph_data import MECH, CHAINS, TICKERS
HERE = os.path.dirname(os.path.abspath(__file__)); con = duckdb.connect(os.path.join(HERE, 'anatole_ai_monitor.duckdb'), read_only=True)

W = {r[0]: dict(trad=r[1], warn=r[2], tier=r[3], dom=r[4]) for r in con.execute("SELECT edge_id,round(tradable_calc,3),round(warning_calc,3),tier,dominant FROM v_edge_calc").fetchall()}
NAME = dict(con.execute("SELECT metric_id,name FROM metric_registry").fetchall())
DIRN = dict(con.execute("SELECT metric_id,direction FROM v_signal_latest").fetchall())
# 前沿信号的闸门结果(源记录级)
GATE = {}
for r in con.execute("SELECT metric_id, industry_impact, verifiability, impact_rationale FROM fct_frontier WHERE impact_rationale LIKE '[L:%'").fetchall():
    GATE.setdefault(r[0], []).append(dict(impact=r[1], verif=r[2], why=r[3]))
KF = dict(con.execute("SELECT target, status_line FROM key_fact WHERE target_type='ticker' AND status_line IS NOT NULL").fetchall())
INBOOK = {r[0] for r in con.execute("SELECT ticker FROM entity_master WHERE in_book AND ticker IS NOT NULL").fetchall()}
# 票的量级 nowcast KPI(KPI-NOWCAST-TIERS 摘要:票→[(KPI,档,前置读数)])
TICKER_KPI = {
 'NBIS': [('云收入/ARR', 'T1', '上电容量×单价 + capex + CRWV 同业(可回归)'), ('上电/合同电力', 'T1', 'PPA/机组/站点合同(lead 90d)'), ('backlog/预付', 'T2', '合同公告拼'), ('cost/token(行业)', 'T2', '定价页 P1')],
 'RBRK': [('Sub-ARR/NRR', 'T2', '仅结构对账(无另类地面数据·缺口①)')],
 'FCEL': [('季度收入', 'T2', 'backlog 转化 + Fit 里程碑'), ('committed backlog', 'T2', '8-K 合同公告拼')],
 'CIEN': [('数据中心收入', 'T2', '光模块海关+拼(系数未校准)')], 'POET': [('数据中心收入', 'T2', '光模块海关+拼(系数未校准)')],
 'MU': [('DC 收入', 'T3', 'HBM/CoWoS 付费定性 P3·缺口②')], 'SNDK': [('DC 收入', 'T3', 'HBM 付费定性 P3')],
 'AMD': [('DC 收入', 'T2', 'NVDA 出货代理+capex')], 'MRVL': [('DC 收入', 'T2', '同')], 'INTC': [('DC 收入', 'T2', '同')], 'SUPX': [('DC 收入', 'T2', '同')],
}
def norm(s): return re.sub(r'\s+', ' ', (s or '').strip())
def short(s, n=15): s = norm(s); return s if len(s) <= n else s[:n] + '…'
def dim1(d): return (d or '').split('/')[0].strip()[:2]

nodes, edges = {}, []
def add(nid, label, kind, meta):
    if nid not in nodes: nodes[nid] = {'data': {'id': nid, 'label': label, 'kind': kind, **meta}}
    return nid
for tk in TICKERS:
    kpis = TICKER_KPI.get(tk, [])
    add(tk, tk, 'ticker', {'full': tk, 'inbook': tk in INBOOK, 'status': norm(KF.get(tk, '')), 'kpis': kpis, 'dim': ''})
for ch in CHAINS:
    eid, tk, fm, dim, mechs, hops, etype = ch
    w = W.get(eid, {}); sc = max(w.get('trad') or 0, w.get('warn') or 0)
    g = (GATE.get(fm) or [{}])[0]
    src = 'm:' + fm
    add(src, short(NAME.get(fm, fm)), 'source', {'full': NAME.get(fm, fm), 'dim': dim1(dim), 'dir': DIRN.get(fm, '—'),
        'impact': g.get('impact', ''), 'verif': g.get('verif', ''), 'why': g.get('why', ''), 'is_frontier': fm in GATE})
    prev = src
    for i, seg in enumerate(mechs):
        mid = 'k:' + seg
        add(mid, short(MECH.get(seg, (seg,))[0], 14), 'mech', {'full': MECH.get(seg, (seg,))[0], 'dim': ''})
        edges.append({'data': {'id': f'{eid}_{i}', 'source': prev, 'target': mid, 'eid': eid, 'w': sc, 'dir': DIRN.get(fm, '—'), 'tier': w.get('tier', 'T3')}})
        prev = mid
    edges.append({'data': {'id': f'{eid}_z', 'source': prev, 'target': tk, 'eid': eid, 'w': sc, 'dir': DIRN.get(fm, '—'), 'tier': w.get('tier', 'T3'),
        'etype': etype, 'hops': hops, 'trad': w.get('trad'), 'warn': w.get('warn'), 'dom': w.get('dom'), 'from': NAME.get(fm, fm)}})

# 坐标:x 按到 ticker 的跳数(ticker 最右),y 同列按 salience 排
import collections
dist = {t: 0 for t in TICKERS}
for _ in range(20):
    ch2 = False
    for e in edges:
        s, t = e['data']['source'], e['data']['target']
        if t in dist and dist.get(s, -1) < dist[t] + 1: dist[s] = dist[t] + 1; ch2 = True
    if not ch2: break
maxd = max(dist.values()) if dist else 0
for e in edges:
    for p in (e['data']['source'], e['data']['target']): nodes[p]['data'].setdefault('sal', 0); nodes[p]['data']['sal'] += e['data']['w']
col = collections.defaultdict(list)
for nid in nodes: col[maxd - dist.get(nid, 0)].append(nid)
for c, ids in col.items():
    ids.sort(key=lambda i: -nodes[i]['data'].get('sal', 0)); y0 = -(len(ids) - 1) * 64 / 2
    for j, i in enumerate(ids): nodes[i]['pos'] = {'x': c * 260, 'y': y0 + j * 64}
node_elems = [{'data': n['data'], **({'position': n['pos']} if 'pos' in n else {})} for n in nodes.values()]

# 闸门统计
outflow = sum(1 for g in [v[0] for v in GATE.values()] if g.get('impact') == '高' and g.get('verif') in ('third_party_verified', 'reproducible'))
watch = sum(1 for g in [v[0] for v in GATE.values()] if g.get('impact') == '高' and g.get('verif') not in ('third_party_verified', 'reproducible'))
radar = sum(1 for v in GATE.values() for g in [v[0]] if g.get('impact') in ('中', '低'))
DATA = {'nodes': node_elems, 'edges': edges, 'gate': {'外溢': outflow, 'watchlist': watch, '雷达': radar}}

HTML = r"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 事件传播面板</title><script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.2/cytoscape.min.js"></script>
<style>
:root{--bg:#fbfbfd;--panel:#fff;--fg:#1a1d24;--mut:#7a828f;--line:#e8eaee;--card:#f6f7f9;--accent:#2563eb;--nbis:#f59e0b;
 --d1:#2563eb;--d2:#0891b2;--d3:#7c3aed;--d5:#0d9488;--d6:#059669;--d7:#e11d48}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0e1014;--panel:#14171d;--fg:#e6e8ec;--mut:#8b93a1;--line:#242832;--card:#181c23}}
:root[data-theme=dark]{--bg:#0e1014;--panel:#14171d;--fg:#e6e8ec;--mut:#8b93a1;--line:#242832;--card:#181c23}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
header{padding:12px 18px;display:flex;align-items:baseline;gap:12px;border-bottom:1px solid var(--line);background:var(--panel)}
h1{font-size:15px;font-weight:650;margin:0}.sub{color:var(--mut);font-size:12px}.theme{margin-left:auto;background:var(--card);border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:5px 10px;cursor:pointer}
.gatebar{display:flex;gap:10px;padding:10px 18px;background:var(--panel);border-bottom:1px solid var(--line);flex-wrap:wrap;font-size:12px}
.gb{border:1px solid var(--line);border-radius:8px;padding:6px 12px}.gb b{font-size:17px;margin-right:6px}
.gb.out b{color:#059669}.gb.watch b{color:#d97706}.gb.radar b{color:#6b7280}
.grid{display:grid;grid-template-columns:1fr 370px;height:calc(100% - 150px)}@media(max-width:760px){.grid{grid-template-columns:1fr;height:auto}#cy{height:56vh}}
#cy{background:radial-gradient(circle at 25% 15%,rgba(37,99,235,.04),transparent 60%),var(--bg)}
#side{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:16px}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:11px;color:var(--mut);padding:8px 18px;border-top:1px solid var(--line);background:var(--panel)}
.sw{display:inline-block;width:20px;border-top-width:3px;border-top-style:solid;vertical-align:middle;margin-right:3px}
.card h2{font-size:14px;margin:0 0 3px}.tag{font-size:11px;color:var(--mut);margin-bottom:10px}
.k{color:var(--mut);font-size:11px;margin-top:12px;font-weight:600}.v{font-size:13px;margin-top:2px}
.pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;border:1px solid var(--line);margin:2px 4px 2px 0;background:var(--card)}
.pill.up{color:#059669}.pill.dn{color:#dc2626}.pill.shock{color:#d97706}
.pill.out{background:rgba(5,150,105,.15);color:#059669;font-weight:600}.pill.watch{background:rgba(217,119,6,.15);color:#b45309;font-weight:600}.pill.radar{background:var(--card);color:#6b7280}
.kpi{border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin-top:6px;background:var(--card)}
.kpi .t1{border-left:3px solid #059669}.kpi .h{font-weight:600;font-size:12.5px}.kpi .m{color:var(--mut);font-size:11.5px;margin-top:2px}
.tierbadge{font-size:10px;padding:1px 6px;border-radius:4px;border:1px solid var(--line);margin-left:6px}
.chain{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin-top:4px}.chain .n{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:3px 7px;font-size:12px}.chain .ar{color:var(--mut);font-size:11px}
.hint{color:var(--mut);font-size:12.5px}.fold{margin-top:14px;font-size:11px;color:var(--mut);border-top:1px dashed var(--line);padding-top:8px}
</style></head><body>
<header><h1>AI 事件传播面板</h1><span class="sub">事件 → 传播路径 → 影响(票 / KPI)· 前沿信号过两闸才外溢</span>
<button class="theme" onclick="var r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'light':'dark'">◐</button></header>
<div class="gatebar" id="gatebar"></div>
<div class="grid"><div id="cy"></div><div id="side"><div class="card"><h2>点节点或边</h2><div class="hint">点 <b>源</b>(左)看信号卡+闸门 · 点 <b>边</b> 看路径卡 · 点 <b>票</b>(右)看节点档案+量级 nowcast KPI。</div></div></div></div>
<div class="legend"><span><b>源</b>=AI 事件(按维色)</span><span><b>○</b>=传导机制</span><span><b>◆</b>=票</span><span>边宽=权重</span>
<span><span class="sw" style="border-top-color:#059669"></span>↑ <span class="sw" style="border-top-color:#dc2626"></span>↓ <span class="sw" style="border-top-color:#d97706"></span>!</span>
<span>线型 <span class="sw" style="border-top-style:solid"></span>T1 <span class="sw" style="border-top-style:dashed"></span>T2 <span class="sw" style="border-top-style:dotted"></span>T3</span></div>
<script>
const DATA=__DATA__;const g=DATA.gate;
document.getElementById('gatebar').innerHTML=
 '<div class="gb out"><b>'+g['外溢']+'</b>外溢到票/KPI(高·证伪过)</div>'+
 '<div class="gb watch"><b>'+g['watchlist']+'</b>watchlist(高·证伪未过)</div>'+
 '<div class="gb radar"><b>'+g['雷达']+'</b>雷达(中/低,不外溢)</div>';
const DIM={D1:'#2563eb',D2:'#0891b2',D3:'#7c3aed',D5:'#0d9488',D6:'#059669',D7:'#e11d48'};
const DIR={'↑':'#059669','↓':'#dc2626','→':'#94a3b8','!':'#d97706','—':'#cbd5e1'};const TIER={T1:'solid',T2:'dashed',T3:'dotted'};
const cy=cytoscape({container:document.getElementById('cy'),elements:{nodes:DATA.nodes,edges:DATA.edges},minZoom:.25,maxZoom:2.5,wheelSensitivity:.25,
 layout:{name:'preset',fit:true,padding:30},
 style:[
  {selector:'node',style:{'label':'data(label)','font-size':'10px','color':'var(--fg)','text-wrap':'wrap','text-max-width':'96px','text-valign':'center','width':'label','height':'label','padding':'7px','shape':'round-rectangle','background-color':'#e5e7eb','border-width':1.5,'border-color':'#cbd5e1','background-opacity':.9}},
  {selector:'node[kind="source"]',style:{'background-color':e=>DIM[e.data('dim')]||'#64748b','background-opacity':.16,'border-color':e=>DIM[e.data('dim')]||'#64748b','border-width':2}},
  {selector:'node[kind="mech"]',style:{'background-color':'#f1f5f9','border-color':'#cbd5e1','border-width':1,'font-size':'9px','color':'var(--mut)'}},
  {selector:'node[kind="ticker"]',style:{'background-color':'#f59e0b','background-opacity':.22,'border-color':'#f59e0b','border-width':3,'shape':'round-rectangle','font-size':'13px','font-weight':700,'padding':'11px'}},
  {selector:'edge',style:{'width':'mapData(w,0,0.4,1.2,7)','line-color':e=>DIR[e.data('dir')]||'#cbd5e1','target-arrow-color':e=>DIR[e.data('dir')]||'#cbd5e1','target-arrow-shape':'triangle','arrow-scale':.8,'curve-style':'bezier','line-style':e=>TIER[e.data('tier')]||'dotted','opacity':.5}},
  {selector:'.dim',style:{'opacity':.1}},{selector:'.hi',style:{'opacity':1}},{selector:'node.hi',style:{'border-width':3}},
  {selector:':selected',style:{'border-width':3,'border-color':'#2563eb','line-color':'#2563eb','target-arrow-color':'#2563eb','opacity':1}}
 ]});cy.ready(()=>cy.fit(undefined,30));
const side=document.getElementById('side');const esc=s=>(s==null?'':(''+s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const dc=d=>d==='↑'?'up':d==='↓'?'dn':d==='!'?'shock':'';
function foc(ele){cy.elements().addClass('dim').removeClass('hi');const n=ele.isNode?ele.closedNeighborhood():ele.connectedNodes().add(ele);n.removeClass('dim').addClass('hi');}
function srcCard(d){
 let gate='';
 if(d.is_frontier){const out=d.impact==='高'&&['third_party_verified','reproducible'].includes(d.verif)?'<span class="pill out">外溢✓</span>':(d.impact==='高'?'<span class="pill watch">watchlist(证伪未过)</span>':'<span class="pill radar">雷达</span>');
  gate='<div class="k">影响力闸</div><div class="v">'+out+'<span class="pill">影响 '+esc(d.impact||'—')+'</span><span class="pill">证伪 '+esc(d.verif||'—')+'</span></div><div class="v" style="margin-top:6px;font-size:12px;color:var(--mut)">'+esc(d.why||'')+'</div>';}
 return '<div class="card"><h2>'+esc(d.full)+'</h2><div class="tag">信号卡 · AI 事件源</div>'+
  '<div class="k">维 / 方向</div><div class="v"><span class="pill">'+esc(d.dim||'—')+'</span><span class="pill '+dc(d.dir)+'">方向 '+esc(d.dir||'—')+'</span></div>'+gate+'</div>';}
function edgeCard(e){const d=e.data();
 const path=e.connectedNodes();let chain=[];e.cy().elements();
 return '<div class="card"><h2>'+esc(d.from||'')+' → '+esc(d.target)+'</h2><div class="tag">路径卡 · '+esc(d.etype||'')+' · '+(d.hops!=null?d.hops+' 跳':'')+'</div>'+
  '<div class="k">方向 × 权重(库算)</div><div class="v"><span class="pill '+dc(d.dir)+'">'+esc(d.dir)+'</span><span class="pill">tier '+esc(d.tier||'')+'</span><span class="pill">可交易 '+(d.trad??'—')+'</span><span class="pill">预警 '+(d.warn??'—')+'</span><span class="pill">'+esc(d.dom||'')+'</span></div>'+
  '<div class="fold">量级由供给侧 T1/T2 承担;前沿 T3 边只给方向(见 KPI-NOWCAST-TIERS)</div></div>';}
function tickerCard(d){
 let kpi='';(d.kpis||[]).forEach(k=>{const t1=k[1]==='T1';kpi+='<div class="kpi'+(t1?' t1':'')+'"><div class="h">'+esc(k[0])+'<span class="tierbadge">可nowcast '+esc(k[1])+'</span></div><div class="m">前置读数:'+esc(k[2])+'</div></div>';});
 return '<div class="card"><h2>◆ '+esc(d.full)+'</h2><div class="tag">节点档案 · 影响落点'+(d.inbook?' · 持仓':'')+'</div>'+
  '<div class="k">当前 regime / 现状</div><div class="v">'+esc(d.status||'—')+'</div>'+
  '<div class="k">量级 nowcast KPI(T1 可回测 / T2 可对账)</div>'+(kpi||'<div class="hint">(未列)</div>')+
  '<div class="fold">量级 nowcast 卡 = 三值(Actual/Forecast/Prior)+Δ+MOE/Confidence,需接共识/回测数据;此处先列 KPI 与可 nowcast 档。方向信号见连入的前沿边。</div></div>';}
cy.on('tap','node',e=>{foc(e.target);const d=e.target.data();side.innerHTML=d.kind==='ticker'?tickerCard(d):d.kind==='source'?srcCard(d):'<div class="card"><h2>○ '+esc(d.full)+'</h2><div class="tag">传导机制</div><div class="hint">多条路径共用</div></div>';});
cy.on('tap','edge',e=>{cy.elements().addClass('dim').removeClass('hi');e.target.removeClass('dim').addClass('hi');e.target.connectedNodes().removeClass('dim').addClass('hi');side.innerHTML=edgeCard(e.target);});
cy.on('tap',e=>{if(e.target===cy){cy.elements().removeClass('dim hi');side.innerHTML='<div class="card"><h2>点节点或边</h2><div class="hint">源=信号卡+闸门 · 边=路径卡 · 票=档案+KPI</div></div>';}});
</script></body></html>"""
open(os.path.join(HERE, 'graph_panel.html'), 'w', encoding='utf-8').write(HTML.replace('__DATA__', json.dumps(DATA, ensure_ascii=False)))
print('nodes', len(node_elems), 'edges', len(edges), 'gate', DATA['gate'])
