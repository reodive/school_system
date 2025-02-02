"""
tasks/views.py

このファイルは、課題（Task）、お知らせ（Announcement）および Google Calendar 連携機能など、
tasks アプリの各種ビューを定義しています。
"""

import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Task, Group, Announcement
from users.models import CustomUser
from .forms import TaskForm, AnnouncementForm
from users.decorators import role_required
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ログ設定
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # 認証情報のパス

def add_to_calendar(task):
    """
    指定された課題 (task) を Google Calendar に登録する関数。
    成功すればイベント情報を返し、失敗すれば None を返す。
    """
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)
        event = {
            "summary": task.title,
            "description": task.description,
            "start": {"date": str(task.due_date)},
            "end": {"date": str(task.due_date)},
        }
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        logger.info("Google Calendar event created: %s", created_event.get("id"))
        return created_event
    except Exception as e:
        logger.error("Google Calendar 連携エラー: %s", e)
        return None

@login_required
def task_list(request):
    """
    すべての課題を一覧表示するビュー。
    """
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def create_task(request):
    """
    課題を作成するビュー。
    ログインユーザーが教師または管理者でなければアクセスできません。
    """
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            # Google Calendar への登録をオプションで実施
            if add_to_calendar(task) is None:
                logger.warning("Google Calendar への登録に失敗しました。")
            return redirect('task_list')
        else:
            logger.warning("TaskForm エラー: %s", form.errors)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def announcement_list(request, group_id):
    """
    指定されたグループ (group_id) に紐づくお知らせを一覧表示するビュー。
    """
    group = get_object_or_404(Group, pk=group_id)
    announcements = group.announcements.order_by('-created_at')
    return render(request, 'tasks/announcement_list.html', {
        'group': group,
        'announcements': announcements,
    })

@login_required
def announcement_create(request, group_id):
    """
    指定されたグループに新しいお知らせを投稿するビュー。
    """
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.group = group
            announcement.created_by = request.user
            announcement.save()
            return redirect('announcement_list', group_id=group.id)
        else:
            logger.warning("AnnouncementForm エラー: %s", form.errors)
    else:
        form = AnnouncementForm()
    return render(request, 'tasks/announcement_form.html', {
        'group': group,
        'form': form,
    })
