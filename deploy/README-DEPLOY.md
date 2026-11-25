# 部署手册 · Anatole 监测面板（公司服务器 + 持续更新）

面板 = `pipeline/serve.py`（极简静态服务器，**纯 Python 标准库、零依赖、无 docker**）服务 `pipeline/panel_full.html`（自包含单文件，由 DuckDB 真理源 + 构建链生成）。

- **构建链唯一第三方依赖**：`duckdb`（见 `deploy/requirements.txt`）。
- **数据更新 = 人工**：没有爬虫/定时任务。更新 = 加原文快照(snapshot) + 写一个 `migrations/00XX_*.py` 入库 → 重建面板。
- **真理源** `pipeline/anatole_ai_monitor.duckdb` 已随仓库提交，迁移自带数据。

---

## 一、架构（Arch 1：整仓上服务器，就地改库 + 重建）—— 推荐

```
公司服务器
  AI-Monitor-Fund/            (git clone)
    pipeline/
      serve.py          ← systemd 常驻, 听 127.0.0.1:8090, 服务 panel_full.html
      panel_full.html   ← 构建产物(update.sh 重建)
      migrations/       ← 加新脚本 = 加新数据
      *.py, *.duckdb    ← 构建链 + 真理源
  (公司 nginx/Caddy) 反代 子域名或路径 → 127.0.0.1:8090
```

serve.py 每次请求都重新读文件 → **重建后无需重启服务**。

### 首次上线
```bash
git clone https://github.com/xxxxm12138/AI-Monitor-Fund.git
cd AI-Monitor-Fund
bash deploy/bootstrap.sh        # 建 venv + 装 duckdb + 首次构建
# 按 bootstrap 结尾提示装 systemd 服务 + 配反代
```
- 常驻服务：把 `deploy/anatole.service` 里的 `/REPLACE_ME/...` 换成实际路径 → 放 `/etc/systemd/system/` → `systemctl enable --now anatole`。
- 反代：`deploy/Caddyfile.snippet` 或 `deploy/nginx.conf.snippet`，二选一（子域名或路径）。

### 持续更新（每次有新数据）
```bash
cd AI-Monitor-Fund/pipeline
# 1) 把新原文快照放进 snapshots/  （带来源 URL、P 级、知悉时间）
# 2) 写 migrations/00XX_新内容.py  （用 m.observe/m.set/m.supersede 改库，格式见现有脚本）
# 3) 重建:
PYTHON=./.venv/bin/python bash ../deploy/update.sh
```
`update.sh` = `migrate.py`（应用新迁移、带字段级 change_log 审计）→ 重跑 export + build → 刷新 `panel_full.html`。

---

## 二、Arch 2（备选）：本地构建，只推产物到服务器

公司服务器只当静态服，**零构建依赖**；更新都在你本地做。
- 本地跑 `update.sh` 生成 `panel_full.html` → `scp panel_full.html serve.py 服务器:~/anatole/`。
- 服务器端只需 systemd 跑 serve.py + 反代。
- 适合：只有你一人更新、且不想在公司服务器上装构建环境。

---

## 三、⚠️ 已知缺口：`evidence_structure.py` 未随仓库提交

- `pipeline/export_result_layer.py` 依赖 `evidence_structure.py`，但该文件**不在仓库里**（也没被 .gitignore，就是没提交）。
- 影响：**「结果层」刷新步骤会跳过**（`update.sh` 已做容错，自动跳过并沿用已提交的 `result_layer_data.json`）。其余层（判断/总览/源）正常，面板能正常构建与显示。
- 要让结果层也能刷新：从**当初本地构建的那台机器**找回 `evidence_structure.py`，放进 `pipeline/`，`update.sh` 会自动启用该步。

---

## 四、访问鉴权（可选）
serve.py 自带 HTTP Basic Auth：在 systemd 里设 `ANATOLE_USER` / `ANATOLE_PASS` 即可（见 `anatole.service` 注释）。公司内网若已有网关鉴权可不开。**切勿把密码提交进仓库**——只写在服务器的 service 文件里。

---

## 五、文件清单（本 deploy/ 目录）
| 文件 | 用途 |
|---|---|
| `README-DEPLOY.md` | 本手册 |
| `requirements.txt` | 构建依赖（duckdb） |
| `bootstrap.sh` | 首次部署（venv + 装依赖 + 首次构建） |
| `update.sh` | 持续更新（改库 → 重建，含缺口容错） |
| `anatole.service` | systemd 常驻服务模板 |
| `Caddyfile.snippet` | Caddy 反代片段（子域名 / 路径） |
| `nginx.conf.snippet` | nginx 反代片段（子域名 / 路径） |
