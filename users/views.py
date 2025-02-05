# users/views.py
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# REST Framework 関連
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# フォーム、シリアライザ、モデルのインポート
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .serializers import UserSerializer
from .models import CustomUser  # 必要に応じて
from tasks.models import Task  # 課題モデル（必要なら追加）
# グループ情報を利用する場合は、グループモデルをインポート（例: tasks.models.Group）
from tasks.models import Group  # ※ Group モデルが tasks アプリにある場合

class UserProfileAPI(APIView):
    """
    認証済みユーザーのプロフィール情報をJSON形式で返すAPI
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


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

def dashboard(request):
    custom_groups = Group.objects.filter(members=request.user)  # 修正
    return render(request, "users/dashboard.html", {"custom_groups": custom_groups})

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
    """
    先生用ダッシュボード
    課題管理情報と最新の活動（ストリーム）を表示する。
    サンプルデータを使用しているが、実際はデータベースから取得すること
    """
    tasks = [
        {'title': '数学の宿題', 'deadline': '2025-02-10', 'pending': 5, 'submitted': 20},
        {'title': '英語レポート', 'deadline': '2025-02-15', 'pending': 3, 'submitted': 22},
    ]
    activities = [
        '生徒Aが「数学の宿題」を提出しました。',
        '生徒Bがコメントを追加しました。',
        '新しい課題「理科の実験レポート」が作成されました。',
    ]
    context = {
        'tasks': tasks,
        'activities': activities,
    }
    return render(request, 'teacher_dashboard.html', context)
