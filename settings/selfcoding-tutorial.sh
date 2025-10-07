#!/bin/bash

# 自力コーディングプロジェクトのチュートリアルスクリプト
# ステップバイステップで実装をガイドする

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

PROGRESS_FILE="settings/selfcoding-progress.csv"

# 引数チェック
if [ $# -lt 1 ]; then
    echo "使用方法: ./selfcoding-tutorial.sh <プロジェクトディレクトリ>"
    echo "例: ./selfcoding-tutorial.sh projects-selfcoding/week01-01-shopping-list"
    exit 1
fi

PROJECT_DIR=$1

# プロジェクトディレクトリの存在確認
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ プロジェクトディレクトリが見つかりません: $PROJECT_DIR"
    exit 1
fi

# 要件定義書と設計書の確認
if [ ! -f "$PROJECT_DIR/requirements.md" ]; then
    echo "⚠️  要件定義書が見つかりません"
    echo "まず要件定義書を作成してください: $PROJECT_DIR/requirements.md"
    exit 1
fi

if [ ! -f "$PROJECT_DIR/design.md" ]; then
    echo "⚠️  設計書が見つかりません"
    echo "まず設計書を作成してください: $PROJECT_DIR/design.md"
    exit 1
fi

# 進捗ファイルから現在のステップを取得
CURRENT_STEP=""
if [ -f "$PROGRESS_FILE" ]; then
    CURRENT_STEP=$(grep "^$PROJECT_DIR," "$PROGRESS_FILE" | cut -d',' -f2)
fi

# 初回実行の場合
if [ -z "$CURRENT_STEP" ]; then
    CURRENT_STEP="要件定義"
    echo "$PROJECT_DIR,要件定義,進行中,$(date +%Y-%m-%d)" >> "$PROGRESS_FILE"
fi

echo "==========================================="
echo "  🎓 自力コーディング チュートリアル"
echo "==========================================="
echo ""
echo "📁 プロジェクト: $PROJECT_DIR"
echo "📍 現在のステップ: $CURRENT_STEP"
echo ""
echo "-------------------------------------------"
echo ""
echo "このチュートリアルでは、ステップバイステップで"
echo "実装をガイドします。"
echo ""
echo "【重要な約束】"
echo "1. コードは自分で書く"
echo "2. エラーが出たら必ず解決してから次に進む"
echo "3. わからないことは質問する"
echo "4. 急がず、理解しながら進める"
echo ""
echo "-------------------------------------------"
echo ""
echo "Claudeに以下のように話しかけてください:"
echo ""
echo "  「このプロジェクトの実装を始めたい」"
echo ""
echo "または"
echo ""
echo "  「次のステップを教えて」"
echo ""
echo "-------------------------------------------"
echo ""
echo "💡 Claudeは以下のようにガイドします:"
echo ""
echo "  1. 今から何を作るか説明"
echo "  2. どのように考えるか解説"
echo "  3. 実装の手順を1つずつ指示"
echo "  4. エラーや質問に対応"
echo "  5. 理解を確認してから次へ"
echo ""
echo "==========================================="
