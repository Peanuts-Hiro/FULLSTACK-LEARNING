# Googleカレンダー連携セットアップ手順

## 1. Google Cloud Projectのセットアップ

### 1.1 Google Cloud Consoleにアクセス
1. https://console.cloud.google.com/ にアクセス
2. 新しいプロジェクトを作成（例: "fullstack-learning"）

### 1.2 Google Calendar APIを有効化
1. 「APIとサービス」→「ライブラリ」に移動
2. "Google Calendar API" を検索
3. 「有効にする」をクリック

### 1.3 OAuth 2.0認証情報を作成
1. 「APIとサービス」→「認証情報」に移動
2. 「認証情報を作成」→「OAuthクライアントID」を選択
3. アプリケーションの種類: 「デスクトップアプリ」を選択
4. 名前を入力（例: "Learning Calendar Sync"）
5. 「作成」をクリック
6. **JSONをダウンロード**して `settings/credentials/credentials.json` として保存

## 2. 必要なPythonパッケージのインストール

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## 3. 初回認証

初回実行時にブラウザが開き、Googleアカウントでの認証が求められます。

```bash
python settings/sync-to-calendar.py
```

認証後、`settings/credentials/token.json` が自動生成されます。

## 4. .gitignoreに追加

認証情報をGitにコミットしないよう、`.gitignore`に以下を追加してください：

```
settings/credentials/
```

## セットアップ完了後の使い方

### カレンダーに同期
```bash
# 方法1: Pythonスクリプトを直接実行
python settings/calendar-sync/scripts/sync-to-calendar.py

# 方法2: ショートカットスクリプト
./settings/calendar-sync/scripts/sync
```

### スケジュールをリスケジュール
```bash
# 第5週以降を2週間後ろにずらす
python settings/calendar-sync/scripts/reschedule-learning.py --from-week 5 --shift-weeks 2

# 第10週以降を1ヶ月後ろにずらす
python settings/calendar-sync/scripts/reschedule-learning.py --from-week 10 --shift-months 1

# リスケジュール後、自動的にGoogleカレンダーに同期
python settings/calendar-sync/scripts/reschedule-learning.py --from-week 5 --shift-weeks 2 --sync
```

### イベント設定のカスタマイズ

`sync-to-calendar.py` の以下の設定を変更できます:

```python
# カレンダー設定
CALENDAR_NAME = 'フルスタック学習プログラム'  # カレンダー名
EVENT_COLOR_ID = '9'  # イベント色（1-11）

# イベント設定（終日イベントとして週全体に表示）
DEFAULT_REMINDER_MINUTES = [1440, 60]  # リマインダー（1日前、1時間前）
```

**注**: イベントは週全体（日曜〜土曜）の終日イベントとして登録されます。

色IDの一覧:
- 1: ラベンダー
- 2: セージ
- 3: ブドウ
- 4: フラミンゴ
- 5: バナナ
- 6: みかん
- 7: ピーコック
- 8: グラファイト
- 9: ブルーベリー（デフォルト）
- 10: バジル
- 11: トマト

## トラブルシューティング

### 認証エラーが出る場合
1. `settings/credentials/token.json` を削除
2. 再度 `sync-to-calendar.py` を実行

### APIクォータエラーが出る場合
- Google Calendar APIは1日あたり100万リクエストまで無料
- このスクリプトは数百イベントでも問題なく動作します

## セキュリティに関する注意

- `credentials.json` と `token.json` は**絶対にGitにコミットしないでください**
- これらのファイルには個人のGoogle認証情報が含まれています
- 共有する場合は必ず削除してください
