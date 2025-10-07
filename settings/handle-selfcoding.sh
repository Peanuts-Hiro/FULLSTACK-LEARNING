#!/bin/bash

# selfcodingコマンドを処理するスクリプト

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# learning.csvから現在の週番号を取得
if [ ! -f "settings/learning.csv" ]; then
    echo "❌ learning.csvが見つかりません"
    exit 1
fi

CURRENT_LINE=$(sed -n '2p' settings/learning.csv)
IFS=',' read -r YEAR MONTH WEEK CONTENT PHASE STATUS MEMO <<< "$CURRENT_LINE"

# 提案を表示
./settings/suggest-selfcoding.sh "$WEEK"

# ユーザーの確認を待つ
echo ""
echo "提案内容に問題がなければ、プロジェクトを作成します。"
echo "プロジェクト番号を入力してください（1, 2, 3...）:"
read -r PROJECT_NUM

# 数値チェック
if ! [[ "$PROJECT_NUM" =~ ^[0-9]+$ ]]; then
    echo "❌ 無効な番号です"
    exit 1
fi

# プロジェクト名を取得
echo "プロジェクト名を入力してください（例: ショッピングリスト）:"
read -r PROJECT_NAME

if [ -z "$PROJECT_NAME" ]; then
    echo "❌ プロジェクト名が入力されていません"
    exit 1
fi

# プロジェクトを作成
./settings/create-selfcoding-project.sh "$WEEK" "$PROJECT_NUM" "$PROJECT_NAME"
