# -*- coding: utf-8 -*-
"""源数据 exporter:metric_registry 按维度分组 + 每指标的真实观测(stg_observation)。
供源数据 tab 点某指标 → 出元信息 + 观测表。每条观测带 source 名/URL，指标头带来源芯片。"""
import duckdb, json, re

c = duckdb.connect("anatole_ai_monitor.duckdb", read_only=True)
DL = {"D1": "算力", "D2": "数据", "D3": "资本", "D4": "人才", "D5": "能力前沿", "D6": "token经济", "D7": "政策能源"}
URL_RE = re.compile(r"https?://[^\s）;；,，<>\"']+")

def split_src(s):
    s = s or ""
    m = URL_RE.search(s)
    if not m:
        return s.strip(), ""
    url = m.group(0).rstrip(").,;；]")
    name = (s[:m.start()] + s[m.end():]).strip(" ；;（()）")
    return name, url

fct_url = {}
for t in ("fct_quant", "fct_event", "fct_opinion", "fct_frontier"):
    for rid, url in c.execute(f"select record_id, source_url from {t} where source_url is not null").fetchall():
        if url:
            fct_url[rid] = url

sm = {}
for sid, name, url, access, tier in c.execute(
        "select source_id, name, url, access, source_tier from source_master").fetchall():
    sm[sid] = dict(name=name or sid, url=url or "", access=access or "", tier=tier or "")

obs = {}
for rid, mid, period, value, otype, prov, kt, note, source in c.execute(
        "select record_id,metric_id,period,value,obs_type,provenance,cast(knowledge_time as varchar),note,source "
        "from stg_observation order by knowledge_time").fetchall():
    name, url = split_src(source)
    if not url:
        url = fct_url.get(rid, "")
    obs.setdefault(mid, []).append(dict(
        period=period or "", value=value or "", otype=otype or "",
        prov=prov or "", kt=(kt or "")[:10], note=(note or "")[:140],
        src=name[:80], url=url))
for k in obs:
    obs[k] = obs[k][-30:]

dims = {}
n_link = 0
for mid, name, dim, dc, unit, fam, sids in c.execute(
        "select metric_id,name,dim,data_class,unit,source_family,source_ids from metric_registry").fetchall():
    pd = (dim or "—").split("/")[0]
    d = dims.setdefault(pd, {"label": DL.get(pd, ""), "metrics": []})
    latest = ""
    rows = obs.get(mid, [])
    if rows:
        acts = [o for o in rows if o["otype"] == "actual"]
        latest = (acts[-1]["value"] if acts else rows[-1]["value"])
    links, seen = [], set()
    try:
        ids = json.loads(sids or "[]")
    except json.JSONDecodeError:
        ids = []
    for sid in ids:
        src = sm.get(sid)
        if not src:
            continue
        key = src["url"] or sid
        if key in seen:
            continue
        seen.add(key)
        links.append(dict(name=src["name"], url=src["url"]))
    for o in rows:
        if o["url"] and o["url"] not in seen:
            seen.add(o["url"])
            links.append(dict(name=o["src"] or "原文", url=o["url"]))
    fam_disp = URL_RE.sub("", fam or "").strip(" ；;")
    if any(x.get("url") for x in links):
        n_link += 1
    d["metrics"].append(dict(id=mid, name=name or mid, dc=(dc or "—"), unit=unit or "",
                             fam=fam_disp, n=len(rows), latest=latest, links=links))

out = dict(dims=dims, obs=obs)
json.dump(out, open("source_data.json", "w"), ensure_ascii=False)
print("source exported:", {k: len(v["metrics"]) for k, v in sorted(dims.items())},
      "· obs metrics", len(obs), "· metrics with url", n_link)
