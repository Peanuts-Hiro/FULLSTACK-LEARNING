#!/bin/bash

# プロジェクト完了後に自力コーディング用プロジェクトを提案・作成するスクリプト

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# 引数チェック（週番号を受け取る）
if [ $# -eq 0 ]; then
    echo "使用方法: ./suggest-selfcoding.sh <週番号>"
    echo "例: ./suggest-selfcoding.sh 1"
    exit 1
fi

WEEK_NUM=$1
WEEK_PADDED=$(printf "%02d" $WEEK_NUM)

# プロジェクトディレクトリを探す
PROJECT_DIR=$(ls -d projects/week${WEEK_PADDED}-* 2>/dev/null | head -n 1)

if [ -z "$PROJECT_DIR" ]; then
    echo "❌ 第${WEEK_NUM}週のプロジェクトが見つかりません"
    exit 1
fi

# 要件定義書と設計書の確認
if [ ! -f "$PROJECT_DIR/requirements.md" ] || [ ! -f "$PROJECT_DIR/design.md" ]; then
    echo "❌ 要件定義書または設計書が見つかりません"
    exit 1
fi

echo "==========================================="
echo "  🎯 自力コーディングプロジェクト提案"
echo "==========================================="
echo ""
echo "第${WEEK_NUM}週で学んだ内容を基に、"
echo "自力で作成できる他のアプリを提案します。"
echo ""
echo "📖 学習元プロジェクト: $PROJECT_DIR"
echo ""

# 学んだ技術を抽出
echo "📚 学んだ技術スタック:"
echo "-----------------------------------------"
grep -A 5 "使用技術" "$PROJECT_DIR/requirements.md" | tail -n +2 | grep -v "^$" || echo "- 情報を取得できませんでした"
echo ""

# 提案プロジェクトのリスト（週番号に応じて異なる提案を行う）
echo "💡 提案プロジェクト:"
echo "-----------------------------------------"

case $WEEK_NUM in
    1)
        # ToDoリスト（第1週）の場合の提案
        echo "1. ショッピングリストアプリ"
        echo "   - タスク管理の応用で商品リスト管理"
        echo "   - 追加/削除機能は同じ、数量管理を追加"
        echo ""
        echo "2. メモアプリ"
        echo "   - テキスト入力とリスト表示の応用"
        echo "   - 編集機能を追加して学習を深める"
        echo ""
        echo "3. カウンターアプリ（複数カウンター対応）"
        echo "   - カウンター名を入力して複数のカウンターを管理"
        echo "   - DOM操作とイベント処理の復習"
        ;;
    2)
        echo "1. 天気表示アプリ"
        echo "2. ニュースリーダー"
        echo "3. 為替レート表示アプリ"
        ;;
    3)
        echo "1. ブログシステム"
        echo "2. タスク管理ボード（Trello風）"
        echo "3. レシピ管理アプリ"
        ;;
    *)
        echo "（プロジェクト提案は週番号に応じて追加予定）"
        ;;
esac

echo ""
echo "-----------------------------------------"
echo "📝 プロジェクトを作成しますか？"
echo ""
echo "コマンド例:"
echo "  ./create-selfcoding-project.sh $WEEK_NUM 1 \"ショッピングリスト\""
echo ""
echo "または、Claudeに以下のように依頼してください:"
echo "  「第${WEEK_NUM}週の自力コーディングプロジェクト1を作成して」"
echo "==========================================="
