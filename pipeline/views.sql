-- ============================================================================
-- 视图层：可推导的一律作视图（doc21 §〇）。看板、健康检查、复验只读视图。
-- 命名沿用 doc21 §四：v_signal_latest（视图 A 监测树）、v_ticker_map（视图 B 蝴蝶结）、v_early_signal。
-- ============================================================================

-- ---------- 四类 fct 统一回接入形态（供上层视图与看板）----------
CREATE OR REPLACE VIEW v_fct AS
SELECT record_id, metric_id, entity_id, obs_type, COALESCE(CAST(value AS TEXT), value_text) AS value, unit, period, knowledge_time, knowledge_date, source_id, source_url, anchor, provenance, owner, status, superseded_by, note, 'fct_quant' AS fct_table FROM fct_quant
UNION ALL SELECT record_id, metric_id, entity_id, 'event', COALESCE(amount_text, CAST(amount AS TEXT)), currency, event_date_text, knowledge_time, knowledge_date, source_id, source_url, anchor, provenance, owner, status, superseded_by, note, 'fct_event' FROM fct_event
UNION ALL SELECT record_id, metric_id, entity_id, 'state', anchor_quote, variable, NULL, knowledge_time, knowledge_date, source_id, source_url, anchor, provenance, owner, status, superseded_by, note, 'fct_opinion' FROM fct_opinion
UNION ALL SELECT record_id, metric_id, entity_id, 'actual', COALESCE(score_text, CAST(score AS TEXT)), benchmark, NULL, knowledge_time, knowledge_date, source_id, source_url, anchor, provenance, owner, status, superseded_by, note, 'fct_frontier' FROM fct_frontier
UNION ALL SELECT record_id, metric_id, NULL, 'position', weight, '13F 权重', period, knowledge_time, knowledge_date, source_id, NULL, NULL, provenance, 'A', 'pass', NULL, note, 'fct_position' FROM fct_position;

CREATE OR REPLACE VIEW v_obs AS                         -- 接入层原样（含实体名、原始 obs_type、来源文本）+ 方向判断 + 路由去向
SELECT s.record_id, s.metric_id, s.entity, s.obs_type, s.value, s.unit, s.period, s.knowledge_time,
       f.knowledge_date, s.source, s.provenance, s.note, s.routed_to,
       m.entry, m.dim, m.ticker_or_entity, m.name AS metric_name,
       COALESCE(d.direction,'—') AS direction, COALESCE(d.direction_note,'') AS direction_note, d.status AS direction_status,
       f.superseded_by
FROM stg_observation s
JOIN metric_registry m ON m.metric_id = s.metric_id
LEFT JOIN v_fct f ON f.record_id = s.record_id
LEFT JOIN observation_direction d ON d.record_id = s.record_id
WHERE f.superseded_by IS NULL;

-- ---------- 指标推导：标题值 / 指引 / 上期 / 仓位（R8）----------
CREATE OR REPLACE VIEW v_metric_headline AS
WITH ranked AS (
  SELECT *, row_number() OVER (PARTITION BY metric_id ORDER BY CASE obs_type WHEN 'actual' THEN 5 WHEN 'event' THEN 4 WHEN 'position' THEN 3 WHEN 'state' THEN 2 WHEN 'computed' THEN 1 END DESC, knowledge_date DESC NULLS LAST, knowledge_time DESC) AS rn
  FROM v_obs WHERE obs_type IN ('actual','event','position','state','computed'))
SELECT metric_id, record_id, entity, obs_type, value, unit, period, knowledge_time, knowledge_date, source, provenance, note FROM ranked WHERE rn = 1;
CREATE OR REPLACE VIEW v_metric_guidance AS                -- 每个目标期间只取最新一版指引（旧版留在记录里，供「上调 / 下调」对照）
WITH g AS (SELECT *, row_number() OVER (PARTITION BY metric_id, period, unit ORDER BY knowledge_date DESC NULLS LAST, knowledge_time DESC) rn FROM v_obs WHERE obs_type IN ('guidance','target'))   -- 同一目标期间 × 同一口径（unit）只取最新版
SELECT metric_id, string_agg(value || COALESCE(' ' || NULLIF(unit,'—'),'') || '（' || period || '）', '；' ORDER BY knowledge_date DESC NULLS LAST) AS expectation_base
FROM g WHERE rn = 1 GROUP BY metric_id;
CREATE OR REPLACE VIEW v_metric_prior AS                   -- 上期值：优先与标题值同一口径（unit 相同）的最近一条，否则任一最近上期
WITH r AS (SELECT o.*, row_number() OVER (PARTITION BY o.metric_id ORDER BY (o.unit = h.unit) DESC, o.knowledge_date DESC NULLS LAST) rn
           FROM v_obs o LEFT JOIN v_metric_headline h USING (metric_id) WHERE o.obs_type='prior')
SELECT metric_id, value || COALESCE(' ' || NULLIF(unit,'—'),'') || '（' || period || '）' AS prior FROM r WHERE rn=1;
CREATE OR REPLACE VIEW v_metric_position AS
WITH r AS (SELECT *, row_number() OVER (PARTITION BY metric_id ORDER BY knowledge_date DESC NULLS LAST) rn FROM v_obs WHERE obs_type='position')
SELECT metric_id, value AS weight, note AS position_note FROM r WHERE rn=1;

-- ---------- 打分（R1–R7）----------
CREATE OR REPLACE VIEW v_metric_score AS
SELECT f.metric_id, m.name, m.entry, m.dim, f.r, f.e, f.l, f.s, f.phi,
       round((SELECT value FROM coefficient WHERE coef_id='w_e')*f.e + (SELECT value FROM coefficient WHERE coef_id='w_s')*f.s
           + (SELECT value FROM coefficient WHERE coef_id='w_r')*f.r + (SELECT value FROM coefficient WHERE coef_id='w_phi')*f.phi, 3) AS valuable_score,
       f.rationale, f.owner, f.status
FROM metric_factor f JOIN metric_registry m USING (metric_id);

CREATE OR REPLACE VIEW v_edge_scored AS                 -- 边 + 记录分数数值化 + tier 归一 + 中间节点数
SELECT e.*, e.map_path AS chain,
       try_cast(replace(tradable_recorded,'~','') AS DOUBLE) AS tradable_num, try_cast(replace(warning_recorded,'~','') AS DOUBLE) AS warning_num,
       split_part(split_part(cert_tier,'（',1),'/',1) AS tier,
       CASE WHEN map_path IS NULL OR map_path='' THEN 0 ELSE length(map_path) - length(replace(map_path,'→','')) + 1 END AS n_intermediate
FROM edge_registry e;

CREATE OR REPLACE VIEW v_edge_calc AS
SELECT e.edge_id, e.from_metric, e.to_ticker, e.side, e.edge_type, e.hops, e.tier, e.is_key, e.chain,
       f.r, f.e AS excl, f.l, f.s, f.phi,
       round((CASE e.tier WHEN 'T1' THEN (SELECT value FROM coefficient WHERE coef_id='base_T1') WHEN 'T2' THEN (SELECT value FROM coefficient WHERE coef_id='base_T2') ELSE (SELECT value FROM coefficient WHERE coef_id='base_T3') END)
             * power((SELECT value FROM coefficient WHERE coef_id='decay'), e.hops), 3) AS c,
       round(least(1.0, (SELECT value FROM coefficient WHERE coef_id='tau_hops')*e.hops + (SELECT value FROM coefficient WHERE coef_id='tau_l')*f.l), 3) AS tau,
       round((CASE e.tier WHEN 'T1' THEN (SELECT value FROM coefficient WHERE coef_id='base_T1') WHEN 'T2' THEN (SELECT value FROM coefficient WHERE coef_id='base_T2') ELSE (SELECT value FROM coefficient WHERE coef_id='base_T3') END) * power((SELECT value FROM coefficient WHERE coef_id='decay'), e.hops) * f.r * f.s * f.phi, 3) AS tradable_calc,
       round(least(1.0, (SELECT value FROM coefficient WHERE coef_id='tau_hops')*e.hops + (SELECT value FROM coefficient WHERE coef_id='tau_l')*f.l) * f.l * f.e, 3) AS warning_calc,
       e.tradable_num AS tradable_recorded, e.warning_num AS warning_recorded,
       CASE WHEN e.tradable_num IS NOT NULL AND abs(e.tradable_num - (CASE e.tier WHEN 'T1' THEN (SELECT value FROM coefficient WHERE coef_id='base_T1') WHEN 'T2' THEN (SELECT value FROM coefficient WHERE coef_id='base_T2') ELSE (SELECT value FROM coefficient WHERE coef_id='base_T3') END) * power((SELECT value FROM coefficient WHERE coef_id='decay'), e.hops) * f.r * f.s * f.phi) > 0.05 THEN '与记录值不一致' END AS reconcile_flag,
       CASE WHEN e.tradable_num IS NULL AND e.warning_num IS NULL THEN '待定'
            WHEN COALESCE(e.tradable_num,0) >= COALESCE(e.warning_num,0) THEN '可交易' ELSE '预警' END AS dominant
FROM v_edge_scored e JOIN metric_factor f ON f.metric_id = e.from_metric;

CREATE OR REPLACE VIEW v_ticker_weight AS
SELECT c.to_ticker, c.edge_id, c.from_metric, c.side, c.tier, c.hops,
       greatest(c.tradable_calc, c.warning_calc) AS strength,
       COALESCE(o.weight_override, round(greatest(c.tradable_calc, c.warning_calc) / sum(greatest(c.tradable_calc, c.warning_calc)) OVER (PARTITION BY c.to_ticker), 3)) AS weight,
       o.weight_override IS NOT NULL AS overridden,
       CASE WHEN c.tradable_calc >= c.warning_calc THEN '可交易' ELSE '预警' END AS dominant_calc
FROM v_edge_calc c
LEFT JOIN (SELECT em.metric_id, etm.ticker, etm.weight_override FROM entity_ticker_map etm JOIN metric_entity em USING (entity_id)) o ON o.metric_id = c.from_metric AND o.ticker = c.to_ticker
WHERE c.hops > 0;

-- ---------- 实体两轴 / 早期信号层（R9）----------
CREATE OR REPLACE VIEW v_entity AS
SELECT e.*, (e.maturity IN ('research','private')) AS early_signal_layer,
       (SELECT count(*) FROM metric_entity me WHERE me.entity_id=e.entity_id) AS n_metrics
FROM entity_master e;
CREATE OR REPLACE VIEW v_early_signal AS
SELECT v.*, m.metric_id, m.data_class,
       CASE WHEN m.data_class LIKE '4%' THEN 'research_frontier' WHEN m.data_class LIKE '2%' AND m.dim LIKE 'D3%' THEN 'startup_vc' WHEN m.dim LIKE 'D4%' THEN 'talent_capital' END AS signal_stream
FROM v_entity v JOIN metric_entity me USING (entity_id) JOIN metric_registry m USING (metric_id) WHERE v.early_signal_layer;

-- ---------- doc21 §四：视图 A / 视图 B ----------
CREATE OR REPLACE VIEW v_metric_latest AS               -- registry + 推导值（看板与视图 A 的基础）
SELECT m.*, h.value AS headline_value, h.unit AS headline_unit, h.entity AS headline_entity, h.period, h.knowledge_time, h.knowledge_date, h.provenance, h.source AS headline_source, h.note AS headline_note,
       g.expectation_base, p.prior, pos.weight, pos.position_note, sc.valuable_score,
       (SELECT count(*) FROM v_obs o WHERE o.metric_id=m.metric_id) AS n_records,
       (SELECT count(*) FROM edge_registry e WHERE e.from_metric=m.metric_id) AS n_edges
FROM metric_registry m
LEFT JOIN v_metric_headline h USING (metric_id) LEFT JOIN v_metric_guidance g USING (metric_id)
LEFT JOIN v_metric_prior p USING (metric_id) LEFT JOIN v_metric_position pos USING (metric_id) LEFT JOIN v_metric_score sc USING (metric_id)
WHERE COALESCE(m.status,'') <> 'deprecated';                         -- deprecated（如非 AI 持仓的经营指标）不进呈现，记录仍在基表与 v_obs 供审计

CREATE OR REPLACE VIEW v_signal_latest AS               -- 视图 A「AI 发展监测树」：按 dim 组织，节点最近方向（三态 = 方向判断；阈值 C6 占位）
SELECT l.metric_id, l.name, l.entry, l.dim, l.data_class, l.signal_role, l.owner, l.lead_time_est, l.valuable_score, l.fill_status,
       d.direction, d.direction_note, l.knowledge_date, l.provenance, l.headline_value, l.headline_unit
FROM v_metric_latest l LEFT JOIN (SELECT o.metric_id, o.direction, o.direction_note FROM v_obs o JOIN v_metric_headline h USING (record_id)) d USING (metric_id);

CREATE OR REPLACE VIEW v_ticker_map AS                  -- 视图 B「持仓蝴蝶结」：按 to_ticker 组织边 + 节点最近状态
SELECT c.to_ticker, c.side, c.edge_type, c.hops, c.tier, c.tradable_calc, c.warning_calc, c.dominant, c.is_key, c.chain, w.weight,
       s.metric_id, s.name AS node_name, s.dim, s.owner, s.direction, s.headline_value, s.headline_unit, s.knowledge_date, s.provenance
FROM v_edge_calc c JOIN v_signal_latest s ON s.metric_id = c.from_metric LEFT JOIN v_ticker_weight w USING (edge_id);

-- ---------- 数据岗：健康 / 复验 / 来源 / 覆盖率 ----------
CREATE OR REPLACE VIEW v_health AS
SELECT m.metric_id, m.name, m.entry, m.dim, m.owner, m.availability, m.fill_status,
       l.n_records, l.knowledge_date AS last_obs, l.provenance,
       try_cast(substr(m.next_release,1,10) AS DATE) AS next_date,
       CASE WHEN try_cast(substr(m.next_release,1,10) AS DATE) < (SELECT max(knowledge_date) FROM v_fct) THEN '过期未更新' END AS overdue,
       CASE WHEN m.fill_status LIKE '已填%' AND COALESCE(l.n_records,0)=0 THEN '已填但无记录' END AS gap_records,
       CASE WHEN m.fill_status LIKE 'placeholder%' THEN 'placeholder' WHEN m.fill_status LIKE '待钉一手%' THEN '待钉一手' WHEN m.fill_status LIKE '付费%' THEN '付费定性' WHEN m.fill_status LIKE '合规%' THEN '合规受限' END AS flag
FROM metric_registry m LEFT JOIN v_metric_latest l USING (metric_id);
CREATE OR REPLACE VIEW v_review_due AS
SELECT o.record_id, o.metric_id, o.entity, o.value, o.provenance, o.knowledge_date, o.source, o.routed_to,
       CASE WHEN o.provenance='P2' THEN '每财报季钉 transcript / IR deck' WHEN o.provenance='P3' THEN '回一手'
            WHEN o.provenance='P4' THEN '实际值出来即替换' WHEN o.provenance='P5' THEN '设计层评分，回测后标定' END AS action
FROM v_obs o WHERE o.provenance IN ('P2','P3','P4','P5') ORDER BY o.provenance, o.knowledge_date;
CREATE OR REPLACE VIEW v_source_master AS
SELECT s.*, (SELECT count(*) FROM v_fct f WHERE f.source_id = s.source_id) AS n_records FROM source_master s;
CREATE OR REPLACE VIEW v_calendar AS
SELECT c.*, (SELECT string_agg(metric_id, ' / ') FROM calendar_metric cm WHERE cm.cal_id=c.cal_id) AS metrics,
       (SELECT k.brief FROM key_fact k WHERE k.target_type='event' AND k.target=c.event AND k.date=c.date LIMIT 1) AS kf_brief,
       (SELECT k.watch FROM key_fact k WHERE k.target_type='event' AND k.target=c.event AND k.date=c.date LIMIT 1) AS kf_watch
FROM calendar c WHERE c.status = 'active';
CREATE OR REPLACE VIEW v_schema_coverage AS              -- 每表每列有值率：设计落地了，值填到哪一步
WITH cols AS (SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='main' AND table_name NOT LIKE 'v_%')
SELECT d.table_name, d.column_name, d.meaning, d.design_ref, d.derivable, d.served_by_view,
       c.column_name IS NOT NULL AS exists_in_db
FROM schema_doc d LEFT JOIN cols c USING (table_name, column_name);

-- ---------- 决策层（R15–R17；JEV-intelligence-graph §五 · PLAN-decision-layer §二）----------
CREATE OR REPLACE VIEW v_decision_health AS             -- 每类判断的吞吐 / 升级率（R16）/ 置信度与 outcome 欠账；替代「填了多少行」的健康观
SELECT r.decision_id, r.name, r.executor_kind, r.executor, r.calib_status, r.owner, r.status,
       count(l.dec_id) AS n_decisions,
       count(*) FILTER (WHERE NOT l.retro) AS n_prospective,
       count(*) FILTER (WHERE NOT l.retro AND l.confidence IS NULL) AS n_missing_confidence,
       count(*) FILTER (WHERE l.escalated) AS n_escalated,
       round(count(*) FILTER (WHERE l.escalated) * 1.0 / NULLIF(count(l.dec_id), 0), 3) AS escalation_rate,
       count(*) FILTER (WHERE l.outcome IN ('correct','wrong','mixed')) AS n_outcome,
       count(*) FILTER (WHERE NOT l.retro AND l.outcome IS NULL) AS n_outcome_gap,
       max(l.decided_at) AS last_decided
FROM decision_registry r LEFT JOIN decision_log l USING (decision_id)
GROUP BY r.decision_id, r.name, r.executor_kind, r.executor, r.calib_status, r.owner, r.status;

CREATE OR REPLACE VIEW v_calibration AS                 -- 校准曲线的表形式（R15）：置信度分桶 vs 命中率；行数会从 0 慢慢长出来
SELECT decision_id, round(confidence, 1) AS conf_bucket, count(*) AS n,
       count(*) FILTER (WHERE outcome = 'correct') AS n_correct,
       round(count(*) FILTER (WHERE outcome = 'correct') * 1.0 / count(*), 3) AS hit_rate,
       round(abs(round(confidence, 1) - count(*) FILTER (WHERE outcome = 'correct') * 1.0 / count(*)), 3) AS calib_error
FROM decision_log WHERE confidence IS NOT NULL AND outcome IN ('correct', 'wrong')
GROUP BY decision_id, round(confidence, 1);

CREATE OR REPLACE VIEW v_divergence AS                  -- 背离清单（R17 布尔版，数值阈值待 C6）：背离 = PROPOSE 触发器，无候选 = 欠账
WITH latest AS (
  SELECT o.metric_id, o.record_id, o.direction, o.direction_note, o.knowledge_date, o.knowledge_time,
         row_number() OVER (PARTITION BY o.metric_id ORDER BY o.knowledge_date DESC NULLS LAST, o.knowledge_time DESC) AS rn
  FROM v_obs o JOIN metric_registry mr USING (metric_id)
  WHERE o.direction <> '—' AND COALESCE(mr.status,'') <> 'deprecated'),         -- deprecated（退出 AI 范围）不触发背离，同 v_metric_latest 不进呈现
lm AS (SELECT * FROM latest WHERE rn = 1),
shock AS (                                              -- ① 记录级：最新未取代观测 direction='!'（冲击需人判）
  SELECT 'record:' || record_id AS div_key, 'shock' AS div_type, metric_id AS subject,
         '! ' || COALESCE(direction_note, '') AS detail, knowledge_date
  FROM lm WHERE direction = '!'),
pair AS (                                               -- ② 票级：同票供给侧与需求侧最新方向相反（三态「背离」的机器可见版）
  SELECT 'ticker:' || e.to_ticker AS div_key, 'supply_demand' AS div_type, e.to_ticker AS subject,
         '供给↑' || sum(CASE WHEN e.side='supply' AND l.direction='↑' THEN 1 ELSE 0 END) || '/↓' || sum(CASE WHEN e.side='supply' AND l.direction='↓' THEN 1 ELSE 0 END)
         || ' · 需求↑' || sum(CASE WHEN e.side='demand' AND l.direction='↑' THEN 1 ELSE 0 END) || '/↓' || sum(CASE WHEN e.side='demand' AND l.direction='↓' THEN 1 ELSE 0 END) AS detail,
         max(l.knowledge_date) AS knowledge_date
  FROM edge_registry e JOIN lm l ON l.metric_id = e.from_metric
  WHERE e.side IN ('supply', 'demand')
  GROUP BY e.to_ticker
  HAVING (sum(CASE WHEN e.side='supply' AND l.direction='↑' THEN 1 ELSE 0 END) > 0 AND sum(CASE WHEN e.side='demand' AND l.direction='↓' THEN 1 ELSE 0 END) > 0)
      OR (sum(CASE WHEN e.side='supply' AND l.direction='↓' THEN 1 ELSE 0 END) > 0 AND sum(CASE WHEN e.side='demand' AND l.direction='↑' THEN 1 ELSE 0 END) > 0))
SELECT d.*,
       (SELECT count(*) FROM candidate_pool c WHERE c.trigger_ref = d.div_key AND c.status IN ('open','selected')) AS n_candidates,
       (SELECT count(*) FROM candidate_pool c WHERE c.trigger_ref = d.div_key AND c.status = 'selected') AS n_selected
FROM (SELECT * FROM shock UNION ALL SELECT * FROM pair) d;

-- ---------- 思路层反查：某表 / 某列是哪个主线节点、哪个决策来的（双向锚定的「数据 → 思路」方向）----------
CREATE OR REPLACE VIEW v_column_origin AS
SELECT a.ref, a.kind,
       CASE WHEN a.kind = 'column' THEN split_part(a.ref, '.', 1) ELSE a.ref END AS table_name,
       CASE WHEN a.kind = 'column' THEN split_part(a.ref, '.', 2) END AS column_name,
       n.node_id, n.seq AS node_seq, n.title AS node_title, f.fork_id, f.question AS fork_question, f.chosen, f.weight, a.how
FROM artifact_anchor a JOIN decision_fork f USING (fork_id) JOIN thesis_node n USING (node_id);
