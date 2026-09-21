# -*- coding: utf-8 -*-
"""判断层数据 exporter:从 DB 生成 judgment_layer_data.json(登记表/实例/分布)。"""
import duckdb, json

DB = "anatole_ai_monitor.duckdb"
con = duckdb.connect(DB, read_only=True)


def short(x, n=120):
    x = x or ""
    return x if len(x) <= n else x[:n] + "…"


reg = [dict(id=r[0], name=r[1], q=r[2], ek=r[3], ex=r[4], calib=r[5], tier=r[6], freq=r[7], owner=r[8], status=r[9])
       for r in con.execute("select decision_id,name,question,executor_kind,executor,calib_status,research_tier,freq_est,owner,status from decision_registry order by decision_id").fetchall()]

agg = {}
for r in con.execute("""select decision_id, count(*), avg(confidence),
    sum(case when outcome is not null and outcome!='' then 1 else 0 end)
    from decision_log group by 1""").fetchall():
    agg[r[0]] = dict(n=r[1], conf=(round(r[2], 2) if r[2] else None), outcome=r[3])

ek = dict(con.execute("select coalesce(executor_kind,'?'),count(*) from decision_registry group by 1").fetchall())
cal = dict(con.execute("select coalesce(calib_status,'?'),count(*) from decision_registry group by 1").fetchall())
tot = con.execute("select count(*), sum(case when outcome is not null and outcome!='' then 1 else 0 end), avg(confidence) from decision_log").fetchone()

inst = {}
for r in con.execute("""select decision_id,dec_id,target_table,target_pk,target_column,state_anchor,
    choice,confidence,executor_kind,executor,basis,outcome,outcome_at,decided_at
    from decision_log order by decision_id, decided_at""").fetchall():
    inst.setdefault(r[0], []).append(dict(
        dec=r[1], target=" ".join(x for x in [r[2], r[3], r[4]] if x),
        anchor=short(r[5], 80), choice=short(r[6], 60), conf=r[7], ek=r[8], ex=r[9],
        basis=short(r[10], 120), outcome=(r[11] or ""),
        outcome_at=(str(r[12]) if r[12] else ""), at=(str(r[13])[:10] if r[13] else "")))

out = dict(registry=reg, logagg=agg, dist_executor=ek, dist_calib=cal,
           log_total=tot[0], log_outcome=tot[1], log_conf=(round(tot[2], 2) if tot[2] else None),
           instances=inst)
json.dump(out, open("judgment_layer_data.json", "w"), ensure_ascii=False, indent=1)
print(f"judgment exported: {len(reg)} types, {tot[0]} instances, outcome {tot[1]}")
