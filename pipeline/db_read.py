# -*- coding: utf-8 -*-
"""给看板构建脚本用的读数入口：read('13-观测记录.csv') 等，返回与根目录 CSV 同列名的 list[dict]，但数据来自库（真源）。
根目录 CSV 建库后已冻结；看板脚本把 `read` 换成这里的即可拿到库里最新填充（新记录 / 取代 / 字段级填充）。
过渡：库里没有的列（例如 UI 侧刚在 CSV 加的 status_line / falsifier），按主键从同名 CSV 左连接补上，并打印提醒 —— 这些列应尽快用 migrations/ 落库。"""
import os, csv, duckdb
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DB = (os.environ.get('ANATOLE_DB') or os.path.join(HERE, 'anatole_ai_monitor.duckdb'))
SQL = {
  '13-观测记录.csv': ("SELECT record_id, metric_id, entity, obs_type, value, unit, period, knowledge_time, source, provenance, direction, direction_note, note FROM v_obs WHERE metric_id IN (SELECT metric_id FROM metric_registry WHERE COALESCE(status,'') <> 'deprecated') ORDER BY record_id", 'record_id'),
  '13-指标总表.csv': ("SELECT metric_id, entry, dim, ticker_or_entity, name, data_class, signal_role, frequency, lead_time_est, owner, availability, source_family, next_release, next_release_basis, status, notes_assumption_ids FROM metric_registry WHERE COALESCE(status,'') <> 'deprecated' ORDER BY metric_id", 'metric_id'),
  '13-边总表.csv':   ("SELECT edge_id, from_metric, to_ticker, side, edge_type, hops, cert_tier, cert_method, tradable_recorded AS tradable_score, warning_recorded AS warning_score, is_key, evidence, status, notes, chain FROM v_edge_scored ORDER BY edge_id", 'edge_id'),
  '13-日历排期.csv': ("SELECT date_raw AS date, date_precision, event, entity_or_ticker, dim_or_entry, related_metric, basis, source_or_rule, notes FROM v_calendar ORDER BY cal_id", None),
  '13-关键事实.csv': ("SELECT kf_id, target_type, strftime(date, '%Y-%m-%d') AS date, target, brief, watch, refs, owner, status, status_line, falsifier FROM key_fact ORDER BY kf_id", 'kf_id'),
}
_warned = set()
def _csv(name):
    p = os.path.join(ROOT, 'data', 'tables', name)
    if not os.path.exists(p): return []
    with open(p, newline='', encoding='utf-8') as fh: return list(csv.DictReader(fh))
def read(name):
    if name not in SQL: return _csv(name)                                   # 库里没有的文件（如 13-术语表.csv）仍读 CSV
    sql, pk = SQL[name]
    con = duckdb.connect(DB, read_only=True); cur = con.execute(sql); cols = [d[0] for d in cur.description]
    rows = [{c: ('' if v is None else str(v)) for c, v in zip(cols, r)} for r in cur.fetchall()]; con.close()
    extra = _csv(name); extra_cols = [c for c in (extra[0].keys() if extra else []) if c not in cols]
    if extra_cols and pk:                                                   # 过渡：CSV 独有列按主键补上
        by = {r[pk]: r for r in extra}
        for r in rows:
            for c in extra_cols: r[c] = by.get(r[pk], {}).get(c, '')
        if name not in _warned: _warned.add(name); print(f'[db_read] {name}: 列 {extra_cols} 只在 CSV、未落库，已按 {pk} 补上；请用 migrations/ 落库')
    return rows
if __name__ == '__main__':
    for n in SQL: print(n, len(read(n)), 'rows')
