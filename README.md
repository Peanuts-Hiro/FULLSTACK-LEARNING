# フルスタックエンジニア学習プログラム

## 概要
このリポジトリは、フルスタックエンジニア（シニアレベル）を目指すための体系的な学習プログラムです。週ごとに実践的なプロジェクトを通して、フロントエンドからバックエンド、インフラまで幅広いスキルを習得できます。

## 特徴
- 📚 **段階的学習**: 要件定義 → 設計 → 実装 → テストの流れで学習
- 💡 **実践重視**: 毎週1つのプロジェクトを完成させる
- 🎯 **自力コーディング**: 学んだ内容を自力で実装する練習プロジェクト
- 📝 **知識の記録**: 学習内容を体系的に記録・復習できる
- 🤖 **Claudeサポート**: AIがステップバイステップでガイド

## 完成プロジェクト例

### Week 01: ToDoリストアプリ
シンプルなWebアプリケーションの基礎を学習します。

**学習内容**:
- HTML/CSS/JavaScriptの基本
- DOM操作とイベント処理
- ローカルストレージを使ったデータ永続化

**デモ**: `projects/week01-todo-app/` を開いて `index.html` をブラウザで開いてください

[完成プロジェクトの詳細はこちら →](projects/week01-todo-app/README.md)

## ディレクトリ構成
```
fullstack-learning/
├── settings/                # 学習プログラム管理用ファイル群
│   ├── schedule.csv         # 全体の学習スケジュール（3年分）
│   ├── learning.csv         # 現在の進捗管理ファイル
│   ├── start-learning.sh    # 学習開始スクリプト
│   ├── handle-selfcoding.sh # 自力コーディングプロジェクト処理
│   ├── suggest-selfcoding.sh # プロジェクト提案スクリプト
│   ├── create-selfcoding-project.sh # プロジェクト作成スクリプト
│   ├── add-knowledge.sh     # 体系的知識記録スクリプト
│   └── add-topic.sh         # エラー・小知識記録スクリプト
├── projects/                # 週ごとのプロジェクトディレクトリ
│   ├── week01-todo-app/
│   │   └── knowledge/       # 学習内容記録
│   │       ├── *.md         # 体系的な知識
│   │       └── error-topic/ # エラーや小さな知識
│   ├── week02-auth-app/
│   └── ...
├── projects-selfcoding/     # 自力コーディング用プロジェクト
│   └── ...
├── start                    # 学習開始ショートカット
├── knowledge                # 体系的知識記録コマンド
├── topic                    # エラー・小知識記録コマンド
└── README.md                # このファイル
```

## 使い方

### 学習を開始する
```bash
./start
```
または
```bash
./settings/start-learning.sh
```
このコマンドで現在の学習進捗と前回の学習内容まとめが表示されます。

### 学習の進め方
1. `./start` で進捗を確認
2. Claudeに「次へ」と入力して次の工程に進む
3. 開発工程ごとに段階的に学習を進めます
4. 各工程が理解できたら「次へ」とリクエストしてください
5. 完了した項目は`settings/schedule.csv`の「完了」列にチェックマークが追記されます

### 自力コーディングプロジェクトを作成する
学習した内容を使って、自力でコーディングするための練習プロジェクトを作成できます。

#### ステップ1: プロジェクト作成
1. `./start` で進捗を確認後、Claudeに「selfcoding」と入力
2. 現在の週に基づいて、類似プロジェクトの提案が表示されます
3. プロジェクト番号（1, 2, 3...）を入力
4. プロジェクト名を入力（例: ショッピングリスト）
5. `projects-selfcoding/` ディレクトリにプロジェクトが作成されます

または、直接スクリプトを実行することもできます:
```bash
./settings/handle-selfcoding.sh
```

#### ステップ2: 要件定義と設計
プロジェクト作成後、以下を作成します:
1. `requirements.md` - 要件定義書
2. `design.md` - 設計書

Claudeに「〇〇プロジェクトの要件定義を手伝って」と依頼できます。

#### ステップ3: 実装（チュートリアルモード）
要件定義と設計が完了したら、チュートリアルモードで実装を開始します。

**重要**: `projects-selfcoding/` 配下では、Claudeはコードを生成しません。代わりに、ステップバイステップで何を書くべきかガイドします。

実装開始方法:
```bash
# コマンドで開始
./settings/selfcoding-tutorial.sh projects-selfcoding/week01-01-プロジェクト名

# またはClaudeに話しかける
「projects-selfcoding/week01-01-プロジェクト名 の実装を始めたい」
```

チュートリアルモードの特徴:
- 一度に1つのステップのみ指示
- コードは自分で書く
- エラーが出たら一緒に解決
- 理解を確認してから次へ進む
- 質問にはすべて答える

### 学習内容を記録する

学習内容は2種類の方法で記録できます:

#### 1. 体系的な知識（knowledge）
DOM、イベント処理などの体系的な学習内容は `knowledge/` ディレクトリに保存します。

```bash
./knowledge "ファイル名" "タイトル"
# 例: ./knowledge "event-handling" "イベント処理の基礎"
```

または:
```bash
./settings/add-knowledge.sh "ファイル名" "タイトル"
```

**保存先**: `projects/week01-xxx/knowledge/ファイル名.md`

#### 2. エラーや小さな知識（topic）
エラー修正、警告対応などの小さな知識は `knowledge/error-topic/` ディレクトリに保存します。

```bash
./topic "ファイル名" "タイトル"
# 例: ./topic "defer-attribute" "defer属性とは"
```

または:
```bash
./settings/add-topic.sh "ファイル名" "タイトル"
```

**保存先**: `projects/week01-xxx/knowledge/error-topic/ファイル名.md`

## 学習の進め方
- 各週のプロジェクトは `projects/` ディレクトリ内に作成されます
- コードには初心者向けの詳細なコメントが記載されます
- 理解できるまで次の工程には進みません
- 質問があればいつでもClaudeに聞いてください

## 現在の進捗
`settings/learning.csv`で現在の学習状況を確認できます。

## セットアップ

### 前提条件
- Claude Code (Anthropic CLI)
- 基本的なターミナル操作の知識

### インストール
```bash
# リポジトリをクローン
git clone https://github.com/あなたのユーザー名/fullstack-learning.git
cd fullstack-learning

# 実行権限を付与
chmod +x start
chmod +x knowledge
chmod +x topic
chmod +x settings/*.sh

# 学習を開始
./start
```

## 推奨される学習の流れ
1. `./start` で現在の進捗を確認
2. Claudeに「次へ」と入力して次の工程へ進む
3. 各週のプロジェクトを完成させる
4. 「selfcoding」で自力コーディングに挑戦
5. 学んだ内容を `knowledge` や `topic` コマンドで記録

## ライセンス
MIT License - 詳細は [LICENSE](LICENSE) を参照してください。

## 貢献
Issue や Pull Request を歓迎します！

## 作者
学習者のための教育プロジェクトです。Claude AIのサポートを受けて構築されています。
