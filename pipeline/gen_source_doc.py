# -*- coding: utf-8 -*-
"""从库生成《数据来源与处理方法说明》→ ../docs/21-数据来源与处理方法说明.md。叙事段固定，统计表 / 清单从库取，保证与库一致。用法：python3 gen_source_doc.py"""
import duckdb, os, json, re, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
con = duckdb.connect(os.environ.get('ANATOLE_DB') or os.path.join(HERE, 'anatole_ai_monitor.duckdb'), read_only=True)
q = lambda s: con.execute(s).fetchall()
HEAD = q("SELECT max(migration_id) FROM migration_log")[0][0]
n_rec, n_vis = q("SELECT count(*) FROM stg_observation")[0][0], q("SELECT count(*) FROM v_obs")[0][0]
n_src, n_snap = q("SELECT count(*) FROM source_master")[0][0], len([f for f in os.listdir(os.path.join(HERE, 'snapshots')) if f.endswith('.txt')])
def fam(s):
    s = re.sub(r'https?://\S+', '', s or ''); s = re.sub(r'\s*[;；]\s*', '；', s); return s.strip('；； ')[:90]
KIND = {'exchange_filing': '交易所归档', 'ir_release': '公司 IR 稿 / 股东信', 'call_transcript': '电话会转录', 'official': '官方机构文本', 'court': '法院文件', 'company_blog': '公司官方博客 / 定价页', 'data_aggregator': '第三方榜单 / 数据聚合', 'news_media': '媒体', None: '（类型待补）'}
DIM = {'D1': 'D1 算力供给', 'D1/D3': 'D1/D3 同业对照', 'D1/D7': 'D1/D7 数据中心电力', 'D2': 'D2 数据供给', 'D3': 'D3 资本', 'D4': 'D4 人才', 'D5': 'D5 能力与算法前沿', 'D6': 'D6 商用落地 / token 经济', 'D7': 'D7 政策 · 能源 · 安全'}
L = []
A = L.append
A(f'# 21 · 数据来源与处理方法说明\n\n由库生成（`pipeline/gen_source_doc.py`，库头 {HEAD}，{dt.date.today()}）。叙事段是固定的方法，表与清单从库里取，改库后重跑即更新。承 doc 23《数据与资料来源总账》与 doc 24v2 / 29 的来源分层。\n')
A('## 〇 本轮覆盖范围与铺开方式\n')
core = q("SELECT ticker_or_entity, count(*) FROM metric_registry WHERE entry='持仓' AND COALESCE(status,'')<>'deprecated' AND ticker_or_entity IN ('NBIS','RBRK','FCEL') GROUP BY 1 ORDER BY 2 DESC")
n_ai = q("SELECT count(*) FROM metric_registry WHERE entry<>'持仓' AND COALESCE(status,'')<>'deprecated'")[0][0]
A('本轮数据是**以持仓票为例子**收集的：核心三票 **NBIS（51.22%）/ RBRK（29.80%）/ FCEL（7.12%）** 逐字段填到 schema 满（' + '、'.join(f'{t} {n} 个指标' for t, n in core) + '），尾仓 8 只（SUPX / SNDK / MU / INTC / CIEN / MRVL / POET / AMD）只填口径与一条最新 KPI，非 AI 持仓（STAA / SLMT / 0679.HK）只留仓位；AI 侧七维 ' + str(n_ai) + ' 个指标按「先补这些票关键边的上游」的顺序填了第一轮。\n')
A('这一轮的目的不是把 AI 发展的全部数据收齐，而是把**来源体系与处理方法**在真实的票上跑通并固定下来：来源怎么分级、怎么留档、怎么路由、怎么校验、怎么改库，都在下文与代码里。之后铺开规模走同一套方法：新票 = 一个 `migrations/` 脚本（registry 口径 → 本体 KPI → 上游边 → 来源）；新维度 / 新来源 = 先进来源总账分级再采；历史回填 = 同样的登记格式按周 / 季追加。方法不变，只是行数变多。\n')
A('## 一、总原则：全部真数，分五级可溯源\n')
A('**回答「用的都是真实数据吗」**：是。库内没有示例值、没有编造值；每条事实带来源 URL 或交易所归档、P 级、知悉时间、原文锚点与本地快照。「真实」≠ 同一等级，按五级标注：\n')
A('| 级 | 含义 | 判定规则 | 用法 |\n|---|---|---|---|\n| P1 | 一手 / 权威 | 公司公告、交易所归档（EDGAR / 巨潮 / HKEX）、股东信、10-Q、官方机构文本（BIS / Federal Register / EUR-Lex / FERC / IEA）、公司官方博客与定价页、第三方榜单的原始发布（Epoch / AA / ARC 官方 JSON） | 可进定量 |\n| P2 | 管理层电话会口径 | 电话会转录（含转载）、IR deck 口径；数字真实但不是书面披露 | 可进定量，标口径；每财报季复验 |\n| P3 | 二手 / 聚合 | 媒体报道、聚合站、免费研究摘要 | 能回一手就回；否则定性或标时效 |\n| P4 | 估算 / 预测 | 明确非实测（占位系数、外推） | 只做方向，🟠 不进阈值 |\n| P5 | 设计层评分 | 因子、系数、regime 判断——不是外部事实 | 只排序，不当数据核 |\n')
A(f'当前：登记记录 {n_rec} 条（可见 {n_vis}，其余为被取代的旧值，不删），来源 {n_src} 个，原文快照 {n_snap} 份。可见记录按 P 级：' + '、'.join(f'{p} {n}' for p, n in q("SELECT provenance, count(*) FROM v_obs GROUP BY 1 ORDER BY 1")) + '。\n')
A('## 二、来源体系\n')
A('下表是**需求锚定后的已采集清单**，不是 AI 全市场扫描。持仓侧以 13F 核心三票（NBIS / RBRK / FCEL）为主，尾仓只留口径与一条最新 KPI；AI 侧七维只收录接到这些票传导边上的上游节点。方法见 §〇：铺开后行数增加，分级与字段不变。\n')
A('### 2.1 持仓侧（需求锚）\n\n原则：本体 KPI 只认交易所归档与公司稿；电话会口径单独标 P2；13F 仓位来自 SEC 13F-HR。IR 站被拦（403）时改抓 EDGAR 同稿。\n')
A('| 票 | 指标 | 来源族 | 最好 P | 记录 | 快照 |\n|---|---|---|---|---|---|')
for t, mid, name, sf, bp, n, ns in q("""SELECT m.ticker_or_entity, m.metric_id, m.name, m.source_family, min(o.provenance), count(o.record_id), count(DISTINCT f.snapshot_id)
  FROM metric_registry m LEFT JOIN v_obs o USING (metric_id) LEFT JOIN (SELECT record_id, snapshot_id FROM fct_quant UNION ALL SELECT record_id, snapshot_id FROM fct_event UNION ALL SELECT record_id, snapshot_id FROM fct_opinion) f ON f.record_id=o.record_id
  WHERE m.entry='持仓' AND COALESCE(m.status,'')<>'deprecated' AND m.ticker_or_entity IN ('NBIS','RBRK','FCEL') GROUP BY 1,2,3,4 ORDER BY 1,2"""):
    A(f'| {t} | {name} | {fam(sf)} | {bp or "—"} | {n} | {ns} |')
A('\n尾仓 8 只（SUPX / SNDK / MU / INTC / CIEN / MRVL / POET / AMD）：13F 仓位 + 各一条最新季度 KPI（8-K Ex.99.1 / IR 稿，全 P1），只填口径不扩 KPI。非 AI 持仓（STAA / SLMT / 0679.HK）只留仓位事实。\n')
A('### 2.2 AI 侧七维：每维用什么源\n\n来源族按维度列出，「最好 P」是该指标名下记录的最高级别；AI 发展的「消息来源」不是一份订阅列表，而是按维度分层的一手 → 二手清单。\n')
for dim, label in DIM.items():
    rows = q(f"""SELECT m.metric_id, m.name, m.source_family, min(o.provenance), count(o.record_id), m.frequency, m.availability
      FROM metric_registry m LEFT JOIN v_obs o USING (metric_id) WHERE m.dim='{dim}' AND m.entry<>'持仓' AND COALESCE(m.status,'')<>'deprecated' GROUP BY 1,2,3,6,7 ORDER BY 1""")
    if not rows: continue
    A(f'\n**{label}**\n\n| 指标 | 来源族 | 最好 P | 记录 | 频率 | 可得 |\n|---|---|---|---|---|---|')
    for mid, name, sf, bp, n, fq, av in rows: A(f'| {name} | {fam(sf)} | {bp or "—"} | {n} | {fq} | {av} |')
A('\n**一等源清单（doc 24v2 §1.3 + 本轮实际接入）**\n')
A('- D1 算力：云厂四家 8-K Ex.99.1 / 10-Q（现金流量表 PP&E 口径）、NVIDIA 官方稿 + CFO commentary、中际旭创 / 新易盛巨潮公告原文、Nebius / Lambda 官方价格页；付费未接：SemiAnalysis / TrendForce（HBM / CoWoS 只定性）。\n- D2 数据：DOJ / S.D.N.Y. 法院文件、Reddit / Wiley 8-K、Meta newsroom、Scale AI 官方博客、arXiv 一手论文页。\n- D3 资本：Anthropic / xAI / Reflection / Cohere 官方稿、软银官方公告、SpaceX / NVIDIA 10-Q 附注、Nebius newsroom；付费未接：PitchBook / Crunchbase 全库（只用免费 H1 报告，P3）。\n- D4 人才：合规受限（领英 ToS），只登记原则，不采。\n- D5 前沿：Epoch AI trends、Artificial Analysis 榜单 / 内嵌 JSON、ARC Prize 官方 JSON、swebench.com、LMArena、Hugging Face API、lab 官方博客（DeepMind / NVIDIA）。\n- D6 落地：OpenAI / Anthropic / Google 官方定价页与 changelog、OpenRouter rankings（P3，只代表路由一角）、QuestMobile 免费摘要（P3）、RBRK 本体 KPI 作企业 adoption 一手样本。\n- D7 政策 · 能源：Federal Register / govinfo、BIS 新闻稿与 PDF、白宫 232 公告、EUR-Lex、加州 leginfo、FERC 文件（ferc.gov 403 时用 Wayback 存档并注明）、Vistra 8-K、IEA 官方页、国家数据局 / 工信部原文、OpenAI 事故技术报告。\n')
A('### 2.3 前沿雷达的源分层（doc 29）\n\n第四类前沿是「监测 AI 发展」最本源的领域，但标的驱动天然拉不到多少，所以 topic-driven 独立采集，源按三维打标：\n\n| 维 | 分档 |\n|---|---|\n| 质量 / 权威 | T_a 一手权威（peer-reviewed 顶会、官方 technical report / model card、第三方实测 Epoch / AA）> T_b 半权威（arXiv 预印、大厂官方博客含 PR 成分）> T_c 社媒 / 自媒体 |\n| 频率 | 日（arXiv / X / HF）· 周（榜单 / AA）· 会议周期（顶会）· 事件（发布） |\n| 立场 | 中立（学术 / 第三方评测）vs 有立场（厂商 PR 自报 SOTA、自媒体流量） |\n\n使用层次：T_a × 中立 → 可入信号；T_b / 有立场 → 先证伪 + 降权，入 watchlist；T_c → 只做早期线索，触发去查一手。证伪四手段落成 `fct_frontier` 两道闸字段：`source_stance`（neutral / vendor_pr / social）与 `verifiability`（reproducible / third_party_verified / claimed_only / rumor）；`industry_impact` 由人判。顶会按方向（通用 ML：NeurIPS / ICML / ICLR；视觉：CVPR / ICCV；NLP：ACL / EMNLP；RL / 机器人：CoRL / RSS；系统：MLSys / OSDI），lab 按厂 × focus × 发表平台分管道，社媒默认低权重。\n')
A('### 2.4 来源统计（source_master）\n')
A('| 类型 | 个数 |\n|---|---|'); [A(f'| {KIND.get(k, k)} | {n} |') for k, n in q("SELECT source_kind, count(*) FROM source_master GROUP BY 1 ORDER BY 2 DESC")]
A('\n| 级别 | 个数 |\n|---|---|'); [A(f'| {k or "—"} | {n} |') for k, n in q("SELECT source_tier, count(*) FROM source_master GROUP BY 1 ORDER BY 1")]
A('\n| 可访问性 | 个数 | 处理 |\n|---|---|---|\n| open | %d | 直接抓，存快照 |\n| blocked | %d | 记 access=blocked，换 EDGAR 同稿 / Wayback / 官方 PDF，不假装还能取 |\n| paywall | %d | 只用免费摘要定性，标 P3 |' % tuple(dict(q("SELECT access, count(*) FROM source_master GROUP BY 1")).get(k, 0) for k in ('open', 'blocked', 'paywall')))
A('\n封锁与付费明细：' + '；'.join(f'{n}（{a}，{v}）' for s, n, a, v in q("SELECT source_id, name, access, verify_status FROM source_master WHERE access<>'open' ORDER BY access")) + '。\n')
A('## 三、采集与留档\n')
A('- **一行一个事实**：登记格式固定为 record_id · metric_id · entity · obs_type（actual / prior / guidance / target / event / state / position / computed）· value · unit · period · knowledge_time · source（名 + URL）· provenance · note。\n- **快照**：每个来源存一份原文文本 `pipeline/snapshots/<snapshot_id>.txt`，头三行 = 标题 / URL / 抓取时间与方式；SEC 用 EDGAR accession，PDF 用 pdftotext，IR 站 403 时改 EDGAR 或浏览器抓取并注明。快照文件必须存在（校验 7f），且记录的原文锚点必须在快照文中（校验 7t，双栏 PDF 只部分命中时 WARN 请人工核）。\n- **锚点**：note 里的 “…” 原文引语自动抽成 anchor；写原文不写转述。\n- **知悉时间按原文粒度**：日 / 月 / 季 / 年，不伪造精度（月 → 15 日只供排序，季 / 年 → NULL）；价格页 / 榜单无发布日时以抓取日登记并在 note 标明（计划 B 加 published / observed 标记）。\n- **事件日**：可解析成日才填 event_date；否则 NULL + `event_date_precision`（quarter / half / year / unknown），不用知悉日兜底。\n- **旧值不删**：纠错 = 新记录 + superseded_by；指引新版本靠 knowledge_time 与 revision_flag 区分；分类纠正（如 P4 → P1）记 change_log。\n- **口径差异写进口径列**：合同电力 ≠ 并网电力、客户承诺 ≠ GAAP backlog、adjusted net new ≠ 未调整、现金 capex ≠ 含融资租赁 ≠ 应计口径、committed ≠ awarded ≠ pipeline；一个指标一种量，混装即拆。\n')
A('## 四、处理链（从登记到看板）\n')
A('| 步 | 做什么 | 规则 / 代码 | 输出 |\n|---|---|---|---|\n| 1 登记 | 一行一个事实进 `stg_observation` | `migrations/NNNN.py` 的 `m.observe()` | 记录 + change_log |\n| 2 路由 | 按指标 data_class 分到四类事实表 | `core.route`：类 4 → fct_frontier；类 3 → fct_opinion；数值 / 类 1 → fct_quant；event / state → fct_event；position → fct_position | fct_* + 通用元数据（来源 / 锚点 / 快照 / 置信 / 状态） |\n| 3 来源入账 | 来源作一等对象 | `core.upsert_source` → `source_master`（类型 / 级别 / 可访问性 / 复验状态）；封锁与付费由 `source_override` 覆盖 | 来源总账 |\n| 4 判断 | 方向 / 因子 / 边定档 / 简报 | 判断表各带 owner / status；规则给初稿（B / rule），人（D）复核置 reviewed；决策层 `decision_log` 记六元组 | 判断账 |\n| 5 推导 | 标题值 / 上期（同比或环比）/ 指引最新版 / 打分 | `views.sql`：v_metric_headline / prior / guidance；R1–R7 打分（系数在 `coefficient`，全部登记为假设）；R14 as-of；R18 / R19 同比环比 | 视图 A / B、看板 JSON |\n| 6 校验 | 约束之外的业务规则 | `checks.py` 30 余条：路由完整、字典完整、证据属上游、快照存在、锚点在文中、时点不先知、权重 Σ=1、provenance 值域、打分对账、背离欠账、判断纪律、生成物落后 | ERROR 必清零 |\n| 7 改库账 | 每次改库一个编号脚本 | `migrate.py`：事务、checksum、字段级 `change_log`（表 / 行 / 列 / 改前 / 改后 / 依据 / owner） | 从零重放 = 增量应用 |\n| 8 出图 | 看板 / 字典 / 浏览器 | `build_dashboard.py` / `gen_schema_doc.py` / `gen_browser.py`，首行带库头 | 生成物 |\n')
A('## 五、复验与已知缺口（诚实收尾）\n')
rv = dict(q("SELECT provenance, count(*) FROM v_review_due GROUP BY 1"))
A(f'- **复验队列**（`v_review_due`）：P2 {rv.get("P2",0)} 条每财报季钉 transcript / IR deck；P3 {rv.get("P3",0)} 条回一手；P4 {rv.get("P4",0)} 条实际值出来即替换；P5 {rv.get("P5",0)} 条是设计层评分不核。\n')
A('- **占位 / 未标定**：海关 HS8517 → 光模块占比系数（C1，🟠 用前必标定，标定前只做方向）；HBM / CoWoS 与 800G 出货为付费源只定性；人才维度合规受限只登记原则；pre-IPO 池只用免费 H1 报告。\n')
A('- **来源治理待做（审计 B）**：44 个来源类型待补、同一来源多 id 的合并、verify_status 由人定而非默认 confirmed、published / observed 知悉基准、13F 补 EDGAR accession 链接、许可转录文本的入库政策。\n')
A('- **信号深度**：周频指标多数只有一次快照，季频最多 5 期；作为「监测」还需按周回填历史（计划 B）。\n')
out = os.path.join(ROOT, 'docs', '21-数据来源与处理方法说明.md')
open(out, 'w', encoding='utf-8').write('\n'.join(L)); print('written', out, len(L), 'lines')
