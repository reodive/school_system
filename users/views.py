# users/views.py
import datetime
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# REST Framework 関連
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# フォーム、シリアライザ、モデルのインポート
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .serializers import UserSerializer
from .models import CustomUser
from tasks.models import Task 
from tasks.models import Group
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .forms import NotificationSettingForm
from .models import NotificationSetting

@login_required
def notification_settings(request):
    """
    ユーザーごとの通知設定を表示・更新するビュー
    """
    # ユーザーに対して通知設定がなければ作成
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

class UserProfileAPI(APIView):
    """
    認証済みユーザーのプロフィール情報をJSON形式で返すAPI
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

def create_task(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        deadline_str = request.POST.get("deadline", None)  # ✅ デフォルト値を None に変更

        # ✅ バリデーション: 空ならエラーメッセージを表示
        if not title:
            messages.error(request, "タイトルを入力してください。")
            return redirect("create_task")
        
        if not deadline_str or deadline_str.strip() == "":
            messages.error(request, "締切日を入力してください。")
            return redirect("create_task")

        try:
            deadline_date = datetime.datetime.strptime(deadline_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "正しい日付形式（YYYY-MM-DD）で入力してください。")
            return redirect("create_task")

        # ✅ データベースに保存（例: Taskモデルを使用）
        Task.objects.create(title=title, description=description, deadline=deadline_date)
        messages.success(request, "課題が作成されました。")
        return redirect("task_list")

    return render(request, "tasks/create_task.html")

@login_required
def group_detail(request, group_id):
    """
    指定したグループの詳細情報、関連する課題やお知らせを表示するビュー
    ※グループは tasks.models.Group を想定
    """
    group = get_object_or_404(Group, pk=group_id)
    # グループに紐づく課題やお知らせを取得
    tasks = group.task_set.all()
    announcements = group.announcements.all().order_by('-created_at')
    return render(request, 'group_detail.html', {
        'group': group,
        'tasks': tasks,
        'announcements': announcements,
    })

def signup(request):
    """
    ユーザー登録フォームの表示と、登録処理を行うビュー
    登録後は自動でログインし、ダッシュボードへリダイレクトする
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  # 登録後のリダイレクト先（適宜変更）
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})


def user_logout(request):
    """
    ログアウト処理後、ホームページにリダイレクトするビュー
    """
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    user = request.user  # 現在のログインユーザー

    if user.role == "student":
        template_name = "users/student_dashboard.html"
        tasks = Task.objects.filter(assigned_to=user)  # 生徒に割り当てられた課題
    elif user.role == "teacher":
        template_name = "users/teacher_dashboard.html"
        tasks = Task.objects.all()  # 先生用にはすべての課題を表示
    else:
        return redirect("/")  # ロールが不明な場合はホームにリダイレクト

    # 課題の進捗を計算
    for task in tasks:
        task.progress = (task.submitted / (task.submitted + task.pending) * 100) if (task.submitted + task.pending) > 0 else 0

    return render(request, template_name, {"user": user, "tasks": tasks})




@login_required
def student_dashboard(request):
    """
    生徒用ダッシュボード
    サンプルデータを用いて課題の提出状況と進捗率を表示する。
    ※実際にはデータベースから動的に取得するよう修正すること
    """
    assignments = [
        {'title': '数学の宿題', 'submitted': False, 'progress': 50},
        {'title': '英語レポート', 'submitted': True, 'progress': 100},
    ]
    context = {
        'assignments': assignments,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    tasks = Task.objects.all()

    for task in tasks:
        task.total = task.submitted + task.pending  # 合計数を事前計算
        task.progress = (task.submitted / task.total * 100) if task.total > 0 else 0  # 進捗率を計算

    activities = [
        '生徒Aが「数学の宿題」を提出しました。',
        '生徒Bがコメントを追加しました。',
        '新しい課題「理科の実験レポート」が作成されました。',
    ]

    context = {
        'tasks': tasks,
        'activities': activities,
    }
    return render(request, 'users/teacher_dashboard.html', context)

@login_required
def profile_settings(request):
    """
    ユーザーのプロフィールを更新するビュー。
    POSTで送信された場合はフォームをバリデーションし、更新。
    GETの場合は現在のユーザー情報をフォームにセットして表示。
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