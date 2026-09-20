# -*- coding: utf-8 -*-
"""出版版监测面板(feed 主视图 + AI 发展态势带 + 持仓 read-through + 因果映射 tab)。
文案走 PANEL-DESIGN §九 专业术语;输出 Artifact 内容页(无 doctype/head/body 包裹)panel_v2.html。"""
import duckdb, os, json, re
from graph_data import MECH, CHAINS, TICKERS
H = os.path.dirname(os.path.abspath(__file__)); con = duckdb.connect(os.path.join(H, 'anatole_ai_monitor.duckdb'), read_only=True)

# 术语翻译
VERIF = {'third_party_verified': '第三方验证', 'reproducible': '可复现', 'claimed_only': '仅厂商声明', 'vendor_pr': '厂商公告', None: '—', '': '—'}
DIRW = {'↑': '↑ 利多', '↓': '↓ 利空', '→': '→ 中性', '!': '! 冲击', '—': '—'}
DIMNAME = {'D1': 'D1 算力供给', 'D2': 'D2 数据供给', 'D3': 'D3 资本', 'D4': 'D4 人才', 'D5': 'D5 能力前沿', 'D6': 'D6 商用落地', 'D7': 'D7 政策·能源'}
NAME = dict(con.execute("SELECT metric_id,name FROM metric_registry").fetchall())
DIRN = dict(con.execute("SELECT metric_id,direction FROM v_signal_latest").fetchall())
# metric → read-through 标的(从 CHAINS)
RT = {}
for eid, tk, fm, dim, mechs, hops, etype in CHAINS: RT.setdefault(fm, set()).add(tk)

# ---- AI 发展态势记分牌(供给侧驱动,不挂票)----
SCORE = [
 ('D1 算力供给', '训练算力', '+5×/年', '↑', '第三方验证', 'Epoch AI'),
 ('D1 算力供给', 'Hyperscaler Capex', '$165B/季', '↑', '一手财报', '四家合计'),
 ('D1 算力供给', '中国光模块营收', '¥418亿 H1', '↑', '交易所公告', '中际旭创'),
 ('D5 能力前沿', '开源–闭源差距', '8 分 (53/45)', '→', '第三方验证', 'Artificial Analysis'),
 ('D5 能力前沿', '推理成本/任务', '$2.0–7.6', '↓', '第三方验证', 'Artificial Analysis'),
 ('D2 数据供给', '数据供给约束', 'data-bound', '→', '可复现', 'CMU·合成数据 +3.4–5.2×'),
]

# ---- 今日分流 feed:一行一独立信号(旁证不进 feed;同指标多记录用各自标题区分)----
def title_of(fm, name, inst, val):
    if fm == 'm_bench_frontier': return (inst or name)            # SWE-bench Verified / ARC-AGI-3 / LMArena Text
    if fm == 'm_new_paradigm':
        core = val.split('发布', 1)[1] if '发布' in val.split('：')[0] else val   # "Inception 发布 Mercury 2.5…" → 取产品名
        return re.split(r'[：(（]', core)[0].strip()[:22]  # 产品名:Gemini Robotics 2 / Cosmos 3 / Mercury 2.5
    return name
feed = []
for r in con.execute("""SELECT record_id, metric_id, COALESCE(score_text,CAST(score AS TEXT)) v, verifiability, industry_impact, impact_rationale, institution, benchmark
FROM fct_frontier WHERE impact_rationale LIKE '[L:%' ORDER BY CASE industry_impact WHEN '高' THEN 0 ELSE 1 END, record_id""").fetchall():
    rid, fm, v, verif, imp, why, inst, bench = r
    if '旁证' in (why or ''): continue                            # 旁证=同一事实的重复统计,不进 feed(不重复外溢)
    ch = re.search(r'渠道:([^·]+)', why); ch = ch.group(1) if ch else '—'
    passed = verif in ('third_party_verified', 'reproducible')
    grade = '可执行' if (imp == '高' and passed) else ('观察 · 待验证' if imp == '高' else '监测')
    rts = sorted(RT.get(fm, set())) or (['组合级 / 纯 KPI'] if fm in ('m_data_wall', 'm_arxiv_topic_slope') else ['—'])
    subv = str(v)[:56]
    if fm == 'm_bench_frontier' and bench: subv = f'{bench} · {subv}'   # 榜首(全部提交)/Bash Only 区分同源
    feed.append(dict(rid=rid, name=title_of(fm, NAME.get(fm, fm), inst, str(v)), val=subv, verif=VERIF.get(verif, verif), impact=imp,
                     channel=ch.strip(), readthrough='、'.join(rts), grade=grade, why=re.sub(r'^\[[^\]]*\]\s*', '', why), metric=fm))

# ---- 持仓 read-through ----
KF = dict(con.execute("SELECT target, status_line FROM key_fact WHERE target_type='ticker' AND status_line IS NOT NULL").fetchall())
FAL = dict(con.execute("SELECT target, falsifier FROM key_fact WHERE target_type='ticker' AND falsifier IS NOT NULL").fetchall())
HOLD = [
 ('NBIS', 'Nebius · Neocloud 算力租赁', '看多确认', KF.get('NBIS', ''), '3Q26 电力并网与客户预付到账'),
 ('RBRK', 'Rubrik · 数据安全 SaaS', '中性', KF.get('RBRK', ''), 'Sub-ARR 增速 vs FY27 指引;fair use 判决走向'),
 ('FCEL', 'FuelCell · 数据中心供电', '中性', KF.get('FCEL', ''), '10-31 产能达 100MW;75MW 协议对手方披露'),
]

# ---- 因果映射(graph)----
gnodes, gedges = {}, []
W = {r[0]: r[1] for r in con.execute("SELECT edge_id, greatest(coalesce(tradable_calc,0),coalesce(warning_calc,0)) FROM v_edge_calc").fetchall()}
def gn(nid, label, kind, dim=''):
    if nid not in gnodes: gnodes[nid] = {'data': {'id': nid, 'label': label, 'kind': kind, 'dim': dim}}
for tk in TICKERS: gn(tk, tk, 'ticker')
for eid, tk, fm, dim, mechs, hops, etype in CHAINS:
    s = 'm:' + fm; gn(s, (NAME.get(fm, fm))[:14], 'source', dim.split('/')[0][:2]); prev = s
    for seg in mechs:
        mid = 'k:' + seg; gn(mid, MECH.get(seg, (seg,))[0][:12], 'mech'); gedges.append({'data': {'id': eid + seg, 'source': prev, 'target': mid, 'w': round(W.get(eid, 0), 3), 'dir': DIRN.get(fm, '—')}}); prev = mid
    gedges.append({'data': {'id': eid + 'z', 'source': prev, 'target': tk, 'w': round(W.get(eid, 0), 3), 'dir': DIRN.get(fm, '—')}})
import collections
dist = {t: 0 for t in TICKERS}
for _ in range(20):
    c = False
    for e in gedges:
        s, t = e['data']['source'], e['data']['target']
        if t in dist and dist.get(s, -1) < dist[t] + 1: dist[s] = dist[t] + 1; c = True
    if not c: break
maxd = max(dist.values())
col = collections.defaultdict(list)
for n in gnodes: col[maxd - dist.get(n, 0)].append(n)
for cc, ids in col.items():
    y0 = -(len(ids) - 1) * 46 / 2
    for j, i in enumerate(ids): gnodes[i]['pos'] = {'x': cc * 230, 'y': y0 + j * 46}
GRAPH = {'nodes': [{'data': n['data'], **({'position': n['pos']} if 'pos' in n else {})} for n in gnodes.values()], 'edges': gedges}

gate_out = sum(1 for f in feed if f['grade'] == '可执行'); gate_watch = sum(1 for f in feed if '观察' in f['grade']); gate_mon = sum(1 for f in feed if f['grade'] == '监测')
DATA = {'score': SCORE, 'feed': feed, 'hold': HOLD, 'fal': FAL, 'graph': GRAPH, 'gate': dict(o=gate_out, w=gate_watch, m=gate_mon), 'asof': '2026-09-20'}
open(os.path.join(H, 'panel_v2.html'), 'w', encoding='utf-8').write(TEMPLATE.replace('__DATA__', json.dumps(DATA, ensure_ascii=False))) if False else None

TEMPLATE = r"""<title>AI 发展监测 · 组合传导</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{--bg:#f4f5f7;--panel:#fff;--fg:#12161c;--mut:#5b6472;--line:#e2e5ea;--card:#f8f9fb;--accent:#1f5eff;--band:#eef1f6;
 --up:#0a7d4f;--dn:#c02636;--warn:#b26a00;--neu:#5b6472;
 --d1:#1f5eff;--d2:#0e7490;--d3:#7c3aed;--d5:#0d9488;--d6:#047857;--d7:#be123c;
 --serif:"Newsreader",Georgia,serif;--sans:"IBM Plex Sans","Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}
:root:not([data-theme=light]) @media(prefers-color-scheme:dark){}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0c0f14;--panel:#141922;--fg:#e6e9ee;--mut:#8c96a6;--line:#232a35;--card:#10141b;--band:#141922;--accent:#5b8cff}}
:root[data-theme=dark]{--bg:#0c0f14;--panel:#141922;--fg:#e6e9ee;--mut:#8c96a6;--line:#232a35;--card:#10141b;--band:#141922;--accent:#5b8cff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:14px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding-block:0;padding-left:16px;padding-right:16px}
h1{font-family:var(--serif);font-weight:600;font-size:19px;margin:0}.eyebrow{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);font-weight:600}
header{background:var(--panel);border-bottom:1px solid var(--line)}
.htop{display:flex;align-items:baseline;gap:12px;padding:14px 0}.htop .asof{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--mut)}
.theme{background:var(--card);border:1px solid var(--line);color:var(--fg);border-radius:7px;padding:5px 9px;cursor:pointer;font-size:12px}
/* signature band */
.band{background:var(--band);border-bottom:1px solid var(--line)}
.bandgrid{display:grid;grid-template-columns:1fr auto 1fr;gap:18px;padding:14px 0}
@media(max-width:760px){.bandgrid{grid-template-columns:1fr;gap:12px}}
.bcol .eyebrow{margin-bottom:8px}.brow{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;padding:3px 0;border-bottom:1px dotted var(--line)}
.brow .lab{color:var(--mut)}.brow .val{font-family:var(--mono);font-weight:600}
.bmid{display:flex;flex-direction:column;justify-content:center;gap:6px;text-align:center;padding:0 6px;border-left:1px solid var(--line);border-right:1px solid var(--line)}
@media(max-width:760px){.bmid{border:none;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:10px 0}}
.gatechip{font-size:11.5px;padding:3px 8px;border:1px solid var(--line);border-radius:6px;background:var(--panel)}
.arrow{color:var(--mut);font-size:11px}
.up{color:var(--up)}.dn{color:var(--dn)}.neu{color:var(--neu)}.warn{color:var(--warn)}
/* tabs */
nav{display:flex;gap:2px;border-bottom:1px solid var(--line);background:var(--panel);position:sticky;top:env(safe-area-inset-top,0px);z-index:5}
nav button{background:none;border:none;border-bottom:2px solid transparent;color:var(--mut);padding:11px 14px;cursor:pointer;font-size:13.5px;font-weight:500;font-family:var(--sans)}
nav button[aria-selected=true]{color:var(--fg);border-bottom-color:var(--accent)}
main{padding-block:18px}
.tabnote{color:var(--mut);font-size:12.5px;margin:0 0 14px}
/* feed table */
table{width:100%;border-collapse:collapse;font-size:13px}
thead th{text-align:left;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600;padding:8px 10px;border-bottom:1px solid var(--line)}
tbody td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr{cursor:pointer}tbody tr:hover{background:var(--card)}
.sig{font-weight:600}.sub{color:var(--mut);font-size:11.5px;margin-top:2px}
.tag{display:inline-block;font-size:11px;padding:1.5px 7px;border-radius:5px;border:1px solid var(--line);background:var(--card);font-family:var(--mono)}
.grade{font-weight:600;font-size:12px;padding:2px 9px;border-radius:6px;white-space:nowrap}
.g-act{background:rgba(10,125,79,.13);color:var(--up)}.g-watch{background:rgba(178,106,0,.13);color:var(--warn)}.g-mon{background:var(--card);color:var(--mut)}
.dimtag{font-family:var(--mono);font-size:10.5px;padding:1px 5px;border-radius:4px;color:#fff}
/* holdings */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.hcard{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:15px}
.hcard .tk{font-family:var(--mono);font-weight:700;font-size:16px}.hcard .nm{color:var(--mut);font-size:12px;margin-top:1px}
.regime{float:right;font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px}
.r-con{background:rgba(10,125,79,.13);color:var(--up)}.r-neu{background:var(--card);color:var(--mut)}.r-cau{background:rgba(192,38,54,.12);color:var(--dn)}
.hk{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600;margin-top:13px}.hv{font-size:12.5px;margin-top:3px}
/* drawer */
.drawer{position:fixed;top:0;right:0;height:100%;width:min(420px,92vw);background:var(--panel);border-left:1px solid var(--line);box-shadow:-8px 0 30px rgba(0,0,0,.12);transform:translateX(100%);transition:transform .22s;z-index:20;overflow:auto;padding:18px}
.drawer.open{transform:none}.drawer .x{float:right;cursor:pointer;color:var(--mut);border:none;background:none;font-size:18px}
#cy{height:min(64vh,560px);border:1px solid var(--line);border-radius:10px;background:var(--panel)}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:11px;color:var(--mut);margin-top:10px}
.sw{display:inline-block;width:18px;border-top-width:3px;border-top-style:solid;vertical-align:middle;margin-right:3px}
.foot{color:var(--mut);font-size:11px;border-top:1px solid var(--line);padding:14px 0;margin-top:8px}
</style>

<header><div class="wrap htop"><div class="eyebrow">AI 发展监测体系</div><h1>AI 发展态势 → 组合传导</h1>
<span class="asof">as-of __ASOF__ · 供给侧驱动</span>
<button class="theme" onclick="var r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'light':'dark'">◐ 主题</button></div>
<div class="band"><div class="wrap bandgrid">
<div class="bcol"><div class="eyebrow">① AI 发展态势(不挂标的)</div><div id="score"></div></div>
<div class="bmid"><div class="eyebrow">② 验证与重要性筛选</div><div class="gatechip">可信度验证 · 分析师复核</div><div class="arrow">↓ 两级筛选 ↓</div><div id="gate"></div></div>
<div class="bcol"><div class="eyebrow">③ 组合传导 (Read-through)</div><div id="bhold"></div></div>
</div></div></header>
<nav id="nav">
 <button data-t="feed" aria-selected="true">今日分流</button>
 <button data-t="hold" aria-selected="false">持仓 Thesis</button>
 <button data-t="map" aria-selected="false">因果映射</button>
</nav>
<main class="wrap">
 <section id="p-feed"><p class="tabnote">AI 前沿信号经<b>可信度验证 → 重要性评估</b>两级筛选后的分流。<b>可执行</b>=重要且已验证,传导至持仓;<b>观察·待验证</b>=重要但源未经独立验证;<b>监测</b>=方向性,留前沿雷达。信号只判方向,量级由供给侧地面读数 nowcast。点行看传导路径。</p>
  <div style="overflow-x:auto"><table><thead><tr><th>信号</th><th>维度</th><th>可信度</th><th>传导渠道</th><th>影响标的</th><th>方向</th><th>分级</th></tr></thead><tbody id="feed"></tbody></table></div></section>
 <section id="p-hold" hidden><p class="tabnote">每只持仓的 thesis 状态、下一催化剂与证伪条件。量级 nowcast(实测/预期/上期 + 与一致预期偏离)接入共识与回测数据后展开。</p><div class="cards" id="hold"></div></section>
 <section id="p-map" hidden><p class="tabnote">因果映射:AI 发展节点 → 传导机制 → 影响标的的有向加权图(doc25 逐票链)。边宽=传导权重,颜色=方向,线型=验证等级。此图为<b>方法论/下钻</b>视图,非日用主视图。</p>
  <div id="cy"></div><div class="legend"><span>源=AI 事件</span><span>○=传导机制</span><span>◆=标的</span><span><span class="sw" style="border-top-color:var(--up)"></span>利多 <span class="sw" style="border-top-color:var(--dn)"></span>利空 <span class="sw" style="border-top-color:var(--warn)"></span>冲击</span></div></section>
</main>
<div class="wrap foot">数据来源分级 P1–P5 · 验证等级 可回测/结构对账/方向性 · 前沿信号仅判方向,不做量级 nowcast · AI 生成 + 分析师复核 · 本页为投研内部监测原型</div>
<div class="drawer" id="drawer"><button class="x" onclick="document.getElementById('drawer').classList.remove('open')">✕</button><div id="dc"></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.2/cytoscape.min.js"></script>
<script>
const D=__DATA__;const DIMC={D1:'#1f5eff',D2:'#0e7490',D3:'#7c3aed',D5:'#0d9488',D6:'#047857',D7:'#be123c'};
const esc=s=>(s==null?'':(''+s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const dcl=d=>d.startsWith('↑')?'up':d.startsWith('↓')?'dn':d.startsWith('!')?'warn':'neu';
// 记分牌
document.getElementById('score').innerHTML=D.score.map(s=>`<div class="brow"><span class="lab">${esc(s[0].slice(3))} · ${esc(s[1])}</span><span class="val ${dcl(s[3])}">${esc(s[2])} ${esc(s[3])}</span></div>`).join('');
document.getElementById('gate').innerHTML=`<span class="gatechip">可执行 <b class="up">${D.gate.o}</b> · 观察 <b class="warn">${D.gate.w}</b> · 监测 <b>${D.gate.m}</b></span>`;
// band 持仓
const RG={'看多确认':'r-con','中性':'r-neu','过热风险':'r-cau'};
document.getElementById('bhold').innerHTML=D.hold.map(h=>`<div class="brow"><span class="lab">${esc(h[0])} ${esc(h[2])}</span><span class="val">${esc((h[4]||'').slice(0,16))}…</span></div>`).join('');
// feed
document.getElementById('feed').innerHTML=D.feed.map((f,i)=>{const g=f.grade==='可执行'?'g-act':f.grade.indexOf('观察')>=0?'g-watch':'g-mon';const dm=(f.name.match(/维/)?'':'');
 return `<tr onclick="openRow(${i})"><td><div class="sig">${esc(f.name)}</div><div class="sub">${esc(f.val)}</div></td><td><span class="tag">${esc(f.channeldim||'')}</span></td><td>${esc(f.verif)}</td><td>${esc(f.channel)}</td><td>${esc(f.readthrough)}</td><td class="${dcl(D.feed[i].dirw||'—')}">${esc(f.dirw||'—')}</td><td><span class="grade ${g}">${esc(f.grade)}</span></td></tr>`;}).join('');
// holdings
document.getElementById('hold').innerHTML=D.hold.map(h=>`<div class="hcard"><span class="regime ${RG[h[2]]||'r-neu'}">${esc(h[2])}</span><div class="tk">${esc(h[0])}</div><div class="nm">${esc(h[1])}</div>
 <div class="hk">Thesis 现状</div><div class="hv">${esc(h[3])}</div><div class="hk">下一催化剂</div><div class="hv">${esc(h[4])}</div><div class="hk">证伪条件</div><div class="hv" style="color:var(--mut)">${esc((D.fal[h[0]]||'—').slice(0,150))}</div></div>`).join('');
// tabs
document.querySelectorAll('#nav button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#nav button').forEach(x=>x.setAttribute('aria-selected',x===b));
 ['feed','hold','map'].forEach(t=>document.getElementById('p-'+t).hidden=(t!==b.dataset.t));if(b.dataset.t==='map')drawGraph();});
// drawer
function openRow(i){const f=D.feed[i];document.getElementById('dc').innerHTML=`<div class="eyebrow">信号 · 传导路径</div><h1 style="font-size:16px;margin:6px 0">${esc(f.name)}</h1>
 <div class="hv">${esc(f.val)}</div><div class="hk">分级 / 可信度</div><div class="hv"><span class="grade ${f.grade==='可执行'?'g-act':f.grade.indexOf('观察')>=0?'g-watch':'g-mon'}">${esc(f.grade)}</span> <span class="tag">${esc(f.verif)}</span> <span class="tag">重要性 ${esc(f.impact)}</span></div>
 <div class="hk">传导渠道 → 影响标的</div><div class="hv">${esc(f.channel)} → <b>${esc(f.readthrough)}</b></div><div class="hk">分析师判读</div><div class="hv" style="color:var(--mut)">${esc(f.why)}</div>
 <div class="hk" style="margin-top:14px">AI 生成 · 分析师复核</div>`;document.getElementById('drawer').classList.add('open');}
// graph
let gdrawn=false;function drawGraph(){if(gdrawn)return;gdrawn=true;const DIR={'↑':'var(--up)','↓':'var(--dn)','→':'#9aa3b0','!':'var(--warn)','—':'#c3c9d2'};
 cytoscape({container:document.getElementById('cy'),elements:D.graph,minZoom:.3,maxZoom:2,wheelSensitivity:.25,layout:{name:'preset',fit:true,padding:26},
  style:[{selector:'node',style:{'label':'data(label)','font-size':'9px','color':'var(--fg)','text-wrap':'wrap','text-max-width':'86px','text-valign':'center','width':'label','height':'label','padding':'6px','shape':'round-rectangle','background-color':'#e4e7ec','border-width':1,'border-color':'#c3c9d2'}},
   {selector:'node[kind="source"]',style:{'background-color':e=>DIMC[e.data('dim')]||'#64748b','background-opacity':.15,'border-color':e=>DIMC[e.data('dim')]||'#64748b','border-width':2}},
   {selector:'node[kind="mech"]',style:{'background-color':'var(--card)','font-size':'8.5px','color':'var(--mut)'}},
   {selector:'node[kind="ticker"]',style:{'background-color':'#1f5eff','background-opacity':.14,'border-color':'#1f5eff','border-width':2.5,'font-weight':700,'font-size':'12px','padding':'9px'}},
   {selector:'edge',style:{'width':'mapData(w,0,.4,1,6)','line-color':e=>DIR[e.data('dir')]||'#c3c9d2','target-arrow-color':e=>DIR[e.data('dir')]||'#c3c9d2','target-arrow-shape':'triangle','arrow-scale':.7,'curve-style':'bezier','opacity':.5}}]});}
</script>"""

# 组装:方向文案 + 维度 tag(按 metric 匹配,不按标题)
for f in DATA['feed']:
    mid = f['metric']
    f['dirw'] = DIRW.get(DIRN.get(mid, '—'), '—')
    dim = next((c[3] for c in CHAINS if c[2] == mid), '')
    f['channeldim'] = (dim or 'D5').split('/')[0] if dim else ('D2' if mid == 'm_data_wall' else 'D5')
open(os.path.join(H, 'panel_v2.html'), 'w', encoding='utf-8').write(TEMPLATE.replace('__DATA__', json.dumps(DATA, ensure_ascii=False)).replace('__ASOF__', DATA['asof']))
print('feed', len(DATA['feed']), 'hold', len(DATA['hold']), 'graph nodes', len(GRAPH['nodes']), 'gate', DATA['gate'])
