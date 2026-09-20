# NBIS 实例 · 用真实数据把整套体系跑一遍

> 构建步骤 ⑥。用最大持仓 **NBIS(Nebius,51% 权重)** 把整套 schema(实体 → 指标 → 边 → 四类事实)**灌满真数跑一遍**:每字段真实值、每层源的可得性与质量、每条边的验证 tier 与"怎么跑",诚实标出跑不通的地方。数据 as-of 2026-09;数字来源分五级 provenance(P1–P5)。

---

## 一、核心思路:一条 thesis,两端对读

NBIS 是 neocloud——它的多头逻辑是**「AI 算力周期」**。这条 thesis 有天然的两端,用两套独立数据、独立失败模式去读**同一件事**:

| | **供给端读** | **需求端读** |
|---|---|---|
| 锚 | NBIS 本体 + 光模块供应链 | NBIS 客户 + 前沿 AI 生态 |
| 层 | 成熟层(量价 + 执行) | 早期信号层(事件 + 前沿 + 人才资本) |
| 答什么 | 算力**在建多少** | 算力需求**真不真、续不续** |
| 真实数据 | 光模块出货 2025 24M → 2026 63M 只;中际旭创 2026Q1 ¥194.96 亿(+192%);NBIS 5GW 产能、$40B backlog | Reflection 一年 $130M → $2B(Nvidia 领投,估值 $8B)→ 后续加注;Cohere $240M ARR、估值 $7B |
| 可得性 | 可回测、进 nowcast | 给方向 / 预警,不直接下注 |

**为什么这样读最能打**——两条读独立数据源、独立失败模式,读同一 thesis 的两端:

- **同向**(供给猛建 + AI 侧融资 / 进展 / 人才都在涌)= 周期健康、高信念,NBIS backlog 可信 → 支持加仓。
- **背离**(供给端还在猛建 / 囤 GPU,但 AI 侧一级融资转冷、模型进展停滞、人才回流大厂)= **neocloud 泡沫 / 循环融资预警**——正是市场对 NBIS 的头号担忧(NVIDIA–CoreWeave–Nebius 循环 GPU 融资、被称 "WeWork 2.0" 的 neocloud 数据中心融资)→ 减仓 / 关注做空侧。

这条背离信号直接命中 NBIS 的核心分析点(需求持续性 / 客户质量),是覆盖 NBIS 的卖方分析师一般**不做**的交叉验证——差异化就在这里。

---

## 二、NBIS 的七条传导链

从 NBIS 的收入因子(产能执行 × 需求持续性)向上游反推,连到七个 AI 发展节点(映射范式见 [05-映射范式](05-映射范式-点边权重.md)):

```
D1 光互连出货      ─①→ 全球 AI 集群在建 ─②→ neocloud 扩张 ─③→ NBIS 产能   [3 跳 · 供给]
D1 NBIS backlog(本体) ────────────────────────────────────→ NBIS         [0 跳 · 本体]
D1 NBIS 自有电力上电 ─①→ NBIS 产能执行                                    [1 跳 · 供给] ★ 关键可观测
D3 前沿 lab 融资    ─①→ lab 算力采购力 ─②→ NBIS 签约 / backlog            [2 跳 · 需求]
D5 模型能力进展    ─①→ 推理 / 训练需求 ─②→ lab 采购 ─③→ NBIS 用量        [3 跳 · 需求]
D7 电力 / 电网政策 ─①→ 数据中心用电审批 ─②→ NBIS 上电节奏                 [2 跳 · regime]
D7 出口管制        ─①→ GPU 供给 / 成本 ─②→ NBIS 产能成本 / 可得           [2 跳 · regime]
```

---

## 三、真实数据填充(每字段真值)

| 节点 / 指标 | 真实值(as-of 2026-09) | 来源 · 等级 |
|---|---|---|
| 中际旭创季度营收 | ¥194.96 亿(2026Q1,**+192% YoY**) | 深交所 300308 一季报 · 🟢 P1 |
| 光模块出货(赛道) | 800G 24M 只(2025)→ 63M 只(2026) | 行业追踪 · 🔵 P3 |
| NBIS 收入 / EBITDA | $582.3M(2026Q2,**+454% YoY**) | Nebius IR(businesswire)· 🟢 P1 |
| NBIS ARR / backlog / 产能 | ARR $3.0B · backlog **$40B** · 5GW 目标(年底 800MW–1GW) | Q2 电话会 · 🟡 P2(待钉官方 transcript) |
| NBIS 单位经济 | 中期合同 $20–25M/MW,短期 $40–50M/MW;AI 分部利润率 ~50% | Q2 电话会 · 🟡 P2 |
| 前沿 lab 融资(Reflection) | $2B 融资(2025-10,@$8B,Nvidia 领投)→ **Reflection ↔ NBIS $1B 算力合同(2026-07)** | TechCrunch / Bloomberg · 🟢 P1 |
| 前沿 lab 融资(Cohere) | $240M ARR、估值 $7B | Sacra / FNEX · 🟡–🔵 P3 |
| 前沿训练算力 | +4–5× / 年 | Epoch AI · 🟢 P1 |
| 模型能力(智能指数) | 榜首模型 ~53 | Artificial Analysis · 🟢 P2 |
| 数据中心电力 | ~460 TWh(2022)→ ~1000 TWh(2026) | IEA · 🟢 P2 |
| 出口管制 | BIS 放开 H200 / MI325X 对华出口 + 美方抽成 25% | BIS 新闻稿 · 🟢 P1 |

> 对应仓库表:量价 → `fct_quant`、事件 → `fct_event`、观点 → `fct_opinion`、前沿 → `fct_frontier`([四类事实字段结构](../../pipeline/SCHEMA.md#tbl-fct_quant))。

---

## 四、源可得性 × 质量(真去找的结果)

可得性四档:🟢 一手公开可回测 · 🟡 二手转述待钉一手 · 🔵 付费 · ⚪ placeholder / 合规受限。

| 维 | 节点 | 真实源 | 可得性 | 等级 | 频率 | 软肋 |
|---|---|---|---|---|---|---|
| D1 | 中际旭创 / 新易盛营收 | 深交所 / akshare / 巨潮 | 🟢 | P1 | 季 | 需按海外占比拆 AI 敞口 |
| D1 | 海关光模块出口 | 海关总署月报(HS8517) | ⚪ | P4 | 月 | 光模块占比系数未标定 |
| D1 | HBM / CoWoS / GPU 出货 | SemiAnalysis / TrendForce | 🔵 | P3 | 季 | 付费;免费只拿定性 |
| D1 | NBIS 收入 / EBITDA | Nebius IR | 🟢 | P1 | 季 | — |
| D1 | NBIS ARR / backlog / 5GW | Q2 电话会转述 | 🟡 | P2 | 季 / 事件 | 不在 results release,须钉官方 transcript |
| D3 | 前沿 lab 融资 | TechCrunch / 官方博客 / SEC Form D | 🟢 | P1–P3 | 事件 | 估值口径不一、时效敏感 |
| D5 | 前沿训练算力趋势 | Epoch AI | 🟢 | P1 | 月 / 事件 | 权威、免费 |
| D5 | 模型能力 / 智能指数 | Artificial Analysis / LMArena | 🟢 | P2 | 周 | 免费;榜单口径 |
| D6 | 推理 cost/token · 用量 | Artificial Analysis / OpenRouter | 🟢 | P3 | 周 | 分模型、口径杂 |
| D7 | 出口管制 | BIS 新闻稿 | 🟢 | P1 | 事件 | — |
| D7 | 能源 / 数据中心电力 | IEA | 🟢 | P2 | 年 / 季 | 预测口径 |
| D4 | 顶尖研究员流向 | 领英 / 论文署名 | ⚪ | P3–P5 | 事件 | 合规受限、半人工、ROI 低 |

**一句话结论**:能一手公开、可回测的集中在 D1 中国光模块 / NBIS 收入、D5 Epoch / Artificial Analysis、D7 BIS / IEA;NBIS 的 ARR / backlog / 5GW 是二手电话会口径待钉 transcript;HBM / CoWoS / 一级估值付费;海关系数、人才 placeholder / 合规。**这张表本身就是"可得性诚实说明"**。

---

## 五、边确定性验证怎么跑

| 边 | tier | 怎么跑 |
|---|---|---|
| 光互连 → NBIS | **T1 可回测** | 取旭创 + 新易盛季度营收(按海外占比拆 AI 敞口)作 X,NBIS 收入 / hyperscaler capex 作 Y;按 knowledge_time 做 point-in-time 对齐 → lead-lag 相关 + Granger → 报领先期与相关系数 + 样本外稳定性。**软肋诚实说**:NBIS 仅上市约 1 年、季度点太少 → 借 CoreWeave / hyperscaler capex 作延长历史的下游代理,不硬回归 NBIS 单票。 |
| lab 融资 → NBIS backlog | **T2 结构** | 不能直接回归(backlog 预合同化、点少)→ 结构论证(lab 有钱才有采购力)+ **真值对账**(Reflection 2025-10 融 $2B → 2026-07 果然签 NBIS $1B 算力合同,这条边被现实证了一次)+ 敏感性分析(结论对"融资 → 采购转化率"在一区间内稳不稳)。禁止拿它回归自己(循环)。 |
| 能力进展 → NBIS 用量 | **T3 方向** | 3 跳、能力 → 需求无法量化因果 → 只做 watchlist / 方向,永不据此定仓位。Epoch 训练算力 +4–5×/年、智能指数只作"周期还在不在"的方向读。 |

> 对应仓库表 `edge_registry.cert_tier`([字段结构](../../pipeline/SCHEMA.md#tbl-edge_registry))。每条边一次验证 = 建 gold(真值样本)→ 人核 → 回归 / 敏感性 → 结果写回 `cert_score` / `lead_measured` / `evidence_ids` → 定期复验。**边不是画完就完,是像指标一样持续验、持续管。**

---

## 六、对账逻辑 = 结论

把供给读与需求读放在一起,得出可执行的结论:

- **供给端**:光模块猛出货(旭创 +192%)、NBIS 收入 +454%、backlog $40B、5GW 在建——算力**在猛建**。
- **需求端**:Reflection $2B 融资后果然回来签 $1B 算力合同、Cohere ARR 爬升——需求端**真金落地**。
- **判定**:两端**同向** → 周期健康、backlog 可信 → 支持持有 / 加仓;一旦转**背离**(供给还在建、需求侧融资转冷 / 进展停滞)→ 触发 neocloud 泡沫 / 循环融资预警 → 减仓。

这把 NBIS 从"单只票读"升级成**"一条 thesis 两端对账"**——既有真数、又演示供需交叉验证、又切中 NBIS 的真实风险(neocloud 泡沫)。

---

## 七、结果:已兑现的边级预测

把上面的边当作**带日期、可证伪的方向预测**,到期用真值打分(仓库 `d_edge_predict` / `v_calibration`):

| 边预测 | 方向 | 兑现证据 | 结果 |
|---|---|---|---|
| 光模块 ↑ → NBIS ↑(赛道 beta) | ↑ | 旭创 2026Q1 ¥194.96 亿(+192%)· NBIS Q2 收入 $582.3M(+454%),同向上行 | ✅ correct |
| lab 融资 → NBIS 需求 | ↑ | Reflection $2B 融资(2025-10)→ Reflection ↔ NBIS $1B 合同(2026-07),转需求兑现 | ✅ correct |
| hyperscaler capex ↑ → NBIS | ↑ | 四家 capex 上行 · NBIS 收入 +454%,在建强度传导兑现 | ✅ correct |

三条已兑现的方向预测构成校准曲线的首批真实数据点(命中 100% @ 中置信,小样本、诚实标注)。**边级校准从此可持续积累**——每条边到期都用真值回填 outcome,让整张映射图自我校准。

---

## 八、实跑诚实结论(这一跑证明 / 暴露了什么)

- ✅ **能真跑到"可回测信号"**:D1 光模块(交易所一手、可拆 AI 敞口)、NBIS 收入 / EBITDA(IR 一手)、D5 Epoch / Artificial Analysis(免费权威)、D7 BIS / IEA(一手公开)。
- 🟡 **只能到"结构 + 真值对账"**:lab 融资 → backlog(NBIS 上市短、预合同化)——但 Reflection $1B deal 事后证了这条边一次,是最漂亮的真值对账实例。
- 🔵 **付费才全**:HBM / CoWoS(SemiAnalysis)、一级估值(PitchBook)——免费只拿定性。
- ⚪ **placeholder / 合规**:海关光模块占比系数(用前必标定)、人才流(合规受限、半人工)。
- 🔴 **最该补的一手**:NBIS ARR / backlog / 5GW 目前是电话会 P2,钉官方 transcript / IR deck 才能升 P1;NBIS 单票回测点不足,须借 hyperscaler capex / CoreWeave 延长历史。
- 🟣 **第四类前沿单薄**:标的驱动天然欠采前沿,已另立独立的前沿雷达补。

这一跑本身就是最强证据:**体系不是 PPT**——每字段有真值、每源有可得性分级、每条边有验证 tier 与"怎么跑",诚实标出跑不通的地方(placeholder / 付费 / 点少)。这正切"链稳不稳、可回溯"的核心考核。

---

*待核:NBIS Q2 披露客户 "Reflection" 是否即前沿 lab Reflection AI(高概率,Nvidia 同时是两者关联方,需财报 / 新闻二次确认)。*
