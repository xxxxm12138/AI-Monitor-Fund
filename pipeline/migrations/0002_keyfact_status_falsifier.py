# -*- coding: utf-8 -*-
"""0002 · key_fact 加两列：status_line（一句话现状）与 falsifier（证伪条件）· owner B · 2026-09-20
UI 侧（E42）先写进了根目录 13-关键事实.csv；库是真源，这里把列与值落库。DDL 走 m.sql，字典同步进 schema_doc。"""
OWNER = 'B'

def up(m):
    m.sql("ALTER TABLE key_fact ADD COLUMN status_line TEXT", basis='E42 面板需要一句话现状')
    m.sql("ALTER TABLE key_fact ADD COLUMN falsifier TEXT", basis='E42 面板证伪条件（PM 视角四处不足之一）')
    m.sql("INSERT INTO schema_doc VALUES ('key_fact','status_line','一句话现状：上游 / 下游 / 政策同向与否 + 下一验证点（B 初稿 D 复核）','E42',false,NULL)", basis='字典同步')
    m.sql("INSERT INTO schema_doc VALUES ('key_fact','falsifier','证伪条件：AI 侧 + 需求侧 + 执行侧，出现即推翻当前判断（B 初稿 D 复核）','E42',false,NULL)", basis='字典同步')
    m.set('key_fact', 'kf055', 'status_line', '上游供给（中国光模块、云厂 capex）与下游需求（lab 融资转合同）同向；Q3 看并网兑现与预付到账', basis='E42 · 13-关键事实.csv 同步')
    m.set('key_fact', 'kf055', 'falsifier', 'AI 侧：Epoch 训练算力增速回落至 2×/年以下、开源与闭源差距归零且前沿档 API 降价，则训练需求逻辑弱化。需求侧：Reflection 类客户不续签、lab 融资转冷（半年无 $10B 级新轮），则需求真实性存疑。执行侧：12-31 并网 <800MW 或 Q3 预付到账明显低于 >$9B 年度指引节奏，则判断转观察。阈值为暂定（C6 未定）。', basis='E42 · 13-关键事实.csv 同步')
    m.set('key_fact', 'kf056', 'status_line', '企业 AI adoption 一手读数（Sub-ARR +33%）向好；政策侧 DOJ 支持 fair use 对数据治理顺风偏空', basis='E42 · 13-关键事实.csv 同步')
    m.set('key_fact', 'kf056', 'falsifier', 'Sub-ARR 增速连续两季低于 FY27 指引节奏（$1,880–1,885M 需约 +30%），或 NRR 转弱；AI-native 安全挑战者拿下大客户；法院采纳 fair use 立场使数据治理预算顺风消失。', basis='E42 · 13-关键事实.csv 同步')
    m.set('key_fact', 'kf057', 'status_line', '收入下滑但首个 75MW 数据中心供电协议落地；验证点是产能目标 100MW 与协议细节披露', basis='E42 · 13-关键事实.csv 同步')
    m.set('key_fact', 'kf057', 'falsifier', '10-31 年化产能未达 100MW；Q4 仍不披露 75MW 对手方与金额；数据中心供电订单半年无新增，则「算力能源约束代理」的逻辑失去证据。', basis='E42 · 13-关键事实.csv 同步')
