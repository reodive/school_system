"""
users/views.py

ユーザーに関連する各種ビューを実装しています。
- パスワード変更、通知設定、ログイン履歴表示
- ユーザー登録、ログアウト
- ダッシュボードの表示（生徒/教師別）
- ユーザープロフィール API

※ 各ビューでは、Django の認証システム、メッセージフレームワーク、セッション更新を適用しています。
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

# フォーム、シリアライザ、モデルのインポート
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
from django.shortcuts import redirect

def switch_mode(request, mode):
    # mode: "simple" または "normal" が渡される
    if mode in ["simple", "normal"]:
        request.session['display_mode'] = mode
    return redirect(request.META.get('HTTP_REFERER', '/'))

# ------------------------------------------------------------------------------
# ユーザーのログイン履歴表示ビュー（LoginHistoryモデル実装済みの場合）
# ------------------------------------------------------------------------------
@login_required
def login_history(request):
    """
    現在のログインユーザーのログイン履歴を最新順に表示します。
    ※LoginHistoryモデルが定義され、Userに関連付けられている前提です。
    """
    histories = request.user.login_histories.order_by('-login_time')
    return render(request, 'users/login_history.html', {'histories': histories})


# ------------------------------------------------------------------------------
# 独自パスワード変更ビュー
# ------------------------------------------------------------------------------
@login_required
def change_password(request):
    """
    ユーザーがパスワードを変更するビューです。
    POST時にフォームのバリデーションを行い、変更後はセッション情報を更新します。
    """
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # ログアウトさせずにパスワード変更後も認証状態を維持
            messages.success(request, "パスワードが変更されました。")
            return redirect('profile_settings')
        else:
            messages.error(request, "エラーがあります。入力内容を確認してください。")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})


# ------------------------------------------------------------------------------
# 通知設定ビュー
# ------------------------------------------------------------------------------
@login_required
def notification_settings(request):
    """
    ユーザーごとの通知設定を表示・更新します。
    通知設定が存在しない場合は自動で作成します。
    """
    notif_setting, created = NotificationSetting.objects.get_or_create(user=request.user)
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


# ------------------------------------------------------------------------------
# ユーザープロフィール API
# ------------------------------------------------------------------------------
class UserProfileAPI(APIView):
    """
    認証済みユーザーのプロフィール情報を JSON 形式で返す API です。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ------------------------------------------------------------------------------
# ユーザー登録ビュー
# ------------------------------------------------------------------------------
def signup(request):
    """
    ユーザー登録フォームを表示し、登録処理を実行します。
    登録後、自動ログインしてダッシュボードにリダイレクトします。
    """
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


# ------------------------------------------------------------------------------
# ログアウトビュー
# ------------------------------------------------------------------------------
def user_logout(request):
    """
    ユーザーをログアウトし、ホームページにリダイレクトします。
    """
    logout(request)
    messages.info(request, "ログアウトしました。")
    return redirect("home")


# ------------------------------------------------------------------------------
# ダッシュボードビュー
# ------------------------------------------------------------------------------
@login_required
def dashboard(request):
    """
    ユーザーのロールに応じたダッシュボードを表示します。
    - 学生の場合: 自身に割り当てられた課題一覧
    - 教師の場合: 全課題の一覧
    """
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

    # 課題の進捗計算（submitted, pending が数値フィールドの場合）
    for task in tasks:
        try:
            task.total = task.submitted + task.pending
            task.progress = (task.submitted / task.total * 100) if task.total > 0 else 0
        except Exception:
            task.progress = 0

    context = {"user": user, "tasks": tasks}
    return render(request, template_name, context)


# ------------------------------------------------------------------------------
# 生徒用ダッシュボードビュー
# ------------------------------------------------------------------------------
@login_required
def student_dashboard(request):
    """
    生徒用ダッシュボードを表示します。
    ※ここではサンプルデータを利用していますが、実際にはデータベースから動的に取得するようにしてください。
    """
    assignments = [
        {'title': '数学の宿題', 'submitted': False, 'progress': 50},
        {'title': '英語レポート', 'submitted': True, 'progress': 100},
    ]
    context = {'assignments': assignments}
    return render(request, 'student_dashboard.html', context)


# ------------------------------------------------------------------------------
# 教師用ダッシュボードビュー
# ------------------------------------------------------------------------------
@login_required
def teacher_dashboard(request):
    """
    教師用ダッシュボードを表示します。
    全課題と最近の活動（例示的なデータ）を表示します。
    """
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
    context = {"tasks": tasks, "activities": activities}
    return render(request, 'users/teacher_dashboard.html', context)


# ------------------------------------------------------------------------------
# プロフィール設定ビュー
# ------------------------------------------------------------------------------
@login_required
def profile_settings(request):
    """
    ユーザーのプロフィール設定画面を表示し、更新を行います。
    """
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
