# tasks/views.py

import logging
import datetime
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # 追加: メッセージフレームワーク
from django.db.models import Q  # 検索やフィルタに使用する場合

# Django REST framework
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

# Google API integration
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Logger configuration
logger = logging.getLogger(__name__)

# 自作のモジュールやモデル、フォームなど
from .serializers import TaskSerializer, AnnouncementSerializer
from .models import Task, Announcement, Submission
from .forms import TaskForm, AnnouncementForm, TaskSubmissionForm
from .utils import add_calendar_event
from users.models import CustomUser
from users.decorators import role_required
from users.serializers import UserSerializer  # REST API用

# Google Calendar API settings
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"


@login_required
def home(request):
    """
    ホームページ
    """
    return render(request, "home.html")


# tasks/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Task, Announcement, Group  # Group モデルを追加している場合
# 既存のインポート等はそのままでOK

@login_required
def task_list(request):
    """
    課題一覧画面
    ・検索、並べ替え、グループフィルタ、ページネーション機能付き
    """
    # GETパラメータを取得
    sort_by = request.GET.get('sort', 'deadline')  # 'deadline'（締切日）をデフォルトでソート
    group_filter = request.GET.get('group', None)    # 特定グループでの絞り込み（例: group=1）
    query = request.GET.get('q', '')                 # キーワード検索

    # 全課題を取得
    tasks = Task.objects.all()

    # 検索フィルター
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # グループ絞り込み（Task モデルに group フィールドがあることを前提）
    if group_filter:
        tasks = tasks.filter(group__id=group_filter)

    # 並べ替え（'deadline', 'title', 'priority' のいずれか）
    if sort_by in ['deadline', 'title', 'priority']:
        tasks = tasks.order_by(sort_by)
    else:
        tasks = tasks.order_by('deadline')

    # ページネーション（1ページあたり10件表示）
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # グループ一覧（フィルタ用プルダウンに利用）
    groups = Group.objects.all()

    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'groups': groups,
        'current_group': group_filter,
        'query': query,
    }
    return render(request, 'tasks/task_list.html', context)

def task_detail(request, task_id):
    """
    課題詳細ビュー
    """
    task = get_object_or_404(Task, id=task_id)
    return render(request, "tasks/task_detail.html", {"task": task})


@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def create_task(request):
    """
    課題作成ビュー
    """
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save()
            messages.success(request, "課題が作成されました。")

            # Google Calendar に登録したい場合
            add_calendar_event(
                title=new_task.title,
                start_date=new_task.deadline,
                end_date=new_task.deadline,
                description=new_task.description
            )

            return redirect("task_list")
        else:
            messages.error(request, "入力に誤りがあります。修正してください。")
    else:
        form = TaskForm()

    return render(request, "tasks/create_task.html", {"form": form})


@login_required
def submit_task(request, task_id):
    """
    課題提出ビュー
    """
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.user = request.user  # 提出者を自動で設定
            submission.save()

            # 例: ステータスを更新する場合
            task.status = '提出済み'
            task.save()

            messages.success(request, "課題を提出しました。")
            return redirect('task_list')
    else:
        form = TaskSubmissionForm()

    return render(request, 'tasks/submit.html', {'form': form, 'task': task})


@login_required
def announcement_list(request):
    """
    お知らせ一覧ビュー
    """
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'tasks/announcement_list.html', {'announcements': announcements})


@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def announcement_create(request):
    """
    お知らせ作成ビュー（教師、管理者のみ）
    """
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, "お知らせが投稿されました。")
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()

    return render(request, 'tasks/announcement_form.html', {'form': form})


def add_to_calendar(task):
    """
    旧 add_to_calendar 関数: 
    こちらでは Task オブジェクトを受け取る想定だが、
    上記 create_task では add_calendar_event() を使用しているので
    どちらかに統一するのが望ましい。
    """
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)

        start_time = task.deadline if task.deadline else datetime.datetime.utcnow()
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
        logger.critical("Google Calendar API credentials file (credentials.json) is missing.")
        return None
    except Exception as e:
        logger.error(f"Google Calendar integration error: {e}", exc_info=True)
        return None


# ==== REST API ====


class TaskListAPI(ListAPIView):
    """
    ログインユーザーに割り当てられた課題を一覧取得するAPI
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class TaskDetailAPI(APIView):
    """
    特定の課題を取得・更新・削除するAPI
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
            logger.info(f"Task updated: {serializer.data}")
            return Response(serializer.data)
        else:
            logger.warning(f"Task update error: {serializer.errors}")
            return Response({"error": "Validation failed.", "details": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    @role_required(allowed_roles=['teacher', 'admin'])
    def delete(self, request, task_id, format=None):
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        logger.info(f"Task deleted: {task_id}")
        return Response(status=status.HTTP_204_NO_CONTENT)
