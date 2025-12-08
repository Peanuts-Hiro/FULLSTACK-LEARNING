# フルスタックエンジニア学習プログラム

## 概要
このリポジトリは、フルスタックエンジニア（シニアレベル）を目指すための体系的な学習プログラムです。週ごとに実践的なプロジェクトを通して、フロントエンドからバックエンド、インフラまで幅広いスキルを習得できます。

## 特徴
- 📚 **段階的学習**: 要件定義 → 設計 → 実装 → テストの流れで学習
- 💡 **実践重視**: 毎週1つのプロジェクトを完成させる
- 🎯 **自力コーディング**: 学んだ内容を自力で実装する練習プロジェクト
- 📝 **知識の記録**: 学習内容を体系的に記録・復習できる
- 🤖 **Claudeサポート**: AIがステップバイステップでガイド


## ディレクトリ構成
```
fullstack-learning/
├── settings/
│   ├── learning-program/          # 学習プログラム関連
│   │   ├── bin/                   # 実行可能スクリプト
│   │   │   ├── start-learning.sh  # 学習開始
│   │   │   ├── handle-selfcoding.sh # 自力コーディング処理
│   │   │   ├── add-knowledge.sh   # 知識記録
│   │   │   └── add-topic.sh       # トピック記録
│   │   ├── lib/                   # ライブラリ/ヘルパー
│   │   │   ├── suggest-selfcoding.sh
│   │   │   ├── create-selfcoding-project.sh
│   │   │   └── selfcoding-tutorial.sh
│   │   ├── data/                  # データファイル
│   │   │   ├── dev-schedule.csv   # 5年間の学習スケジュール
│   │   │   ├── learning.csv       # 現在の進捗
│   │   │   └── selfcoding-progress.csv
│   │   └── docs/                  # ドキュメント
│   │       └── selfcoding-instructions.md
│   ├── calendar-sync/             # Googleカレンダー同期
│   │   ├── scripts/               # 同期スクリプト
│   │   └── docs/                  # セットアップガイド
│   └── credentials/               # 認証情報（.gitignore）
├── projects/                      # 週ごとのプロジェクト
│   ├── week01-portfolio/
│   │   └── knowledge/             # 学習内容記録
│   └── ...
├── projects-selfcoding/           # 自力コーディング用
├── start                          # 学習開始ショートカット
├── knowledge                      # 知識記録コマンド
├── topic                          # トピック記録コマンド
└── README.md
```

## 使い方

### 学習を開始する
```bash
./start
```
または
```bash
./settings/learning-program/bin/start-learning.sh
```
このコマンドで現在の学習進捗と前回の学習内容まとめが表示されます。

### 学習の進め方
1. `./start` で進捗を確認
2. Claudeに「次へ」と入力して次の工程に進む
3. 開発工程ごとに段階的に学習を進めます
4. 各工程が理解できたら「次へ」とリクエストしてください
5. 完了した項目は`settings/learning-program/data/dev-schedule.csv`の「完了」列にチェックマークが追記されます

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
./settings/learning-program/bin/handle-selfcoding.sh
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
./settings/learning-program/lib/selfcoding-tutorial.sh projects-selfcoding/week01-01-プロジェクト名

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
./settings/learning-program/bin/add-knowledge.sh "ファイル名" "タイトル"
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
./settings/learning-program/bin/add-topic.sh "ファイル名" "タイトル"
```

**保存先**: `projects/week01-xxx/knowledge/error-topic/ファイル名.md`

## 学習の進め方
- 各週のプロジェクトは `projects/` ディレクトリ内に作成されます
- コードには初心者向けの詳細なコメントが記載されます
- 理解できるまで次の工程には進みません
- 質問があればいつでもClaudeに聞いてください

## 現在の進捗
`settings/learning-program/data/learning.csv`で現在の学習状況を確認できます。

## Googleカレンダー連携

学習スケジュールをGoogleカレンダーに同期できます。

### セットアップ
詳細は `settings/calendar-sync/docs/CALENDAR_SETUP.md` を参照してください。

### 使い方
```bash
# カレンダーに同期
./settings/calendar-sync/scripts/sync

# リスケジュール（第5週以降を2週間後ろにずらす）
python settings/calendar-sync/scripts/reschedule-learning.py --from-week 5 --shift-weeks 2 --sync
```

### 機能
- ✅ 全学習スケジュールを自動でカレンダーに登録（週全体に終日イベントとして表示）
- ✅ イベントの更新・削除に対応
- ✅ リスケジュール機能（予定の一括変更）
- ✅ リマインダー設定（1日前、1時間前）
- ✅ 重複を防ぐ仕組み（extendedPropertiesで管理）

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
chmod +x start knowledge topic
chmod +x settings/learning-program/bin/*.sh
chmod +x settings/learning-program/lib/*.sh
chmod +x settings/calendar-sync/scripts/*

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
