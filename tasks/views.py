import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# モデル、フォーム、ユーザー管理、カスタムデコレーターのインポート
from .models import Task, Announcement
from users.models import CustomUser
from .forms import TaskForm, AnnouncementForm, TaskSubmissionForm
from users.decorators import role_required

# Google API 関連のライブラリ
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Django REST framework 関連
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer, AnnouncementSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

# ログ設定
logger = logging.getLogger(__name__)

# Google Calendar API 設定
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"

def add_to_calendar(task):
    """
    課題を Google Calendar に登録する関数
    """
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)
        
        start_time = task.due_date if task.due_date else datetime.utcnow()
        end_time = start_time + timedelta(hours=1)
        
        event = {
            "summary": task.title,
            "description": task.description,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Tokyo"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Tokyo"},
        }
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        logger.info(f"Google Calendar event created: {created_event}")
        return created_event
    except Exception as e:
        logger.error(f"Google Calendar 連携エラー: {e}", exc_info=True)
        return None

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def create_task(request):
    """
    課題を作成するビュー（教師・管理者専用）
    """
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            created_event = add_to_calendar(task)
            if created_event is None:
                logger.warning("Google Calendar への登録に失敗しました。")
            return redirect('task_list')
        else:
            logger.warning(f"TaskForm エラー: {form.errors}")
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def submit_task(request, task_id):
    """
    課題を提出するビュー
    """
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.submitted_by = request.user
            submission.status = "提出済み"  # 提出状態を変更
            submission.save()
            return redirect('task_list')
    else:
        form = TaskSubmissionForm()
    return render(request, 'tasks/submit.html', {'form': form, 'task': task})

class TaskDetailAPI(APIView):
    """
    特定の課題を取得・更新・削除する API
    """
    def get(self, request, task_id, format=None):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @role_required(allowed_roles=['teacher', 'admin'])
    def put(self, request, task_id, format=None):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @role_required(allowed_roles=['teacher', 'admin'])
    def delete(self, request, task_id, format=None):
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)