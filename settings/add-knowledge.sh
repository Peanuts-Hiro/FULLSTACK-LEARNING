#!/bin/bash

# 体系的な学習内容をknowledgeディレクトリに追加するスクリプト
# 使い方: ./add-knowledge.sh "ファイル名" "タイトル"

# 現在のディレクトリを確認
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# 引数チェック
if [ $# -lt 2 ]; then
    echo "使い方: ./add-knowledge.sh <ファイル名> <タイトル>"
    echo "例: ./add-knowledge.sh \"dom-basics\" \"DOM基礎\""
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

# knowledgeディレクトリを作成
KNOWLEDGE_DIR="$ACTUAL_PROJECT_DIR/knowledge"
mkdir -p "$KNOWLEDGE_DIR"

# ファイルパスを生成
FILEPATH="$KNOWLEDGE_DIR/${FILENAME}.md"

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

## 概要
ここに学習内容の概要を記載します。

## 詳細

### セクション1
内容を記載

### セクション2
内容を記載

## コード例

\`\`\`javascript
// コード例をここに記載
\`\`\`

## まとめ
- ポイント1
- ポイント2
- ポイント3

---
**学習日:** $(date +%Y-%m-%d)
EOF

echo "✅ 体系的な知識ファイルを作成しました"
echo "📄 場所: $FILEPATH"
echo ""
echo "💡 このファイルは体系的な学習内容用です"
echo "   エラーや小さな知識は ./topic コマンドを使用してください"
echo ""
echo "次のコマンドでファイルを編集できます:"
echo "  vi $FILEPATH"
echo "  または"
echo "  code $FILEPATH"
