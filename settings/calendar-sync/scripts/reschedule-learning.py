#!/usr/bin/env python3
"""
フルスタック学習プログラム - リスケジュールスクリプト

【このスクリプトの目的】
dev-schedule.csvのスケジュールを一括で後ろにずらし、
Googleカレンダーに反映します。

【使用例】
# 第5週以降を2週間後ろにずらす
python reschedule-learning.py --from-week 5 --shift-weeks 2

# 第10週以降を1ヶ月後ろにずらして、自動的にカレンダーに同期
python reschedule-learning.py --from-week 10 --shift-months 1 --sync

【処理の流れ】
1. コマンドライン引数を解析
2. dev-schedule.csvを読み込み
3. 指定された週以降のスケジュールをシフト
4. CSVファイルを更新
5. （--syncオプションがあれば）Googleカレンダーに同期
"""

# ============================================================
# ライブラリのインポート
# ============================================================

import csv
import argparse  # コマンドライン引数を解析
import sys
from datetime import datetime, timedelta  # 日付計算用
from pathlib import Path  # ファイルパス操作用

# 同期スクリプトから関数をインポート
# sync-to-calendar.pyで定義された関数を再利用する
try:
    from sync_to_calendar import (
        get_calendar_service,       # Google Calendar API認証
        get_or_create_calendar,     # カレンダー取得/作成
        sync_events_to_calendar,    # イベント同期
        load_schedule               # CSVファイル読み込み
    )
except ImportError:
    print("❌ sync-to-calendar.py が見つかりません")
    sys.exit(1)


# ============================================================
# 関数定義
# ============================================================

def shift_schedule(csv_path, from_week, shift_weeks=0, shift_months=0):
    """
    スケジュールをシフト（後ろにずらす）

    【処理フロー】
    1. CSVファイルを全行読み込み
    2. 各行の週番号をチェック
    3. from_week以降の行は日付を計算してシフト
    4. from_week未満の行はそのまま
    5. 全行をCSVファイルに書き戻す

    【アルゴリズム】
    - total_week = (年度 - 2025) * 52 + 月 * 4 + 週
      → 全体の通算週番号を概算で計算
    - total_week >= from_week なら対象

    【引数】
    csv_path: CSVファイルのパス
    from_week: この週以降をシフト対象とする（例: 5）
    shift_weeks: 何週間ずらすか（例: 2）
    shift_months: 何ヶ月ずらすか（例: 1）
    """
    # ステップ1: CSVファイルを読み込む
    rows = []  # 全行を格納するリスト

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # fieldnames = CSVのヘッダー行（列名）
        # 後で書き戻すときに必要
        fieldnames = reader.fieldnames

        for row in reader:
            # 各行のデータを取得
            year = int(row['年度'])
            month = int(row['月'])
            week = int(row['週'])

            # ステップ2: この行をシフトするか判定
            # 通算週番号を計算（年度と月を考慮）
            # 例: 2025年12月の第1週 → (2025-2025)*52 + 12*4 + 1 = 49
            # 例: 2026年1月の第1週 → (2026-2025)*52 + 1*4 + 1 = 57
            total_week = (year - 2025) * 52 + month * 4 + week
            from_total_week = from_week

            # from_week以降の行はシフト対象
            if total_week >= from_total_week:
                # ステップ3: 日付を計算
                # その年・月・週の開始日を計算
                # month=1, week=1 → 1月1日から0週後 = 1月1日
                current_date = datetime(year, month, 1) + timedelta(weeks=(week - 1))

                # ステップ4: シフト
                # shift_weeks週間 + shift_months*30日 後ろにずらす
                # 注: 1ヶ月=30日として概算
                new_date = current_date + timedelta(weeks=shift_weeks, days=shift_months * 30)

                # ステップ5: 新しい年度・月を設定
                row['年度'] = str(new_date.year)
                row['月'] = str(new_date.month)
                # 週番号はそのまま維持
                # （月内での相対的な週番号なので変更しない）

            # この行をリストに追加
            rows.append(row)

    # ステップ6: CSVファイルに書き戻す
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # ヘッダー行を書き込み
        writer.writerows(rows)  # 全データ行を書き込み

    print(f"✓ スケジュールを更新しました: {csv_path}")


def main():
    """
    メイン処理

    【処理フロー】
    1. コマンドライン引数を解析
    2. 引数の検証
    3. CSVファイルのパスを構築
    4. 確認メッセージを表示
    5. スケジュールをシフト
    6. （--syncオプションがあれば）Googleカレンダーに同期

    【コマンドライン引数】
    --from-week: 開始週番号（必須）
    --shift-weeks: シフトする週数（オプション、デフォルト: 0）
    --shift-months: シフトする月数（オプション、デフォルト: 0）
    --sync: 同期フラグ（オプション、指定すると自動同期）
    """
    # ステップ1: コマンドライン引数パーサーを作成
    parser = argparse.ArgumentParser(
        description='学習スケジュールをリスケジュール（後ろにずらす）します'
    )

    # 引数を定義
    parser.add_argument(
        '--from-week',
        type=int,  # 整数型
        required=True,  # 必須引数
        help='この週以降をリスケジュール対象とする（例: 5）'
    )
    parser.add_argument(
        '--shift-weeks',
        type=int,
        default=0,  # デフォルト値
        help='何週間後ろにずらすか（例: 2）'
    )
    parser.add_argument(
        '--shift-months',
        type=int,
        default=0,
        help='何ヶ月後ろにずらすか（例: 1）'
    )
    parser.add_argument(
        '--sync',
        action='store_true',  # フラグ（True/False）
        help='リスケジュール後、Googleカレンダーに自動同期する'
    )

    # 引数を解析
    # コマンドライン: python script.py --from-week 5 --shift-weeks 2
    # → args.from_week = 5, args.shift_weeks = 2
    args = parser.parse_args()

    # ステップ2: 引数の検証
    # shift_weeks と shift_months の両方が0の場合はエラー
    if args.shift_weeks == 0 and args.shift_months == 0:
        print("❌ --shift-weeks または --shift-months を指定してください")
        sys.exit(1)

    print("=" * 60)
    print("  学習スケジュール リスケジュール")
    print("=" * 60)

    # ステップ3: CSVファイルのパスを構築
    # __file__ = このスクリプトのパス
    # .parent.parent.parent = 3つ上のディレクトリ
    script_dir = Path(__file__).parent.parent.parent
    csv_path = script_dir / 'settings' / 'learning-program' / 'data' / 'dev-schedule.csv'

    # CSVファイルの存在確認
    if not csv_path.exists():
        print(f"❌ スケジュールファイルが見つかりません: {csv_path}")
        sys.exit(1)

    # ステップ4: 確認メッセージを表示
    print(f"\n📋 リスケジュール内容:")
    print(f"  - 対象: Week {args.from_week} 以降")
    if args.shift_weeks > 0:
        print(f"  - シフト: {args.shift_weeks} 週間後ろへ")
    if args.shift_months > 0:
        print(f"  - シフト: {args.shift_months} ヶ月後ろへ")

    print(f"\n⚠️  この操作により、{csv_path} が更新されます")

    # ユーザーに確認を求める
    confirm = input("続行しますか？ (yes/no): ")

    # 'yes' または 'y' 以外が入力されたらキャンセル
    if confirm.lower() not in ['yes', 'y']:
        print("❌ キャンセルしました")
        sys.exit(0)

    # ステップ5: スケジュールをシフト
    print("\n📊 スケジュールを更新中...")
    shift_schedule(csv_path, args.from_week, args.shift_weeks, args.shift_months)

    # ステップ6: Googleカレンダーに同期（--syncオプションがある場合）
    if args.sync:
        print("\n🔄 Googleカレンダーに同期中...")

        # Google Calendar API認証
        service = get_calendar_service()
        if not service:
            print("❌ Google認証に失敗しました")
            sys.exit(1)

        # カレンダー取得/作成
        calendar_id = get_or_create_calendar(service)

        # 更新後のスケジュールを読み込み
        schedule = load_schedule(csv_path)

        # イベント同期
        sync_events_to_calendar(service, calendar_id, schedule)
    else:
        # --syncオプションがない場合は手動同期の案内
        print("\n💡 Googleカレンダーに同期する場合は、以下を実行してください:")
        print("   python settings/calendar-sync/scripts/sync-to-calendar.py")

    print("\n" + "=" * 60)
    print("✅ リスケジュールが完了しました！")
    print("=" * 60)


# ============================================================
# スクリプトのエントリーポイント
# ============================================================

# このスクリプトが直接実行された場合
# （import されていない場合）main()を実行
if __name__ == '__main__':
    main()
