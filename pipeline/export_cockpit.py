# -*- coding: utf-8 -*-
"""驾驶舱(总览)数据 exporter:从 DB 全量计算 cockpit_data.json。
口径:metric_green=fill_status='已填';p1_ratio=stg_observation 中 P1 占比;
cov=v_schema_coverage;review_due=v_review_due;radar=fct_frontier;heat=metric_registry dim×data_class。"""
import duckdb, json

c = duckdb.connect("anatole_ai_monitor.duckdb", read_only=True)


def q1(s, d=0):
    r = c.execute(s).fetchone()
    return r[0] if r and r[0] is not None else d


prov = dict(c.execute("select provenance,count(*) from stg_observation group by 1").fetchall())
calib = dict(c.execute("select calib_status,count(*) from decision_registry group by 1").fetchall())
execd = dict(c.execute("select executor_kind,count(*) from decision_registry group by 1").fetchall())
radar_by_track = dict(c.execute("select coalesce(topic_cluster,'—'),count(*) from fct_frontier group by 1 order by 2 desc").fetchall())
dirc = dict(c.execute("select direction,count(*) from observation_direction group by 1").fetchall())
dir7 = {k: dirc[k] for k in ("↑", "↓", "!") if dirc.get(k)}

heat = {}
for dim, dc, n in c.execute("select coalesce(dim,'—'),coalesce(data_class,'—'),count(*) from metric_registry group by 1,2").fetchall():
    heat.setdefault(dim, {})[dc] = n

upcoming = [dict(date=r[0], event=r[1], tk=r[2] or "", dim=r[3] or "")
            for r in c.execute("select cast(date as varchar),event,entity_or_ticker,dim_or_entry "
                               "from calendar where date is not null and date>current_date order by date limit 6").fetchall()]

out = dict(
    heat=heat, upcoming=upcoming, calib=calib, exec=execd,
    dec_total=q1("select count(*) from decision_log"),
    dec_outcome=q1("select count(*) from decision_log where outcome is not null and outcome!=''"),
    dec_prospective=q1("select count(*) from decision_log where retro is not true"),
    metric_total=q1("select count(*) from metric_registry"),
    metric_green=q1("select count(*) from metric_registry where fill_status='已填'"),
    p1_ratio=round(100 * prov.get("P1", 0) / max(1, sum(prov.values())), 1),
    cov_exist=q1("select count(*) from v_schema_coverage where exists_in_db"),
    cov_total=q1("select count(*) from v_schema_coverage"),
    review_due=q1("select count(*) from v_review_due"),
    radar=q1("select count(*) from fct_frontier"),
    radar_by_track=radar_by_track, dir7=dir7,
    etl_last=(q1("select cast(max(run_at) as varchar) from etl_log", "") or "")[:16],
)
json.dump(out, open("cockpit_data.json", "w"), ensure_ascii=False)
print(f"cockpit exported: metric {out['metric_green']}/{out['metric_total']} · p1 {out['p1_ratio']}% · "
      f"cov {out['cov_exist']}/{out['cov_total']} · radar {out['radar']} · review {out['review_due']} · dir7 {dir7}")
