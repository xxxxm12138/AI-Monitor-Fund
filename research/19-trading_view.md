我来实际打开这两个页面看一下，先看股息日历概览页。

我把三个页面都实际翻了一遍（日历 → VLSFINANCE 概览 → 股息页 → Technicals），下面按"看到了什么 → 设计逻辑 → 指标思路 → 用户/场景 → 从基金视角看断点"来拆。

## 一、实际的信息链条（以 VLSFINANCE 为例串起来）

| 层级 | 页面 | 回答的问题 | 一眼结论 | 可展开明细 |
|---|---|---|---|---|
| L0 发现 | 股息日历 | 什么时候、谁、多少 | 周视图上每天的事件计数（Economic / Earnings / Dividends / IPO），如 Thu 17 = 1004 条股息 | 6 列表格：Logo+代码、公司名、Amount(USD)、**Ex-dividend date**、Payment date、Dividend yield |
| L1 定位 | 个股 Overview | 这是家什么公司、值不值得看 | Key stats 里 **Dividend yield (indicated)** 排第二位，紧挨市值；1D~All time 多周期涨跌 | 财务图、新闻、社区 Ideas、Technicals 三仪表缩略、Seasonals、FAQ（"Does X pay dividends?" "Is X a good dividend stock?"） |
| L2 验证 | Financials › Dividends | 这笔股息可靠吗、有没有历史 | 模板生成的一句话："Payouts are made annually. The last DPS was 1.50 INR. Yield (TTM) is 0.63%" + 4 张 KPI 卡 | 20 年 DPS 柱 + Yield 线；指标表 DPS / Yield(FY) / **Payout ratio(FY)**（老年份上锁付费）；逐笔 payout history（ex / record / pay / amount / frequency） |
| L3 择时 | Technicals | 现在能不能进、在什么价位 | 三个仪表盘：Oscillators / **Summary** / Moving Averages，各带 Sell/Neutral/Buy 计数（15/9/2） | 11 个振荡器表、15 条均线表（Name / Value / Action），Pivots 表（Classic / Fibonacci / Camarilla / Woodie / DM × R3~S3） |

日历页的过滤器只有三个：国家（默认 G20）、Primary listing 开关（去重跨市场挂牌）、时区。同一公司在日历里是按"挂牌"出现的（a2 Milk 出现 4 行：ASX / LSX / GETTEX / LS），说明底层实体是 **event × listing**，不是 company。

## 二、链条背后的设计逻辑

**1. 漏斗结构：事件驱动的发现 → 单标的资格确认 → 择时执行。**
每跳一个 URL，每跳只回答一个问题。日历不试图告诉你"值不值"，Technicals 也不试图告诉你"这家公司是干什么的"。这种严格的关注点分离让每一层都可以被单独抵达（SEO 也是这么做的：每页都有一组 FAQ）。

**2. 每一层都是 "结论先行 + 明细可展开"。**
日历是计数 → 表格；股息页是一句话 → KPI 卡 → 图 → 表；Technicals 是仪表 → 计数 → 26 行指标表。用户不用读完就能停在任何深度。

**3. 以 Ex-date 为主键，而不是 Payment date。**
日历默认按 ex-date 排、加粗显示 ex-date。因为 ex-date 是唯一影响价格行为的日子（持有权截止、机械除权），pay date 只是现金流。这是一个明确的"交易者视角"而非"会计视角"的选择。

**4. 用计数暴露置信度。**
Technicals 不只给你"Sell"，还给 15/9/2。同样 Sell，15/9/2 和 9/9/8 完全是两个意思。这比大多数"评分"产品诚实。

**5. 同一指标多口径并列，而不是选一个。**
Yield 在三个页面是三种口径：indicated（前瞻年化）/ TTM（回看）/ FY（年报可比）。Pivots 给 5 种算法并排——不是让你选一个，是让你看**共识区**：VLS 的 5 种 P 都在 250.7–253.9（强共识），S1 却分散在 224–240（弱共识）。

## 三、指标设计的具体思路

**日历只放 4 个数，且各有分工：**
- Amount（绝对值，统一换成 USD）→ 用来估 ex-date 的价格缺口
- Yield（相对值）→ 跨标的比较
- Ex-date / Pay date → 行动窗口的起点和终点

**股息页的三个指标是"三角验证"：** DPS 看绝对水平，Yield 看相对估值，Payout ratio 看可持续性。VLS 这个案例很典型：DPS 五年纹丝不动 1.50，Payout ratio 却从 1.6% 摆到 23%——说明股息不是从盈利里"算"出来的，是从"惯例"里定的；盈利本身（投资公司，市值波动计入损益）极不稳定。这是页面没有明说、但把数据摆在一起后能读出来的东西。

**Technical Ratings 的压缩算法**（TradingView 公开规则）：每个指标映射成 {-1, 0, +1}，取平均；>0.5 强买、0.1~0.5 买、±0.1 中性、-0.5~-0.1 卖、<-0.5 强卖；Summary = MA 评级与振荡器评级的平均。规则是"状态 + 方向"的组合：RSI 37.6 是 Neutral（规则要求 <30 且回升才 Buy），CCI −151 是 Buy（<−100 且回升），Hull MA 237.68 < 价格 238.20 所以 Buy，其余 14 条均线都在价格上方所以全 Sell。本质是把 26 个异构指标压成一个可比标量，并且让用户能逐行核对每个 -1/0/+1 是怎么来的。

## 四、用户 / 场景 → 信息需求的映射

| 用户 | 关心什么 | 被路由到 |
|---|---|---|
| 股息捕获 / 短线套利 | ex-date、amount、当日缺口、流动性 | 日历 + Technicals 短周期（1m~4h） |
| 收益型长期持有 | Yield TTM、Payout ratio、连续性、增长 | 股息页 20 年图 + 指标表 |
| 事件驱动 / 量化 | 批量、跨市场、去重、时区一致 | 日历的 G20 / Primary listing / 时区过滤就是给这类人的 |
| 图表交易者 | 多周期评级、支撑阻力 | Technicals 的 timeframe 切换 + Pivots |

同一个入口进来，靠点击深度自然分流，没有让用户先选"我是谁"。

## 五、从对冲基金数据 / AI 研究员视角看：断点在哪

**1. 日历和 Technicals 之间缺了"股息-价格"这一环，而且这一环恰好在 VLS 上肉眼可见。**
VLS 9/18 是 ex-date，当天 −1.47 INR；股息 1.50 INR。跌幅就是机械除权，几乎不含任何信息。但 Technicals 里的 14 条均线 Sell 恰恰是被这个除权缺口进一步推低的。日历不告诉你"预计缺口 ≈ 0.63%"，Technicals 也不告诉你"今天的跌是除权"。基金侧必须自己做：**在 dividend-adjusted 序列和 raw 序列上分别跑评级，看分歧**。

**2. 日历没有质量维度，1004 行无法排优先级。**
没有 payout ratio、没有连续增派年数、没有 yield 的历史分位、没有市值 / 成交额。唯一能做的是 sort by yield，而高 yield 往往是价格崩了（yield trap）。Saudia Dairy 6.39% 和 Riyadh Steel 0.00% 并排出现，但没有任何字段帮你判断哪个值得点进去。

**3. 没有"预期 vs 实际"。**
Earnings calendar 有 EPS estimate vs actual，Dividend calendar 没有 expected vs declared，也没有 cut / raise 标记。股息的 alpha 大多来自"变化"而非"水平"，这一层完全空白。

**4. Technicals 是无状态快照。**
评级从什么时候变成 Sell 的、Sell 持续了几天、历史上这个评级组合的后验胜率——都没有。26 个指标等权平均，没有按 IC 加权，也没有因子间去相关（15 条均线本质上是一个因子）。

**5. 跨市场可比性是半成品。**
Amount 换成了 USD 但 yield 是本币口径；去重靠一个 Primary listing 开关，而不是把 listing 聚合到 issuer。

**值得直接抄的：** 事件→标的→执行的三跳导航、结论先行 + 明细可展开、用计数暴露置信度、多口径并列、以及那句模板生成的 narrative sentence——这是最早期的"数据→自然语言"，在 AI 时代可以直接升级为带证据链的 LLM 摘要。

**AI 化的机会：** 给日历每一行打一个"可交易性分数" = f(yield 分位, payout 可持续性, 流动性, 预期除权缺口, 在 dividend-adjusted 序列上的技术评级)，让 1004 行变成 top 20；把 26 个 -1/0/+1 换成 IC 加权并输出"评级切换时刻"作为事件。

如果你要拿这份拆解给团队看，我可以整理成一页带截图和链条图的页面。