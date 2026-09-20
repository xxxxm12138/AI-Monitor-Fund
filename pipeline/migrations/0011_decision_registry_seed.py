# -*- coding: utf-8 -*-
"""0011 · decision_registry 首批 10 类判断落库 + 假设 C19–C21 + 修正 0010 的假设编号引用 · owner B · 2026-09-20
上游：PLAN-decision-layer §三（词表 = 现状盘点：候选全部抄自现有 CHECK 约束与词表，没有发明新词）。
P0 已拍板（四问均甲案）：置信度 H/M/L 三档映射 .9/.6/.3（C21）；d_direction 只记人工改判；escalation 首版 = 现状描述、数值阈值挂 C19；outcome 并入复验节奏。
编号修正：计划中的 C9/C10/C11 在落库时已被领域假设占用（C9 财报日估计…C18 循环融资敞口），顺延为 C19/C20/C21；
0010 已应用不可改，其写入 calc_rule R15/R16 与 schema_doc 两列的旧编号在此幂等覆盖（重放顺序 0010→0011 保证最终态一致）。
读法：#1 d_route 证明 cascade 的 auto 端已存在（确定性代码）；#2 d_direction 证明 assisted 已存在（directions.py 初判 + 人改判）——
这张表是现状盘点 + 演进路径，不是愿景；每行 = 未来一个专用小模型的岗位描述（state_schema 输入契约 × candidates 输出契约）。"""
import json
OWNER = 'B'
J = lambda *xs: json.dumps(list(xs), ensure_ascii=False)
REF = 'PLAN-decision-layer §三'

ROWS = [  # decision_id, name, question, state_schema, candidates, output_home, executor_kind, executor, freq_est, escalation, calib_status, assumption_ids, owner, notes
  ('d_route', '接入路由', '这条观测进哪张 fct', 'stg_observation.obs_type / value / note + metric_registry.data_class',
   J('fct_quant','fct_event','fct_opinion','fct_frontier','fct_position'), 'stg_observation.routed_to', 'rule', 'core.route()',
   '每条观测一次（现 231 条）', '确定性代码无升级；词表外情形代码直接报错（checks 7b 路由完整性兜底）', 'auto', None, 'B',
   'cascade 的 auto 端已存在：deterministic code，校准闸豁免（executor_kind=rule）'),
  ('d_direction', '方向判断（A11）', '这条观测对所喂持仓票的 thesis 方向如何', 'stg_observation 全行 + metric_registry.dim / signal_role（directions.py 的输入）',
   J('↑','↓','→','!','—'), 'observation_direction.direction', 'rule', 'directions.py 初判 · 人工改判走 m.observe(direction=…)',
   '每条观测一次', '规则拿不准（新指标语义 / 冲击类）→ B 改判；仓位含义升级 D。数值阈值挂 C19', 'assisted', 'C19,C21', 'B',
   'assisted 已存在：规则初判 + 人改判。Q2 甲案：decision_log 只记人工改判（observe 钩子自动落六元组），规则初判不记；未来模型旁跑时再切全记'),
  ('d_falsify_gate', '前沿证伪闸（doc29 第一道）', '这条前沿信息可证伪吗（立场 × 可验证性）', 'fct_frontier.institution / anchor / source_id + source_master.source_kind / source_tier',
   json.dumps({'source_stance': ['neutral','vendor_pr','social'], 'verifiability': ['reproducible','third_party_verified','claimed_only','rumor']}, ensure_ascii=False),
   'fct_frontier.source_stance + fct_frontier.verifiability', 'human', 'B（core.fct_row 对第三方基准源给规则初值）',
   '每条前沿记录一次（现 14 条，填 8）', '立场存疑 / rumor 级 → D；复合判断不进 7k 单列对账', 'human', None, 'B',
   '复合候选（两列一次判），choice 记「stance=…; verifiability=…」'),
  ('d_impact_gate', '前沿影响力闸（doc29 第二道）', '过了证伪闸的前沿信息影响多大', 'fct_frontier（过闸行）+ topic_cluster + 相关边 evidence',
   J('高','中','低'), 'fct_frontier.industry_impact', 'human', 'D', '每条过闸前沿一次', '本闸即最高档（owner D），无升级；量化口径待 C8', 'human', 'C8', 'D',
   '过闸才外溢到票（doc29 §两道闸）'),
  ('d_regime', '三态对账', '对账节点当前是同向 / 平 / 背离', '对账 pair 两端最新方向（v_signal_latest）+ v_divergence；阈值版输入待 C6',
   J('同向','平','背离'), None, 'human', 'D（规则 C6 占位）', '每对账节点每数据周期一次', '本判断即 D 级；阈值挂 C6（placeholder，禁用于告警）', 'human', 'C6', 'D',
   'output_home 空：三态结论落 decision_log；key_fact.status_line 是叙述载体不是词表值。背离 → 触发 d_divergence_explain（R17）'),
  ('d_edge_tier', '边验证档位', '这条边的确定性档位 T1 / T2 / T3', 'edge_registry（机制 / 跳数 / evidence_ids）+ 回测结果（cert_method / cert_score）',
   J('T1','T2','T3'), 'edge_registry.cert_tier', 'human', 'D 定 gold · A 跑回测', '每边一次 + 复验时重判（现 35 条边）',
   'T1 主张必须过回测（R2）；对账分歧（7d reconcile_flag）交 D', 'human', 'A3,A4', 'D',
   '家中现值可带「（提议）」后缀，7k 前缀匹配容忍；提议 → 复核 = 一次新判断'),
  ('d_source_tier', '来源分级', '这个来源什么等级（P1–P5）', 'source_master.source_kind / publisher / url + 记录 provenance（doc23 分级标准）',
   J('P1','P2','P3','P4','P5'), 'source_master.source_tier', 'human', 'B（upsert_source 从 provenance 派生初值）', '每新源一次（现 123 源）',
   '降级（如电话会转述 P2）与失效（blocked）→ 复验队列；标准争议 → D', 'human', None, 'B', '登记记录时的 P 级判断即本判断的实例；source_tier 取该源最佳 P 级'),
  ('d_fill_priority', '填数优先级', '这个缺口先填谁', 'v_health（缺口 / 过期 / flag）+ metric_registry.dim × 基金视角双排序（doc26）',
   J('1','2','3','4','5','6','7','8','9','跳过'), None, 'human', 'D', '每轮填数一次（13-思路总梳理 §九 = 首版实例）',
   '本判断即 D 级；合规受限（D4）直接「跳过」', 'human', None, 'D', 'output_home 空：优先级是排序判断，metric_registry.fill_status 是执行结果不是候选值'),
  ('d_calendar_scope', '排期入围', '这个排期事件在不在 AI 发展范围', 'calendar 行 + entity_master.in_book / ticker（是否非 AI 持仓业务）',
   J('active','retired'), 'calendar.status', 'human', 'B 提议 · D 复核', '每排期行一次（现 58 行）', '边界案例（如 FCEL 非 AI 业务收入）→ D', 'human', None, 'B',
   '先例 = 0007_retire_non_ai（STAA / SLMT 等 retired）'),
  ('d_divergence_explain', '背离解释', '这个背离最可能的解释是什么', 'v_divergence + 背离两侧最新观测 + 边 evidence + 来源可信度',
   'open→candidate_pool', None, 'human', 'D（候选生成 = B / llm，PROPOSE）', '每背离一次（v_divergence 现 3 条欠账）',
   '候选由 B / llm 提出（PROPOSE），选择必须 D；选错成本高，永不下放 auto', 'human', 'C6', 'D',
   '全图唯一需要开放式生成的位置：PROPOSE 扩空间 → SELECT 压回来；choice = 选中的 cand_id，同步 candidate_pool.status/resolved_by'),
]

ASSUMPTIONS = [  # assumption_id, section, text, current_value, kind, impact, refine_by, status
  ('C19', '领域', '决策层升级规则（escalation）暂无数值阈值：何种置信度以下升级给谁，首版只作现状描述', '现状描述（见 decision_registry.escalation 各行）', '占位', '🟠',
   'v_calibration 按 decision_id 累积后标定各档阈值；阈值定前 escalation 不得写具体数字', 'placeholder'),
  ('C20', '领域', '校准闸口径：calib_status ∈ {assisted, auto} 且执行者为 llm / model 的判断类型，其关联假设须全部 validated（checks 7l）；validated 判据 = v_calibration 校准误差与样本量达标（阈值待定）',
   '定性闸已生效（7l ERROR 级）；数值判据未定', '设计选择', '🟠', '第一类走完 human → shadow 的判断类型出现后，用其校准曲线定「达标」数值', 'assumption'),
  ('C21', '领域', '判断置信度三档锚：人写 H / M / L，映射 0.9 / 0.6 / 0.3，与 A1 因子锚同一词表（Q1 甲案：先有校准数据，再谈精度）', 'H=.9 M=.6 L=.3（migrate.py CONF）', '设计选择', '🔵',
   '校准数据积累后可细分档位或直写小数', 'assumption'),
]

FIX_RULES = [  # 0010 写入的旧编号 → 幂等覆盖（与 metadata.py 现文一致）
  ('R15','校准误差','calib_error = |bucket 命中率 − bucket 置信度|（按 decision_id × round(confidence,1) 分桶；只统计 outcome ∈ correct/wrong）','decision_log','v_calibration','C20,C21','PLAN-decision-layer §五','校准未 validated 的决策类型禁标 assisted / auto（🟠闸扩展）'),
  ('R16','升级率','escalation_rate = 升级次数（escalated）/ 判断次数，按 decision_id','decision_log','v_decision_health','C19','PLAN-decision-layer §五','越低说明下层执行者越可信'),
]
FIX_DOC = [
  ('decision_registry','escalation','升级规则：首版 = 现状描述，数值阈值挂 C19','PLAN-decision-layer §六 Q3'),
  ('decision_log','confidence','置信度 0–1；人按 H/M/L 写映射 .9/.6/.3（C21）','PLAN-decision-layer §六 Q1'),
]

def up(m):
    for a in ASSUMPTIONS:
        m.insert('assumption', dict(zip(('assumption_id','section','text','current_value','kind','impact','refine_by','status'), a)),
                 basis='PLAN-decision-layer §五 / §六（P0 拍板）· 同步 15-假设台账增补.md §十一')
    for (did, name, q, ss, cands, home, ek, ex, fq, esc, cs, aids, owner, notes) in ROWS:
        m.insert('decision_registry', dict(decision_id=did, name=name, question=q, state_schema=ss, candidates=cands, output_home=home,
                 executor_kind=ek, executor=ex, freq_est=fq, escalation=esc, calib_status=cs, assumption_ids=aids,
                 owner=owner, status='draft', design_ref=REF, notes=notes), basis=REF + '（现状盘点：候选抄自现有 CHECK 约束与词表）', owner=owner)
    for row in FIX_RULES:
        m.sql('INSERT OR REPLACE INTO calc_rule VALUES (?,?,?,?,?,?,?,?)', basis='修正 0010 的假设编号（C9/C10/C11 → C19/C20/C21，原编号被领域假设占用）', params=list(row))
    for row in FIX_DOC:
        m.sql('INSERT OR REPLACE INTO schema_doc VALUES (?,?,?,?,false,NULL)', basis='同上：字典两列的假设编号修正', params=list(row))
