#!/bin/bash

# 自力コーディング用プロジェクトを作成するスクリプト

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# 引数チェック
if [ $# -lt 3 ]; then
    echo "使用方法: ./create-selfcoding-project.sh <学習週番号> <プロジェクト番号> <プロジェクト名>"
    echo "例: ./create-selfcoding-project.sh 1 1 \"ショッピングリスト\""
    exit 1
fi

WEEK_NUM=$1
PROJECT_NUM=$2
PROJECT_NAME=$3

WEEK_PADDED=$(printf "%02d" $WEEK_NUM)
PROJECT_NUM_PADDED=$(printf "%02d" $PROJECT_NUM)

# 元のプロジェクトディレクトリを確認
SOURCE_PROJECT=$(ls -d projects/week${WEEK_PADDED}-* 2>/dev/null | head -n 1)

if [ -z "$SOURCE_PROJECT" ]; then
    echo "❌ 第${WEEK_NUM}週のプロジェクトが見つかりません"
    exit 1
fi

# プロジェクト名からディレクトリ名を生成（スペースをハイフンに変換）
PROJECT_DIR_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
TARGET_DIR="projects-selfcoding/week${WEEK_PADDED}-${PROJECT_NUM_PADDED}-${PROJECT_DIR_NAME}"

# ディレクトリが既に存在する場合
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  プロジェクトディレクトリが既に存在します: $TARGET_DIR"
    echo "続行しますか？ (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "キャンセルしました"
        exit 0
    fi
fi

# ディレクトリ作成
mkdir -p "$TARGET_DIR"

echo "==========================================="
echo "  🎯 自力コーディングプロジェクト作成"
echo "==========================================="
echo ""
echo "📁 プロジェクト: $PROJECT_NAME"
echo "📂 ディレクトリ: $TARGET_DIR"
echo "📖 学習元: $SOURCE_PROJECT"
echo ""

# README.mdを作成
cat > "$TARGET_DIR/README.md" << EOF
# $PROJECT_NAME

## 📚 このプロジェクトについて

このプロジェクトは、**第${WEEK_NUM}週の学習内容を活かして自力で作成する**練習用プロジェクトです。

### 学習元プロジェクト
- \`$SOURCE_PROJECT\`

### 目的
第${WEEK_NUM}週で学んだ技術やパターンを使って、似た機能を持つアプリを**自力で**実装することで、理解を深めます。

---

## 🎯 実装の進め方

### ステップ1: 要件定義
学習元プロジェクトの \`requirements.md\` を参考に、このプロジェクトの要件定義を考えてみましょう。

- どんな機能が必要か？
- 何を入力として受け取るか？
- どのように表示するか？

まずは自分で考えて、\`requirements.md\` を作成してください。

### ステップ2: 設計
学習元プロジェクトの \`design.md\` を参考に、画面構成やデータの流れを設計しましょう。

- HTML構造はどうするか？
- どんなイベントが必要か？
- どんな関数を作るか？

\`design.md\` を作成してください。

### ステップ3: 実装
設計に基づいて、実際にコードを書いていきます。

**重要:** 最初は学習元を見ずに、自力で書いてみましょう。
詰まったら学習元のコードを確認してもOKですが、コピペではなく理解して書くことが大切です。

### ステップ4: テスト
実装した機能が正しく動くか確認しましょう。

---

## 📝 チェックリスト

進捗管理用のチェックリストです。

- [ ] 要件定義書を作成 (\`requirements.md\`)
- [ ] 設計書を作成 (\`design.md\`)
- [ ] HTMLファイルを作成 (\`index.html\`)
- [ ] CSSファイルを作成 (\`style.css\`)
- [ ] JavaScriptファイルを作成 (\`script.js\`)
- [ ] 基本機能の実装完了
- [ ] テスト完了
- [ ] 学習元と比較して復習

---

## 💡 学習元を確認する

詰まったときや、実装後に比較するときは、学習元プロジェクトを確認しましょう:

\`\`\`bash
# 学習元のディレクトリを開く
cd $SOURCE_PROJECT
\`\`\`

---

## 🚀 次のステップ

このプロジェクトが完成したら:

1. 学習元プロジェクトと比較して、違いや改善点を確認
2. 自分なりの機能追加に挑戦
3. 次の週の学習に進む

頑張ってください！ 💪
EOF

echo "✅ README.mdを作成しました"
echo ""
echo "📋 次のステップ:"
echo "  1. $TARGET_DIR/requirements.md を作成"
echo "  2. $TARGET_DIR/design.md を作成"
echo "  3. チュートリアルモードで実装を開始"
echo ""
echo "💡 要件定義と設計:"
echo "   Claudeに「第${WEEK_NUM}週プロジェクト${PROJECT_NUM}の要件定義を手伝って」と依頼できます"
echo ""
echo "💡 実装開始:"
echo "   要件定義と設計が完了したら、以下のコマンドでチュートリアル開始:"
echo "   ./settings/selfcoding-tutorial.sh $TARGET_DIR"
echo ""
echo "   またはClaudeに「$TARGET_DIR の実装を始めたい」と話しかけてください"
echo ""
echo "==========================================="
echo "プロジェクト作成完了: $TARGET_DIR"
echo "==========================================="
