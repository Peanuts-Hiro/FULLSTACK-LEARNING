# 環境変数設定ガイド

このプロジェクトでは、APIキーやシークレット情報をシステム環境変数で管理します。

## 設定方法

### 1. シェル設定ファイルを開く

使用しているシェルに応じて設定ファイルを編集します：

```bash
# Bashの場合
nano ~/.bashrc

# Zshの場合
nano ~/.zshrc

# Fishの場合
nano ~/.config/fish/config.fish
```

### 2. 環境変数を追加

ファイルの末尾に以下を追加：

```bash
# ==========================================
# フルスタック学習プログラム - 環境変数
# ==========================================

# Google Calendar API
export GOOGLE_CALENDAR_ID="primary"  # または特定のカレンダーID

# Notion API（使用する場合）
export NOTION_API_KEY="secret_xxxxxxxxxxxxx"
export NOTION_ROADMAP_PAGE_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export NOTION_DATABASE_ID=""  # オプション

# その他（将来の拡張用）
# export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
# export OPENAI_API_KEY="sk-xxxxxxxxxxxxx"
```

### 3. 設定を反映

```bash
# Bashの場合
source ~/.bashrc

# Zshの場合
source ~/.zshrc

# Fishの場合
source ~/.config/fish/config.fish
```

### 4. 設定確認

```bash
# 環境変数が設定されているか確認
echo $NOTION_API_KEY
echo $GOOGLE_CALENDAR_ID

# すべての環境変数を確認
env | grep NOTION
env | grep GOOGLE
```

## 必要な環境変数一覧

### Google Calendar連携

| 変数名 | 必須 | 説明 | 例 |
|--------|------|------|-----|
| `GOOGLE_CALENDAR_ID` | ○ | カレンダーID | `primary` または `xxxxx@group.calendar.google.com` |

**取得方法**:
1. Googleカレンダーを開く
2. 左側のカレンダー一覧から対象カレンダーの設定を開く
3. 「カレンダーの統合」セクションにある「カレンダーID」をコピー

### Notion連携（オプション）

| 変数名 | 必須 | 説明 | 例 |
|--------|------|------|-----|
| `NOTION_API_KEY` | ○ | Notionインテグレーショントークン | `secret_xxxxx...` |
| `NOTION_ROADMAP_PAGE_ID` | ○ | ロードマップページのID | 32文字の英数字 |
| `NOTION_DATABASE_ID` | - | データベースID（自動取得可） | 32文字の英数字 |

**取得方法**:

**APIキー**:
1. https://www.notion.so/my-integrations にアクセス
2. 「New integration」をクリック
3. 名前を入力して作成
4. 「Internal Integration Token」をコピー

**ページID**:
1. Notionでページを開く
2. URLを確認: `https://www.notion.so/ページ名-{ここの32文字}`
3. その32文字をコピー
4. ページの「…」メニューから「接続」→作成したインテグレーションを追加

## セキュリティのベストプラクティス

### ✅ 推奨

- システム環境変数に直接設定
- 設定ファイル（~/.bashrc等）のパーミッションを確認: `chmod 600 ~/.bashrc`
- 定期的にトークンをローテーション

### ❌ 非推奨

- `.env`ファイルにシークレット情報を記載（Claude等のAIツールから見える）
- スクリプト内にハードコーディング
- Gitリポジトリにコミット

## トラブルシューティング

### 環境変数が反映されない

```bash
# 現在のシェルを確認
echo $SHELL

# 正しい設定ファイルを編集しているか確認
# /bin/bash → ~/.bashrc
# /bin/zsh → ~/.zshrc

# 再度sourceコマンドを実行
source ~/.bashrc  # または ~/.zshrc
```

### 環境変数が見つからないエラー

```bash
# 環境変数が設定されているか確認
env | grep NOTION

# 設定されていない場合は再設定
export NOTION_API_KEY="your_actual_key"
```

### シェル起動時に毎回設定が必要

- 設定ファイル（~/.bashrc等）に追加されていない可能性
- ファイルを編集後、`source`コマンドを実行していない

## スクリプトでの使用方法

環境変数は既存のスクリプトで自動的に読み込まれます：

```bash
# カレンダー同期
./settings/calendar-sync/scripts/sync

# Notion同期（実装時）
./settings/notion-sync/scripts/sync
```

各スクリプトは環境変数が設定されていない場合、エラーメッセージを表示します。
