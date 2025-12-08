#!/usr/bin/env python3
"""
フルスタック学習プログラム - Googleカレンダー同期スクリプト

【このスクリプトの目的】
dev-schedule.csvに記載された学習スケジュールを読み込み、
Googleカレンダーに週単位の終日イベントとして自動登録・更新します。

【処理の流れ】
1. Google Calendar APIで認証
2. 専用カレンダーを取得/作成
3. CSVファイルから学習スケジュールを読み込み
4. 各週のイベントをカレンダーに同期（新規作成 or 更新）

【主な変数の依存関係】
main() → get_calendar_service() → service（APIクライアント）
main() → get_or_create_calendar(service) → calendar_id（カレンダーID）
main() → load_schedule() → schedule（学習データのリスト）
main() → sync_events_to_calendar(service, calendar_id, schedule)
"""

# ============================================================
# ライブラリのインポート
# ============================================================

import csv  # CSVファイル読み書き
import sys  # システム終了処理
from datetime import datetime, timedelta  # 日付計算用
from pathlib import Path  # ファイルパス操作用

# Google Calendar API関連のライブラリをインポート
# これらがインストールされていない場合はエラーメッセージを表示
try:
    from google.auth.transport.requests import Request  # トークン更新用
    from google.oauth2.credentials import Credentials  # 認証情報管理
    from google_auth_oauthlib.flow import InstalledAppFlow  # OAuth認証フロー
    from googleapiclient.discovery import build  # APIクライアント構築
except ImportError:
    print("❌ 必要なライブラリがインストールされていません")
    print("\n以下のコマンドを実行してください:")
    print("pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# ============================================================
# グローバル設定（スクリプト全体で使う定数）
# ============================================================

# Google Calendar APIのアクセス権限スコープ
# 'calendar'はカレンダーの読み書き権限を意味する
SCOPES = ['https://www.googleapis.com/auth/calendar']

# カレンダー設定
CALENDAR_NAME = 'フルスタック学習プログラム'  # 作成するカレンダーの名前
EVENT_COLOR_ID = '9'  # イベントの色（1-11の数字で指定、9=青色）

# イベント設定
# リマインダーを設定（単位: 分）
# 1440分 = 24時間 = 1日前、60分 = 1時間前
DEFAULT_REMINDER_MINUTES = [1440, 60]


# ============================================================
# 関数定義
# ============================================================

def get_calendar_service():
    """
    Google Calendar APIサービスを取得

    【処理フロー】
    1. 既存のtoken.jsonを確認（保存済みの認証情報）
    2. トークンが無効/期限切れなら更新
    3. トークンが存在しない場合は新規認証
       - credentials.jsonからOAuth設定を読み込み
       - ブラウザで認証URLを開いてコードを取得
       - 取得したコードでトークンを生成
    4. APIクライアント（service）を返す

    【変数の依存関係】
    credentials_path (credentials.json) → flow → creds → service
    token_path (token.json) → creds → service

    【戻り値】
    service: Google Calendar APIクライアント（Noneの場合は認証失敗）
    """
    creds = None  # 認証情報を格納する変数

    # パスの構築
    # __file__ = このスクリプトのパス
    # parent = 親ディレクトリ（scripts/ → calendar-sync/ → settings/）
    script_dir = Path(__file__).parent.parent  # settings/calendar-sync/
    token_path = script_dir.parent / 'credentials' / 'token.json'  # settings/credentials/token.json
    credentials_path = script_dir.parent / 'credentials' / 'credentials.json'  # settings/credentials/credentials.json

    # ステップ1: 既存のトークンファイルを確認
    # token.jsonが存在する場合、保存済みの認証情報を読み込む
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # ステップ2: 認証情報の検証と更新
    # creds.valid = Trueなら有効な認証情報
    if not creds or not creds.valid:
        # トークンが期限切れで、かつリフレッシュトークンがある場合
        if creds and creds.expired and creds.refresh_token:
            # トークンを更新（再認証不要）
            creds.refresh(Request())
        else:
            # ステップ3: 新規認証が必要
            # credentials.jsonが存在しない場合はエラー
            if not credentials_path.exists():
                print(f"❌ 認証情報ファイルが見つかりません: {credentials_path}")
                print("📖 セットアップ手順: settings/calendar-sync/docs/CALENDAR_SETUP.md を参照してください")
                return None

            # OAuth認証フローを開始
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)

            # WSL2環境用の設定
            # redirect_uriを'urn:ietf:wg:oauth:2.0:oob'に設定すると、
            # ブラウザでコードが表示され、手動入力できる
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

            # 認証URLを生成して表示
            print("\n以下のURLをブラウザで開いて認証してください:")
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"\n{auth_url}\n")

            # ユーザーが入力した認証コードを取得
            code = input("認証コードを入力してください: ")

            # 認証コードを使ってトークンを取得
            flow.fetch_token(code=code)
            creds = flow.credentials

        # ステップ4: トークンを保存（次回以降の認証を省略）
        # ディレクトリが存在しない場合は作成
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # ステップ5: APIクライアントを構築して返す
    # build()で'calendar' APIのv3バージョンを使うクライアントを作成
    return build('calendar', 'v3', credentials=creds)


def get_or_create_calendar(service):
    """
    専用カレンダーを取得または作成

    【処理フロー】
    1. 既存のカレンダー一覧を取得
    2. CALENDAR_NAMEと一致するカレンダーを探す
    3. 見つかればそのIDを返す
    4. 見つからなければ新規作成してIDを返す

    【引数】
    service: Google Calendar APIクライアント

    【戻り値】
    calendar_id: カレンダーのID（文字列）
    """
    # ステップ1: 既存のカレンダーリストを取得
    # service.calendarList().list() = カレンダー一覧取得API
    # .execute() = APIリクエストを実行
    calendar_list = service.calendarList().list().execute()

    # ステップ2: カレンダー名で検索
    # calendar_list.get('items', []) = カレンダーの配列を取得（なければ空配列）
    for calendar in calendar_list.get('items', []):
        # summary = カレンダーの表示名
        if calendar['summary'] == CALENDAR_NAME:
            print(f"✓ カレンダーを見つけました: {CALENDAR_NAME}")
            return calendar['id']  # カレンダーIDを返す

    # ステップ3: カレンダーが存在しない場合は新規作成
    print(f"📅 新しいカレンダーを作成: {CALENDAR_NAME}")
    calendar = {
        'summary': CALENDAR_NAME,  # カレンダー名
        'timeZone': 'Asia/Tokyo',  # タイムゾーン
        'description': 'フルスタックエンジニア学習プログラムのスケジュール'
    }
    # service.calendars().insert() = カレンダー作成API
    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar['id']


def calculate_week_date(year, month, week):
    """
    年、月、週番号から日付を計算

    【ロジック】
    - week=1 → その月の第1週の土曜日
    - week=2 → その月の第2週の土曜日
    - 以降同様

    【アルゴリズム】
    1. その月の1日を取得
    2. その月の最初の土曜日を見つける
    3. 週番号に応じて土曜日を計算

    【引数】
    year: 年（例: 2025）
    month: 月（例: 12）
    week: 週番号（例: 1）

    【戻り値】
    target_date: datetime オブジェクト（土曜日の日付）
    """
    # ステップ1: その月の1日を取得
    first_day = datetime(year, month, 1)

    # ステップ2: 最初の土曜日を計算
    # weekday() = 曜日を数値で返す（月曜=0, 火曜=1, ..., 土曜=5, 日曜=6）
    # (5 - first_day.weekday()) % 7 = 1日から土曜日まであと何日か
    #
    # 例: 1日が水曜日（2）の場合
    #   (5 - 2) % 7 = 3 → 3日後が土曜日
    # 例: 1日が土曜日（5）の場合
    #   (5 - 5) % 7 = 0 → 当日が土曜日
    days_until_saturday = (5 - first_day.weekday()) % 7
    first_saturday = first_day + timedelta(days=days_until_saturday)

    # ステップ3: 週番号に基づいて日付を計算
    # week=1 → first_saturday + 0週
    # week=2 → first_saturday + 1週
    # week=3 → first_saturday + 2週
    target_date = first_saturday + timedelta(weeks=(week - 1))

    return target_date


def load_schedule(csv_path):
    """
    dev-schedule.csvを読み込む

    【処理フロー】
    1. CSVファイルを開く
    2. 各行をdictionary形式で読み込み
    3. 必要な列を抽出してリストに格納

    【引数】
    csv_path: CSVファイルのパス

    【戻り値】
    schedule: 学習データのリスト
    [
        {
            'year': 2025,
            'month': 12,
            'week': 1,
            'content': 'HTML/CSS基礎',
            'project': '個人ポートフォリオ作成',
            'process': '要件定義 → 設計 → 実装 → テスト',
            'claude_usage': 'Claudeで設計レビュー',
            'url': 'https://example.com'
        },
        ...
    ]
    """
    schedule = []

    # CSVファイルを開く（UTF-8エンコーディング）
    with open(csv_path, 'r', encoding='utf-8') as f:
        # DictReader = 各行を辞書型で読み込む
        # 1行目（ヘッダー）をキーとして使用
        reader = csv.DictReader(f)

        for row in reader:
            # 各行から必要な情報を抽出
            schedule.append({
                'year': int(row['年度']),       # 文字列を整数に変換
                'month': int(row['月']),
                'week': int(row['週']),
                'content': row['学習内容'],
                'project': row['実践課題'],
                'process': row['開発工程'],
                'claude_usage': row['Claude活用法'],
                'url': row['メモ・参考URL']
            })

    return schedule


def create_event_body(item, start_date, end_date):
    """
    カレンダーイベントのボディ（データ）を作成

    【処理フロー】
    1. イベントの説明文を作成
    2. ユニークキーを生成（重複チェック用）
    3. Google Calendar API形式のイベントデータを構築

    【引数】
    item: 学習データ（dictionary）
    start_date: イベント開始日（datetime）
    end_date: イベント終了日（datetime）

    【戻り値】
    event_body: Google Calendar API用のイベントデータ（dictionary）
    """
    # ステップ1: イベントの説明文を作成
    description_parts = [
        f"📚 学習内容: {item['content']}",
        f"🎯 実践課題: {item['project']}",
        f"📋 開発工程: {item['process']}",
        f"🤖 {item['claude_usage']}",
    ]
    # URLが存在する場合のみ追加
    if item['url']:
        description_parts.append(f"\n📖 参考URL: {item['url']}")

    # リストを改行で結合
    description = '\n'.join(description_parts)

    # ステップ2: ユニークキーを生成
    # 形式: "2025-12-1" （年-月-週）
    # このキーで既存イベントを検索・更新する
    unique_key = f"{item['year']}-{item['month']:02d}-{item['week']}"

    # ステップ3: Google Calendar API形式でイベントデータを構築
    return {
        # イベントのタイトル
        'summary': f"Week {item['week']}: {item['content']}",

        # イベントの説明文
        'description': description,

        # 開始日（終日イベントなので'date'を使用、'dateTime'ではない）
        'start': {
            'date': start_date.strftime('%Y-%m-%d'),  # '2025-12-01'形式
        },

        # 終了日（Google Calendarの終日イベントは終了日を含まない）
        # 例: 日曜〜土曜のイベントなら、start=日曜、end=次の日曜
        'end': {
            'date': end_date.strftime('%Y-%m-%d'),
        },

        # イベントの色
        'colorId': EVENT_COLOR_ID,

        # リマインダー設定
        'reminders': {
            'useDefault': False,  # デフォルトのリマインダーを使わない
            'overrides': [
                # リスト内包表記でリマインダーを生成
                {'method': 'popup', 'minutes': min_before}
                for min_before in DEFAULT_REMINDER_MINUTES
            ],
        },

        # 拡張プロパティ（カスタムデータを保存）
        # このキーで既存イベントを検索できる
        'extendedProperties': {
            'private': {
                'fslearning_key': unique_key  # '2025-12-1'
            }
        }
    }


def sync_events_to_calendar(service, calendar_id, schedule):
    """
    スケジュールをカレンダーに同期

    【処理フロー】
    1. スケジュールの各項目をループ
    2. 週の開始日・終了日を計算
    3. イベントデータを作成
    4. 既存イベントを検索（extendedPropertiesのキーで）
    5. 既存イベントがあれば更新、なければ新規作成

    【変数の依存関係】
    schedule → item → saturday → sunday, next_sunday → event_body
    service, calendar_id, event_body → API呼び出し → 作成/更新

    【引数】
    service: Google Calendar APIクライアント
    calendar_id: カレンダーID
    schedule: 学習データのリスト
    """
    print(f"\n📊 同期開始: {len(schedule)} 件のイベント")

    # カウンター変数（統計情報用）
    created_count = 0   # 新規作成したイベント数
    updated_count = 0   # 更新したイベント数
    skipped_count = 0   # エラーでスキップしたイベント数

    # スケジュールの各項目を処理
    for item in schedule:
        try:
            # ステップ1: その週の土曜日を計算
            saturday = calculate_week_date(item['year'], item['month'], item['week'])

            # ステップ2: 週の範囲を計算（日曜〜土曜）
            # 土曜日から6日前が日曜日
            # 例: 土曜が12/7なら、日曜は12/1
            sunday = saturday - timedelta(days=6)

            # Google Calendarの終日イベントは終了日を含まないため、
            # 終了日は次の日曜日（土曜日 + 1日）
            # 例: 土曜が12/7なら、終了日は12/8
            next_sunday = saturday + timedelta(days=1)

            # ステップ3: イベントデータを作成
            event_body = create_event_body(item, sunday, next_sunday)
            unique_key = f"{item['year']}-{item['month']:02d}-{item['week']}"

            # ステップ4: 既存イベントを検索
            # privateExtendedProperty で extendedProperties の値で検索
            # 'fslearning_key=2025-12-1' のようなイベントを探す
            events_result = service.events().list(
                calendarId=calendar_id,
                privateExtendedProperty=f"fslearning_key={unique_key}",
                maxResults=1  # 最大1件（同じキーは1つしかないはず）
            ).execute()

            existing_events = events_result.get('items', [])

            # ステップ5: 既存イベントがあれば更新、なければ新規作成
            if existing_events:
                # イベントが既に存在する場合は更新
                existing_event = existing_events[0]
                service.events().update(
                    calendarId=calendar_id,
                    eventId=existing_event['id'],  # 既存イベントのID
                    body=event_body  # 新しいデータで上書き
                ).execute()
                updated_count += 1
                print(f"  ✓ 更新: {item['year']}/{item['month']:02d} Week{item['week']} - {item['content']}")
            else:
                # イベントが存在しない場合は新規作成
                service.events().insert(
                    calendarId=calendar_id,
                    body=event_body
                ).execute()
                created_count += 1
                print(f"  + 作成: {item['year']}/{item['month']:02d} Week{item['week']} - {item['content']}")

        except Exception as e:
            # エラーが発生した場合はスキップして次へ
            print(f"  ✗ エラー: {item['year']}/{item['month']:02d} Week{item['week']} - {e}")
            skipped_count += 1

    # 統計情報を表示
    print(f"\n✅ 同期完了!")
    print(f"  - 新規作成: {created_count} 件")
    print(f"  - 更新: {updated_count} 件")
    print(f"  - スキップ: {skipped_count} 件")


def main():
    """
    メイン処理

    【全体の流れ】
    1. CSVファイルのパスを構築
    2. ファイルの存在確認
    3. Google Calendar APIで認証
    4. カレンダーを取得/作成
    5. スケジュールを読み込み
    6. カレンダーに同期

    【変数の流れ】
    csv_path → schedule
    credentials → service
    service → calendar_id
    service, calendar_id, schedule → sync_events_to_calendar()
    """
    print("=" * 50)
    print("  Googleカレンダー同期スクリプト")
    print("=" * 50)

    # ステップ1: CSVファイルのパスを構築
    # __file__ = このスクリプトのパス（settings/calendar-sync/scripts/sync-to-calendar.py）
    # .parent.parent.parent = 3つ上のディレクトリ（fullstack-learning/）
    script_dir = Path(__file__).parent.parent.parent
    csv_path = script_dir / 'settings' / 'learning-program' / 'data' / 'dev-schedule.csv'

    # ステップ2: CSVファイルの存在確認
    if not csv_path.exists():
        print(f"❌ スケジュールファイルが見つかりません: {csv_path}")
        return

    # ステップ3: Google Calendar APIで認証
    print("\n🔐 Google認証中...")
    service = get_calendar_service()
    if not service:
        # 認証失敗の場合は終了
        return

    print("✓ 認証成功")

    # ステップ4: カレンダーを取得または作成
    calendar_id = get_or_create_calendar(service)

    # ステップ5: スケジュールを読み込む
    print(f"\n📖 スケジュールを読み込み: {csv_path}")
    schedule = load_schedule(csv_path)
    print(f"✓ {len(schedule)} 件の学習項目を読み込みました")

    # ステップ6: カレンダーに同期
    sync_events_to_calendar(service, calendar_id, schedule)

    print("\n" + "=" * 50)
    print("🎉 すべての処理が完了しました！")
    print("📅 Googleカレンダーを確認してください")
    print("=" * 50)


# ============================================================
# スクリプトのエントリーポイント
# ============================================================

# このスクリプトが直接実行された場合（import されていない場合）
# main()を実行
if __name__ == '__main__':
    main()
