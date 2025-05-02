"""
users/views.py

ユーザー関連の各種ビューを実装。
- パスワード変更、通知設定、ログイン履歴表示
- ユーザー登録、ログアウト
- ダッシュボード（生徒/教師別）の表示
- ユーザープロフィール API
- モード切替（simple / normal）
"""

import datetime
from django.contrib.auth import login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    ProfileUpdateForm,
    NotificationSettingForm,
    CustomPasswordChangeForm,
)
from .serializers import UserSerializer
from .models import CustomUser, NotificationSetting
from tasks.models import Task, Group
from tasks.views import group_detail as tasks_group_detail

# モード切替ビュー
@login_required
def switch_mode(request, mode):
    if mode in ['simple', 'normal']:
        request.session['display_mode'] = mode
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# tasks/views.py の group_detail をそのまま利用
@login_required
def group_detail(request, group_id):
    return tasks_group_detail(request, group_id)

@login_required
def login_history(request):
    histories = request.user.login_histories.order_by('-login_time')
    return render(request, 'users/login_history.html', {'histories': histories})

@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "パスワードが変更されました。")
            return redirect('profile_settings')
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def notification_settings(request):
    notif_setting, _ = NotificationSetting.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = NotificationSettingForm(request.POST, instance=notif_setting)
        if form.is_valid():
            form.save()
            messages.success(request, "通知設定が更新されました。")
            return redirect("notification_settings")
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = NotificationSettingForm(instance=notif_setting)
    return render(request, "users/notification_settings.html", {"form": form})

class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "ユーザー登録が完了しました。")
            return redirect("dashboard")
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.info(request, "ログアウトしました。")
    return redirect("home")

@login_required
def dashboard(request):
    user = request.user
    if user.role == "student":
        template_name = "users/student_dashboard.html"
        tasks = Task.objects.filter(assigned_to=user)
    elif user.role == "teacher":
        template_name = "users/teacher_dashboard.html"
        tasks = Task.objects.all()
    else:
        messages.error(request, "ユーザー権限が不正です。")
        return redirect("home")
    for task in tasks:
        try:
            task.total = task.submitted + task.pending
            task.progress = (task.submitted / task.total * 100) if task.total > 0 else 0
        except Exception:
            task.progress = 0
    return render(request, template_name, {"user": user, "tasks": tasks})

@login_required
def student_dashboard(request):
    assignments = [
        {'title': '数学の宿題', 'submitted': False, 'progress': 50},
        {'title': '英語レポート', 'submitted': True, 'progress': 100},
    ]
    return render(request, 'student_dashboard.html', {'assignments': assignments})

@login_required
def teacher_dashboard(request):
    tasks = Task.objects.all()
    for task in tasks:
        try:
            task.total = task.submitted + task.pending
            task.progress = (task.submitted / task.total * 100) if task.total > 0 else 0
        except Exception:
            task.progress = 0
    activities = [
        '生徒Aが「数学の宿題」を提出しました。',
        '生徒Bがコメントを追加しました。',
        '新しい課題「理科の実験レポート」が作成されました。',
    ]
    return render(request, 'users/teacher_dashboard.html', {"tasks": tasks, "activities": activities})

@login_required
def profile_settings(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "プロフィールが更新されました。")
            return redirect("profile_settings")
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "users/profile_settings.html", {"form": form})
