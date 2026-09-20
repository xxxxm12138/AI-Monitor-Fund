# KPI 落点(sink)可 nowcast 分档 + 与影响力闸的对齐

**日期** 2026-09-20 ｜ **来源** 子 agent 实查 metric_registry(84)/edge_registry(35)+ doc23/doc24v2 ｜ **性质** 参考清单(B · 待 D 复核)｜ **用途** 定 sink 的 cert_tier、给 KPI-sink 面板(PLAN-graph-refactor §十一)供数

## 〇 分档定义
- **T1 可 nowcast**:有另类/一手地面数据领先预判**量级**(海关月度领先季报、上电进度领先收入确认)
- **T2 可对账**:无干净时序回测,但可**结构+真值对账**(backlog 由合同公告拼、cost/token 由定价页读)
- **T3 只方向**:只有定性方向、无法预判量级(benchmark 分、论文斜率、政策事件)

## 一 关键对齐结论(① 影响力闸 × ② 可 nowcast)

**6 条影响力闸"外溢"信号(r142/r146/r153/r500/r504/r501)自身指标全是 T3。** 即前沿 D5/D2 信号结构性无法 nowcast 量级(它们是叶子,无"正式披露"可提前预判)。
→ **它们外溢到票 = 给方向 / regime,不给量级。** 量级 nowcast 的终点 KPI 由**供给侧地面读数**承担,不是前沿信号。
→ 客观印证 doc25 原设计:**可交易度(量级,供给侧 T1/T2)vs 预警度(方向,前沿 T3)**。
→ 面板分两类呈现:**量级 nowcast 卡**(供给侧)vs **方向/regime 信号**(前沿雷达/watchlist)。

## 二 T1(可领先预判量级)—— 量级 nowcast 的真落点
| KPI | 属票/纯 | 前置地面读数 |
|---|---|---|
| m_cn_optics_zte 旭创营收 · m_cn_optics_eoptolink 新易盛营收 | 票 | 海关 HS8517 月度(领先季报)**⚠️占比系数 placeholder,标定前只作方向** |
| m_nbis_capacity 上电/合同电力 | 票 | PPA/机组/站点合同事件(lead 90d) |
| m_nbis_rev NBIS 收入 · m_nbis_arr ARR | 票 | 上电容量×单价 + capex + 光模块赛道 beta + CRWV 同业(可回归) |
| m_app_retention_cn AI 应用留存 | 纯 | 第三方活跃/下载(QuestMobile/榜单)领先披露 |

## 三 T2(可结构对账)—— 摘要
NBIS:m_nbis_backlog/capex/sites/ebitda/cash(合同事件拼/结构派生)· m_crwv_peer(同业可回归)· cost/token(m_cost_per_token 定价页 P1)· m_gpu_rental_price(价格页周读)· m_token_usage/m_token_share_openrouter(OpenRouter 周抓,覆盖不全)· m_enterprise_adoption + RBRK ARR 族(结构互校,无另类地面数据)· m_gpu_ship(供应链拼)· m_hyperscaler_capex(指引前瞻)· m_800g_shipment(海关+拼)· m_dc_power_iea(IEA+并网结构)· FCEL 族(m_fcel_rev/backlog/awarded/dc_ppa/capacity,合同里程碑对账)· m_lab_contract_reflection_nbis(合同事件)· m_lab_funding_frontier(SEC Form D/官方博客一手)。

## 四 T3(只方向)—— 前沿/政策/资本,雷达层不下注量级
m_aa_intel_index · m_bench_frontier · m_train_compute_epoch · m_arxiv_topic_slope · m_open_vs_closed · m_infer_price_perf · m_new_paradigm · m_data_wall · m_data_labeling · m_copyright_lit · m_rl_environments · m_export_ctrl_bis · m_energy_grid · m_domestic_sub_policy · m_ai_regulation · m_safety_incident · m_circular_financing · m_lab_funding_reflection/cohere · m_vc_flow · m_preipo_pool · m_talent_flow · m_hbm_cowos(付费定性 P3)· m_nbis_calltone / m_rbrk_calltone(措辞 arbiter)。
出 scope:m_staa_* / m_slmt / m_hkex_0679 / m_13f_book / m_reconcile_nbis(派生)。

## 五 缺口(哪些 edge 终点还没有可 nowcast 读数)—— 量级 nowcast 的边界
1. **RBRK 全链无另类地面数据**(最实缺口):e_adoption_rbrk 仅 T2 结构对账,doc24v2 列的 JD/招聘/支出调查未接入 → 只能事后对账,不能真 nowcast。
2. **D1 尾仓芯片上游只 P3 定性**:m_hbm_cowos 付费定性未标定 → MU/SNDK 终点缺量级;AMD/INTC/MRVL/SUPX 靠 NVDA 出货代理 + capex 勉强 T2。
3. **光模块 T1 被 placeholder 卡住**:海关→光模块占比系数(m_cn_optics_customs)是最大 placeholder → T1 目前"有读数未校准",标定前只作方向。
4. **NBIS 能力/资本侧上游边全 T3**:e_aa/e_bench/e_capability/e_frontierfund/e_costtoken/e_priceperf/e_openclosed 均 3 跳只方向 → NBIS 用量的量级 nowcast 全靠供给侧 T1/T2 边承担。
5. **纯 AI 发展读数(D5/D7)天然无 nowcast 档**:结构性(叶子),非可修复缺口 → 作雷达方向层,不作下注终点。
6. **NBIS T2 资本边样本薄**:e_labfund_nbis 只 Reflection 一例(278d lead),lab 融资指标本身还 T3。

## 六 对面板 / 下一步的含义
- **量级 nowcast 卡**(§十一 三值+Δ+MOE)只对 T1/T2 供给侧 KPI 成立(NBIS 收入/上电、光模块营收、FCEL backlog、cost/token);其余前沿信号走**方向/regime 呈现**。
- 具体修正队列(① 暴露 + ② 印证):① r504 应加打 NBIS 的边(现错接 RBRK 竞对);② 光模块 T1 标"未校准占位";③ RBRK/尾仓缺另类地面数据,标 T2-only。
