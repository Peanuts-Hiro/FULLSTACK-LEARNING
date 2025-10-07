#!/bin/bash

# エラーや小さな知識をerror-topicディレクトリに追加するスクリプト
# 使い方: ./add-topic.sh "ファイル名" "タイトル"

# 現在のディレクトリを確認
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# 引数チェック
if [ $# -lt 2 ]; then
    echo "使い方: ./add-topic.sh <ファイル名> <タイトル>"
    echo "例: ./add-topic.sh \"defer-attribute\" \"defer属性とは\""
    echo ""
    echo "実行後、エディタで内容を追加してください。"
    exit 1
fi

FILENAME="$1"
TITLE="$2"

# learning.csvから現在の週を取得
if [ ! -f "settings/learning.csv" ]; then
    echo "⚠️  learning.csvが見つかりません"
    exit 1
fi

# CSVの2行目から週番号を取得
WEEK=$(sed -n '2p' settings/learning.csv | cut -d',' -f3)

# プロジェクトディレクトリを特定
PROJECT_DIR="projects/week$(printf "%02d" $WEEK)-*"

if ! ls -d $PROJECT_DIR 2>/dev/null | head -n 1 > /dev/null; then
    echo "⚠️  プロジェクトディレクトリが見つかりません"
    exit 1
fi

ACTUAL_PROJECT_DIR=$(ls -d $PROJECT_DIR 2>/dev/null | head -n 1)

# knowledge/error-topicディレクトリを作成
ERROR_TOPIC_DIR="$ACTUAL_PROJECT_DIR/knowledge/error-topic"
mkdir -p "$ERROR_TOPIC_DIR"

# ファイルパスを生成
FILEPATH="$ERROR_TOPIC_DIR/${FILENAME}.md"

# ファイルが既に存在する場合は確認
if [ -f "$FILEPATH" ]; then
    echo "⚠️  ファイルが既に存在します: $FILEPATH"
    read -p "上書きしますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "キャンセルしました"
        exit 0
    fi
fi

# テンプレートを作成
cat > "$FILEPATH" << EOF
# $TITLE

## 発生したエラー/警告
\`\`\`
ここにエラーメッセージや警告メッセージを記載
\`\`\`

## 原因
エラーや警告が発生した理由を説明

## 修正内容

### 修正前
\`\`\`html
<!-- 修正前のコード -->
\`\`\`

### 修正後
\`\`\`html
<!-- 修正後のコード -->
\`\`\`

## 解説
なぜこの修正で解決するのか、技術的な説明

## 参考リンク
- [関連ドキュメント](URL)

---
**記録日:** $(date +%Y-%m-%d)
EOF

echo "✅ トピックファイルを作成しました"
echo "📄 場所: $FILEPATH"
echo ""
echo "次のコマンドでファイルを編集できます:"
echo "  vi $FILEPATH"
echo "  または"
echo "  code $FILEPATH"
