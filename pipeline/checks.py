# -*- coding: utf-8 -*-
"""数据健康检查（约束之外的业务规则）。用法：python3 checks.py  → 打印报告；有 ERROR 时退出码 1。"""
import duckdb, os, sys
DB = (os.environ.get('ANATOLE_DB') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anatole_ai_monitor.duckdb'))
con = duckdb.connect(DB, read_only=True)
errors, warns = [], []
def q(sql): return con.execute(sql).fetchall()
# 1 已填但无记录
for (mid,) in q("SELECT metric_id FROM v_health WHERE gap_records IS NOT NULL"): errors.append(f'已填但无观测记录: {mid}')
# 2 边的中间节点数 = hops-1（hops≥2 时）；hops≤1 时 chain 须为空
for (eid,h,n) in q("SELECT edge_id,hops,n_intermediate FROM v_edge_scored WHERE (hops>=2 AND n_intermediate<>hops-1) OR (hops<=1 AND n_intermediate>0)"): warns.append(f'边 {eid}: hops={h} 但中间节点={n}（chain 未填或不一致）')
# 3 排期引用但不存在的指标（related_metric 里的 token 未进 calendar_metric）
for (cid,ev,rm) in q("SELECT cal_id,event,related_metric FROM calendar"):
    toks=[x.strip() for x in rm.split('/')]; have={m for (m,) in q(f"SELECT metric_id FROM calendar_metric WHERE cal_id='{cid}'")}
    for t in toks:
        if t and t not in have: errors.append(f'排期 {cid}「{ev}」引用不存在的指标 {t}')
# 4 已排期事件无简报
for (cid,ev,d) in q("SELECT cal_id,event,date FROM v_calendar WHERE date IS NOT NULL AND kf_brief IS NULL"): warns.append(f'已排期事件无关键事实: {d} {ev}')
# 5 过期未更新
for (mid,nd) in q("SELECT metric_id,next_date FROM v_health WHERE overdue IS NOT NULL"): warns.append(f'过期未更新: {mid} next={nd}')
# 6 备注里引用的假设 ID 必须在台账
import re
ids={a for (a,) in q("SELECT assumption_id FROM assumption")}
for (mid,notes) in q("SELECT metric_id, notes_assumption_ids FROM metric_registry WHERE notes_assumption_ids IS NOT NULL"):
    for a in re.findall(r'\b([ABCR]\d{1,2})\b', notes or ''):
        if a not in ids: warns.append(f'{mid} 引用未登记假设 {a}')
# 7 观测记录 knowledge_time 无法解析日期的（只能按文本排）
n=q("SELECT count(*) FROM v_fct WHERE knowledge_date IS NULL")[0][0]
if n: warns.append(f'{n} 条观测记录 knowledge_time 非日期粒度（年 / 季 / —），只能按文本排序')
# 7b 路由完整性：每条登记记录恰好落一张 fct
n2=q("SELECT count(*) FROM stg_observation s WHERE NOT EXISTS (SELECT 1 FROM v_fct f WHERE f.record_id=s.record_id)")[0][0]
if n2: errors.append(f'{n2} 条登记记录未路由到任何 fct 表')
# 7c 字典完整性
miss=q("SELECT c.table_name||'.'||c.column_name FROM information_schema.columns c LEFT JOIN schema_doc d ON d.table_name=c.table_name AND d.column_name=c.column_name WHERE c.table_schema='main' AND c.table_name NOT LIKE 'v_%' AND d.column_name IS NULL")
for (x,) in miss: errors.append(f'字典缺列说明: {x}')
# 7d 打分对账
for (eid,tr,tc) in q("SELECT edge_id, tradable_recorded, tradable_calc FROM v_edge_calc WHERE reconcile_flag IS NOT NULL"): warns.append(f'边分数对账不一致: {eid} 记录 {tr} vs 规则 {tc}（因子待 D 复核）')
# 7e 证据引用：evidence_ids 里的每个 record 必须存在，且属于 from_metric 或该边显式关联的指标
EXTRA={'e_labfund_nbis':{'m_lab_contract_reflection_nbis'},'e_capex_nbis':{'m_capex_msft','m_capex_googl','m_capex_amzn','m_capex_meta'}}
for (eid,fm,ev) in q("SELECT edge_id, from_metric, evidence_ids FROM edge_registry WHERE evidence_ids IS NOT NULL"):
    import json as _j
    for rid in _j.loads(ev):
        row=q(f"SELECT metric_id FROM stg_observation WHERE record_id='{rid}'")
        if not row: errors.append(f'边 {eid} 证据 {rid} 不存在'); continue
        if row[0][0]!=fm and row[0][0] not in EXTRA.get(eid,set()): errors.append(f'边 {eid} 证据 {rid} 属于 {row[0][0]}，不是上游 {fm}')
# 7f 快照文件存在
import os as _os
for (t,) in [('fct_quant',),('fct_event',),('fct_opinion',),('fct_frontier',)]:
    for (rid,sn) in q(f"SELECT record_id, snapshot_id FROM {t} WHERE snapshot_id IS NOT NULL"):
        if not _os.path.exists(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'snapshots',sn+'.txt')): errors.append(f'{t}.{rid} 快照 {sn} 文件缺失')
# 7g 改库账完整性：change_log 指向的行必须存在；migrations/ 脚本 checksum 与 migration_log 一致（已应用脚本不可改）
import hashlib as _h, glob as _g
from core import PK as PKS   # 可写表清单与 migrate.py 同源
for (t,pk,n) in q("SELECT table_name, pk, count(*) FROM change_log WHERE table_name<>'(sql)' GROUP BY 1,2"):
    if t not in PKS: errors.append(f'change_log 指向未知表 {t}'); continue
    if not q(f"SELECT 1 FROM {t} WHERE \"{PKS[t]}\"='{pk}'"): errors.append(f'change_log 指向不存在的行 {t}.{pk}（{n} 条）')
_here=_os.path.dirname(_os.path.abspath(__file__))
applied=dict(q("SELECT migration_id, checksum FROM migration_log"))
for f in sorted(_g.glob(_os.path.join(_os.environ.get('ANATOLE_MIGRATIONS') or _os.path.join(_here,'migrations'),'[0-9][0-9][0-9][0-9]_*.py'))):
    mid=_os.path.basename(f)[:-3]; cs=_h.sha256(open(f,'rb').read()).hexdigest()[:16]
    if mid not in applied: warns.append(f'migrations/{mid} 尚未应用（python3 migrate.py）')
    elif applied[mid]!=cs: errors.append(f'migrations/{mid} 已应用但脚本被改（checksum 不符）；已应用脚本不可改，请写下一个编号')
# 7h 根目录 CSV 建库后被改：改动不会进库（库是真源），提醒改走 migrations/
ROOT=_os.path.dirname(_here)
srcs=''.join(open(_os.path.join(ROOT,'data','tables',f),encoding='utf-8').read() for f in ('13-观测记录.csv','13-指标总表.csv','13-边总表.csv','13-假设台账.csv','13-关键事实.csv','13-日历排期.csv'))
if applied.get('0000_bootstrap') and applied['0000_bootstrap']!=_h.sha256(srcs.encode()).hexdigest()[:16]: warns.append('根目录 13-*.csv 在建库后被改过：库是真源，CSV 改动不会进库；新增 / 修改请写 migrations/ 脚本（或明确要重建再 init_db.py --force）')
# 7i 思路层锚点：引用的表 / 列 / 视图 / 规则 / 假设 / 系数必须存在（思路与数据不允许两张皮）
have_tab={t for (t,) in q("SELECT table_name FROM information_schema.tables WHERE table_schema='main'")}
have_col={(t,c) for (t,c) in q("SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='main'")}
have_rule={r for (r,) in q("SELECT rule_id FROM calc_rule")}; have_coef={r for (r,) in q("SELECT coef_id FROM coefficient")}; have_mig={r for (r,) in q("SELECT migration_id FROM migration_log")}
for (aid,kind,ref) in q("SELECT anchor_id, kind, ref FROM artifact_anchor"):
    ok = (kind in ('table','view') and ref in have_tab) or (kind=='column' and tuple(ref.split('.',1)) in have_col) or (kind=='rule' and ref in have_rule) or (kind=='assumption' and ref in ids) or (kind=='coefficient' and ref in have_coef) or (kind=='migration' and ref in have_mig) or kind in ('check','file')
    if not ok: errors.append(f'思路层锚点 {aid} 引用不存在: {kind} {ref}')
# 7j 决策层：choice 必须在判断时刻的候选内（open 候选除外）
import json as _j2
for (dec,did,ch,cands) in q("SELECT dec_id, decision_id, choice, candidates_shown FROM decision_log"):
    try: cl=_j2.loads(cands or 'null')
    except ValueError: cl=None
    if isinstance(cl,list) and ch not in [str(x) for x in cl]: errors.append(f'decision_log {dec}（{did}）: choice {ch} 不在候选 {cl}')
# 7k 判断与家一致：单列 output_home 的判断类型，每个 target 最新一条判断的 choice 须与家中现值一致（前缀匹配容忍「T2（提议）」类写法）
for (did,home) in q("SELECT decision_id, output_home FROM decision_registry WHERE output_home IS NOT NULL AND output_home LIKE '%.%' AND output_home NOT LIKE '%+%'"):
    ht,hc=home.split('.',1)
    if ht not in PKS: errors.append(f'decision_registry {did}: output_home 表 {ht} 未注册'); continue
    for (tp,ch) in q(f"SELECT target_pk, choice FROM decision_log WHERE decision_id='{did}' AND target_pk IS NOT NULL QUALIFY row_number() OVER (PARTITION BY target_pk ORDER BY decided_at DESC, dec_id DESC)=1"):
        cur=q(f"SELECT \"{hc}\" FROM {ht} WHERE \"{PKS[ht]}\"='{tp}'")
        if not cur: errors.append(f'decision_log（{did}）指向不存在的行 {ht}.{tp}'); continue
        v='' if cur[0][0] is None else str(cur[0][0])
        if not (v==ch or v.startswith(ch)): errors.append(f'判断与家不一致: {did} → {ht}.{tp}.{hc} 现值「{v}」vs 最新判断「{ch}」')
# 7l 校准闸（🟠闸扩展）：assisted / auto 且执行者是 llm / model 的判断类型，关联假设必须全部 validated；rule 豁免
ast=dict(q("SELECT assumption_id, status FROM assumption"))
for (did,cs,aids) in q("SELECT decision_id, calib_status, assumption_ids FROM decision_registry WHERE calib_status IN ('assisted','auto') AND executor_kind IN ('llm','model')"):
    linked=re.findall(r'\b([ABCR]\d{1,2})\b', aids or ''); bad=[a for a in linked if ast.get(a)!='validated']
    if not linked or bad: errors.append(f'校准闸: {did} calib_status={cs} 但关联假设未 validated（{bad or "无关联假设"}）——未校准禁 assisted/auto')
# 7m candidate_pool 生命周期：selected/rejected 必须有 resolved_by 且指向存在的判断；selected 候选的判断 choice 应含其 cand_id
for (cid,st,rb) in q("SELECT cand_id, status, resolved_by FROM candidate_pool"):
    if st in ('selected','rejected') and not rb: errors.append(f'candidate_pool {cid} status={st} 但无 resolved_by')
    if rb and not q(f"SELECT 1 FROM decision_log WHERE dec_id='{rb}'"): errors.append(f'candidate_pool {cid} resolved_by {rb} 不存在')
# 7n 背离 PROPOSE 欠账：超 7 天无解释候选（R17）
asof=q("SELECT max(knowledge_date) FROM v_fct")[0][0]
for (k,sub,kd2,nc) in q("SELECT div_key, subject, knowledge_date, n_candidates FROM v_divergence WHERE n_candidates=0"):
    if kd2 and asof and (asof-kd2).days>7: warns.append(f'背离 {k}（{sub}，{kd2}）超 7 天无解释候选（PROPOSE 欠账，登记进 candidate_pool）')
# 7o 判断纪律：前瞻判断要写置信度（H/M/L 即可）；超 60 天未回填 outcome 并入复验
nc1=q("SELECT count(*) FROM decision_log WHERE NOT retro AND confidence IS NULL")[0][0]
if nc1: warns.append(f'{nc1} 条前瞻判断未写置信度（敢写才能校准；H/M/L 三档映射 .9/.6/.3）')
nc2=q("SELECT count(*) FROM decision_log WHERE NOT retro AND outcome IS NULL AND decided_at < current_timestamp - INTERVAL 60 DAY")[0][0]
if nc2: warns.append(f'{nc2} 条判断超 60 天未回填 outcome（并入复验节奏，owner 跟原判断走）')
# 8 复验队列规模
rv=q("SELECT provenance,count(*) FROM v_review_due GROUP BY 1 ORDER BY 1")
print('== 复验队列 ==', dict(rv))
print('== 健康标记 ==', dict(q("SELECT flag,count(*) FROM v_health WHERE flag IS NOT NULL GROUP BY 1")))
print(f'== ERROR {len(errors)} ==');  [print('  ✗', e) for e in errors]
print(f'== WARN {len(warns)} ==');    [print('  !', w) for w in warns]
sys.exit(1 if errors else 0)
