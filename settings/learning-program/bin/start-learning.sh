#!/bin/bash

# フルスタック学習プログラム - 学習開始スクリプト

# 現在のディレクトリを確認
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$ROOT_DIR"

echo "========================================="
echo "  フルスタック学習プログラム"
echo "========================================="
echo ""

# learning.csvから現在の進捗を読み込む
if [ -f "settings/learning-program/data/learning.csv" ]; then
    echo "📊 現在の学習進捗:"
    echo "-----------------------------------------"

    # CSVの2行目（データ行）を読み込む
    CURRENT_LINE=$(sed -n '2p' settings/learning-program/data/learning.csv)

    # カンマで分割
    IFS=',' read -r YEAR MONTH WEEK CONTENT PHASE STATUS MEMO <<< "$CURRENT_LINE"

    echo "📅 年月: ${YEAR}年${MONTH}月 第${WEEK}週"
    echo "📝 第${WEEK}週の開発内容: $CONTENT"
    echo "🔧 現在の開発工程: $PHASE"
    echo "✅ ステータス: $STATUS"
    echo "💡 学習メモ: $MEMO"
    echo ""

    # 前回の学習内容のまとめを表示
    echo "-----------------------------------------"
    echo "📚 前回の学習内容まとめ:"
    echo "-----------------------------------------"

    # プロジェクトディレクトリを確認
    PROJECT_DIR="projects/week$(printf "%02d" $WEEK)-*"

    if ls -d $PROJECT_DIR 2>/dev/null | head -n 1 > /dev/null; then
        ACTUAL_PROJECT_DIR=$(ls -d $PROJECT_DIR 2>/dev/null | head -n 1)

        # requirements.mdが存在するか確認
        if [ -f "$ACTUAL_PROJECT_DIR/requirements.md" ]; then
            echo "✓ 要件定義書が作成されました"
            echo "  場所: $ACTUAL_PROJECT_DIR/requirements.md"
        fi

        # design.mdが存在するか確認
        if [ -f "$ACTUAL_PROJECT_DIR/design.md" ]; then
            echo "✓ 設計書が作成されました"
            echo "  場所: $ACTUAL_PROJECT_DIR/design.md"
        fi

        # 実装ファイルの存在確認
        if [ -f "$ACTUAL_PROJECT_DIR/index.html" ]; then
            echo "✓ HTMLファイルが実装されました"
        fi

        if [ -f "$ACTUAL_PROJECT_DIR/style.css" ]; then
            echo "✓ CSSファイルが実装されました"
        fi

        if [ -f "$ACTUAL_PROJECT_DIR/script.js" ]; then
            echo "✓ JavaScriptファイルが実装されました"
        fi

        echo ""
        echo "現在の工程: $PHASE"
        echo ""
    else
        echo "まだプロジェクトが開始されていません"
        echo "これから「$CONTENT」の学習を始めます"
        echo ""
    fi

    echo "-----------------------------------------"
    echo "💬 Claudeに「次へ」と入力すると次の工程に進めます"
    echo "💬 「selfcoding」と入力すると自力コーディングプロジェクトを提案します"
    echo "💬 質問がある場合はいつでも聞いてください"
    echo "========================================="

else
    echo "⚠️  learning.csvが見つかりません"
    echo "学習プログラムを初期化してください"
fi
