# tasks/utils.py
import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

def add_calendar_event(title, start_date, end_date, description=""):
    """
    Google Calendar にイベントを追加する関数。
    - title: イベントのタイトル（例：課題名）
    - start_date, end_date: 日付（datetime.date または ISO フォーマット文字列）
    - description: イベントの詳細説明
    """
    # サービスアカウントを使った認証情報の取得
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    
    service = build('calendar', 'v3', credentials=credentials)
    
    # 開始・終了日時のフォーマット（ここでは日付のみなので、全日イベントとして登録）
    if isinstance(start_date, datetime.date):
        start_date = start_date.isoformat()
    if isinstance(end_date, datetime.date):
        end_date = end_date.isoformat()
    
    event = {
        'summary': title,
        'description': description,
        'start': {
            'date': start_date,  # 全日イベントの場合 'date' を使う
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'date': end_date,  # 終了日（通常は開始日の翌日）
            'timeZone': 'Asia/Tokyo',
        },
    }
    
    created_event = service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=event).execute()
    return created_event
