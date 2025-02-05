import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .serializers import TaskSerializer, AnnouncementSerializer  # TaskSerializer was missing

# Importing models, forms, user management, and custom decorators
from .models import Task, Announcement
from users.models import CustomUser
from .forms import TaskForm, AnnouncementForm, TaskSubmissionForm
from users.decorators import role_required
from .models import Task, Submission

# Google API integration
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Django REST framework imports

from rest_framework import status
from .serializers import AnnouncementSerializer  # ← UserSerializer を削除
from users.serializers import UserSerializer  # ← users から正しくインポート
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .utils import add_calendar_event
import datetime

# Logger configuration
logger = logging.getLogger(__name__)

# Google Calendar API settings
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"

@login_required

def task_list(request):
    # 必要なコンテキストデータを用意
    tasks = [
        # ダミーデータまたは実際のデータを取得
        {'title': '数学の宿題', 'deadline': '2025-02-10'},
        {'title': '英語レポート', 'deadline': '2025-02-15'},
    ]
    context = {'tasks': tasks}
    return render(request, 'tasks/task_list.html', context)


def add_to_calendar(task):
    """
    Function to add a task to Google Calendar
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
    except FileNotFoundError:
        logger.critical("Google Calendar API credentials file (credentials.json) is missing. Task cannot be added.")
        return None
    except Exception as e:
        logger.error(f"Google Calendar integration error: {e}", exc_info=True)
        return None

@login_required
def announcement_list(request):
    """
    View to display a list of announcements
    """
    announcements = Announcement.objects.all()
    return render(request, 'tasks/announcement_list.html', {'announcements': announcements})

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def announcement_create(request):
    """
    View to create an announcement (for teachers and admins only)
    """
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'tasks/announcement_form.html', {'form': form})

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
# tasks/views.py

def create_task(request):
    if request.method == 'POST':
        # フォームからデータを取得する処理（ここでは簡易例）
        title = request.POST.get('title')
        deadline_str = request.POST.get('deadline')  # 例: '2025-02-10'
        description = request.POST.get('description', '')
        
        # データベースに課題を保存する処理（省略）
        # 例: task = Task.objects.create(...)

        # 締切日の文字列を datetime.date に変換
        deadline_date = datetime.datetime.strptime(deadline_str, '%Y-%m-%d').date()
        # 終了日は締切日の翌日（全日イベントとして登録）
        end_date = deadline_date + datetime.timedelta(days=1)
        
        # Google Calendar へのイベント登録を呼び出す
        event = add_calendar_event(
            title=title,
            start_date=deadline_date,
            end_date=end_date,
            description=description
        )
        
        # 登録完了後のリダイレクト
        return redirect('task_list')
    
    # GETリクエストの場合はフォームを表示する
    return render(request, 'tasks/create_task.html')

@login_required
def submit_task(request, task_id):
    """
    View to submit a task
    """
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.submitted_by = request.user
            submission.status = "Submitted"
            submission.save()
            return redirect('task_list')
    else:
        form = TaskSubmissionForm()
    return render(request, 'tasks/submit.html', {'form': form, 'task': task})

class TaskListAPI(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskDetailAPI(APIView):
    """
    API to retrieve, update, and delete a specific task
    """
def get(self, request, task_id, format=None):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(task)
    return Response(serializer.data)


    @role_required(allowed_roles=['teacher', 'admin'])
    def put(self, request, task_id, format=None):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        logger.warning(f"Task update error: {serializer.errors}")
        return Response({"error": "Validation failed.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @role_required(allowed_roles=['teacher', 'admin'])
    def delete(self, request, task_id, format=None):
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def home(request):
    return render(request, 'home.html')