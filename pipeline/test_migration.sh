#!/bin/bash
# 在真库副本上单独测试一个改库脚本：./test_migration.sh /path/to/00NN_name.py [工作目录]
# 不碰真库、不碰 migrations/；副本 = 当前真库（已应用 0000–0009）+ 只应用这一个脚本 → 跑 checks.py
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; SCRIPT="$1"; WORK="${2:-/tmp/anatole_test_$$}"
mkdir -p "$WORK/migrations"; cp "$HERE/anatole_ai_monitor.duckdb" "$WORK/test.duckdb"; cp "$SCRIPT" "$WORK/migrations/"
export ANATOLE_DB="$WORK/test.duckdb" ANATOLE_MIGRATIONS="$WORK/migrations"
cd "$HERE" && python3 migrate.py && python3 checks.py
echo "副本：$ANATOLE_DB（可用 python3 -c 'import duckdb;...' 查看）"
