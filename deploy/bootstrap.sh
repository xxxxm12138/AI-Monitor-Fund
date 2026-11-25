#!/usr/bin/env bash
# 首次部署(服务器上, 已 git clone 本仓库后跑): 建 venv + 装依赖 + 首次构建一次面板。
# 之后装 systemd 常驻服务(见末尾提示) + 配反代(deploy/Caddyfile.snippet 或 nginx.conf.snippet)。
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR/pipeline"

echo ">>> 建 venv + 装 duckdb"
python3 -m venv .venv
./.venv/bin/pip install -q --upgrade pip
./.venv/bin/pip install -q -r "$REPO_DIR/deploy/requirements.txt"

echo ">>> 首次构建面板"
PYTHON="$REPO_DIR/pipeline/.venv/bin/python" bash "$REPO_DIR/deploy/update.sh"

echo ""
echo "✓ 首次构建完成。接下来:"
echo "  1) 装常驻服务(serve.py 用系统 python3 即可):"
echo "       sed 's#/REPLACE_ME/AI-Monitor-Fund#$REPO_DIR#g' $REPO_DIR/deploy/anatole.service | sudo tee /etc/systemd/system/anatole.service"
echo "       sudo systemctl daemon-reload && sudo systemctl enable --now anatole"
echo "       # 验证: curl -s http://127.0.0.1:8090/ | head"
echo "  2) 配反代: 见 $REPO_DIR/deploy/Caddyfile.snippet 或 nginx.conf.snippet"
echo "  3) 以后更新数据: 加 snapshot + migrations/00XX_*.py, 然后"
echo "       PYTHON=$REPO_DIR/pipeline/.venv/bin/python bash $REPO_DIR/deploy/update.sh"
