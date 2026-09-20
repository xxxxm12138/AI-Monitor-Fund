# -*- coding: utf-8 -*-
"""库（anatole_ai_monitor.duckdb）→ JSON → 注入 template.html → ../assets/16-AI发展监测日历.html
用法（pipeline/ 下）：python3 build_dashboard.py。数据一律来自库（db_read.read 与根目录 CSV 同列名）；根目录 13-*.csv 建库后冻结，不再是数据来源。"""
import csv, json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'assets', '16-AI发展监测日历.html')
import duckdb as _dd
AS_OF = str(_dd.connect((os.environ.get('ANATOLE_DB') or os.path.join(HERE, 'anatole_ai_monitor.duckdb')), read_only=True).execute('SELECT max(knowledge_date) FROM v_fct').fetchone()[0])  # 数据快照日 = 最新观测的知悉日（R14）

sys.path.insert(0, HERE)
from db_read import read   # 库是真源：同名同列，数据来自 anatole_ai_monitor.duckdb

metrics = read('13-指标总表.csv')
edges = read('13-边总表.csv')
cal = read('13-日历排期.csv')
records = read('13-观测记录.csv')
keyfacts = read('13-关键事实.csv')


# ---- derive display fields from records (registry stores no values) ----
PRI = {'actual': 5, 'event': 4, 'position': 3, 'state': 2, 'computed': 1}
by_m = {}
for r in records: by_m.setdefault(r['metric_id'], []).append(r)
def fmt(r):
    v = r['value']; u = r['unit']
    if not v or v == '—': return '—'
    import re as _re
    if u in ('', '—') or not _re.match(r'^[\d≈~>+\-−.]', v): return v
    if u.startswith('USD') or u.startswith('CNY') or u.startswith('HKD') or u.startswith('EUR'):
        cur = {'USD':'$','CNY':'¥','HKD':'HK$','EUR':'€'}[u[:3]]; rest = u[3:].strip()
        return f"{cur}{v}{(' ' + rest) if rest else ''}"
    return f"{v} {u}"
for m in metrics:
    rs = by_m.get(m['metric_id'], [])
    m['records'] = sorted(rs, key=lambda r: r['knowledge_time'], reverse=True)
    heads = [r for r in rs if r['obs_type'] in PRI]
    heads.sort(key=lambda r: (PRI[r['obs_type']], r['knowledge_time']), reverse=True)
    h = heads[0] if heads else None
    ents = {r['entity'] for r in rs}
    pre = (h['entity'] + ' · ') if (h and len(ents) > 1) else ''
    m['value_latest'] = (pre + fmt(h) + ((' · ' + h['note'].split('；')[0]) if h and h['note'] else '')) if h else ('—' if not rs else fmt(rs[0]))
    m['period'] = h['period'] if h else (rs[0]['period'] if rs else '')
    m['knowledge_time'] = h['knowledge_time'] if h else (rs[0]['knowledge_time'] if rs else '')
    m['provenance'] = h['provenance'] if h else (rs[0]['provenance'] if rs else '')
    m['source'] = h['source'] if h else m['source_family']
    g = sorted([r for r in rs if r['obs_type'] in ('guidance', 'target')], key=lambda r: r['knowledge_time'], reverse=True)
    m['expectation_base'] = '；'.join(f"{fmt(r)}（{r['period']}）" for r in g[:2]) if g else ''
    pr = sorted([r for r in rs if r['obs_type'] == 'prior'], key=lambda r: r['knowledge_time'], reverse=True)
    m['prior_or_yoy'] = (f"{fmt(pr[0])}（{pr[0]['period']}）" if pr else '') or ((h['note'].split('；')[0]) if h and h['note'] and ('YoY' in h['note'] or '%' in h['note'].split('；')[0]) else '')
    m['fill_status'] = m['status']
    posr = [r for r in rs if r['obs_type'] == 'position']
    m['weight'] = posr[0]['value'] if posr else ''
    m['position_note'] = posr[0]['note'] if posr else ''

# ---- derived fields ----
CN_HINT = ('300308', '300502', '海关', '工信部', '中国', '亚洲电信', '0679')
US_HINT = ('MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'BIS', 'Scale', 'Reflection', 'OpenAI', 'Anthropic', 'xAI', 'Nvidia', '版权诉讼', 'OpenRouter', '前沿 lab')
def region(m):
    t = m['ticker_or_entity'] + ' ' + m['name']
    if '0679' in t: return 'HK'
    if any(h in t for h in CN_HINT): return 'CN'
    if m['ticker_or_entity'] == 'NBIS': return 'EU'  # 阿姆斯特丹注册，NASDAQ 上市
    if m['ticker_or_entity'].startswith('EU'): return 'EU'
    if m['entry'] == '持仓': return 'US'
    if any(h in t for h in US_HINT): return 'US'
    return 'GL'

star = {}
for e in edges:
    n = e['is_key'].count('★')
    star[e['from_metric']] = max(star.get(e['from_metric'], 0), n)
def importance(m):
    mid = m['metric_id']
    if mid in star and star[mid] > 0: return min(3, star[mid])
    if m['ticker_or_entity'] in ('NBIS', 'RBRK', 'FCEL', '组合'): return 3
    if m['dim'] in ('D1', 'D7', 'D3', 'D1/D7'): return 3
    if m['dim'] in ('D5', 'D6'): return 2
    return 1

for m in metrics:
    m['region'] = region(m)
    m['importance'] = importance(m)
    m['edges'] = [e for e in edges if e['from_metric'] == m['metric_id']]

WEIGHT = {'NBIS':'51.22%','RBRK':'29.80%','STAA':'8.03%','FCEL':'7.12%','SUPX':'1.30%','SNDK':'0.83%','SLMT':'0.42%','MU':'0.37%','INTC':'0.24%','CIEN':'0.23%','MRVL':'0.15%','POET':'0.15%','AMD':'0.13%'}
SIDE_CN = {'supply':'供给侧上游','demand':'需求侧下游','regime':'政策 regime','compete':'竞对 / 做空侧','self':'本体'}
def numS(v):
    try: return float(str(v).replace('~','').replace('—','x'))
    except: return None
def dominant(e):
    t, w = numS(e['tradable_score']), numS(e['warning_score'])
    if t is None and w is None: return '待定'
    return '可交易' if (t or 0) >= (w or 0) else '预警'
def tier_sentence(e):
    tier = e['cert_tier'].split('（')[0].split('/')[0].strip()
    ev = e['evidence'] if e['evidence'] not in ('', '—') else '尚无证据记录'
    if tier == 'T1': return f"T1 可回测：{e['cert_method']}；证据：{ev}"
    if tier == 'T2': return f"T2 结构成立、需真值对账：{e['cert_method']}；证据：{ev}"
    return f"T3 只给方向：{e['cert_method']}；不据此定仓位"
for m in metrics:
    m['impacts'] = [dict(edge_id=e['edge_id'], ticker=e['to_ticker'], weight=WEIGHT.get(e['to_ticker'],''), side=SIDE_CN.get(e['side'], e['side']), hops=e['hops'], chain=e['chain'], tier=e['cert_tier'], dominant=dominant(e), tradable=e['tradable_score'], warning=e['warning_score'], is_key=e['is_key'], sentence=tier_sentence(e)) for e in edges if e['from_metric'] == m['metric_id']]
    m['upstream'] = [dict(edge_id=e['edge_id'], from_metric=e['from_metric'], side=SIDE_CN.get(e['side'], e['side']), hops=e['hops'], chain=e['chain'], tier=e['cert_tier'], dominant=dominant(e), is_key=e['is_key'], sentence=tier_sentence(e)) for e in edges if e['to_ticker'] == m['ticker_or_entity']]
mid_set = {m['metric_id'] for m in metrics}
for r in cal:
    r['metrics'] = [x.strip() for x in r['related_metric'].split('/') if x.strip() in mid_set]
    d = r['date']
    r['dated'] = bool(re.match(r'^\d{4}-\d{2}-\d{2}$', d))
    r['is_past'] = r['dated'] and d <= AS_OF
    r['basis_kind'] = r['basis'].split('（')[0]

# ---- role + signal table ----
def role_of(m):
    sr=m['signal_role'] or ''; dc=m['data_class'] or ''
    if m['metric_id']=='m_reconcile_nbis': return '对账'
    if m['metric_id'] in ('m_slmt','m_13f_book','m_hkex_0679') or m['metric_id'].startswith('m_tail_'): return '仓位'
    if dc.startswith('4'): return '前沿'
    if 'regime' in sr: return 'regime'
    if dc=='3' or 'arbiter' in sr: return '观点'
    if m['entry']=='持仓': return '本体'
    if '2' in dc: return '事件'
    return '领先'
TEMPLATE={'领先':'A','本体':'A','仓位':'A','事件':'B','regime':'B','前沿':'C','观点':'C','对账':'T'}
for m in metrics:
    m['role']=role_of(m); m['tpl']=TEMPLATE[m['role']]
import datetime as _dt
def _d(x):
    try: return _dt.date.fromisoformat(x[:10])
    except:
        try: return _dt.date.fromisoformat(x[:7]+'-15')
        except: return None
asof = _d(AS_OF)
rec_by = {}
for r in records: rec_by.setdefault(r['metric_id'], []).append(r)
def recs_in(mids, days):
    out=[]
    for mid in mids:
        for r in rec_by.get(mid, []):
            d=_d(r['knowledge_time'])
            if d and 0 <= (asof-d).days <= days and r['direction'] not in ('—',''): out.append(r)
    return out
def agg(rs):
    if not rs: return '—'
    c={k:sum(1 for r in rs if r['direction']==k) for k in '↑↓→!'}
    base = '↓' if c['↓']>=max(c['↑'],1) and c['↓']>0 else ('↑' if c['↑']>0 else ('→' if c['→']>0 else ''))
    return (base + ('!' if c['!']>0 else '')) or ('!' if c['!'] else '—')
tickers = list(WEIGHT.keys())
own = {t: [m['metric_id'] for m in metrics if m['ticker_or_entity'] == t] for t in tickers}
def side_mids(t, side):
    return [e['from_metric'] for e in edges if e['to_ticker']==t and e['side']==side]
def tier_of(e): return e['cert_tier'].split('（')[0].split('/')[0].strip()
watch=[]
for t in tickers:
    sup = side_mids(t,'supply') + own[t]; dem = side_mids(t,'demand'); reg = side_mids(t,'regime'); comp=side_mids(t,'compete')
    st = {'供':agg(recs_in(sup,60)), '需':agg(recs_in(dem,60)), '政':agg(recs_in(reg,60))}
    # 本周动了什么：7 天内、关键边或本体、方向 ≠ →
    key_m = {e['from_metric']:e['is_key'].count('★') for e in edges if e['to_ticker']==t}
    for mid in own[t]: key_m[mid]=max(key_m.get(mid,0),3)
    wk=[r for r in recs_in(list(key_m.keys()),7) if r['direction']!='→']
    wk.sort(key=lambda r:(key_m.get(r['metric_id'],0), r['knowledge_time']), reverse=True)
    def sname(mid):
        if mid in own[t]: return '本体'
        for e in edges:
            if e['to_ticker']==t and e['from_metric']==mid: return {'supply':'供','demand':'需','regime':'政','compete':'竞'}.get(e['side'],'')
        return ''
    moved = (f"{sname(wk[0]['metric_id'])}{wk[0]['direction']} {wk[0]['entity'][:10]}") if wk else '—'
    moved_note = (f"{wk[0]['knowledge_time']} {wk[0]['value']} {wk[0]['unit']} · {wk[0]['direction_note'] or wk[0]['note'][:40]}") if wk else ''
    # 预警：60 天内 ! 或 ↓（预警占优边 / regime / 本体），+ 口径警示
    warn_edges=[e['from_metric'] for e in edges if e['to_ticker']==t and (dominant(e)=='预警' or e['side'] in ('regime','compete'))]
    wr=[r for r in recs_in(set(warn_edges+own[t]),60) if r['direction'] in ('!','↓')]
    kj=[r for mid in own[t] for r in rec_by.get(mid,[]) if ('口径' in r['note'] or 'multi_year_cap' in r['note'] or 'contracted' in r['unit'])]
    warn_n=len(wr)+ (1 if kj else 0)
    warn_note='；'.join(f"{r['entity'][:12]} {r['direction']} {(r['direction_note'] or r['note'])[:36]}" for r in wr[:4]) + ('；口径：合同电力≠并网 / 承诺≠backlog' if kj else '')
    # 领先读：T1/T2 供给 / 需求边 90 天
    lead_e=[e for e in edges if e['to_ticker']==t and tier_of(e) in ('T1','T2') and e['side'] in ('supply','demand')]
    ls=agg(recs_in([e['from_metric'] for e in lead_e if e['side']=='supply'],90)); ld=agg(recs_in([e['from_metric'] for e in lead_e if e['side']=='demand'],90))
    lead = ' '.join(x for x in [f"供{ls}" if ls!='—' else '', f"需{ld}" if ld!='—' else ''] if x) or '—'
    lead_tier = 'T1' if any(tier_of(e)=='T1' for e in lead_e) else ('T2' if lead_e else '')
    nxt = sorted([c for c in cal if c['dated'] and not c['is_past'] and any(mm in set(own[t])|set(side_mids(t,'supply'))|set(dem)|set(reg) for mm in c['metrics'])], key=lambda c: c['date'])
    verify = next((c for c in nxt if any(k in c['event'] for k in ('目标','results','季报','财报','截止'))), nxt[0] if nxt else None)
    mainm = next((m for m in metrics if m['ticker_or_entity'] == t and m['entry'] == '持仓'), None)
    watch.append(dict(ticker=t, weight=WEIGHT[t], st=st, moved=moved, moved_note=moved_note, warn=warn_n, warn_note=warn_note, lead=lead, lead_tier=lead_tier,
        verify=(dict(d=(_d(verify['date'])-asof).days, ev=verify['event'], basis=verify['basis'].split('（')[0]) if verify else None),
        regime=('信念' if t=='NBIS' else ''), main=(mainm['metric_id'] if mainm else ''), group=('core' if t in ('NBIS','RBRK','FCEL') else 'nonai' if t in ('STAA','SLMT') else 'tail')))

# ---- 层 / 独家性 / 阶梯 / 结构 / 90 天时间条 ----
def layer_of(m):
    if m['entry']=='持仓': return '公司数据层'
    return '产业确认层' if (m['dim'] or '').startswith('D1') else 'AI 发展层'
for m in metrics: m['layer']=layer_of(m)
import re as _re2
EXCL_FALLBACK={'e_optics_nbis':'中国侧','e_eoptolink_nbis':'中国侧','e_labfund_nbis':'交叉验证','e_capability_nbis':'公开','e_export_nbis':'公开','e_power_reg_nbis':'公开','e_power_nbis':'公司数据','e_backlog_nbis':'公司数据','e_token_nbis':'公开','e_dcppa_fcel':'公司数据'}
def excl_of(e):
    mm=_re2.search(r'e(0\.\d)', e['notes'] or '')
    if mm:
        v=float(mm.group(1)); return '中国侧 / 独家' if v>=0.85 else ('半公开 / 交叉验证' if v>=0.5 else '公开')
    return EXCL_FALLBACK.get(e['edge_id'], '公开')
for e in edges: e['excl']=excl_of(e); e['tier']=tier_of(e)
CONF={'T1':'可回测','T2':'结构成立','T3':'方向级'}
RUNGS=[('D5','能力前沿','前沿模型还在靠算力堆出来吗'),('D6','范式与成本','需求从训练转向推理了吗，推理单价往哪走'),('D3','前沿 lab 的钱与采购','买算力的人有钱吗、真在买吗、买谁的'),('D2','数据供给','训练数据还够吗、版权规则在变吗'),('D4','人才','顶尖研究员往哪流'),('D7','AI 政策','算力的供给规则在变吗'),('D1','产业确认','上面几级有没有变成在建'),('OWN','公司数据','公司自己报了什么')]
def dim_key(m): return (m['dim'] or '').split('/')[0].strip()
def latest_points(mids, n=2):
    rs=[]
    for mid in mids:
        for r in rec_by.get(mid,[]):
            if r['obs_type'] in ('actual','event','state','target') and r['direction'] not in ('',):
                rs.append(r)
    rs.sort(key=lambda r:r['knowledge_time'], reverse=True)
    out=[]
    for r in rs[:n]:
        out.append(dict(entity=r['entity'], value=r['value'], unit=r['unit'], kt=r['knowledge_time'], dir=r['direction'], note=(r['direction_note'] or r['note'].split('；')[0])[:60], metric_id=r['metric_id']))
    return out
mdict={m['metric_id']:m for m in metrics}
def ladder_for(t):
    ups=[e for e in edges if e['to_ticker']==t]
    rungs=[]
    for key,label,q in RUNGS:
        if key=='OWN':
            mids=own.get(t,[]); es=[]
        else:
            es=[e for e in ups if dim_key(mdict[e['from_metric']])==key]; mids=list({e['from_metric'] for e in es})
        if not mids: continue
        win = 120 if key in ('D5','D6','D2','D4','D3') else 90
        st=agg(recs_in(mids,win))
        tiers=[e['tier'] for e in es]
        conf = '可回测' if 'T1' in tiers else ('结构成立' if 'T2' in tiers else ('方向级' if 'T3' in tiers else ('公司数据' if key=='OWN' else '—')))
        excl=sorted({e['excl'] for e in es}, key=lambda x: ['中国侧 / 独家','半公开 / 交叉验证','公开','公司数据','中国侧','交叉验证'].index(x) if x in ['中国侧 / 独家','半公开 / 交叉验证','公开','公司数据','中国侧','交叉验证'] else 9)
        rungs.append(dict(key=key,label=label,question=q,state=st,conf=conf,n_edges=len(es),n_metrics=len(mids),excl=excl[:2],points=latest_points(mids,2),metrics=mids,layer=('公司数据层' if key=='OWN' else '产业确认层' if key=='D1' else 'AI 发展层')))
    return rungs
def structure_for(t):
    ups=[e for e in edges if e['to_ticker']==t]
    side={k:sum(1 for e in ups if e['side']==k) for k in ('supply','demand','regime','compete','self')}
    tier={k:sum(1 for e in ups if e['tier']==k) for k in ('T1','T2','T3')}
    excl={}
    for e in ups: excl[e['excl']]=excl.get(e['excl'],0)+1
    layer={'AI 发展层':0,'产业确认层':0,'公司数据层':0}
    for e in ups: layer[mdict[e['from_metric']]['layer']]+=1
    return dict(total=len(ups), side=side, tier=tier, excl=excl, layer=layer)
def upcoming_for(rel, days=120):
    out=[]
    for c in cal:
        if not c['dated'] or c['is_past']: continue
        if not any(m in rel for m in c['metrics']): continue
        d=(_d(c['date'])-asof).days
        if d<=days: out.append(dict(date=c['date'], d=d, event=c['event'], basis=c['basis'].split('（')[0], cal_id=c.get('cal_id','')))
    out.sort(key=lambda x:x['d']); return out
for w in watch:
    t=w['ticker']; w['ladder']=ladder_for(t); w['structure']=structure_for(t)
    rel=set(own.get(t,[]))|{e['from_metric'] for e in edges if e['to_ticker']==t}
    w['upcoming']=upcoming_for(rel)
    w['weight_meta']=dict(mv=next((r['note'] for mid in own.get(t,[]) for r in rec_by.get(mid,[]) if r['obs_type']=='position'),''))
# 术语表（内部名 → 界面名）
GLOSS=[('供','上游供给','60 天内供给侧关键边上观测方向的合成','分析'),('需','下游需求','60 天内需求侧关键边上观测方向的合成','分析'),('政','政策环境','60 天内政策 / regime 边上观测方向的合成','分析'),('regime','综合判断','供给态 × 需求态 合流的三态判断，分析师负责','分析'),('信念','同向偏多','供需同向','分析'),('预警','风险提示','60 天内 ! 或 ↓ 的观测计数，含口径警示','分析'),('领先读','领先指标','仅用可回测 / 结构成立的领先边','分析'),('验证点','下一个关键数据','能证实或证伪判断的下一个数据点','用户'),('盯','关注','接下来看什么','用户'),('本体','公司数据','公司自身披露','用户'),('书','持仓','13F 权重','用户'),('打到谁','影响持仓','该节点通过边打到的持仓票','分析'),('多确定','可信程度','边的验证层级','分析'),('T1','可回测','两端可观测时序，lead-lag 可测','分析'),('T2','结构成立','结构论证 + 真值对账','分析'),('T3','方向级','只给方向，不据此定仓位','分析'),('P1','公司公告 / 交易所 / 一手','provenance 一级','方法'),('P2','电话会口径','provenance 二级','方法'),('P3','二手媒体 / 聚合','provenance 三级','方法'),('P4','估算 / 预测','provenance 四级','方法'),('P5','设计层评分','非外部数据','方法'),('owner','分工','A/B/C/D 人机分工','方法'),('可交易度','偏可交易','边的可交易度分数，仅排序','方法'),('预警度','偏预警','边的预警度分数，仅排序','方法'),('跳','传导步数','从票到节点的因果箭头数','分析'),('E3_customer','客户需求','六类边之一','分析'),('假设 A11','方向为分析判断','B 初稿 D 复核，不进阈值','方法')]
with open(os.path.join(ROOT,'data','tables','13-术语表.csv'),'w',newline='',encoding='utf-8') as fh:
    wr=csv.writer(fh, quoting=csv.QUOTE_ALL); wr.writerow(['internal','ui_label','definition','layer']); wr.writerows(GLOSS)

# 未持仓 · 上游可交易实体
POT=[('CRWV','m_crwv_peer'),('300308.SZ','m_cn_optics_zte'),('300502.SZ','m_cn_optics_eoptolink'),('NVDA','m_gpu_ship'),('MSFT','m_capex_msft'),('GOOGL','m_capex_googl'),('AMZN','m_capex_amzn'),('META','m_capex_meta')]
potential=[]
for tk_, mid in POT:
    m=next(x for x in metrics if x['metric_id']==mid)
    rs=sorted([r for r in rec_by.get(mid,[]) if r['direction'] not in ('—','')], key=lambda r:r['knowledge_time'], reverse=True)
    fm = 'm_hyperscaler_capex' if mid.startswith('m_capex_') else mid
    feeds=sorted({e['to_ticker'] for e in edges if e['from_metric']==fm})
    nxt=sorted([c for c in cal if c['dated'] and not c['is_past'] and mid in c['metrics']], key=lambda c:c['date'])
    potential.append(dict(ticker=tk_, mid=mid, name=m['name'], dir=(rs[0]['direction'] if rs else '—'), dir_note=(rs[0]['direction_note'] or rs[0]['note'][:40]) if rs else '', latest=m['value_latest'], feeds=feeds, next=(dict(d=(_d(nxt[0]['date'])-asof).days, ev=nxt[0]['event']) if nxt else None)))
kf_ev = {(k['date'], k['target']): k for k in keyfacts if k['target_type'] == 'event'}
kf_tk = {k['target']: k for k in keyfacts if k['target_type'] == 'ticker'}
for i, r in enumerate(cal):
    r['cal_id'] = f'c{i+1:03d}'
    k = kf_ev.get((r['date'], r['event']))
    r['kf'] = {'brief': k['brief'], 'watch': k['watch'], 'owner': k['owner'], 'status': k['status']} if k else None
for k in kf_tk.values(): k.setdefault('status_line',''); k.setdefault('falsifier','')
data = {'as_of': AS_OF, 'watch': watch, 'potential': potential, 'kf_ticker': kf_tk, 'gloss': GLOSS, 'metrics': metrics, 'edges': edges, 'calendar': cal, 'n_records': len(records)}
payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')

with open(os.path.join(os.path.dirname(__file__), 'template.html'), encoding='utf-8') as fh:
    tpl = fh.read()
html = tpl.replace('__DATA__', payload).replace('__AS_OF__', AS_OF)
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(html)
print('written', OUT, len(html), 'bytes;', len(metrics), 'metrics,', len(records), 'records,', len(edges), 'edges,', len(cal), 'calendar rows')
