#!/usr/bin/env bash
# 全量刷新:从 DuckDB 重生成三层数据 → 重建面板 → 推送到服务器
# serve.py/容器每次请求读文件,无需重启
set -e
cd "$(dirname "$0")"
echo "[1/6] 结果层"; python3 export_result_layer.py
echo "[2/6] 判断层"; python3 export_judgment.py
echo "[3/6] 总览";   python3 export_cockpit.py
echo "[4/6] 源数据"; python3 export_source.py
echo "[5/6] 构建面板"; python3 build_panel_full.py
echo "[6/6] 推送";   scp -q panel_full.html serve.py creatoraix:~/anatole/
echo "✓ deployed → https://creatoraix.top/AI-Monitoring-System ($(date +%H:%M))"
