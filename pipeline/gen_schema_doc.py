# -*- coding: utf-8 -*-
"""从库里的 schema_doc / relation_doc / calc_rule / v_schema_coverage 生成 SCHEMA.md（文档不手写，避免漂移）。用法：python3 gen_schema_doc.py"""
import duckdb, os
HERE=os.path.dirname(os.path.abspath(__file__)); con=duckdb.connect((os.environ.get('ANATOLE_DB') or os.path.join(HERE,'anatole_ai_monitor.duckdb')), read_only=True)
out=['# SCHEMA · Anatole AI 发展监测体系（由库生成，勿手改）','',
     '分层：接入 `stg_*` → 资产（doc21）`entity_master` / `entity_ticker_map` / `metric_registry` / `edge_registry` / `fct_quant` / `fct_event` / `fct_opinion` / `fct_frontier` / `fct_position` / `source_master` → 治理（判断表）`assumption` / `coefficient` / `metric_factor` / `observation_direction` / `key_fact` → 元数据 `schema_doc` / `relation_doc` / `calc_rule` / `etl_log` → 视图。',
     '','原则（doc21 §〇）：表只存不可再推导的原子事实与人的判断；可推导的一律作视图。','']
tables=[r[0] for r in con.execute("SELECT DISTINCT table_name FROM schema_doc ORDER BY CASE WHEN table_name LIKE 'stg%' THEN 0 WHEN table_name IN ('entity_master','entity_ticker_map','metric_entity','metric_registry','edge_registry') THEN 1 WHEN table_name LIKE 'fct%' THEN 2 WHEN table_name='source_master' THEN 3 WHEN table_name IN ('assumption','coefficient','metric_factor','observation_direction','key_fact','source_override') THEN 4 WHEN table_name IN ('calendar','calendar_metric') THEN 5 ELSE 6 END, table_name").fetchall()]
def cnt(t):
    try: return con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
    except Exception: return '—'
def fillrate(t,c):
    try:
        n,f=con.execute(f'SELECT count(*), count("{c}") FROM "{t}"').fetchone(); return f'{f}/{n}' if n else '0/0'
    except Exception: return '—'
out.append('## 一、表与字段（含当前有值率：非空 / 总行）'); out.append('')
for t in tables:
    out.append(f'### `{t}`  · {cnt(t)} 行'); out.append(''); out.append('| 列 | 含义 | 设计出处 | 有值 | 可推导→视图 |'); out.append('|---|---|---|---|---|')
    for (c,m,ref,der,view) in con.execute("SELECT column_name, meaning, design_ref, derivable, served_by_view FROM schema_doc WHERE table_name=? ORDER BY rowid", [t]).fetchall():
        out.append(f'| `{c}` | {m} | {ref or ""} | {"—" if der else fillrate(t,c)} | {("→ " + view) if der else ""} |')
    out.append('')
out.append('## 二、表间关系'); out.append(''); out.append('| 从 | 列 | 到 | 列 | 基数 | 含义 |'); out.append('|---|---|---|---|---|---|')
for r in con.execute("SELECT * FROM relation_doc ORDER BY rowid").fetchall(): out.append('| ' + ' | '.join(f'`{x}`' if i<4 else str(x) for i,x in enumerate(r)) + ' |')
out.append(''); out.append('## 三、计算规则（系数在 `coefficient`，挂假设台账）'); out.append(''); out.append('| 规则 | 名称 | 公式 | 输入 | 输出视图 | 假设 | 出处 | 说明 |'); out.append('|---|---|---|---|---|---|---|---|')
for r in con.execute("SELECT * FROM calc_rule ORDER BY rowid").fetchall(): out.append('| ' + ' | '.join(str(x or '') for x in r) + ' |')
out.append(''); out.append('## 四、系数当前值'); out.append(''); out.append('| 系数 | 值 | 假设 | 说明 |'); out.append('|---|---|---|---|')
for r in con.execute("SELECT * FROM coefficient ORDER BY rowid").fetchall(): out.append('| ' + ' | '.join(str(x or '') for x in r) + ' |')
out.append(''); out.append('## 五、视图'); out.append('')
for (v,) in con.execute("SELECT table_name FROM information_schema.tables WHERE table_type='VIEW' AND table_name LIKE 'v_%' ORDER BY 1").fetchall(): out.append(f'- `{v}`')
open(os.path.join(HERE,'SCHEMA.md'),'w',encoding='utf-8').write('\n'.join(out)); print('SCHEMA.md', len(out), 'lines')
