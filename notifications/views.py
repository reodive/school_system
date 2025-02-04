# notifications/views.py

import datetime  # 日時操作用モジュール
from django.http import JsonResponse  # JSONレスポンスを返すためのモジュール
from django.contrib.auth.decorators import login_required  # ログイン状態を確認するデコレーター

@login_required  # ログイン済みのユーザーのみアクセス可能にする
def get_notifications(request):
    """
    最新の活動通知情報を取得してJSON形式で返すビューです。

    サンプル実装では、固定の通知データを返していますが、
    実際にはデータベースや他の情報ソースから最新の通知情報を取得する処理に置き換えてください。

    Returns:
        JsonResponse: 通知情報を含むJSONオブジェクトを返す。
        例:
        {
            "notifications": [
                {"message": "生徒Aが「数学の宿題」を提出しました。", "timestamp": "2025-02-10T10:00:00"},
                {"message": "生徒Bがコメントを追加しました。", "timestamp": "2025-02-10T09:55:00"},
                {"message": "新しい課題「理科の実験レポート」が作成されました。", "timestamp": "2025-02-10T09:50:00"}
            ]
        }
    """

    # サンプルの通知データを作成
    notifications = [
        {
            "message": "生徒Aが「数学の宿題」を提出しました。",
            # 現在時刻をISOフォーマットで設定
            "timestamp": datetime.datetime.now().isoformat()
        },
        {
            "message": "生徒Bがコメントを追加しました。",
            # 5分前の時刻をISOフォーマットで設定
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat()
        },
        {
            "message": "新しい課題「理科の実験レポート」が作成されました。",
            # 10分前の時刻をISOフォーマットで設定
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=10)).isoformat()
        }
    ]

    # 作成した通知データをJSON形式で返す
    return JsonResponse({"notifications": notifications})
