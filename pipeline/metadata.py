# -*- coding: utf-8 -*-
"""元数据：字段字典 / 表间关系 / 计算规则。SCHEMA.md 由这里生成（gen_schema_doc.py）。
每个库里的列都必须在 SCHEMA_DOC 里有一条，load_csv.py 会校验。"""
COMMON_FCT = {  # 通用元数据层（doc17 §2.1）
  'record_id': ('记录主键，来自接入层 stg_observation', 'doc17 §2.1 溯源'),
  'metric_id': ('挂到哪个指标（真源 R）', 'doc17 §2.1 关联'),
  'entity_id': ('主实体（entity_master）', 'doc17 §2.1 关联'),
  'knowledge_time': ('何时可知（as-of），按原文粒度：日 / 月 / 季 / 年；回测生命线', 'doc17 §2.1 溯源'),
  'knowledge_date': ('knowledge_time 解析成日期（月→15 日；年 / 季→NULL），供排序与窗口，不伪造精度', '实现'),
  'source_id': ('来源（source_master）', 'doc17 §2.1 溯源 / doc23'),
  'source_url': ('来源 URL', 'doc17 §2.1 溯源'),
  'anchor': ('原文锚点 / 页码 / 时间码 / 短引', 'doc17 §2.1 溯源'),
  'snapshot_id': ('原始快照 id（raw 湖）', 'doc17 §2.1 溯源'),
  'ingest_time': ('入库时间', 'doc17 §2.1 溯源'),
  'provenance': ('可信度五级 P1 一手 / P2 电话会口径 / P3 二手 / P4 估算预测 / P5 设计层评分', 'doc23 §一'),
  'owner': ('人机分工 A AI独立·人抽检 / B AI初稿·人必复核 / C 人定义·AI执行 / D 人定', 'doc09 / doc17 §2.1 质量'),
  'confidence': ('抽取置信度', 'doc17 §2.1 质量'),
  'code_score': ('代码闸门得分（JSON；Langfuse trace 锚点）', 'doc17 §2.1 质量'),
  'judge_score': ('LLM judge 得分', 'doc17 §2.1 质量'),
  'status': ('pass / pending（待人工）/ rejected', 'doc17 §2.1 质量'),
  'superseded_by': ('旧值不删，标被哪条记录取代（与 revision_flag 同构）', 'doc23 §五'),
  'note': ('备注 / 口径说明', '实现'),
}
T = {}
T['stg_observation'] = {
  'record_id': ('登记记录主键 r###', '实现'), 'metric_id': ('指标 id', 'doc21'), 'entity': ('实体名（文本，路由后映射 entity_id）', '实现'),
  'obs_type': ('actual 实测 / prior 上期 / guidance 指引 / target 目标 / event 事件 / state 状态 / position 仓位 / computed 计算值', '实现'),
  'value': ('值（文本原样）', '实现'), 'unit': ('单位 / 口径短语', '实现'), 'period': ('期间', '实现'), 'knowledge_time': ('何时可知，原文粒度', 'doc17'),
  'source': ('来源名 + URL', 'doc23'), 'provenance': ('P1–P5', 'doc23'), 'note': ('备注 / 原文短引 / 假设 id', '实现'), 'routed_to': ('路由到的资产表', '实现'),
}
T['entity_master'] = {
  'entity_id': ('实体主键 ent_*', 'doc21 §一'), 'name': ('名称', 'doc21 §一'), 'aliases': ('别名（JSON 数组；Postgres TEXT[]）', 'doc21 §一'),
  'type': ('company / institution / person / track / index', 'doc21 §一'), 'layer': ('价值栈 L1 硬件 … L6 具身（在哪变现）；两轴之一', 'doc16 §二 / doc21 §一'),
  'maturity': ('成熟度 research / private / pre_ipo / public（信号多早）；两轴之二。早期信号层 = maturity∈research/private 的视图', 'doc16 §三 / doc21 §〇'),
  'track': ('赛道', 'doc21 §一'), 'country': ('CN / US / HK / EU / other；中国侧是附加标签不是主判据', 'doc16 §六'), 'ticker': ('公开票代码', 'doc21 §一'),
  'parent_id': ('母实体', 'doc21 §一'), 'in_book': ('是否 13F 持仓', '实现'), 'created_at': ('创建时间', 'doc21 §一'), 'owner': ('分工', 'doc09'), 'status': ('draft / reviewed / retired', '实现'),
}
T['entity_ticker_map'] = {
  'map_id': ('主键', 'doc21 §一'), 'entity_id': ('实体', 'doc21 §一'), 'ticker': ('影响哪只公开票', 'doc21 §一'),
  'relation': ('self / supplier / customer / competitor / supply_chain_read / demand_driver', 'doc21 §一'), 'map_path': ('传导链（补丁③）', 'doc18 补丁③'),
  'weight_override': ('人工覆盖权重（owner D）；默认权重由 v_ticker_weight 推导', 'doc21 §6.4'), 'owner': ('分工', 'doc09'), 'status': ('draft / reviewed / retired', '实现'),
}
T['metric_entity'] = {'metric_id': ('指标', '实现'), 'entity_id': ('实体（一指标可挂多实体，如 hyperscaler 合计）', '实现')}
T['metric_registry'] = {
  'metric_id': ('指标主键 m_*（真源 R 的节点）', 'doc21 §二'), 'name': ('名称', 'doc21 §二'), 'entity_id': ('主实体', 'doc21 §二'), 'ticker_or_entity': ('登记时的实体 / 票标签（原文）', '实现'), 'entry': ('入口：持仓（需求侧）/ AI（供给侧）', 'doc33 §〇'),
  'track': ('赛道', 'doc21 §二'), 'layer': ('价值栈 L1–L6（由主实体继承）', 'doc21 §二'), 'dim': ('AI 发展七维 D1–D7', 'doc24v2'),
  'data_class': ('1 量价 / 2 事件 / 3 观点 / 4 前沿（决定落哪张 fct）', 'doc17 §一'), 'signal_role': ('predictor / expectation_base / regime / arbiter / human_input', 'doc17 §2.1'),
  'source_ids': ('来源 id 列表（JSON）', 'doc21 §二'), 'source_family': ('来源族描述', '实现'), 'frequency': ('更新频率', 'doc21 §二'),
  'lead_time_est': ('领先期先验（补丁④，假设 B*）', 'doc18 补丁④ / doc30'), 'kou_jing': ('口径定义', 'doc21 §二'), 'unit': ('单位', 'doc21 §二'),
  'owner': ('分工', 'doc09'), 'upstream_deps': ('上游依赖（JSON）', 'doc21 §二'), 'availability': ('🟢一手公开 🟡待钉一手 🔵付费 ⚪placeholder / 合规', 'doc28 §一'),
  'next_release': ('下次发布', '实现'), 'next_release_basis': ('依据：公司公告 / 规则推定 / 估计 / 待定', '实现'),
  'status': ('testing / production / deprecated', 'doc21 §二'), 'fill_status': ('填数状态：已填 / 待填 / 待钉一手 / 付费定性 / placeholder / 合规受限', '实现'),
  'notes_assumption_ids': ('备注与引用的假设 id', 'doc30'), 'last_validated': ('最近验证日', 'doc21 §二'),
}
T['edge_registry'] = {
  'edge_id': ('边主键 e_*（真源 E）', 'doc21 §二.5'), 'from_metric': ('上游 AI 节点', 'doc21 §二.5'), 'to_ticker': ('持仓票', 'doc21 §二.5'),
  'side': ('supply / demand / regime / compete / self（蝴蝶结左右 / 顶带）', 'doc25 §五'), 'edge_type': ('六类边 E1 本体 … E6 资金人才流', 'doc25 §1.1'),
  'hops': ('跳数 = 从票的利润因子反推到节点跨过的因果箭头数', 'doc25 §1.2'), 'map_path': ('中间机制节点（→ 分隔）；跳数 = 中间节点数 + 1', 'doc25 §1.2 / A10'),
  'mechanism': ('机制描述', 'doc21 §二.5'), 'cert_tier': ('T1 可回测 / T2 结构 + 真值对账 + 敏感性 / T3 方向不下注', 'doc25 §六'), 'cert_method': ('验证方法', 'doc25 §六'),
  'cert_score': ('验证得分（回测 / 对账写回）', 'doc21 §二.5'), 'lead_measured': ('实测领先期', 'doc21 §二.5'),
  'tradable_recorded': ('记录的可交易度（doc28 手写 / 早期计算）；推导值见 v_edge_calc', 'doc25 §1.3'), 'warning_recorded': ('记录的预警度', 'doc25 §1.3'),
  'is_key': ('重点 ★ 计数', 'doc25 §二'), 'evidence_ids': ('证据记录 / trace id（JSON）', 'doc21 §二.5'), 'evidence': ('证据描述', '实现'),
  'owner': ('分工', 'doc09'), 'status': ('testing / production / deprecated', 'doc21 §二.5'), 'notes': ('备注（含因子赋值理由）', '实现'), 'last_validated': ('最近验证日', 'doc21 §二.5'),
}
def fct(extra):
  d = dict(COMMON_FCT); d.update(extra); return d
T['fct_quant'] = fct({
  'obs_type': ('actual / prior / guidance / target / computed', '实现'), 'period': ('期间文本', 'doc21 §三'), 'period_start': ('期间起', 'doc21 §三 DATERANGE'), 'period_end': ('期间止', 'doc21 §三 DATERANGE'),
  'value': ('数值', 'doc21 §三'), 'value_text': ('无法数值化的原文（区间 / ≈ / ±）', '实现'), 'unit': ('单位', 'doc21 §三'), 'currency': ('币种', 'doc21 §三'),
  'yoy': ('同比', 'doc21 §三'), 'qoq': ('环比', 'doc21 §三'), 'revision_flag': ('initial / revised', 'doc21 §三'),
  'conversion_assumption': ('换算假设（补丁①，如海关占比系数）', 'doc18 补丁①'), 'assumption_source': ('换算假设的来源', 'doc18 补丁①'),
})
T['fct_event'] = fct({
  'event_type': ('funding / launch / personnel / order / approval / contract / policy / litigation / investment / pricing / other', 'doc21 §三（扩展）'),
  'subject_entity': ('主体', 'doc21 §三'), 'object_entity': ('客体', 'doc21 §三'), 'relation': ('关系', 'doc21 §三'),
  'amount': ('金额', 'doc21 §三'), 'amount_text': ('无法数值化的金额原文', '实现'), 'currency': ('币种', 'doc21 §三'),
  'amount_type': ('one_time / multi_year_cap / annualized / range（补丁②）', 'doc18 补丁②'), 'is_estimate': ('是否估算', 'doc18 补丁②'), 'round': ('融资轮次', 'doc21 §三'),
  'event_date': ('事件日期', 'doc21 §三'), 'event_date_text': ('事件日期原文', '实现'),
})
T['fct_opinion'] = fct({
  'variable': ('表述变量（单价 / 利用率 / regime …）', 'doc21 §三'), 'speaker': ('发言人', 'doc21 §三'), 'speaker_role': ('management / analyst_q / expert / media / official', 'doc21 §三'),
  'level': ('分级', 'doc21 §三'), 'strength': ('强度', 'doc21 §三'), 'direction': ('方向', 'doc21 §三'), 'anchor_quote': ('原话锚点', 'doc21 §三'),
  'codebook_version': ('codebook 版本', 'doc21 §三'), 'model_version': ('模型版本', 'doc21 §三'),
})
T['fct_frontier'] = fct({
  'doc_id': ('文献 / 榜单 id', 'doc21 §三'), 'topic_cluster': ('主题簇', 'doc21 §三'), 'method': ('方法', 'doc21 §三'), 'benchmark': ('基准', 'doc21 §三'),
  'score': ('分数', 'doc21 §三'), 'score_text': ('无法数值化的分数原文', '实现'), 'institution': ('机构', 'doc21 §三'), 'authors': ('作者（JSON）', 'doc21 §三'), 'citation_velocity': ('引用速度', 'doc21 §三'),
  'source_stance': ('neutral / vendor_pr / social（证伪闸）', 'doc29 §四'), 'verifiability': ('reproducible / third_party_verified / claimed_only / rumor（证伪闸）', 'doc29 §四'),
  'industry_impact': ('产业影响 高 / 中 / 低（影响力闸，owner D；量化占位 C8）', 'doc29 §四'), 'impact_rationale': ('影响力理由', 'doc29 §四'),
})
T['fct_position'] = {
  'record_id': ('记录主键', '实现'), 'metric_id': ('指标', '实现'), 'ticker': ('票', '实现'), 'period': ('13F 期间', '实现'), 'weight': ('13F 权重', 'xlsx'), 'note': ('市值 / 股数 / 操作', 'xlsx'),
  'knowledge_time': ('申报日', 'doc17'), 'knowledge_date': ('申报日解析', '实现'), 'source_id': ('来源', 'doc23'), 'provenance': ('P 级', 'doc23'),
}
T['source_master'] = {
  'source_id': ('来源主键 src_*', 'doc23 §二'), 'name': ('名称', 'doc23 §二'), 'publisher': ('发布方', 'doc23 §二'), 'source_tier': ('P1–P5', 'doc23 §二'),
  'source_kind': ('ir_release / exchange_filing / prospectus / customs / call_transcript / broker_research / news_media / data_aggregator / official / court / company_blog / api', 'doc23 §二（扩展）'),
  'data_class': ('供给哪几类数据（JSON）', 'doc23 §二'), 'covers_entity': ('覆盖实体（JSON）', 'doc23 §二'), 'covers_metric': ('覆盖指标（JSON）', 'doc23 §二'), 'url': ('URL', 'doc23 §二'),
  'access': ('open / paywall / blocked', 'doc23 §二'), 'frequency': ('频率', 'doc23 §二'), 'reliability_note': ('为何是这个 tier / 软肋', 'doc23 §二'),
  'verify_status': ('confirmed / pending / stale / placeholder', 'doc23 §二'), 'superseded_by': ('旧源不删，标被谁取代', 'doc23 §二'), 'first_seen': ('首见', 'doc23 §二'), 'last_validated': ('最近核验', 'doc23 §二'),
}
T['assumption'] = {'assumption_id': ('A 打分系数 / B 领先期 / C 领域 / R 退役', 'doc30'), 'section': ('分区', 'doc30'), 'text': ('假设内容', 'doc30'), 'current_value': ('当前值', 'doc30'),
  'kind': ('先验 / 占位 / 预测 / 设计选择 / 时效 / 领域事实', 'doc30 §〇'), 'impact': ('🔵仅排序 / 🟠也影响绝对量（未验证禁用于 sizing 与阈值）', 'doc30 §〇'), 'refine_by': ('用什么细化', 'doc30 §〇'), 'status': ('assumption / calibrating / validated / retired / placeholder', 'doc30 §〇')}
T['coefficient'] = {'coef_id': ('系数 id', 'doc21 §六'), 'value': ('值', 'doc21 §六'), 'assumption_id': ('挂哪条假设', 'doc30 §一'), 'note': ('说明', '实现')}
T['metric_factor'] = {'metric_id': ('节点', 'doc21 §6.1'), 'r': ('可靠性（provenance→r，A8）', 'doc21 §6.1'), 'e': ('独家性', 'doc21 §6.1'), 'l': ('固有领先性', 'doc21 §6.1'), 's': ('可观测 / 信噪', 'doc21 §6.1'), 'phi': ('频率适配', 'doc21 §6.1'),
  'rationale': ('赋值理由', '实现'), 'owner': ('分工', 'doc09'), 'status': ('draft / reviewed / retired', '实现')}
T['observation_direction'] = {'record_id': ('记录', 'A11'), 'direction': ('↑增强 / ↓削弱 / →中性 / !冲击需人判 / —不适用，相对所喂持仓票的 thesis', 'A11'), 'direction_note': ('一句理由', 'A11'), 'owner': ('分工', 'doc09'), 'status': ('draft / reviewed / retired', '实现')}
T['key_fact'] = {'kf_id': ('简报 id', '实现'), 'target_type': ('event / ticker / metric', '实现'), 'date': ('事件日', '实现'), 'target': ('事件名 / 票 / 指标', '实现'), 'brief': ('前因 / 关键数据 / 相关方 / 后果', '实现'), 'watch': ('盯什么', '实现'), 'refs': ('引用记录', '实现'), 'owner': ('分工', 'doc09'), 'status': ('draft / reviewed / retired', '实现')}
T['source_override'] = {'source_pattern': ('子串匹配来源名', '实现'), 'access': ('open / paywall / blocked', 'doc23'), 'verify_status': ('confirmed / pending / stale / placeholder', 'doc23'), 'note': ('说明', '实现')}
T['calendar'] = {'cal_id': ('排期 id', '实现'), 'date_raw': ('日期原文 / event / weekly', '实现'), 'date': ('日期', '实现'), 'date_precision': ('精度：day / window / deadline', '实现'), 'event': ('事件', '实现'),
  'entity_or_ticker': ('实体 / 票', '实现'), 'dim_or_entry': ('维 / 入口', '实现'), 'related_metric': ('相关指标（文本）', '实现'), 'basis': ('已发生 / 公司公告 / 规则推定 / 估计 / 待核 / 待定 / 事件驱动', '实现'), 'source_or_rule': ('依据来源或规则', '实现'), 'notes': ('备注', '实现'), 'status': ('active / retired：retired = 事件与 AI 发展无关（非 AI 持仓业绩等），不进呈现', 'E46')}
T['calendar_metric'] = {'cal_id': ('排期', '实现'), 'metric_id': ('指标', '实现')}
T['schema_doc'] = {'table_name': ('表', '元数据'), 'column_name': ('列', '元数据'), 'meaning': ('含义', '元数据'), 'design_ref': ('设计出处', '元数据'), 'derivable': ('设计为字段但可推导', 'doc21 §〇'), 'served_by_view': ('由哪个视图提供', 'doc21 §〇')}
T['relation_doc'] = {'from_table': ('从表', '元数据'), 'from_col': ('从列', '元数据'), 'to_table': ('到表', '元数据'), 'to_col': ('到列', '元数据'), 'cardinality': ('基数', '元数据'), 'meaning': ('含义', '元数据')}
T['calc_rule'] = {'rule_id': ('规则 id', '元数据'), 'name': ('名称', '元数据'), 'formula': ('公式', '元数据'), 'inputs': ('输入', '元数据'), 'output_view': ('输出视图', '元数据'), 'assumption_ids': ('挂的假设', 'doc30'), 'design_ref': ('设计出处', '元数据'), 'note': ('说明', '元数据')}
T['etl_log'] = {'run_id': ('运行 id', '元数据'), 'run_at': ('时间', '元数据'), 'step': ('步骤', '元数据'), 'rows_in': ('输入行', '元数据'), 'rows_out': ('输出行', '元数据'), 'note': ('说明', '元数据')}
T['migration_log'] = {'migration_id': ('改库脚本编号 NNNN_name（migrations/）', '元数据'), 'applied_at': ('应用时间', '元数据'), 'checksum': ('脚本 sha256 前 16 位；应用后脚本不可再改', '元数据'), 'owner': ('本次改库的 owner', '元数据'), 'n_changes': ('写入 change_log 的行数', '元数据'), 'note': ('脚本 docstring 第一行', '元数据')}
T['change_log'] = {'change_id': ('改动 id = migration_id-序号', '元数据'), 'migration_id': ('属于哪次改库', '元数据'), 'table_name': ('改了哪张表', '元数据'), 'pk': ('哪一行（主键值）', '元数据'), 'column_name': ('哪一列；整行新增记 (insert)', '元数据'),
  'old_value': ('改前值（文本）', '元数据'), 'new_value': ('改后值（文本）', '元数据'), 'basis': ('依据：原文页码 / 快照 id / doc 编号 / 规则', 'doc14 A1 可溯源'), 'owner': ('A–D', 'doc09'), 'applied_at': ('应用时间', '元数据')}
T['thesis_node'] = {'node_id': ('主线节点 N1–N7', '思路层'), 'seq': ('顺序', '思路层'), 'title': ('标题', '思路层'), 'question': ('这一节点在问什么', '思路层'), 'conclusion': ('核心结论', '思路层'), 'rings': ('对应思维链环号', 'doc31 / 17'), 'doc_refs': ('出处 doc / E##', '思路层'), 'owner': ('A–D', 'doc09'), 'status': ('draft / reviewed / retired', '思路层')}
T['decision_fork'] = {'fork_id': ('分叉 id F<节点>.<序>', '思路层'), 'node_id': ('属于哪个主线节点', '思路层'), 'seq': ('顺序', '思路层'), 'question': ('分叉在问什么', '思路层'), 'options': ('备选方案 JSON 数组', '思路层'), 'chosen': ('最终选择', '思路层'), 'rationale': ('决策依据', '思路层'), 'before_after': ('改前 → 改后', 'doc31 纠偏格式'), 'weight': ('core 面试主讲 / detail 折叠', '认知 7±2'), 'log_ref': ('环 / E## / doc', '思路层'), 'owner': ('A–D', 'doc09'), 'status': ('draft / reviewed / retired', '思路层')}
T['artifact_anchor'] = {'anchor_id': ('锚点 id', '思路层'), 'fork_id': ('来自哪个决策', '思路层'), 'kind': ('table / column / view / rule / assumption / coefficient / check / migration / file', '思路层'), 'ref': ('引用：表 / 表.列 / 视图 / R# / A# / 系数 / 校验号 / 脚本 / 路径', '思路层'), 'how': ('这一产物怎么体现该决策', '思路层')}
# 决策层（JEV-intelligence-graph §四 · PLAN-decision-layer §二）。migrations/0010 内同文 INSERT OR REPLACE，两条路径幂等。
T['decision_registry'] = {'decision_id': ('判断类型主键 d_*', 'PLAN-decision-layer §二'), 'name': ('名称', 'PLAN-decision-layer §二'), 'question': ('这类判断在问什么（一句）', 'PLAN-decision-layer §二'),
  'state_schema': ('输入 state 由哪些表列 / 视图构成（= 未来专用模型的输入契约）', 'JEV-intelligence-graph §四.1'), 'candidates': ('候选词表 JSON 数组（= 输出契约）；开放候选 = open→candidate_pool', 'JEV-intelligence-graph §四.1'),
  'output_home': ('判断结果写回哪张表哪列（表.列；复合列 + 连接；只落 decision_log 则空）', 'PLAN-decision-layer §二'), 'executor_kind': ('rule / human / llm / model', 'PLAN-decision-layer §二'), 'executor': ('A–D / 规则名 / 模型名', 'doc09'),
  'freq_est': ('发生频率量级', 'PLAN-decision-layer §二'), 'escalation': ('升级规则：首版 = 现状描述，数值阈值挂 C19', 'PLAN-decision-layer §六 Q3'), 'calib_status': ('human → shadow → assisted → auto（doc30 状态机平移）', 'JEV-intelligence-graph §四.2'),
  'assumption_ids': ('挂的假设', 'doc30'), 'owner': ('A–D', 'doc09'), 'status': ('draft / reviewed / retired', '实现'), 'design_ref': ('设计出处', '元数据'), 'notes': ('说明', '实现'),
  'research_tier': ('投研重要性分层：A 直接投研判断 / B 准入·可信 / C 运维·流程（决定复核与注意力分配的优先级）', 'E50')}
T['decision_log'] = {'dec_id': ('判断实例 id = migration_id-dec 序号', 'PLAN-decision-layer §二'), 'decision_id': ('哪类判断', 'PLAN-decision-layer §二'), 'target_table': ('判断对象所在表', 'PLAN-decision-layer §二'), 'target_pk': ('对象主键', 'PLAN-decision-layer §二'), 'target_column': ('列级判断的列', 'PLAN-decision-layer §二'),
  'state_anchor': ('判断时刻输入的引用 JSON（record_id 集合 + as_of），判断可复现', 'JEV-intelligence-graph §四.2'), 'candidates_shown': ('判断时刻 registry.candidates 快照', 'PLAN-decision-layer §二'), 'choice': ('选择', 'PLAN-decision-layer §二'),
  'confidence': ('置信度 0–1；人按 H/M/L 写映射 .9/.6/.3（C21）', 'PLAN-decision-layer §六 Q1'), 'executor_kind': ('rule / human / llm / model', 'PLAN-decision-layer §二'), 'executor': ('本次判断的执行者', 'doc09'), 'escalated': ('是否从默认执行者升级（R16 分子）', 'PLAN-decision-layer §二'),
  'basis': ('依据（六元组之一）', 'doc14 A1 可溯源'), 'decided_at': ('判断时间', '实现'), 'retro': ('回填行：confidence 允许空，禁止编造', 'PLAN-decision-layer P3'), 'outcome': ('事后对错 correct / wrong / mixed / unresolved', 'JEV-intelligence-graph §四.2'),
  'outcome_basis': ('回填依据', 'PLAN-decision-layer §六 Q4'), 'outcome_at': ('回填日期', '实现'), 'note': ('说明', '实现')}
T['candidate_pool'] = {'cand_id': ('候选 id', 'PLAN-decision-layer §二'), 'decision_id': ('属于哪类判断（通常 d_divergence_explain）', 'PLAN-decision-layer §二'), 'trigger_ref': ('触发对象 record:<id> / ticker:<t> / metric:<id>，与 v_divergence.div_key 对齐', 'JEV-intelligence-graph §四.3'),
  'kind': ('explanation / new_edge / new_edge_type / new_metric / new_assumption', 'JEV-intelligence-graph §四.3'), 'candidate_text': ('候选内容', 'PLAN-decision-layer §二'), 'proposed_by': ('A–D / llm', 'doc09'),
  'status': ('open / selected / rejected / merged：选中前不是结论', 'PLAN-decision-layer F-b'), 'created_at': ('提出日期', '实现'), 'resolved_by': ('选中 / 否决它的判断（decision_log.dec_id）', 'PLAN-decision-layer §二'), 'note': ('说明', '实现')}

# 设计为字段、实现为视图（doc21 §〇）
DERIVED = [
  ('metric_registry','valuable_score','节点固有价值 = w_e·e + w_s·s + w_r·r + w_phi·φ','doc21 §6.2',True,'v_metric_score'),
  ('edge_registry','tradable_score','可交易度 = c·r·s·φ','doc21 §6.3',True,'v_edge_calc'),
  ('edge_registry','warning_score','预警度 = τ·l·e','doc21 §6.3',True,'v_edge_calc'),
  ('entity_ticker_map','weight','每票上游边 max(tradable,warning) 归一','doc21 §6.4',True,'v_ticker_weight'),
  ('entity_master','signal_stream','三子流 research_frontier / startup_vc / talent_capital','doc21 §〇（E24 删字段）',True,'v_early_signal'),
  ('fct_*','ticker_map / map_path / layer / track / maturity / valuable_score','由 metric → entity / edge 连接推导','doc17 §2.1 关联',True,'v_signal_latest / v_ticker_map'),
]
SCHEMA_DOC = [(t, c, m, ref, False, None) for t, cols in T.items() for c, (m, ref) in cols.items()] + DERIVED

RELATIONS = [
  ('stg_observation','metric_id','metric_registry','metric_id','N:1','登记记录挂指标'),
  ('stg_observation','record_id','fct_quant|fct_event|fct_opinion|fct_frontier|fct_position','record_id','1:1','按 data_class × obs_type 路由，routed_to 记录去向'),
  ('metric_registry','entity_id','entity_master','entity_id','N:1','主实体'),
  ('metric_entity','metric_id / entity_id','metric_registry / entity_master','metric_id / entity_id','N:M','一指标多实体'),
  ('metric_registry','layer','entity_master','layer','继承','价值栈由主实体继承'),
  ('edge_registry','from_metric','metric_registry','metric_id','N:1','边的上游节点'),
  ('edge_registry','to_ticker','entity_master','ticker','N:1','边的下游票'),
  ('entity_ticker_map','entity_id','entity_master','entity_id','N:1','实体→票；初始行由边表推导'),
  ('fct_*','metric_id','metric_registry','metric_id','N:1','四类事实挂指标'),
  ('fct_*','entity_id','entity_master','entity_id','N:1','四类事实挂实体'),
  ('fct_*','source_id','source_master','source_id','N:1','四类事实挂来源'),
  ('fct_*','superseded_by','fct_*','record_id','N:1','旧值被谁取代'),
  ('metric_factor','metric_id','metric_registry','metric_id','1:1','节点五因子'),
  ('observation_direction','record_id','stg_observation','record_id','1:1','记录级方向判断'),
  ('coefficient','assumption_id','assumption','assumption_id','N:1','系数挂假设'),
  ('metric_registry','notes_assumption_ids','assumption','assumption_id','N:M（文本引用）','指标引用假设'),
  ('key_fact','target (event)','calendar','event + date','N:1','事件简报'),
  ('key_fact','target (ticker)','entity_master','ticker','N:1','票简报'),
  ('calendar_metric','cal_id / metric_id','calendar / metric_registry','cal_id / metric_id','N:M','排期挂指标'),
  ('change_log','migration_id','migration_log','migration_id','N:1','每条字段改动属于一次改库'),
  ('change_log','(table_name, pk)','任意资产 / 治理表','主键','N:1','改动指向被改的那一行；表名与主键值成对'),
  ('decision_fork','node_id','thesis_node','node_id','N:1','分叉属于主线节点'),
  ('artifact_anchor','fork_id','decision_fork','fork_id','N:1','产物来自决策'),
  ('artifact_anchor','ref','任意表 / 列 / 视图 / 规则 / 假设','—','N:1','双向锚定：v_column_origin 反查某列来自哪一步决策'),
  ('decision_log','decision_id','decision_registry','decision_id','N:1','每次判断属于登记过的一类判断'),
  ('decision_log','(target_table, target_pk)','任意资产 / 治理表','主键','N:1','判断结果写回的家（output_home）；choice 与家中现值由校验对账'),
  ('candidate_pool','decision_id','decision_registry','decision_id','N:1','候选属于哪类判断（通常 d_divergence_explain）'),
  ('candidate_pool','resolved_by','decision_log','dec_id','N:1','选中 / 否决该候选的那次判断'),
]
CALC_RULES = [
  ('R1','节点固有价值','valuable_score = w_e·e + w_s·s + w_r·r + w_phi·φ','metric_factor × coefficient','v_metric_score','A1,A2,A8','doc21 §6.2','与哪只票无关、不含跳数；仅排序'),
  ('R2','传导确定性','c = base_tier × decay^hops','edge_registry.cert_tier, hops × coefficient','v_edge_calc','A3,A4','doc21 §6.1','tier base T1 .9 / T2 .6 / T3 .3'),
  ('R3','领先期归一','τ = min(1, tau_hops·hops + tau_l·l)','edge_registry.hops, metric_factor.l × coefficient','v_edge_calc','A5','doc21 §6.1',''),
  ('R4','可交易度','tradable = c·r·s·φ（因子取 from_metric）','R2 + metric_factor','v_edge_calc','A6','doc21 §6.3','进 nowcast / 定仓位（回测标定前只排序）'),
  ('R5','预警度','warning = τ·l·e','R3 + metric_factor','v_edge_calc','A6','doc21 §6.3','上 watchlist / 给方向'),
  ('R6','实体→票权重','weight_i = max(tradable_i, warning_i) / Σ_j max(tradable_j, warning_j)（同票归一；weight_override 优先）','v_edge_calc','v_ticker_weight','A7','doc21 §6.4','人可覆盖（owner D）'),
  ('R7','可靠性映射','r = P1→0.9 / P2,P3→0.6 / P4,P5→0.3（取该节点最佳 provenance）','fct_* provenance','metric_factor.r（load 时）','A8','doc21 §6.1','规则默认，D 可改'),
  ('R8','标题值','每指标取 actual > event > position > state > computed 中 knowledge_date 最新一条','fct_*','v_metric_headline','—','实现','呈现层'),
  ('R9','早期信号层','maturity ∈ {research, private}','entity_master','v_early_signal','—','doc21 §〇','视图不是字段（E24）'),
  ('R10','三态','供给态 × 需求态 → 信念 / 观察 / 泡沫预警；阈值未定','fct_* + observation_direction','v_signal_latest（占位）','C6','doc22 §五','阈值 C6 placeholder，未验证禁用于告警'),
  ('R11','健康','过期 = next_release < as-of；已填无记录；placeholder / 待钉一手 / 付费 / 合规 标记','metric_registry × fct_*','v_health','—','实现','数据岗巡检'),
  ('R12','复验节奏','P2 每财报季钉 transcript；P3 回一手；P4 实际值替换；P5 回测标定','fct_* provenance','v_review_due','—','doc23 §五',''),
  ('R13','跳数一致性','hops = 中间节点数 + 1（map_path）','edge_registry','checks.py','A10','doc25 §1.2','校验规则'),
  ('R14','as-of','数据快照日 = max(fct_*.knowledge_date)','fct_*','build_dashboard.py','—','实现','point-in-time 基准'),
  ('R15','校准误差','calib_error = |bucket 命中率 − bucket 置信度|（按 decision_id × round(confidence,1) 分桶；只统计 outcome ∈ correct/wrong）','decision_log','v_calibration','C20,C21','PLAN-decision-layer §五','校准未 validated 的决策类型禁标 assisted / auto（🟠闸扩展）'),
  ('R16','升级率','escalation_rate = 升级次数（escalated）/ 判断次数，按 decision_id','decision_log','v_decision_health','C19','PLAN-decision-layer §五','越低说明下层执行者越可信'),
  ('R17','背离判定','① 记录级：最新未取代观测 direction=! ｜ ② 票级：同票供给侧与需求侧最新方向相反（布尔版；数值阈值待 C6）；deprecated 指标不触发','v_obs × metric_registry × edge_registry × candidate_pool','v_divergence','C6','JEV-intelligence-graph §四.3','背离 = PROPOSE 触发器：超 7 天无候选记 WARN'),
]
