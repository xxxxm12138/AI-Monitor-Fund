# -*- coding: utf-8 -*-
"""改库：按编号应用 migrations/NNNN_name.py 里尚未应用的脚本，每个脚本一个事务，登记 migration_log + 字段级 change_log。
用法（pipeline/ 下）：python3 migrate.py            # 应用所有待应用脚本，然后刷新视图
                     python3 migrate.py --status   # 只看哪些已应用 / 待应用
脚本格式：模块级 OWNER = 'B'，def up(m): 用 m.observe / m.set / m.supersede / m.sql 改库。已应用的脚本不可再改（checksum 校验），要改就写下一个编号。"""
import os, re, sys, glob, hashlib, json, duckdb, datetime as dt, importlib.util
from core import *

class Migration:
    """一次改库的上下文：每个写操作都落 change_log（表 / 行 / 列 / 改前 / 改后 / 依据 / owner）。"""
    def __init__(self, con, mid, owner):
        self.con, self.mid, self.owner, self.n = con, mid, owner, 0
        self.types = column_types(con)
        self.mcls = dict(con.execute('SELECT metric_id, data_class FROM metric_registry').fetchall())
        self.ent_of = dict(con.execute('SELECT metric_id, entity_id FROM metric_registry').fetchall())
        self.snaps = set(os.listdir(SNAP_DIR)) if os.path.isdir(SNAP_DIR) else set()
        self.dmod = mod('directions')
    def _refresh_metrics(self):
        self.mcls = dict(self.con.execute('SELECT metric_id, data_class FROM metric_registry').fetchall())
        self.ent_of = dict(self.con.execute('SELECT metric_id, entity_id FROM metric_registry').fetchall())
    def _log(self, table, pk, col, old, new, basis, owner=None):
        self.n += 1
        self.con.execute('INSERT INTO change_log (change_id, migration_id, table_name, pk, column_name, old_value, new_value, basis, owner) VALUES (?,?,?,?,?,?,?,?,?)',
            [f'{self.mid}-{self.n:04d}', self.mid, table, pk, col, None if old is None else str(old), None if new is None else str(new), basis, owner or self.owner])
    def observe(self, record_id, metric_id, entity, obs_type, value, unit, period, knowledge_time, source, provenance, note='', direction=None, direction_note='', basis=None, direction_confidence=None):
        """登记一条新事实：stg_observation → 路由到 fct_* → 来源 upsert → 方向判断。等价于原来在 13-观测记录.csv 追加一行。
        显式传 direction = 人工改判（覆盖 directions.py 规则初判）→ 自动记一条 d_direction 判断（六元组，PLAN §六 Q2 甲案：只记人工改判）。"""
        if metric_id not in self.mcls: self._refresh_metrics()                  # 本脚本刚 insert 的新指标
        if metric_id not in self.mcls: raise ValueError(f'{record_id}: 指标 {metric_id} 未登记（先 m.insert metric_registry）')
        if self.con.execute('SELECT 1 FROM stg_observation WHERE record_id=?', [record_id]).fetchone(): raise ValueError(f'{record_id} 已存在；纠错用新 record_id + supersede')
        r = dict(record_id=record_id, metric_id=metric_id, entity=entity, obs_type=obs_type, value=str(value), unit=unit or '', period=period or '', knowledge_time=knowledge_time, source=source, provenance=prov_norm(provenance), note=note or '')
        t, row = fct_row(r, self.mcls.get(metric_id), self.ent_of.get(metric_id))
        self.con.execute('INSERT INTO stg_observation VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', [r['record_id'], r['metric_id'], r['entity'], r['obs_type'], r['value'], r['unit'], r['period'], r['knowledge_time'], r['source'], r['provenance'], r['note'], t])
        insert_rows(self.con, t, [row])
        upsert_source(self.con, r, self.mcls.get(metric_id))
        d, dn = (direction, direction_note) if direction else tuple(self.dmod.assign(r))
        self.con.execute('INSERT INTO observation_direction VALUES (?,?,?,?,?)', [record_id, d, dn, self.owner, 'draft'])
        self._log('stg_observation', record_id, '(insert)', None, f'{t} · {metric_id} · {obs_type} · {value} {unit} · {period}', basis or src_name(source))
        if direction and self._dec_registered('d_direction'):                   # 只记人工改判；0011 之前（registry 未 seed）静默跳过，保证 0001–0009 重放同构
            self.decide('d_direction', d, direction_note or basis or '人工改判', target=f'observation_direction:{record_id}',
                        confidence=direction_confidence, state_anchor={'record_id': record_id, 'as_of': knowledge_time}, executor_kind='human', executor=self.owner)
        return t
    CONF = {'H': 0.9, 'M': 0.6, 'L': 0.3}                                       # C21：与因子锚同一词表（Q1 甲案）
    def _dec_registered(self, decision_id):
        return ('decision_registry', 'decision_id') in self.types and bool(self.con.execute('SELECT 1 FROM decision_registry WHERE decision_id=?', [decision_id]).fetchone())
    def decide(self, decision_id, choice, basis, target=None, confidence=None, state_anchor=None,
               executor=None, executor_kind=None, escalated=False, retro=False, outcome=None, outcome_basis=None, note=None, sync=False):
        """记一次判断（六元组入 decision_log）。target = 'table:pk' 或 'table:pk.column'；confidence 可 'H'/'M'/'L'（映射 .9/.6/.3，C11）或 0–1。
        sync=True 且该判断类型 output_home 为单列时，同步把 choice 写回家（内部走 set，照进 change_log）。回填历史判断传 retro=True 且不编造 confidence（C21 见假设台账）。"""
        reg = self.con.execute('SELECT candidates, output_home, executor_kind, executor FROM decision_registry WHERE decision_id=?', [decision_id]).fetchone()
        if reg is None: raise ValueError(f'判断类型 {decision_id} 未登记（先 m.insert decision_registry）')
        cands, home, ek0, ex0 = reg
        if confidence in self.CONF: confidence = self.CONF[confidence]
        if confidence is not None and not (0 <= float(confidence) <= 1): raise ValueError(f'{decision_id}: confidence {confidence} 超出 [0,1]（或用 H/M/L）')
        try: clist = json.loads(cands)
        except (ValueError, TypeError): clist = None
        if isinstance(clist, list) and str(choice) not in [str(c) for c in clist]: raise ValueError(f'{decision_id}: choice {choice} 不在候选 {clist}')
        tt = tp = tc = None
        if target:
            tt, rest = target.split(':', 1)
            if tt not in PK: raise ValueError(f'decide target 表 {tt} 不在可写表清单')
            tp, tc = rest.split('.', 1) if '.' in rest else (rest, None)
            if not self.con.execute(f'SELECT 1 FROM {tt} WHERE "{PK[tt]}" = ?', [tp]).fetchone(): raise ValueError(f'decide target 不存在: {tt}.{tp}')
        self.ndec = getattr(self, 'ndec', 0) + 1
        dec_id = f'{self.mid}-dec{self.ndec:03d}'
        self.insert('decision_log', dict(dec_id=dec_id, decision_id=decision_id, target_table=tt, target_pk=tp, target_column=tc,
            state_anchor=(json.dumps(state_anchor, ensure_ascii=False, default=str) if isinstance(state_anchor, (dict, list)) else state_anchor),
            candidates_shown=cands, choice=str(choice), confidence=confidence, executor_kind=executor_kind or ek0, executor=executor or ex0,
            escalated=escalated, basis=basis, retro=retro, outcome=outcome, outcome_basis=outcome_basis, note=note), basis=basis)
        if sync:
            if not (home and '.' in home and '+' not in home and tp): raise ValueError(f'{decision_id}: sync 需要单列 output_home 与 target')
            ht, hc = home.split('.', 1)
            self.set(ht, tp, hc, choice, basis=f'{dec_id}：{basis}')
        return dec_id
    def set(self, table, key, column, value, basis, owner=None):
        """填一个字段：UPDATE + change_log（改前值自动记录）。"""
        if (table, column) not in self.types: raise ValueError(f'{table}.{column} 不存在')
        if column == 'snapshot_id' and value and (str(value) + '.txt') not in self.snaps: raise ValueError(f'快照文件缺失 snapshots/{value}.txt')
        pk = PK[table]
        old = self.con.execute(f'SELECT "{column}" FROM {table} WHERE "{pk}" = ?', [key]).fetchone()
        if old is None: raise ValueError(f'{table} 无主键 {key}')
        v = cast(self.types, table, column, value)
        self.con.execute(f'UPDATE {table} SET "{column}" = ? WHERE "{pk}" = ?', [v, key])
        self._log(table, key, column, old[0], v, basis, owner)
        if table == 'metric_registry' and column in ('data_class', 'entity_id'): self._refresh_metrics()   # 路由依赖的指标属性变了
    def supersede(self, old_record_id, new_record_id, reason, owner=None):
        """旧记录被新记录取代：旧行不删，superseded_by + status=superseded。"""
        if not self.con.execute('SELECT 1 FROM stg_observation WHERE record_id=?', [new_record_id]).fetchone(): raise ValueError(f'取代者 {new_record_id} 不存在')
        hit = 0
        for t in FCT:
            if self.con.execute(f'SELECT 1 FROM {t} WHERE record_id=?', [old_record_id]).fetchone():
                self.set(t, old_record_id, 'superseded_by', new_record_id, reason, owner); self.set(t, old_record_id, 'status', 'superseded', reason, owner); hit += 1
        if not hit: raise ValueError(f'被取代者 {old_record_id} 不在任何 fct 表')
    def insert(self, table, row, basis, owner=None):
        """整行新增（新指标 / 新边 / 新假设 / 新实体等非观测行）：按列类型转换后 INSERT，记 (insert)。观测记录请用 observe()。"""
        if table not in PK: raise ValueError(f'{table} 不在可写表清单')
        for c in row:
            if (table, c) not in self.types: raise ValueError(f'{table}.{c} 不存在')
        vals = {c: cast(self.types, table, c, v) for c, v in row.items()}
        self.con.execute(f'INSERT INTO {table} ({",".join(vals)}) VALUES ({",".join(["?"]*len(vals))})', list(vals.values()))
        self._log(table, str(row.get(PK[table], '-')), '(insert)', None, json.dumps(row, ensure_ascii=False, default=str)[:500], basis, owner)
    def sql(self, statement, basis, params=None):
        """兜底：任意 SQL（如新指标 / 新边 / 新假设 INSERT）；整句记入 change_log。"""
        self.con.execute(statement, params or [])
        if re.match(r'\s*(ALTER|CREATE|DROP)\b', statement, re.I): self.types = column_types(self.con)   # DDL 后刷新列类型
        self._log('(sql)', '-', '(sql)', None, statement.strip()[:500], basis)

def checksum(path): return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]
def main():
    if not os.path.exists(DB): sys.exit('!! 库不存在：先 python3 init_db.py')
    con = duckdb.connect(DB)
    applied = {r[0]: r[1] for r in con.execute('SELECT migration_id, checksum FROM migration_log').fetchall()}
    mig_dir = os.environ.get('ANATOLE_MIGRATIONS') or os.path.join(HERE, 'migrations')   # ANATOLE_MIGRATIONS=… 可指向私有目录（子任务在副本上单独测试自己的脚本）
    files = sorted(glob.glob(os.path.join(mig_dir, '[0-9][0-9][0-9][0-9]_*.py')))
    pending = []
    for f in files:
        mid = os.path.basename(f)[:-3]
        if mid in applied:
            if applied[mid] != checksum(f): sys.exit(f'!! {mid} 已应用但脚本被改过（checksum {applied[mid]} ≠ {checksum(f)}）。已应用脚本不可改，请写下一个编号。')
        else: pending.append((mid, f))
    if '--status' in sys.argv:
        for mid, cs in applied.items(): print('applied', mid, cs)
        for mid, f in pending: print('pending', mid)
        return
    for mid, f in pending:
        spec = importlib.util.spec_from_file_location(mid, f); mmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mmod)
        owner = getattr(mmod, 'OWNER', 'B'); note = (mmod.__doc__ or '').strip().splitlines()[0] if mmod.__doc__ else ''
        m = Migration(con, mid, owner)
        con.execute('BEGIN')
        try:
            con.execute('INSERT INTO migration_log (migration_id, checksum, owner, n_changes, note) VALUES (?,?,?,?,?)', [mid, checksum(f), owner, 0, note])  # 先登记（change_log 外键指向它），失败整体回滚
            mmod.up(m)
            con.execute('UPDATE migration_log SET n_changes = ? WHERE migration_id = ?', [m.n, mid])
            con.execute('COMMIT')
        except Exception as ex:
            con.execute('ROLLBACK'); sys.exit(f'!! {mid} 失败，已回滚：{ex}')
        print(f'applied {mid}: {m.n} changes · owner {owner} · {note}')
    if not pending: print('无待应用脚本')
    con.execute(open(os.path.join(HERE, 'views.sql'), encoding='utf-8').read())
    con.close()
if __name__ == '__main__': main()
