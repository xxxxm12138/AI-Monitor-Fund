# -*- coding: utf-8 -*-
import json, os
S=os.path.dirname(os.path.abspath(__file__))
R=json.load(open(S+"/result_layer_data.json"))
J=json.load(open(S+"/judgment_layer_data.json"))
C=json.load(open(S+"/cockpit_data.json"))
SD=json.load(open(S+"/source_data.json"))

TPL=r"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI-Monitoring-System</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#f6f7f9;--card:#fff;--soft:#fafbfc;--ink:#1a1d29;--cap:#565b6b;--mut:#8a8f9c;--line:#ecedf1;--line2:#f3f4f7;
--ac:#5b5bd6;--ac2:#6d5ef0;--ac-soft:#eef0fe;--ac-bd:#d7d9fb;
--up:#16a34a;--up-w:#e7f6ec;--dn:#dc2626;--dn-w:#fcebeb;--warn:#b7791f;--warn-w:#fdf4e3;
--bl:#3b82f6;--pk:#ec4899;--gr:#10b981;--pp:#7c6cf0;--am:#d97706;--risk:#dc2626}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:"Inter","PingFang SC","Microsoft YaHei",sans-serif;font-size:13px;line-height:1.5;-webkit-font-smoothing:antialiased}
.num{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
svg{display:block}
/* header */
.hdr{background:var(--card);border-bottom:1px solid var(--line);height:56px;display:flex;align-items:center;gap:14px;padding:0 16px;position:sticky;top:0;z-index:20}
.ava{width:30px;height:30px;border-radius:50%;background:var(--ac);color:#fff;display:grid;place-items:center;font-weight:700;font-size:14px}
.idc .nm{font-weight:700;font-size:14px;line-height:1.1}
.idc .ch{display:flex;gap:5px;margin-top:2px;align-items:center}
.tk-chip{background:var(--up-w);color:var(--up);font-weight:600;font-size:10.5px;border-radius:3px;padding:1px 6px}
.mini{color:var(--mut);font-size:10.5px}
.clk{cursor:pointer}.clk:hover{background:var(--soft)}.clk.sel,tr.sel{background:var(--ac-soft)}
.tg{cursor:pointer}
.hdr-left{display:flex;align-items:center;gap:14px;flex:none}
.hsum{display:flex;align-items:baseline;gap:8px;border-left:1px solid var(--line);padding-left:14px;margin-left:2px}
.hsum .big{font-size:20px;font-weight:700}.hsum .sub{font-size:12px;font-weight:600}
.hsum .sub.dn{color:var(--dn)}.hsum .sub.up{color:var(--up)}
.hsum .st-weak{color:var(--warn);font-weight:700}.hsum .st-mid{color:var(--ac);font-weight:700}.hsum .st-strong{color:var(--up);font-weight:700}
.grow{flex:1}
.tabs{display:flex;gap:4px}
.tab{display:inline-flex;align-items:center;gap:6px;border:1px solid transparent;border-radius:8px;padding:7px 11px;font-size:12.5px;font-weight:600;color:var(--cap);cursor:pointer;background:transparent;font-family:inherit}
.tab:hover{background:var(--soft)}
.tab.on{background:var(--ac-soft);border-color:var(--ac-bd);color:var(--ac)}
.hq{width:28px;height:28px;border:1px solid var(--line);border-radius:7px;display:grid;place-items:center;color:var(--mut);cursor:pointer}
/* layout */
.wrap{padding:14px 16px 40px;max-width:1520px;margin:0 auto}
.toprow{display:grid;grid-template-columns:340px 1fr;gap:14px;margin-bottom:14px;height:248px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px}
.toprow .panel{height:248px;display:flex;flex-direction:column;overflow:hidden}
.toprow .ph{flex:none}.toprow .pb{overflow:auto;flex:1}
.ph{padding:11px 14px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:8px}
.ph .t{font-size:13px;font-weight:700}.ph .st{color:var(--mut);font-size:11px}
.ph .r{margin-left:auto;color:var(--mut);font-size:11px}
.pb{padding:13px 14px}
.subtabs{display:flex;gap:2px}
.subtab{font-size:11.5px;font-weight:600;color:var(--mut);padding:3px 8px;border-radius:6px;cursor:pointer}
.subtab.on{background:var(--ink);color:#fff}
/* work area */
.work{display:grid;grid-template-columns:300px 1fr;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;align-items:stretch}
.rail{border:0;border-right:1px solid var(--line);border-radius:0;overflow:auto}
.legend{padding:12px 14px;border-bottom:1px solid var(--line)}
.legend .lh{display:flex;justify-content:space-between;align-items:center;font-size:11px;font-weight:700;color:var(--mut);letter-spacing:.02em}
.legend .sel{margin-top:8px;border:1px dashed var(--line);border-radius:6px;padding:9px;color:var(--mut);font-size:11.5px;text-align:center}
.legend .sel.multi{display:flex;flex-wrap:wrap;gap:5px;text-align:left;padding:7px;border-style:solid;border-color:var(--ac-bd);color:var(--ink)}
.schip{display:inline-flex;align-items:center;gap:5px;max-width:100%;background:#fff;border:1px solid var(--ac-bd);color:var(--ac);border-radius:5px;padding:3px 7px;font-size:11px;font-weight:600;cursor:pointer;line-height:1.25}
.schip:hover{background:var(--ac-soft)}.schip .x{color:var(--mut);font-weight:700;font-size:12px}
.search{margin:12px 14px;display:flex;align-items:center;gap:7px;border:1px solid var(--line);border-radius:7px;padding:6px 9px;color:var(--mut)}
.search input{border:0;outline:0;font-family:inherit;font-size:12px;width:100%;background:transparent;color:var(--ink)}
.cats{display:flex;gap:5px;padding:0 14px 10px;border-bottom:1px solid var(--line)}
.cat{flex:1;height:30px;border:1px solid var(--line);border-radius:7px;display:grid;place-items:center;color:var(--mut);cursor:pointer}
.cat.on{background:var(--ac-soft);border-color:var(--ac-bd);color:var(--ac)}
.grp{border-bottom:1px solid var(--line2)}
.grp .gh{display:flex;align-items:center;gap:7px;padding:9px 14px;font-size:10.5px;font-weight:700;letter-spacing:.03em}
.grp .gh .cnt{margin-left:auto;color:var(--mut);font-weight:600;font-size:10.5px}
.item{display:flex;align-items:center;gap:8px;padding:8px 14px 8px 24px;font-size:12.5px;color:var(--cap);cursor:pointer;border-top:1px solid var(--line2)}
.item:hover{background:var(--soft)}.item.on{background:var(--ac-soft);color:var(--ac);font-weight:600}
.item .ico{color:var(--mut)}.item.on .ico{color:var(--ac)}
.item .c{margin-left:auto;font-size:10.5px;color:var(--mut);border:1px solid var(--line);border-radius:10px;padding:0 6px}
.item .w{margin-left:auto;font-size:11px;color:var(--mut)}
/* canvas */
.canvas{border:0;border-radius:0;overflow:hidden;min-height:520px;display:flex;flex-direction:column}
.ctrl{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:7px;overflow:hidden}
.seg button{border:0;background:#fff;font-family:inherit;font-size:11.5px;font-weight:600;color:var(--cap);padding:5px 10px;cursor:pointer}
.seg button.on{background:var(--ac-soft);color:var(--ac)}
.field{border:1px solid var(--line);border-radius:7px;padding:4px 9px;font-size:11.5px;color:var(--cap);display:inline-flex;flex-direction:column;line-height:1.15}
.field .fl{font-size:8.5px;color:var(--ac);font-weight:700;text-transform:uppercase}
.field .fv{font-weight:600}
.chkrow{display:flex;gap:6px;flex-wrap:wrap}
.chk{font-size:11.5px;color:var(--cap);border:1px solid var(--line);border-radius:14px;padding:3px 10px;display:inline-flex;align-items:center;gap:5px}
.chk.off{color:var(--mut);opacity:.55}
.chk .b{width:11px;height:11px;border-radius:3px;border:1.5px solid var(--mut)}.chk.on .b{background:var(--ac);border-color:var(--ac)}
.btn-ac{margin-left:auto;background:var(--ac);color:#fff;border:0;border-radius:7px;padding:6px 12px;font-size:11.5px;font-weight:600;cursor:pointer;font-family:inherit;display:inline-flex;align-items:center;gap:6px}
.stage{flex:1;padding:14px 16px;position:relative;overflow:auto}
.empty{height:100%;min-height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--mut)}
.empty .ei{width:56px;height:56px;border-radius:12px;background:var(--ac-soft);color:var(--ac);display:grid;place-items:center;margin-bottom:14px}
.empty h3{color:var(--ink);margin:0 0 4px;font-size:16px}
.qsel{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px;width:320px}
.qs{border:1px solid var(--line);border-radius:8px;padding:9px;font-size:12px;color:var(--cap);display:flex;align-items:center;gap:7px;cursor:pointer}
.qs:hover{border-color:var(--ac-bd);background:var(--soft)}
/* cards grid */
.ovgrid{display:grid;grid-template-columns:1.35fr .95fr;gap:12px}
.ovrow{display:grid;grid-template-columns:64px 1fr 46px 1fr 44px;gap:8px;align-items:center;padding:6px 0;border-bottom:1px solid var(--line2);font-size:12px}
.ovrow:last-child{border-bottom:0}
.ovtk{font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ovb{height:8px;background:var(--line2);border-radius:2px;overflow:hidden}
.ovb i{display:block;height:100%}
.ovb i.w{background:var(--ink)}.ovb i.e{background:var(--ac)}
.ovhd{font-size:9.5px;color:var(--mut);font-weight:600;text-transform:uppercase}
.ovstat{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.ovstat .kcard{padding:10px 12px}
.kcard{border:1px solid var(--line);border-radius:9px;overflow:hidden}
.kh{padding:9px 12px;border-bottom:1px solid var(--line2);display:flex;align-items:center;gap:7px}
.kh .dot{width:8px;height:8px;border-radius:50%}.kh .t{font-weight:600;font-size:12.5px}.kh .tg{margin-left:auto;font-size:10px;color:var(--mut);border:1px solid var(--line);border-radius:10px;padding:0 7px}
.kb{padding:11px 12px}
.locked{filter:grayscale(1);opacity:.75}
.lockbox{display:flex;flex-direction:column;align-items:center;gap:7px;padding:20px;color:var(--mut);text-align:center}
.lockbox .up{background:var(--ac);color:#fff;border-radius:6px;padding:5px 11px;font-size:11px;font-weight:600}
/* tables/bars */
table{width:100%;border-collapse:collapse;font-size:11.5px}
th{text-align:left;color:var(--mut);font-weight:600;font-size:9.5px;text-transform:uppercase;padding:6px 8px;border-bottom:1px solid var(--line)}
th.r,td.r{text-align:right}
td{padding:6px 8px;border-bottom:1px solid var(--line2)}tr:last-child td{border-bottom:0}
.mk{color:var(--pp);font-size:10px;border:1px solid var(--line2);border-radius:3px;padding:0 4px}
.tier{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--mut);border:1px solid var(--line);border-radius:3px;padding:0 5px}
.dom{font-size:10px;font-weight:600}.dom.可交易{color:var(--up)}.dom.预警{color:var(--warn)}.dom.待定{color:var(--mut)}
.bar{display:grid;grid-template-columns:130px 1fr 46px;align-items:center;gap:9px;margin:7px 0;font-size:12px}
.bar .bl{color:var(--cap);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bar .bt{height:9px;background:var(--line2);border-radius:2px;overflow:hidden}.bar .bt i{display:block;height:100%;background:var(--ac)}.bar .bt.risk i{background:var(--risk)}
.bar .bp{text-align:right;font-weight:700}
.ln{display:flex;gap:10px;align-items:baseline;padding:7px 0;border-bottom:1px solid var(--line2)}.ln:last-child{border-bottom:0}
.ln .k{font-size:9.5px;font-weight:700;color:var(--mut);width:46px;flex:none;text-transform:uppercase;padding-top:1px}
.ln .v{font-size:12.5px;flex:1}.ln.al{border-left:2px solid var(--dn);padding-left:9px;margin-left:-11px}.ln.al .k{color:var(--dn)}
.tag{font-size:10px;font-weight:600;border-radius:3px;padding:1px 6px}.tag.w{background:var(--warn-w);color:var(--warn)}.tag.n{background:var(--soft);color:var(--mut);border:1px solid var(--line)}.tag.g{background:var(--up-w);color:var(--up)}
.robtag{font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:4px}.rob-s{background:var(--up-w);color:var(--up)}.rob-m{background:var(--ac-soft);color:var(--ac)}.rob-w{background:var(--warn-w);color:var(--warn)}
.pill{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:6px;padding:4px 9px;font-size:11.5px}
.heat{display:grid;grid-template-columns:52px repeat(4,1fr);gap:3px;font-size:10px}
.heat .hc{padding:5px 3px;text-align:center;border-radius:2px;min-height:22px}.heat .hl{color:var(--mut);text-align:left;padding:3px 4px}
.mut{color:var(--mut)}
.scrow{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
.scard{border:1px solid var(--line);border-radius:8px;padding:8px 10px;cursor:pointer}
.scard:hover{border-color:var(--ac-bd);background:var(--ac-soft)}
.scard .n{font-size:20px;font-weight:700;line-height:1.15}
.scard .l{font-size:10.5px;color:var(--mut);font-weight:600;margin-top:2px}
.mmd{background:#fff;border:1px solid var(--line);border-radius:8px;padding:6px 8px 8px;margin:0 0 14px;overflow:hidden;cursor:zoom-in;display:flex;flex-direction:column}
.mmdh{display:flex;justify-content:space-between;align-items:center;padding:0 2px 4px;flex:none;user-select:none;gap:8px}
.mmd .mermaid{margin:0;flex:1;min-height:0;overflow:hidden;display:flex;align-items:center;justify-content:center;cursor:grab;touch-action:none}
.mmd .mermaid.grabbing{cursor:grabbing}
.mmd-0{height:168px}
.mmd-1{height:340px}
.mmd-ph{pointer-events:none;visibility:hidden;margin-bottom:14px}
.mmdov{position:fixed;inset:0;background:rgba(26,29,41,.42);z-index:40;display:flex;align-items:center;justify-content:center;padding:24px;cursor:zoom-out}
.mmdov .mmd{width:min(1240px,94vw);height:min(82vh,760px);margin:0;cursor:default;overflow:hidden}
.mmd-0 .mermaid svg,.mmd-1 .mermaid svg,.mmdov .mmd .mermaid svg{max-width:100%!important;max-height:100%!important;width:auto!important;height:auto!important;transform-origin:0 0;will-change:transform}
.ladder{display:inline-flex;gap:2px;align-items:center}.ladder .s{font-size:8.5px;padding:1px 5px;border-radius:3px;background:var(--line2);color:var(--mut)}.ladder .s.cur{background:var(--ac);color:#fff;font-weight:700}.ladder .a{color:var(--mut);font-size:8px}
.ekb{font-size:9.5px;font-weight:700;padding:1px 6px;border-radius:3px}.ek-rule{background:var(--up-w);color:var(--up)}.ek-human{background:var(--soft);color:var(--cap);border:1px solid var(--line)}.ek-llm{background:var(--ac-soft);color:var(--ac)}
a.ext{color:var(--ac);text-decoration:none;font-weight:600}a.ext:hover{text-decoration:underline}
/* guide mode */
.guide-btn{border:1px solid var(--line);border-radius:8px;padding:6px 11px;font-size:12px;font-weight:600;color:var(--cap);background:#fff;cursor:pointer;font-family:inherit}
.guide-btn:hover{background:var(--soft)}.guide-btn.on{background:var(--ac-soft);border-color:var(--ac-bd);color:var(--ac)}
body.guide-on .wrap{margin-right:336px;transition:margin-right .2s}
.guide-panel{position:fixed;top:56px;right:0;width:320px;height:calc(100vh - 56px);background:var(--card);border-left:1px solid var(--line);display:flex;flex-direction:column;transform:translateX(100%);transition:transform .22s ease;box-shadow:-8px 0 24px rgba(26,29,41,.06)}
body.guide-on .guide-panel{transform:translateX(0)}
.guide-head{padding:14px 16px 10px;border-bottom:1px solid var(--line2);flex:none}
.guide-head .gt{font-size:14px;font-weight:700}
.guide-head .gd{display:inline-flex;align-items:center;gap:4px;margin-top:5px;font-size:11px;font-weight:600;color:var(--ac);text-decoration:none}
.guide-head .gd:hover{text-decoration:underline}
.guide-head .gs{font-size:11px;color:var(--mut);margin-top:6px;line-height:1.45}
.guide-body{padding:12px 14px 16px;overflow:auto;flex:1}
.guide-card{border:1px solid var(--line);border-radius:9px;padding:10px 12px;margin-bottom:8px;cursor:pointer;background:#fff}
.guide-card:hover{border-color:var(--ac-bd);background:var(--soft)}
.guide-card.on{border-color:var(--ac);background:var(--ac-soft);box-shadow:0 0 0 1px var(--ac-bd)}
.guide-card .gn{font-size:12px;font-weight:700;margin-bottom:4px}
.guide-card .gr{font-size:10px;font-weight:700;color:var(--ac);text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px}
.guide-card .gx{font-size:11px;color:var(--cap);line-height:1.5}
.guide-card .gx b{color:var(--ink);font-weight:600}
.guide-foot{padding:10px 14px;border-top:1px solid var(--line2);font-size:10.5px;color:var(--mut);flex:none}
.guide-spot{position:fixed;z-index:26;display:none;pointer-events:none;border-radius:10px;outline:2px solid var(--ac);outline-offset:0;box-shadow:0 0 0 9999px rgba(26,29,41,.28);transition:top .15s ease,left .15s ease,width .15s ease,height .15s ease,border-radius .15s ease}
body.guide-spot-on .guide-spot{display:block}
body.guide-on [data-guide]{cursor:pointer}
body.guide-on [data-guide]:hover{box-shadow:0 0 0 1px var(--ac-bd)}
.guide-panel{z-index:30}
/* first-visit onboarding */
.onboard{position:fixed;inset:0;z-index:60;display:none}
.onboard.on{display:block}
.onboard-mask{position:absolute;inset:0;background:rgba(26,29,41,.42)}
.onboard-card{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:min(440px,calc(100vw - 32px));background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 22px 18px;box-shadow:0 18px 48px rgba(26,29,41,.18);z-index:62}
.onboard-card .ot{font-size:18px;font-weight:700;margin:0 0 8px}
.onboard-card .ob{font-size:13px;color:var(--cap);line-height:1.55;margin:0 0 14px}
.onboard-layers{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px}
.onboard-layer{border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:11.5px;color:var(--cap);background:var(--soft)}
.onboard-layer b{display:block;font-size:12px;color:var(--ink);margin-bottom:2px}
.onboard-actions{display:flex;justify-content:flex-end;gap:8px}
.onboard-btn{border:1px solid var(--line);border-radius:8px;padding:7px 14px;font-size:12px;font-weight:600;color:var(--cap);background:#fff;cursor:pointer;font-family:inherit}
.onboard-btn:hover{background:var(--soft)}
.onboard-btn.primary{background:var(--ac);border-color:var(--ac);color:#fff}
.onboard-btn.primary:hover{filter:brightness(1.05)}
.onboard-spot{position:fixed;z-index:61;display:none;pointer-events:none;border-radius:10px;outline:2px solid var(--ac);box-shadow:0 0 0 9999px rgba(26,29,41,.42)}
.onboard-tip{position:fixed;z-index:63;width:min(300px,calc(100vw - 24px));background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 16px 14px;box-shadow:0 14px 36px rgba(26,29,41,.16)}
.onboard-tip .ot{font-size:15px;font-weight:700;margin:0 0 6px}
.onboard-tip .ob{font-size:12px;color:var(--cap);line-height:1.5;margin:0 0 12px}
.onboard-tip .ob b{color:var(--ac)}
.guide-btn.onboard-pulse{position:relative;z-index:62;animation:onboardPulse 1.4s ease-in-out infinite}
@keyframes onboardPulse{0%,100%{box-shadow:0 0 0 0 rgba(91,91,214,.45)}50%{box-shadow:0 0 0 8px rgba(91,91,214,0)}}
body.onboard-on{overflow:hidden}
@media(max-width:1100px){body.guide-on .wrap{margin-right:0}.guide-panel{width:100%;max-width:360px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}.guide-btn.onboard-pulse{animation:none;box-shadow:0 0 0 3px var(--ac-soft)}}
</style></head><body>
<div class="hdr" id="hdr"></div>
<div class="onboard" id="onboard"></div>
<div class="guide-spot" id="guide-spot"></div>
<aside class="guide-panel" id="guide"></aside>
<div class="wrap"><div class="toprow" id="toprow"></div>
 <div class="work"><aside class="rail" id="rail"></aside>
  <section class="canvas"><div class="ctrl" id="ctrl"></div><div class="stage" id="stage"></div></section></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
const R=__R__,J=__J__,C=__C__,SRC=__S__;
const cv=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const MLAB={};Object.values(R.tickers).forEach(t=>t.paths.forEach(p=>MLAB[p.src]=p.src_label));
const SF={supply:{l:'供给',c:'--bl'},demand:{l:'需求',c:'--gr'},regime:{l:'政体',c:'--am'},compete:{l:'竞对',c:'--pp'},self:{l:'本体',c:'--mut'}};
const IC={grid:'<path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/>',db:'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',cpu:'<rect x="6" y="6" width="12" height="12" rx="1"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',chart:'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',search:'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/>',chev:'<path d="M9 6l6 6-6 6"/>',save:'<path d="M6 3h12v18l-6-4-6 4z"/>',ext:'<path d="M7 17L17 7M9 7h8v8"/>'};
function svg(p,s){return `<svg width="${s||14}" height="${s||14}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`}
const TABS=[['overview','Overview','grid'],['source','Source','db'],['judge','Judgment','cpu'],['result','Results','chart']];
let tab='overview', ticker='NBIS', mmZ=0, mmS=1, mmX=0, mmY=0, guideOn=false, guideFocus='', onboardStep=0, onboardChecked=false;
const ONBOARD_KEY='ams-onboard-v1';
const GUIDE_README='https://github.com/xxxxm12138/AI-Monitor-Fund/blob/main/README.md#monitoring-panel';
const GUIDE={
 overview:[
  {id:'ov-shared',title:'Shared Exposure',what:'Upstream nodes shared by 2+ holdings.',for:'Systemic risk — one break hits multiple positions.',when:'Start of week · before earnings season · when a macro node moves.'},
  {id:'ov-weekly',title:'Weekly Focus',what:'Curated alert, portfolio snapshot, events, mandate.',for:'Priority triage without opening every tab.',when:'Monday AM · pre-market · after a major shock. Click rows to drill.'},
  {id:'ov-holdings',title:'Holdings Coverage',what:'Weight vs independent evidence paths per ticker.',for:'Spot oversized positions with thin graphs (weight ↑ evidence ↓).',when:'Rebalancing prep · deciding which name needs a deep dive in Results.'},
  {id:'ov-calendar',title:'Data Calendar',what:'Scheduled data releases — filings, customs, capacity nodes.',for:'Lead time for nowcast / falsifier checks (not news headlines).',when:'Planning the week · T-7 / T-3 before a release. Click to jump Source or Results.'},
  {id:'ov-kpi',title:'KPI Strip',what:'Metric coverage · P1 source ratio · review queue · outcome backfill.',for:'Pipeline health at a glance.',when:'Daily standup · before trusting a signal · audit backlog.'},
  {id:'ov-rail',title:'Views · Search',what:'Tab switcher and search on the left rail.',for:'Navigate layers or filter lists on other tabs.',when:'Switch Overview → Source / Judgment / Results.'},
  {id:'ov-ctrl',title:'Control Hint',what:'Context bar for the active page.',for:'Quick reminder of what you can do on this tab.',when:'First visit to a layer · training new users.'}],
 source:[
  {id:'src-topbar',title:'Source Snapshot',what:'Metrics = total KPIs in the source DB. P1 % = share with primary (tier-1) provenance — higher = more auditable ground truth.',for:'Sanity-check data-base size and source quality before drilling.',when:'Entering Source · before earnings season.'},
  {id:'src-dimension',title:'Dimension Coverage',what:'D1–D7 metrics × certainty (T1/T2/T3/Frontier).',for:'Find which AI dimension is thin or missing depth.',when:'Planning data collection · before trusting a cross-dimension thesis.'},
  {id:'src-calendar',title:'Data Calendar',what:'Upcoming releases mapped to metrics.',for:'Jump straight to the series behind an event.',when:'T-7 / T-3 before earnings · customs · capacity nodes. Click an event to select metrics.'},
  {id:'src-rail',title:'Source Metrics',what:'Metric tree by dimension · multi-select · search.',for:'Pick KPIs to inspect raw observations.',when:'Verifying a number · tracing provenance · comparing actual vs guidance.'},
  {id:'src-ctrl',title:'Data Class Filter',what:'Quant · Event · View · Frontier toggles.',for:'Narrow the metric list to the kind of ground truth you need.',when:'Only price/volume · only events · only views · frontier placeholders.'},
  {id:'src-obs',title:'Observations',what:'Period · value · type · provenance · source links per selected metric.',for:'Audit trail for every data point — the L0 ground truth layer.',when:'Nowcast · falsifier check · any "where did this number come from?"'}],
 judge:[
  {id:'jud-topbar',title:'Judgment Snapshot',what:'Outcome backfill = decisions with logged outcomes / total decision logs — pipeline closure rate.',for:'Judgment pipeline closure at a glance.',when:'Daily standup · before registry drill-down.'},
  {id:'jud-coverage',title:'Decision Coverage',what:'Decision groups × calibration stage (Human/Shadow/Assisted/Auto).',for:'See which judgment types are still shadow vs production.',when:'Process audit · planning what to promote to assisted/auto.'},
  {id:'jud-exec',title:'Execution & Signals',what:'Rule/Human/Review counts plus divergence & calendar feed.',for:'Operational queue — what needs human review today.',when:'Daily triage · chasing review backlog · linking shocks to source.'},
  {id:'jud-rail',title:'Decision Filters',what:'Executor · calibration · tier · group · owner filters.',for:'Narrow the registry to the decision class you are auditing.',when:'Deep dive on one gate type · LLM monitor mode · owner handoff.'},
  {id:'jud-ctrl',title:'Control Hint',what:'How to use filters, registry rows, and LLM mode.',for:'Orientation on this layer.',when:'First visit to Judgment · training.'},
  {id:'jud-registry',title:'Decision Registry',what:'12 decision types with executor, calibration, logs, outcome counts.',for:'Type-level status of the judgment pipeline.',when:'Pick a decision type to inspect instances · track outcome backfill.'},
  {id:'jud-instances',title:'Instances',what:'Six-tuple records for one decision type (target · choice · conf · basis · outcome).',for:'Audit a specific judgment call.',when:'After clicking a registry row · outcome pending · dispute resolution.'},
  {id:'jud-llm',title:'LLM Monitor',what:'Preview layout for future LLM judgment ops (health · queue · types).',for:'Placeholder for assisted/auto LLM decisions — not active yet.',when:'Roadmap review only · demo mode when Executor = LLM.'}],
 result:[
  {id:'res-topbar',title:'Ticker Snapshot',what:'Weight % = portfolio allocation for the selected ticker. Strength = evidence depth (independent paths × tradable score) — Weak / Medium / Strong. Not a buy/sell label.',for:'Spot large positions with thin graphs (e.g. 30% weight + Weak strength).',when:'Every Results visit · each ticker switch on the rail.'},
  {id:'res-coverage',title:'Evidence Coverage',what:'Paths by side (supply/demand/regime/entity/peers) × tier/alert.',for:'See where evidence is dense vs where warnings cluster.',when:'Pick which side of thesis to stress-test for this ticker.'},
  {id:'res-signals',title:'Signals & Catalysts',what:'Shocks and calendar items linked to this ticker\'s paths.',for:'In-layer drill — filter paths or switch ticker without leaving Results.',when:'Something moved · event approaching · follow a signal into the path table.'},
  {id:'res-rail',title:'Holdings Rail',what:'Core · watchlist · tail positions with weights.',for:'Switch the ticker under analysis.',when:'Compare NBIS vs RBRK · tail names with thin graphs.'},
  {id:'res-ctrl',title:'Control Hint',what:'Select ticker · graph · path table workflow.',for:'Orientation on Results layer.',when:'First deep dive on a name.'},
  {id:'res-structure',title:'Evidence Structure',what:'Raw vs independent path count · min-cut choke point.',for:'Quick read on graph redundancy before reading every row.',when:'Assessing thesis fragility · "what breaks if one node fails?"'},
  {id:'res-graph',title:'Transmission Graph',what:'Mermaid flowchart — upstream → mechanisms → ticker.',for:'Explain causality visually; click to expand · scroll to zoom.',when:'PM/reviewer needs the chain story · not for daily sort.'},
  {id:'res-paths',title:'Path Table',what:'Each source signal · chain · tradable/warning · tier · dominant.',for:'Sortable evidence rows — which edges matter most.',when:'Sizing attention across paths · filtering after a signal click.'}]};
const GUIDE_RAIL={overview:'ov-rail',source:'src-rail',judge:'jud-rail',result:'res-rail'};
const GUIDE_CTRL={overview:'ov-ctrl',source:'src-ctrl',judge:'jud-ctrl',result:'res-ctrl'};
const GUIDE_TOP={source:'src-topbar',judge:'jud-topbar',result:'res-topbar'};
let srcSels=['m_nbis_rev'], srcOpen='D1', q='', srcDC='all', srcHit='';
let judEK='all', judType=(J.registry[0]||{}).id||null, resFocus=null;
const TG={'表征/源':['d_source_tier'],'边':['d_edge_predict','d_edge_tier','d_factor'],'闸':['d_falsify_gate','d_impact_gate'],'regime/方向':['d_regime','d_divergence_explain','d_direction'],'运维':['d_route','d_fill_priority','d_calendar_scope']};
let fCal=new Set(['human','shadow','assisted','auto']), fTier=new Set(['A','B','C','—']), fGrp=new Set(Object.keys(TG)), fOwner=new Set();
const LLM={health:{esc:0.14,eval:0.85,halluc:1,cost:'$12/日',todo:5,shadow:3,assisted:1},
 types:[{id:'d_source_classify',name:'源分类五元组',op:'REPRESENT',calib:'shadow',eval:0.91,esc:0.08,n:210,prompt:'src_cls@v5'},
  {id:'d_topic_cluster',name:'主题聚类',op:'PROPOSE',calib:'shadow',eval:0.83,esc:0.15,n:64,prompt:'topic@v2'},
  {id:'d_falsify_stance',name:'证伪闸 stance',op:'REPRESENT',calib:'assisted',eval:0.86,esc:0.12,n:31,prompt:'falsify_stance@v3'},
  {id:'d_divergence_draft',name:'背离解释初稿',op:'SELECT',calib:'shadow',eval:0.79,esc:0.22,n:12,prompt:'div_draft@v1'}],
 queue:[{sev:'high',kind:'幻觉旗标',txt:'背离解释初稿 · r158 · 引用了不存在的公告',type:'d_divergence_draft',trace:'lf_tr_2a70'},
  {sev:'high',kind:'低分待复核',txt:'背离解释初稿 · r166 · eval 0.58 < 阈 0.70',type:'d_divergence_draft',trace:'lf_tr_2a91'},
  {sev:'high',kind:'低分待复核',txt:'主题聚类 · 顶刊批次 #12 · eval 0.61',type:'d_topic_cluster',trace:'lf_tr_0f77'},
  {sev:'mid',kind:'OOD 逃逸',txt:'源分类 · 新型来源(播客转写)· 已自动转人工',type:'d_source_classify',trace:'lf_tr_1c30'},
  {sev:'act',kind:'待晋升审批',txt:'源分类五元组 · shadow 连续 6 窗 ≥ 人 → 升 assisted?',type:'d_source_classify',trace:'lf_tr_1c33'}],
 inst:{d_falsify_stance:[{dec:'lf_0207',target:'fct_frontier r147',choice:'stance=支持证伪·可核=高·过闸',conf:0.86,ev:['rubric 0.86','幻觉无','vs人标一致'],trace:'lf_tr_9f2a',esc:false},
   {dec:'lf_0205',target:'fct_frontier r141',choice:'stance=待定',conf:0.55,ev:['rubric 0.58','vs人标分歧'],trace:'lf_tr_7a02',esc:true}],
  d_source_classify:[{dec:'lf_0330',target:'stg_observation r241',choice:'维=D1·机制=GPU供给·类2·T_a/P1',conf:0.93,ev:['P/R/F1 0.92','幻觉无'],trace:'lf_tr_1c33',esc:false},
   {dec:'lf_0329',target:'stg_observation r240',choice:'维=D5·低置信',conf:0.44,ev:['P/R/F1 0.55','OOD'],trace:'lf_tr_1c30',esc:true}],
  d_topic_cluster:[{dec:'lf_0288',target:'batch#12',choice:'簇=推理架构效率↑,新主题候选',conf:0.61,ev:['一致性 0.61','边界模糊'],trace:'lf_tr_0f77',esc:true}],
  d_divergence_draft:[{dec:'lf_0410',target:'stg r166',choice:'草稿:循环融资=regime,方向不下注',conf:0.58,ev:['rubric 0.58','幻觉疑'],trace:'lf_tr_2a91',esc:true},
   {dec:'lf_0409',target:'stg r158',choice:'草稿:引用不存在公告',conf:0.40,ev:['rubric 0.40','幻觉是'],trace:'lf_tr_2a70',esc:true}]}};
const LF_HOST='https://cloud.langfuse.com';
function lfTraceUrl(id){return id?LF_HOST+'/trace/'+encodeURIComponent(id):LF_HOST}
function tgOf(id){for(const g in TG)if(TG[g].includes(id))return g;return '运维'}
function judRows(){return J.registry.filter(r=>(judEK==='all'||r.ek===judEK)&&fCal.has(r.calib)&&fTier.has(r.tier||'—')&&fGrp.has(tgOf(r.id))&&(fOwner.size===0||fOwner.has(r.owner))&&(!q||(r.name||'').includes(q)))}
function setJudEK(k){judEK=k;judType=null;if(guideOn)guideFocus=defaultGuideFocus();render()}
function togS(s,k){s.has(k)?s.delete(k):s.add(k);render()}
function setJudType(id){judType=(judType===id?null:id);render()}
function setSrcDC(dc){srcDC=dc;render()}
function setQ(v){q=v;render()}
function lad(c){const s=['human','shadow','assisted','auto'],L={human:'Human',shadow:'Shadow',assisted:'Assisted',auto:'Auto'},ci=s.indexOf(c);return '<span class="ladder">'+s.map((x,i)=>`<span class="s ${i==ci?'cur':''}">${L[x]}</span>`+(i<3?'<span class="a">›</span>':'')).join('')+'</span>'}
function judDrill(id){const reg=J.registry.find(r=>r.id===id),ins=(J.instances||{})[id]||[];
 let h=`<div style="margin-top:12px;border:1px solid var(--ac-bd);border-radius:8px;background:#fbfbff;padding:10px 12px"><div style="font-size:12px;font-weight:700;color:var(--ac);margin-bottom:6px">Instances · ${reg.name} · ${ins.length}</div>`;
 if(!ins.length)return h+'<div class="mini">No instances</div></div>';
 return h+`<table><thead><tr><th>ID</th><th>Target</th><th>Choice</th><th class="r">Conf</th><th>Basis</th><th>Outcome</th></tr></thead><tbody>`+
  ins.map(x=>`<tr><td class="mini">${x.dec}</td><td style="font-size:11px">${x.target||'—'}</td><td style="font-size:11px">${x.choice||'—'}</td><td class="r num">${x.conf==null?'—':x.conf}</td><td class="mini" style="color:var(--mut)">${x.basis||'—'}</td><td class="mini" style="color:${x.outcome?'var(--up)':'var(--mut)'}">${x.outcome||'Pending'}</td></tr>`).join('')+`</tbody></table></div>`}
function renderLLM(){const H=LLM.health;
 const kpi=(l,v,warn)=>`<div class="kcard" style="padding:8px 11px"><div class="mini">${l}</div><div style="font-size:19px;font-weight:700;${warn?'color:var(--warn)':''}">${v}</div></div>`;
 let h=`<div class="tag w" style="display:inline-block;margin-bottom:10px">LLM decisions = 0 active · preview layout</div>
  <div class="mini" style="margin:2px 0 5px;font-weight:700;color:var(--ink)">LLM Health</div>
  <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-bottom:12px">${kpi('Escalation',(H.esc*100).toFixed(0)+'%',H.esc>0.1)}${kpi('Eval Avg',H.eval)}${kpi('Hallucination',H.halluc,H.halluc>0)}${kpi('Cost',H.cost)}${kpi('Queue',H.todo,H.todo>0)}${kpi('Calibration','Sh '+H.shadow+' · As '+H.assisted)}</div>
  <div class="mini" style="margin:2px 0 5px;font-weight:700;color:var(--ink)">Priority Queue</div>
  <div class="kcard" style="margin-bottom:12px">${LLM.queue.map(z=>`<div class="ln" style="padding:8px 12px"><span class="tag ${z.sev==='high'?'w':'n'}">${z.kind}</span><span class="v" style="flex:1">${z.txt}</span><a class="mini" href="${lfTraceUrl(z.trace)}" target="_blank" rel="noopener" style="color:var(--ac);text-decoration:none;font-weight:600" title="Open trace in Langfuse">Trace ↗</a></div>`).join('')}</div>
  <div class="mini" style="margin:2px 0 5px;font-weight:700;color:var(--ink)">LLM Decision Types</div>
  <table><thead><tr><th>Type</th><th>Operator</th><th>Calibration</th><th class="r">Eval</th><th class="r">Escalation</th><th class="r">Logs</th><th>Prompt</th></tr></thead><tbody>${LLM.types.map(t=>`<tr class="clk ${judType===t.id?'sel':''}" onclick="setJudType('${t.id}')"><td style="font-weight:600">${t.name}</td><td><span class="tier">${t.op}</span></td><td>${lad(t.calib)}</td><td class="r num" style="color:${t.eval>=0.85?'var(--up)':t.eval>=0.7?'var(--warn)':'var(--dn)'}">${t.eval}</td><td class="r num" style="color:${t.esc>0.15?'var(--dn)':''}">${(t.esc*100).toFixed(0)}%</td><td class="r num">${t.n}</td><td class="mini">${t.prompt}</td></tr>`).join('')}</tbody></table>`;
 if(judType&&LLM.inst[judType]){const t=LLM.types.find(x=>x.id===judType),ins=LLM.inst[judType];
  h+=`<div style="margin-top:12px;border:1px solid var(--ac-bd);border-radius:8px;background:#fbfbff;padding:10px 12px"><div style="font-size:12px;font-weight:700;color:var(--ac);margin-bottom:6px">${t.name} · eval ${t.eval} · escalation ${(t.esc*100).toFixed(0)}% · ${t.prompt} · <a href="${LF_HOST}" target="_blank" rel="noopener" style="color:var(--ac);text-decoration:none">Langfuse ↗</a></div>
   <table><thead><tr><th>ID</th><th>Target</th><th>Choice</th><th class="r">Conf</th><th>Eval</th><th>Trace</th></tr></thead><tbody>${ins.map(x=>`<tr><td class="mini">${x.dec}</td><td class="mini">${x.target}</td><td style="font-size:11px">${x.choice}${x.esc?' <span class="tag w">Escalated</span>':''}</td><td class="r num">${x.conf}</td><td class="mini">${x.ev.join(' · ')}</td><td><a href="${lfTraceUrl(x.trace)}" target="_blank" rel="noopener" class="ext" title="Open trace ${esc(x.trace)} in Langfuse">${svg(IC.ext,14)}</a></td></tr>`).join('')}</tbody></table></div>`}
 return h}
const DCT={'1':['Quant','--bl'],'2':['Event','--am'],'3':['View','--pp'],'4':['Frontier','--gr']};
const OTYPE={actual:'Actual',guidance:'Guidance',prior:'Prior',event:'Event',state:'State',position:'Position',computed:'Computed',target:'Target'};
const GL={'表征/源':'Represent','边':'Edge','闸':'Gate','regime/方向':'Regime','运维':'Ops'};
function dcTag(dc){const t=DCT[(dc||'—')[0]]||['—','--mut'];return `<span style="font-size:9px;font-weight:700;color:var(${t[1]})">${t[0]}</span>`}
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function linkify(s){return esc(s).replace(/(https?:\/\/[^\s）;；,，&<]+)/g,'<a class="ext" href="$1" target="_blank" rel="noopener">Link</a>')}
function srcA(name,url){const lab=(name||'Source').trim();if(!url)return `<span class="mini" title="${esc(lab)}">${esc(lab? (lab.length>28?lab.slice(0,26)+'…':lab):'—')}</span>`;
  const t=lab||'Source';return `<a class="ext" href="${esc(url)}" target="_blank" rel="noopener" title="${esc(t)}">${esc(t.length>28?t.slice(0,26)+'…':t)}</a>`}
function srcChips(m){const ls=m.links||[];if(!ls.length)return m.fam?`<span class="mini">${esc(m.fam)}</span>`:'';
  return ls.map(x=>srcA(x.name,x.url)).join('<span class="mini"> · </span>')}
function metricOf(id){for(const d in SRC.dims){const m=SRC.dims[d].metrics.find(x=>x.id===id);if(m)return m}return null}
function seedSource(dim){
  const d=dim||srcOpen||'D1';
  const ms=((SRC.dims[d]||{}).metrics)||[];
  const hit=ms.find(m=>(SRC.obs[m.id]||[]).length)||ms[0]
    ||Object.values(SRC.dims).flatMap(x=>x.metrics||[]).find(m=>(SRC.obs[m.id]||[]).length);
  if(hit){srcSels=[hit.id];srcOpen=dimOfMetric(hit.id)}
}
function setSource(id){srcHit='';const i=srcSels.indexOf(id);if(i>=0)srcSels.splice(i,1);else srcSels.push(id);if(!srcSels.length)seedSource();render()}
function srcObs(id){return SRC.obs[id]||[]}
function srcBlockRows(id){
  const m=metricOf(id)||{},os=srcObs(id);
  const head=`<tr><td colspan="7" style="background:var(--soft);padding:7px 8px"><b style="font-size:12.5px">${esc(m.name||id)}</b> ${dcTag(m.dc)}${m.unit?` <span class="mini">${esc(m.unit)}</span>`:''} <span class="mini">· ${esc(id)} · latest <b class="num" style="color:var(--ink)">${esc(m.latest||'—')}</b> · ${os.length} obs</span><div class="mini" style="margin-top:3px">Sources ${srcChips(m)}</div></td></tr>`;
  if(!os.length)return head+`<tr><td colspan="7" class="mini">No observations</td></tr>`;
  return head+os.slice().reverse().map(o=>{
    const hit=srcHit&&((o.kt||'').slice(0,10)===srcHit||(o.kt||'').slice(0,7)===srcHit.slice(0,7)||(o.period||'').includes(srcHit.slice(0,7)));
    return `<tr class="${hit?'sel':''}"><td>${esc(o.period)}</td><td class="r num" style="font-weight:600">${esc(o.value)}</td><td><span class="mini">${OTYPE[o.otype]||o.otype}</span></td><td><span class="tier">${esc(o.prov)}</span></td><td>${srcA(o.src,o.url)}</td><td class="mini num">${esc(o.kt)}</td><td class="mini" style="color:var(--mut)">${linkify(o.note||'')}</td></tr>`}).join('');
}
function toggleDim(d){srcOpen=(srcOpen===d?null:d);render()}
const NUM=v=>{const m=(''+v).replace(/[,%]/g,'').match(/-?\d+(\.\d+)?/);return m?parseFloat(m[0]):null}
function lineChart(vals){if(vals.length<2)return '';const w=560,h=110,pad=10,mn=Math.min(...vals),mx=Math.max(...vals),rng=(mx-mn)||1;
 const pts=vals.map((v,i)=>[pad+i*(w-2*pad)/(vals.length-1),h-pad-(v-mn)/rng*(h-2*pad)]);
 const d=pts.map((p,i)=>(i?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' ');
 return `<svg viewBox="0 0 ${w} ${h}" width="100%" style="margin:4px 0 12px"><path d="${d}" fill="none" stroke="${cv('--ac')}" stroke-width="2"/>${pts.map(p=>`<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="2.6" fill="${cv('--ac')}"/>`).join('')}</svg>`}

function guideIds(){return(GUIDE[tab]||[]).map(it=>it.id)}
function guideHit(el){const id=el&&el.getAttribute('data-guide');return id&&guideIds().includes(id)?id:''}
function guideSpotInit(){if(window._guideSpotOn)return;window._guideSpotOn=1;
 const ref=()=>{if(guideOn&&guideFocus)positionGuideSpot()};
 window.addEventListener('resize',ref);window.addEventListener('scroll',ref,true);
 document.addEventListener('click',function(e){
  if(!guideOn||e.target.closest('#guide')||e.target.closest('.guide-btn')||e.target.closest('.tab'))return;
  const hit=guideHit(e.target.closest('[data-guide]'));
  if(hit){e.preventDefault();e.stopPropagation();setGuideFocus(hit);return}
  if(!guideFocus)return;
  const s=document.getElementById('guide-spot'),r=s&&s.getBoundingClientRect();
  if(!r)return;
  const x=e.clientX,y=e.clientY;
  if(x<r.left||x>r.right||y<r.top||y>r.bottom)setGuideFocus(guideFocus);
 },true)}
function clearGuideSpot(){document.body.classList.remove('guide-spot-on');clearGuideHL();const s=document.getElementById('guide-spot');if(s)s.style.display='none'}
function positionGuideSpot(){
 const el=guideFocus&&document.querySelector('[data-guide="'+guideFocus+'"]'),s=document.getElementById('guide-spot');
 if(!guideOn||!guideFocus||!el||!s){clearGuideSpot();return}
 const pad=6,r=el.getBoundingClientRect(),cs=getComputedStyle(el);
 const rad=cs.borderRadius&&cs.borderRadius!=='0px'?cs.borderRadius:'10px';
 s.style.top=(r.top-pad)+'px';s.style.left=(r.left-pad)+'px';s.style.width=(r.width+pad*2)+'px';s.style.height=(r.height+pad*2)+'px';s.style.borderRadius=rad;s.style.display='block';
 document.body.classList.add('guide-spot-on')}
function defaultGuideFocus(){const items=GUIDE[tab]||[];if(tab==='judge'&&judEK==='llm')return'jud-llm';return items.length?items[0].id:''}
function toggleGuide(){guideOn=!guideOn;guideFocus=guideOn?defaultGuideFocus():'';document.body.classList.toggle('guide-on',guideOn);clearGuideSpot();if(guideOn)guideSpotInit();renderGuide();render()}
function finishOnboard(openGuide){try{localStorage.setItem(ONBOARD_KEY,'1')}catch(e){}onboardStep=0;renderOnboard();if(openGuide&&!guideOn)toggleGuide()}
function onboardNext(){onboardStep=2;renderOnboard()}
function positionOnboardSpot(){
 const btn=document.getElementById('guide-btn'),spot=document.getElementById('onboard-spot'),tip=document.getElementById('onboard-tip');
 if(!btn||!spot||!tip||onboardStep!==2)return;
 const pad=8,r=btn.getBoundingClientRect();
 spot.style.display='block';spot.style.top=(r.top-pad)+'px';spot.style.left=(r.left-pad)+'px';spot.style.width=(r.width+pad*2)+'px';spot.style.height=(r.height+pad*2)+'px';
 btn.classList.add('onboard-pulse');
 const tw=tip.offsetWidth||300,th=tip.offsetHeight||160;
 let tx=r.left+ r.width/2 - tw/2,ty=r.bottom+14;
 if(tx<12)tx=12;if(tx+tw>innerWidth-12)tx=innerWidth-tw-12;
 if(ty+th>innerHeight-12)ty=r.top-th-14;
 tip.style.top=ty+'px';tip.style.left=tx+'px'}
function renderOnboard(){
 const root=document.getElementById('onboard');if(!root)return;
 document.body.classList.toggle('onboard-on',!!onboardStep);
 const btn=document.getElementById('guide-btn');if(btn)btn.classList.remove('onboard-pulse');
 if(!onboardStep){root.innerHTML='';root.classList.remove('on');return}
 root.classList.add('on');
 if(onboardStep===1){
  root.innerHTML=`<div class="onboard-mask"></div><div class="onboard-card" role="dialog" aria-modal="true">
   <div class="ot">Welcome to AI Monitoring System</div>
   <p class="ob">A four-layer dashboard for monitoring AI-linked holdings — from portfolio overview down to source data, judgment calls, and per-ticker evidence paths.</p>
   <div class="onboard-layers">
    <div class="onboard-layer"><b>Overview</b>Whole-portfolio view & weekly focus</div>
    <div class="onboard-layer"><b>Source</b>Metrics, provenance & observations</div>
    <div class="onboard-layer"><b>Judgment</b>Decision registry & outcomes</div>
    <div class="onboard-layer"><b>Results</b>Evidence graphs per holding</div>
   </div>
   <div class="onboard-actions"><button class="onboard-btn primary" onclick="onboardNext()">Continue</button></div>
  </div>`}
 else if(onboardStep===2){
  root.innerHTML=`<div class="onboard-mask" onclick="finishOnboard(false)"></div><div class="onboard-spot" id="onboard-spot"></div>
   <div class="onboard-tip" id="onboard-tip" role="dialog" aria-modal="true">
    <div class="ot">Try the module Guide</div>
    <p class="ob">Click <b>Guide</b> in the header anytime to spotlight each panel and read what it does. Click modules on the page or in the side panel to explore.</p>
    <div class="onboard-actions"><button class="onboard-btn" onclick="finishOnboard(false)">Skip for now</button><button class="onboard-btn primary" onclick="finishOnboard(true)">Open Guide</button></div>
   </div>`;
  requestAnimationFrame(()=>requestAnimationFrame(positionOnboardSpot))}}
function maybeOnboard(){if(onboardChecked)return;onboardChecked=true;try{if(localStorage.getItem(ONBOARD_KEY))return}catch(e){}onboardStep=1;renderOnboard()}
if(!window._onboardResize){window._onboardResize=1;window.addEventListener('resize',()=>{if(onboardStep===2)positionOnboardSpot()})}
function setGuideFocus(id){guideFocus=(guideFocus===id?'':id);renderGuide()}
function clearGuideHL(){}
function applyGuideHL(){clearGuideSpot();if(!guideOn||!guideFocus)return;guideSpotInit();
 const el=document.querySelector('[data-guide="'+guideFocus+'"]');if(!el)return;
 try{el.scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}
 requestAnimationFrame(()=>requestAnimationFrame(positionGuideSpot))}
function renderGuide(){
 const el=document.getElementById('guide');if(!guideOn){el.innerHTML='';clearGuideSpot();return}
 if(guideOn)guideSpotInit();
 const tabLab=(TABS.find(t=>t[0]===tab)||[,''])[1],items=GUIDE[tab]||[];
 let body='';
 if(items.length){body=items.map(it=>`<div class="guide-card ${guideFocus===it.id?'on':''}" onclick="setGuideFocus('${it.id}')"><div class="gr">${tabLab}</div><div class="gn">${it.title}</div><div class="gx"><b>What</b> ${it.what}<br><b>For</b> ${it.for}<br><b>When</b> ${it.when}</div></div>`).join('')}
 else{body=`<div class="guide-card on"><div class="gr">${tabLab}</div><div class="gn">No modules</div><div class="gx">Guide copy for this page is empty.</div></div>`}
 el.innerHTML=`<div class="guide-head"><div class="gt">Guide · ${tabLab}</div><a class="gd" href="${GUIDE_README}" target="_blank" rel="noopener">${svg(IC.ext,12)} Full write-up on GitHub</a><div class="gs">Click a module on the page or in this panel. Switch tabs to switch guides. Click dimmed area to clear.</div></div><div class="guide-body">${body}</div><div class="guide-foot">${items.length} modules · two-way spotlight</div>`;
 applyGuideHL();
 if(guideFocus){const card=el.querySelector('.guide-card.on');if(card)try{card.scrollIntoView({block:'nearest',behavior:'smooth'})}catch(e){}}}
function strengthUi(s){
 const m={弱:['Weak','st-weak'],中:['Medium','st-mid'],强:['Strong','st-strong'],Weak:['Weak','st-weak'],Medium:['Medium','st-mid'],Strong:['Strong','st-strong']};
 const x=m[s]||[s,''];return `<span class="sub">Strength <span class="${x[1]}">${x[0]}</span></span>`;}
// ---------- header ----------
function hdr(){
 const gKpi=GUIDE_TOP[tab]?` data-guide="${GUIDE_TOP[tab]}"`:'';
 let sum='';
 if(tab==='result'){const d=R.tickers[ticker];sum=`<div class="hsum"${gKpi}><span class="big num">${d.weight}%</span>${strengthUi(d.sizing.strength)}</div>`}
 else if(tab==='source'){sum=`<div class="hsum"${gKpi}><span class="big num">${C.metric_total}</span><span class="sub">Metrics · P1 ${C.p1_ratio}%</span></div>`}
 else if(tab==='judge'){sum=`<div class="hsum"${gKpi}><span class="big num">${J.log_outcome}/${J.log_total}</span><span class="sub dn">Outcome Backfill</span></div>`}
 else{sum=`<span class="mini hdr-kpi"${gKpi} style="color:var(--mut);white-space:nowrap;border-left:1px solid var(--line);padding-left:14px;margin-left:2px">Portfolio view</span>`}
 document.getElementById('hdr').innerHTML=`
  <div class="hdr-left"><div class="idc"><div class="nm">AI Monitoring System</div></div>${sum}</div>
  <div class="grow"></div>
  <button class="guide-btn ${guideOn?'on':''}" id="guide-btn" onclick="toggleGuide()">Guide</button>
  <div class="tabs">${TABS.map(t=>`<button class="tab ${tab===t[0]?'on':''}" onclick="settab('${t[0]}')">${t[1]}</button>`).join('')}</div>
  `;
}
function resetMm(){mmS=1;mmX=0;mmY=0}
function settab(t){tab=t;if(guideOn)guideFocus=defaultGuideFocus();if(t!=='result'){mmZ=0;resetMm();resFocus=null}if(t!=='source')srcHit='';render()}
function setTicker(t){if(!R.tickers[t])return;ticker=t;mmZ=0;resetMm();resFocus=null;render()}
function setMmZ(z){mmZ=z==null?(mmZ+1)%3:z;resetMm();render()}
function dimOfMetric(id){for(const d in SRC.dims){if((SRC.dims[d].metrics||[]).some(m=>m.id===id))return d}return srcOpen}
function goSource(id){tab='source';if(id){srcSels=[id];srcOpen=dimOfMetric(id);srcHit=''}render()}
function goSourceDim(d){tab='source';srcHit='';if(d)srcOpen=d;seedSource(srcOpen);render()}
function goResult(tk){tab='result';if(tk&&R.tickers[tk]){ticker=tk;mmZ=0;resetMm();resFocus=null}render()}
function firstTk(s){for(const p of String(s||'').split(/[\s/,]+/).filter(Boolean)){if(R.tickers[p]||R.positions[p]!=null)return p}return ''}
function metOfCal(e){
  const raw=(e.tk||'').trim(), ev=e.event||'', blob=raw+' '+ev;
  if(firstTk(e.tk)==='MU'||/Micron|美光/.test(blob))return ['m_tail_mu'];
  if(raw==='300308.SZ'||/中际旭创/.test(blob))return ['m_cn_optics_zte'];
  if(raw==='300502.SZ'||/新易盛/.test(blob))return ['m_cn_optics_eoptolink'];
  if(/capex|hyperscaler/i.test(blob))return ['m_hyperscaler_capex'];
  if(/海关/.test(blob))return ['m_cn_optics_customs'];
  if(firstTk(e.tk)==='FCEL'||/FuelCell|年化产能/.test(blob))return ['m_fcel_capacity'];
  return []}
function pickSrc(csv, date){
  const ids=String(csv||'').split(',').filter(id=>metricOf(id));if(!ids.length)return;
  srcSels=ids;srcOpen=dimOfMetric(ids[0]);srcHit=date||'';render()}
function pickRes(src, tk){
  src=src||'';tk=tk||'';
  if(tk&&R.tickers[tk])ticker=tk;
  else if(src){const has=t=>R.tickers[t]&&R.tickers[t].paths.some(p=>p.src===src);
    if(!has(ticker)){const hit=['NBIS','RBRK','STAA','FCEL','MU','SUPX','SNDK','INTC','CIEN','MRVL','POET','AMD'].find(has)||Object.keys(R.tickers).find(has);if(hit)ticker=hit}
    if(!(R.tickers[ticker]&&R.tickers[ticker].paths.some(p=>p.src===src)))src=''}
  resFocus=src||null;mmZ=0;resetMm();render()}
function goCal(e){
  const tk=firstTk(e.tk);if(tk)return `goResult('${tk}')`;
  const ids=metOfCal(e);if(ids.length)return `goSource('${ids[0]}')`;
  const dm=(e.dim||'').match(/D[1-7]/);if(dm)return `goSourceDim('${dm[0]}')`;
  return ''}
function feedRow(e){return `<div class="ln${e.go?' clk':''}${e.on?' sel':''}" ${e.go?`onclick="${e.go}"`:''}><span class="k num">${esc(e.d)}</span><span class="v">${e.t}${e.sub?`<div class="mini">${e.sub}</div>`:''}</span>${e.go?'<span class="mini" style="color:var(--ac);flex:none">View</span>':''}</div>`}
function wfRow(k,v,go,al){return `<div class="ln${al?' al':''}${go?' clk':''}" ${go?`onclick="${go}"`:''}><span class="k">${k}</span><span class="v">${v}</span>${go?'<span class="mini" style="color:var(--ac);flex:none">View</span>':''}</div>`}

// ---------- evidence graph (result) ----------
function chan(d,ch){let ps=d.paths.filter(p=>p.mechs.includes(ch)||p.src===ch||p.src_label===ch),label=ch,side='self';if(ps.length){side=ps[0].side;if(ch.startsWith('m_'))label=ps[0].src_label}return{n:ps.length,side,label}}
function wrapLab(s,n){s=String(s||'').replace(/["\[\]#<>&]/g,' ').replace(/\s+/g,' ').trim();
 if(s.length<=n)return s;
 const parts=s.split(/(\s*\/\s*|、)/);let lines=[],cur='';
 if(parts.length>1){parts.forEach(p=>{if(!cur)cur=p;else if((cur+p).length<=n+6)cur+=p;else{lines.push(cur.trim());cur=p}});if(cur)lines.push(cur.trim());
  return lines.filter(Boolean).slice(0,3).join('\\n')}
 const a=[];for(let i=0;i<s.length&&a.length<3;i+=n)a.push(s.slice(i,i+n));return a.join('\\n')+(s.length>n*3?'…':'')}
function nid(kind,s){let h=0,t=kind+'|'+s;for(let i=0;i<t.length;i++)h=(h*33+t.charCodeAt(i))>>>0;return kind+h.toString(36)}
function tree(tk){const d=R.tickers[tk];if(!d||!d.paths.length)return '<div class="mini">No paths in graph</div>';
 const SIDEG=[['supply','Supply'],['demand','Demand'],['regime','Regime'],['self','Entity'],['compete','Peers']];
 const tid=nid('t',tk),seen=new Set(),fan=[];
 const lines=['flowchart LR',
  '  classDef box fill:#fff,stroke:#111,stroke-width:1.2px,color:#111',
  '  classDef tk fill:#fff,stroke:#111,stroke-width:2px,color:#111'];
 SIDEG.forEach(([sd,lab],si)=>{const ps=d.paths.filter(p=>p.side===sd);if(!ps.length)return;
  lines.push(`  subgraph sg${si}["${lab}"]`,`    direction LR`);
  ps.forEach(p=>{const sid=nid('s',p.src);
    if(!seen.has(sid)){seen.add(sid);lines.push(`    ${sid}["${wrapLab(p.src_label,18)}"]`);}
   let prev=sid;
   (p.mechs||[]).forEach(m=>{const mid=nid('m',m);
    if(!seen.has(mid)){seen.add(mid);lines.push(`    ${mid}["${wrapLab(m,18)}"]`);}
    const e=prev+'-->'+mid;if(!seen.has(e)){seen.add(e);lines.push(`    ${prev} --> ${mid}`);}
    prev=mid;});
   const e=prev+'-->'+tid;if(!seen.has(e)){seen.add(e);fan.push(`  ${prev} --> ${tid}`);}});
  lines.push('  end');});
 lines.push(`  ${tid}["${wrapLab(tk,16)}"]`,...fan,`  class ${tid} tk;`);
 const src=lines.join('\n');
 const hint=['Thumbnail · click to expand','Medium · click again','Full · scroll to zoom · click backdrop to close'][mmZ];
 const body=`<div class="mmdh"${mmZ===2?' onclick="setMmZ(0)"':''}><span class="mini">Transmission Graph</span><span class="mini">${hint}</span></div><pre class="mermaid">${src}</pre>`;
 if(mmZ===2) return `<div class="mmdov" onclick="setMmZ(0)"><div class="mmd" onclick="event.stopPropagation()">${body}</div></div><div class="mmd mmd-0 mmd-ph"></div>`;
 return `<div class="mmd mmd-${mmZ}" onclick="setMmZ()" title="${hint}">${body}</div>`}
function mmInit(){if(!window.mermaid||window._mmOn)return;
 mermaid.initialize({startOnLoad:false,securityLevel:'loose',theme:'base',
  themeVariables:{primaryColor:'#fff',primaryTextColor:'#111',primaryBorderColor:'#111',lineColor:'#111',
   secondaryColor:'#fff',tertiaryColor:'#fafbfc',clusterBkg:'#fafbfc',clusterBorder:'#888',
   edgeLabelBackground:'#fff',fontFamily:'Inter,PingFang SC,sans-serif',fontSize:'12px'},
  flowchart:{htmlLabels:true,curve:'linear',padding:8,nodeSpacing:28,rankSpacing:52,useMaxWidth:true}});
 window._mmOn=1}
function fitMmSvg(n){const svg=n.querySelector('svg');if(!svg)return;svg.removeAttribute('width');svg.removeAttribute('height');svg.style.maxWidth='100%';svg.style.maxHeight='100%';svg.style.width='auto';svg.style.height='auto'}
function applyMm(n){const svg=n.querySelector('svg');if(!svg)return;svg.style.transformOrigin='0 0';svg.style.transform=`translate(${mmX}px,${mmY}px) scale(${mmS})`}
function bindMm(n){fitMmSvg(n);applyMm(n);
 n.addEventListener('wheel',function(e){e.preventDefault();e.stopPropagation();
  const r=n.getBoundingClientRect(),cx=e.clientX-r.left,cy=e.clientY-r.top,old=mmS||1;
  const next=Math.min(6,Math.max(.4,old*(e.deltaY<0?1.12:1/1.12)));
  mmX=cx-(cx-mmX)*(next/old);mmY=cy-(cy-mmY)*(next/old);mmS=next;applyMm(n);},{passive:false});
 let drag=null;
 n.addEventListener('pointerdown',function(e){if(e.button!==0)return;e.stopPropagation();
  drag={x:e.clientX,y:e.clientY,ox:mmX,oy:mmY,moved:0};n.classList.add('grabbing');try{n.setPointerCapture(e.pointerId)}catch(err){}});
 n.addEventListener('pointermove',function(e){if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>3)drag.moved=1;mmX=drag.ox+dx;mmY=drag.oy+dy;applyMm(n)});
 n.addEventListener('pointerup',function(e){const moved=drag&&drag.moved;drag=null;n.classList.remove('grabbing');if(moved){e.preventDefault();e.stopPropagation()}});
 n.addEventListener('pointercancel',function(){drag=null;n.classList.remove('grabbing')})}
function paintMermaid(){mmInit();const nodes=[...document.querySelectorAll('.mmd .mermaid')];if(!nodes.length||!window.mermaid)return;
 const run=mermaid.run({nodes});const after=()=>nodes.forEach(bindMm);if(run&&run.then)run.then(after);else after()}

function heatGrid(cols, rows){
  let mx=1; rows.forEach(r=>r.c.forEach(v=>{if(v>mx)mx=v}));
  let h=`<div class="heat"><div></div>${cols.map(x=>`<div class="hc mut">${x}</div>`).join('')}`;
  rows.forEach(r=>{h+=`<div class="hl">${r.l}</div>`+r.c.map(v=>`<div class="hc" style="background:${v?`rgba(91,91,214,${0.12+0.6*v/mx})`:'var(--line2)'};color:${v/mx>0.5?'#fff':'var(--cap)'}">${v||''}</div>`).join('')});
  return h+'</div>';
}
function layerFeed(intro, sub, evs){
  return `<div style="font-size:12px;color:var(--cap)">${intro}</div>
     <div style="font-weight:700;font-size:11px;color:var(--mut);margin:11px 0 4px">${sub}</div>
     ${evs.map(feedRow).join('')}`;
}
function topCards(lt, lr, heat, cap, rt, rr, intro, sub, evs, gidL, gidR){
  const gL=gidL?` data-guide="${gidL}"`:'';const gR=gidR?` data-guide="${gidR}"`:'';
  return `<div class="panel"${gL}><div class="ph"><span class="t">${lt}</span><span class="r">${lr}</span></div>
    <div class="pb">${heat}<div class="mini" style="margin-top:8px">${cap}</div></div></div>
   <div class="panel"${gR}><div class="ph"><span class="t">${rt}</span><span class="r">${rr}</span></div>
    <div class="pb">${layerFeed(intro, sub, evs)}</div></div>`;
}

// ---------- toprow per tab ----------
function toprow(){let h='';
 if(tab==='result'){const d=R.tickers[ticker],kf=R.keyfact[ticker]||{},my=R.divergence.filter(x=>d.paths.some(p=>p.src===x.metric));
  const rows=[['supply','Supply'],['demand','Demand'],['regime','Regime'],['self','Entity'],['compete','Peers']].map(([sd,lab])=>{
    const ps=d.paths.filter(p=>p.side===sd);
    return {l:lab,c:[ps.filter(p=>p.tier==='T1').length,ps.filter(p=>p.tier==='T2').length,ps.filter(p=>p.tier==='T3').length,ps.filter(p=>p.dominant==='预警').length]};
  });
  const evs=my.map(x=>({d:(x.date||'').slice(5),t:esc(MLAB[x.metric]||x.metric),sub:'Shock',go:x.metric?`pickRes('${x.metric}')`:'',on:resFocus===x.metric}))
    .concat(C.upcoming.map(e=>{const tk=firstTk(e.tk),ids=metOfCal(e),src=tk?'':(ids[0]||'');
      return {d:e.date.slice(5),t:esc(e.event),sub:esc(e.tk||e.dim||''),go:tk?`pickRes('','${tk}')`:(src?`pickRes('${src}')`:''),on:tk?(ticker===tk&&!resFocus):resFocus===src}}));
  h=topCards('Evidence Coverage',`${d.independent}/${d.raw} independent`,heatGrid(['T1','T2','T3','Alert'],rows),'Paths by side × tier · darker = denser',
    'Signals & Catalysts',`Updated ${C.etl_last}`,kf.status_line||`${ticker} · ${d.raw} paths · ${d.independent} independent`,'ACTIVE',evs,'res-coverage','res-signals');
 } else if(tab==='source'){
  const dl={D1:'Compute',D2:'Data',D3:'Capital',D4:'Talent',D5:'Frontier',D6:'Token',D7:'Policy'};
  const rows=['D1','D3','D5','D6','D7','D2'].map(dm=>{const row=C.heat[dm]||{},g=k=>row[k]||0;
    return {l:`${dm} ${dl[dm]||''}`,c:[g('1')+g('1/3'),g('2')+g('2/3'),g('3'),g('4')]}});
  h=topCards('Dimension Coverage',`${C.cov_exist}/${C.cov_total} in DB`,heatGrid(['T1','T2','T3','Frontier'],rows),'Metrics by dimension × certainty · darker = denser',
    'Data Calendar',`Updated ${C.etl_last}`,'D1–D7 source layer · quant / event / view / frontier observations','EVENTS',
    C.upcoming.map(e=>{const ids=metOfCal(e);
      return {d:e.date.slice(5),t:esc(e.event),sub:esc([e.dim,e.tk].filter(Boolean).join(' · ')),go:ids.length?`pickSrc('${ids.join(',')}','${e.date||''}')`:'',on:ids.length>0&&ids.every(id=>srcSels.includes(id))&&srcSels.length===ids.length}}),'src-dimension','src-calendar');
 } else if(tab==='judge'){
  const CALS=[['human','Human'],['shadow','Shadow'],['assisted','Assisted'],['auto','Auto']];
  const rowsH=Object.keys(TG).map(g=>{const ids=TG[g],rs=J.registry.filter(r=>ids.includes(r.id));
    return {l:GL[g]||g,c:CALS.map(([k])=>rs.filter(r=>r.calib===k).length)}});
  const nRule=C.exec.rule||0,nHum=C.exec.human||0,nRev=C.review_due||0;
  const cards=`<div class="scrow">
    <div class="scard" onclick="setJudEK('rule')"><div class="n num">${nRule}</div><div class="l">Rule</div></div>
    <div class="scard" onclick="setJudEK('human')"><div class="n num">${nHum}</div><div class="l">Human</div></div>
    <div class="scard" onclick="setJudEK('human')"><div class="n num" style="color:${nRev?'var(--warn)':''}">${nRev}</div><div class="l">Review Queue</div></div></div>`;
  const evs=[];
  (R.divergence||[]).forEach(x=>{
    const lab=MLAB[x.metric]||x.metric, why=esc((x.detail||'').replace(/^!\s*/,'').trim());
    const kind=x.metric==='m_cost_per_token'?'Falsifier':'Shock';
    evs.push({d:(x.date||'').slice(5), t:`${esc(lab)}${why?` · ${why}`:''}`, sub:kind, go:`goSource('${x.metric}')`});
  });
  (C.upcoming||[]).forEach(e=>{
    evs.push({d:e.date.slice(5), t:esc(e.event), sub:esc([e.dim,e.tk].filter(Boolean).join(' · ')), go:goCal(e)});
  });
  h=`<div class="panel" data-guide="jud-coverage"><div class="ph"><span class="t">Decision Coverage</span><span class="r">${C.dec_outcome}/${C.dec_total} outcomes</span></div>
    <div class="pb">${heatGrid(CALS.map(x=>x[1]),rowsH)}<div class="mini" style="margin-top:8px">Decision types by group × calibration · darker = denser</div></div></div>
   <div class="panel" data-guide="jud-exec"><div class="ph"><span class="t">Execution & Signals</span><span class="r">Updated ${C.etl_last}</span></div>
    <div class="pb">${cards}<div style="font-weight:700;font-size:11px;color:var(--mut);margin:2px 0 4px">SIGNALS & CATALYSTS</div>${evs.map(feedRow).join('')}</div></div>`;
 } else { // overview
  const mx=Math.max(...R.book.filter(b=>b.n_tk>=2).map(b=>b.weight));
  h=`<div class="panel" data-guide="ov-shared"><div class="ph"><span class="t">Shared Exposure</span><span class="r">Portfolio exposure</span></div><div class="pb">
     ${R.book.filter(b=>b.n_tk>=2).sort((a,b)=>b.weight-a.weight).slice(0,4).map(b=>`<div class="bar"><span class="bl">${MLAB[b.node]||b.node}</span><div class="bt ${b.disconnected&&b.disconnected.length?'risk':''}"><i style="width:${(b.weight/mx*100)|0}%"></i></div><span class="bp num">${b.weight.toFixed(0)}%</span></div>`).join('')}
     <div class="mini" style="margin-top:8px">% of portfolio if upstream node breaks · shared across holdings</div></div></div>
   <div class="panel" data-guide="ov-weekly"><div class="ph"><span class="t">Weekly Focus</span><span class="r clk" style="color:var(--ac);font-weight:600" onclick="settab('result')">View Signals ›</span></div><div class="pb">
     ${wfRow('Alert','FCEL divergence · revenue <span class="num">−29%</span> · 75MW pending',`goResult('FCEL')`,1)}
     ${wfRow('Portfolio','NBIS 51% · covered · RBRK 30% · thin · FCEL 7% · narrow · STAA 8% · no graph',`goResult('NBIS')`)}
     ${wfRow('Events','<span class="num">09-30</span> MU · <span class="num">10-28</span> Hyperscaler capex · <span class="num">10-31</span> FCEL capacity',`settab('source')`)}
     ${wfRow('Mandate','<span class="mut">Reorder attention only · sizing unchanged</span>',`settab('judge')`)}
   </div></div>`;
 }
 document.getElementById('toprow').innerHTML=h;
}

// ---------- rail per tab ----------
function grp(color,title,cnt,items){return `<div class="grp"><div class="gh" style="color:var(${color})">${title}<span class="cnt">${cnt}</span></div>${items}</div>`}
function rail(){let sel='',cats='',body='';
 const catRow=`<div class="cats">${['search','db','chart','cpu','grid'].map((c,i)=>`<div class="cat ${i==0?'on':''}">${svg(IC[c],15)}</div>`).join('')}</div>`;
 if(tab==='result'){
  const live=t=>R.tickers[t];
  const core=['NBIS','RBRK','STAA','FCEL'].filter(live);
  const tail=['SUPX','SNDK','MU','INTC','CIEN','MRVL','POET','AMD'].filter(live);
  const pot=['CRWV'].filter(live);
  const row=(t,ico)=>`<div class="item ${ticker===t?'on':''}" onclick="setTicker('${t}')">${ico?`<span class="ico">${svg(IC.chart,13)}</span>`:''}${t}<span class="w num">${R.positions[t]!=null?(R.positions[t]+'%'):'Not held'}</span></div>`;
  body=grp('--ac','Core Holdings',core.length,core.map(t=>row(t,1)).join(''))
    +(pot.length?grp('--pp','Watchlist',pot.length,pot.map(t=>row(t,0)).join('')):'')
    +grp('--mut','Tail Positions',tail.length,tail.map(t=>row(t,0)).join(''));
 } else if(tab==='source'){
  sel = srcSels.length ? srcSels.map(id=>`<span class="schip" onclick="setSource('${id}')">${(metricOf(id)||{}).name||id}<span class="x">×</span></span>`).join('') : 'No series selected';
  const order=['D1','D2','D3','D4','D5','D6','D7'];
  const total=Object.values(SRC.dims).reduce((a,d)=>a+d.metrics.length,0);
  const flt=m=>(srcDC==='all'||(m.dc||'—')[0]===srcDC)&&(!q||m.name.includes(q));
  const dimhtml=order.filter(d=>SRC.dims[d]).map(d=>{const dd=SRC.dims[d];const ms=dd.metrics.filter(flt);const open=(srcOpen===d)||(!!q&&ms.length>0);
    if(q&&!ms.length)return '';
    const items=open?ms.map(m=>`<div class="item ${srcSels.includes(m.id)?'on':''}" onclick="setSource('${m.id}')" title="${m.name}"><span class="ico">${svg(IC.chart,12)}</span><span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${m.name}</span> ${dcTag(m.dc)}<span class="c">${m.n}</span></div>`).join(''):'';
    return `<div class="grp"><div class="gh" style="color:var(--bl);cursor:pointer" onclick="toggleDim('${d}')"><span style="display:inline-block;transform:rotate(${open?90:0}deg)">${svg(IC.chev,11)}</span> ${d} ${dd.label}<span class="cnt">${ms.length}</span></div>${items}</div>`}).join('');
  body=`<div class="grp"><div class="gh" style="color:var(--ac)">Source Metrics<span class="cnt">${total}</span></div></div>`+dimhtml;
 } else if(tab==='judge'){
  sel = judType ? ('Drill: '+((J.registry.find(r=>r.id===judType)||{}).name||judType)) : (judEK==='llm'?'LLM Monitor':'Decision Filters');
  const owners=[...new Set(J.registry.map(r=>r.owner).filter(Boolean))].sort();
  const cbox=on=>`<span class="ico">${on?'☑':'☐'}</span>`;
  const ekRow=[['all','All',12],['rule','Rule',J.dist_executor.rule||0],['human','Human',J.dist_executor.human||0],['llm','LLM',J.dist_executor.llm||0],['model','Model',J.dist_executor.model||0]]
    .map(([k,l,n])=>`<div class="item ${judEK===k?'on':''} ${k==='model'?'dis':''}" ${k==='model'?'':`onclick="setJudEK('${k}')"`}>${l}${k==='llm'?' <span class="tier" style="border-color:var(--am);color:var(--am)">demo</span>':''}<span class="c">${n}${(k==='llm'||k==='model')&&n===0?' · off':''}</span></div>`).join('');
  const calRow=[['human','Human'],['shadow','Shadow'],['assisted','Assisted'],['auto','Auto']].map(([k,l])=>`<div class="item" onclick="togS(fCal,'${k}')">${cbox(fCal.has(k))}${l}<span class="c">${J.dist_calib[k]||0}</span></div>`).join('');
  const tierRow=['A','B','C','—'].map(t=>`<span class="tg" style="${fTier.has(t)?'border-color:var(--ac);color:var(--ac)':''}" onclick="togS(fTier,'${t}')">${t}</span>`).join(' ');
  const grpRow=Object.keys(TG).map(g=>`<div class="item" onclick="togS(fGrp,'${g}')">${cbox(fGrp.has(g))}${GL[g]||g}<span class="c">${TG[g].length}</span></div>`).join('');
  const ownRow=owners.map(o=>`<span class="tg" style="${(fOwner.size===0||fOwner.has(o))?'border-color:var(--ac);color:var(--ac)':''}" onclick="togS(fOwner,'${o}')">${o}</span>`).join(' ');
  body=`<div class="grp"><div class="gh" style="color:var(--ac)">Executor<span class="cnt">single</span></div>${ekRow}</div>
   <div class="grp"><div class="gh" style="color:var(--bl)">Calibration Stage</div>${calRow}</div>
   <div class="grp"><div class="gh" style="color:var(--bl)">Research Tier</div><div style="padding:6px 14px">${tierRow}</div></div>
   <div class="grp"><div class="gh" style="color:var(--bl)">Decision Groups</div>${grpRow}</div>
   <div class="grp"><div class="gh" style="color:var(--bl)">Owner</div><div style="padding:6px 14px">${ownRow}</div></div>`;
 } else {
  sel='Portfolio View';body=grp('--ac','Views',4,TABS.map(t=>`<div class="item ${tab===t[0]?'on':''}" onclick="settab('${t[0]}')">${t[1]}</div>`).join(''));
 }
 const gRail=GUIDE_RAIL[tab]?` data-guide="${GUIDE_RAIL[tab]}"`:'';
 document.getElementById('rail').innerHTML=`
  <div class="legend"${gRail}><div class="lh"><span>LEGEND</span><span class="mini">${tab==='source'?'Multi-select metrics':'Select from left rail'}</span></div>${tab==='result'?'':`<div class="sel${tab==='source'&&srcSels.length?' multi':''}">${sel}</div>`}</div>
  <div class="search">${svg(IC.search,14)}<input placeholder="Search (Enter)…" value="${q}" onchange="setQ(this.value)"></div>
  ${body}`;
}

// ---------- control bar per tab ----------
function ctrl(){let h='';
 if(tab==='source'){const dc=[['all','All'],['1','Quant'],['2','Event'],['3','View'],['4','Frontier']];
   h=`<div class="seg">${dc.map(([k,l])=>`<button class="${srcDC===k?'on':''}" onclick="setSrcDC('${k}')">${l}</button>`).join('')}</div><span class="mini">Filter by data class · multi-select metrics · observations on right</span>`;}
 else if(tab==='judge'){h=`<span class="mini">Filter left rail · click type for instances · LLM executor for monitor mode</span>`;}
 else if(tab==='result'){h=`<span class="mini">Select ticker · Transmission graph · Path table</span>`;}
 else {h=`<span class="mini">Portfolio Overview · Holdings Coverage · Data Calendar · KPI</span>`;}
 const ctrlEl=document.getElementById('ctrl');ctrlEl.innerHTML=h;
 const gCtrl=GUIDE_CTRL[tab];if(gCtrl)ctrlEl.setAttribute('data-guide',gCtrl);else ctrlEl.removeAttribute('data-guide');
}

// ---------- stage per tab ----------
function stage(){let h='';
 if(tab==='result'){const d=R.tickers[ticker];
  let ch=d.mincut.map(c=>({c,...chan(d,c)}));const choke=ch.filter(x=>x.n>=2).sort((a,b)=>b.n-a.n)[0];
  const SIDEG=[['supply','Supply','--f1'],['demand','Demand','--f2'],['regime','Regime','--f5'],['self','Entity','--fg'],['compete','Peers','--pp']];
  let rows='';
  SIDEG.forEach(([sd,lab,col])=>{const ps=d.paths.filter(p=>p.side===sd&&(!resFocus||p.src===resFocus)).sort((a,b)=>b.tradable-a.tradable);if(!ps.length)return;
    rows+=`<tr><td colspan="6" style="background:var(--soft);padding:6px 8px"><span class="dot" style="background:var(${col})"></span><b style="font-size:11px">${lab}</b> <span class="mini">${ps.length} paths</span></td></tr>`;
    rows+=ps.map(p=>{const chain=p.mechs.length?p.mechs.map(m=>`<span class="mk">${m}</span>`).join(' <span class="mut">→</span> '):'<span class="mut">Direct</span>';
      const dom={可交易:'Tradable',预警:'Warning',待定:'Pending'}[p.dominant]||p.dominant;
      return `<tr class="${resFocus===p.src?'sel':''}"><td style="font-weight:600">${p.src_label}</td><td style="color:var(--cap)">${chain} <span class="mini">·${p.hops} hop</span></td><td class="r num">${p.tradable.toFixed(2)}</td><td class="r num">${p.warning.toFixed(2)}</td><td><span class="tier">${p.tier}</span></td><td><span class="dom ${p.dominant}">${dom}</span></td></tr>`}).join('')});
  h=`<div data-guide="res-structure"><div class="mini" style="margin-bottom:2px">Evidence Structure${resFocus?` · filtered ${esc(MLAB[resFocus]||resFocus)} <span class="clk" style="color:var(--ac)" onclick="pickRes('')">Show all</span>`:''}</div>
   <div style="font-size:12.5px;margin-bottom:8px"><b class="num">${d.raw}</b> paths → <b class="num">${d.independent}</b> independent${choke?` · min-cut <b>${esc(choke.label)}</b> (fan-in ${choke.n})`:''}</div></div>
   <div data-guide="res-graph">${tree(ticker)}</div>
   <div data-guide="res-paths"><table><thead><tr><th>Source Signal</th><th>Chain → ${ticker}</th><th class="r">Tradable</th><th class="r">Warning</th><th>Tier</th><th>Dominant</th></tr></thead><tbody>${rows||'<tr><td colspan="6" class="mini">No paths for this filter</td></tr>'}</tbody></table></div>`;
 } else if(tab==='source'){
  if(!srcSels.length)seedSource();
  const nObs=srcSels.reduce((a,id)=>a+srcObs(id).length,0);
   h=`<div data-guide="src-obs"><div class="mini" style="margin-bottom:8px">Selected <b class="num" style="color:var(--ink)">${srcSels.length}</b> metrics · <b class="num" style="color:var(--ink)">${nObs}</b> observations</div>
     <table><thead><tr><th>Period</th><th class="r">Value</th><th>Type</th><th>Provenance</th><th>Source</th><th>Known</th><th>Notes</th></tr></thead><tbody>${srcSels.map(srcBlockRows).join('')}</tbody></table></div>`;
 } else if(tab==='judge'){
  if(judEK==='llm'){h=`<div data-guide="jud-llm">${renderLLM()}</div>`;}
  else{const rows=judRows();
   h=`<div data-guide="jud-registry"><div class="mini" style="margin-bottom:6px">Decision Registry · <b class="num" style="color:var(--ink)">${rows.length}</b>/12 matched · click row for instances</div>
    <table><thead><tr><th>Decision Type</th><th>Executor</th><th>Calibration</th><th>Tier</th><th class="r">Logs</th><th class="r">Outcome</th></tr></thead><tbody>
    ${rows.map(r=>{const ag=J.logagg[r.id]||{n:0,outcome:0};
     return `<tr class="clk ${judType===r.id?'sel':''}" onclick="setJudType('${r.id}')"><td style="font-weight:600">${r.name}<div class="mini">${r.id} · view instances</div></td><td><span class="ekb ek-${r.ek}">${r.ek==='rule'?'Rule':'Human'}</span></td><td>${lad(r.calib)}</td><td><span class="tier">${r.tier||'—'}</span></td><td class="r num">${ag.n}</td><td class="r num" style="color:${ag.outcome?'var(--up)':'var(--mut)'}">${ag.outcome}</td></tr>`}).join('')||'<tr><td colspan=6 class="mini">No match · adjust filters</td></tr>'}
    </tbody></table></div>`;
   if(judType)h+=`<div data-guide="jud-instances">${judDrill(judType)}</div>`;}
 } else {
  const rows=Object.entries(R.positions).map(([t,w])=>{const d=R.tickers[t];return {t,w,ind:d?d.independent:0,raw:d?d.raw:0,live:!!d}}).sort((a,b)=>b.w-a.w);
  const big=rows.filter(r=>r.w>=1), tail=rows.filter(r=>r.w<1);
  if(tail.length) big.push({t:'Tail',w:+tail.reduce((a,r)=>a+r.w,0).toFixed(2),ind:tail.reduce((a,r)=>a+r.ind,0),raw:tail.reduce((a,r)=>a+r.raw,0),live:false});
  const mxW=Math.max(...big.map(r=>r.w),1), mxI=Math.max(...big.map(r=>r.ind),1);
  const today=new Date('2026-09-21');
  const cal=C.upcoming.map(e=>{
    const days=Math.max(0,Math.round((new Date(e.date)-today)/86400000));
    const tk=firstTk(e.tk), ids=metOfCal(e);
    const go=tk?`goResult('${tk}')`:(ids[0]?`goSource('${ids[0]}')`:'');
    return `<div class="ln${go?' clk':''}" ${go?`onclick="${go}"`:''}><span class="k num">${e.date.slice(5)}</span><span class="v">${esc(e.event)}<div class="mini">T+${days}d${tk?` · ${tk}`:(ids[0]?' · Source':` · ${esc(e.dim||'')}`)}</div></span></div>`;
  }).join('');
  h=`<div class="ovgrid">
    <div class="kcard" data-guide="ov-holdings"><div class="kh"><span class="t">Holdings Coverage</span><span class="tg clk" onclick="settab('result')">View Results</span></div><div class="kb">
      <div class="ovrow"><span class="ovhd"></span><span class="ovhd">Weight</span><span></span><span class="ovhd">Evidence</span><span class="ovhd">Paths</span></div>
      ${big.map(r=>`<div class="ovrow${r.live?' clk':''}" ${r.live?`onclick="goResult('${r.t}')"`:''}><span class="ovtk" style="${r.live?'':'color:var(--mut)'}">${r.t}</span><div class="ovb"><i class="w" style="width:${(r.w/mxW*100).toFixed(0)}%"></i></div><span class="num">${r.w}%</span><div class="ovb"><i class="e" style="width:${(r.ind/mxI*100).toFixed(0)}%;opacity:${r.live?1:.35}"></i></div><span class="num">${r.live?r.ind+'/'+r.raw:'—'}</span></div>`).join('')}
      <div class="mini" style="margin-top:8px">Weight vs independent evidence paths · grey = position without graph</div>
    </div></div>
    <div class="kcard" data-guide="ov-calendar"><div class="kh"><span class="t">Data Calendar</span><span class="tg">${C.upcoming.length} events</span></div><div class="kb">${cal}</div></div>
   </div>
   <div class="ovstat" data-guide="ov-kpi">
    <div class="kcard clk" onclick="settab('source')"><div class="mini">Metric Coverage</div><div class="num" style="font-size:20px;font-weight:700">${C.metric_green}/${C.metric_total}</div><div class="ovb" style="margin-top:6px"><i class="e" style="width:${Math.round(100*C.metric_green/C.metric_total)}%"></i></div></div>
    <div class="kcard clk" onclick="settab('source')"><div class="mini">Primary Source</div><div class="num" style="font-size:20px;font-weight:700">${C.p1_ratio}%</div><div class="ovb" style="margin-top:6px"><i class="e" style="width:${C.p1_ratio}%"></i></div></div>
    <div class="kcard clk" onclick="settab('judge')"><div class="mini">Review Queue</div><div class="num" style="font-size:20px;font-weight:700;color:var(--warn)">${C.review_due}</div><div class="mini" style="margin-top:6px">P2–P5</div></div>
    <div class="kcard clk" onclick="settab('judge')"><div class="mini">Outcome Backfill</div><div class="num" style="font-size:20px;font-weight:700">${C.dec_outcome}/${C.dec_total}</div><div class="ovb" style="margin-top:6px"><i class="w" style="width:${Math.round(100*C.dec_outcome/Math.max(1,C.dec_total))}%"></i></div></div>
   </div>`;
 }
 document.getElementById('stage').innerHTML=h;
}
function render(){hdr();toprow();rail();ctrl();stage();paintMermaid();renderGuide();if(onboardStep===2)requestAnimationFrame(positionOnboardSpot);maybeOnboard()}
render();
</script></body></html>"""
html=TPL.replace("__R__",json.dumps(R,ensure_ascii=False)).replace("__J__",json.dumps(J,ensure_ascii=False)).replace("__C__",json.dumps(C,ensure_ascii=False)).replace("__S__",json.dumps(SD,ensure_ascii=False))
open(os.path.join(S,"panel_full.html"),"w",encoding="utf-8").write(html)
print("wrote panel_full.html",len(html))
