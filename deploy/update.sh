#!/usr/bin/env bash
# 就地改库 → 重建面板(不 scp)。serve.py 每次请求读文件,重建后无需重启。
# 用法: 在服务器上, 加完新 snapshot + migrations/00XX_*.py 后跑:
#   PYTHON=../pipeline/.venv/bin/python bash deploy/update.sh
# (PYTHON 不传则用系统 python3;构建需要 duckdb,建议用装了依赖的 venv)
set -euo pipefail
cd "$(dirname "$0")/../pipeline"
PY="${PYTHON:-python3}"

echo "[1/6] 应用迁移(改库, 带 change_log 审计)"; "$PY" migrate.py
echo "[2/6] 结果层"
if [ -f evidence_structure.py ]; then
  "$PY" export_result_layer.py
else
  echo "  ⚠ 跳过: 缺 evidence_structure.py(未随仓库提交)。结果层沿用已有 result_layer_data.json。"
  echo "    补回该文件后本步才会刷新 —— 见 deploy/README-DEPLOY.md「已知缺口」。"
fi
echo "[3/6] 判断层"; "$PY" export_judgment.py
echo "[4/6] 总览";   "$PY" export_cockpit.py
echo "[5/6] 源数据"; "$PY" export_source.py
echo "[6/6] 构建面板"; "$PY" build_panel_full.py
echo "✓ 重建完成 → $(pwd)/panel_full.html  ($(date '+%F %H:%M'))"
