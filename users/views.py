from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from tasks.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

class UserProfileAPI(APIView):
    """
    API to retrieve user profile information
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    # グループに紐づく課題やお知らせなども取得できる
    tasks = group.task_set.all()
    announcements = group.announcements.all().order_by('-created_at')
    return render(request, 'group_detail.html', {
        'group': group,
        'tasks': tasks,
        'announcements': announcements,
    })


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  # ログイン後はダッシュボードへ
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    # ユーザーが参加しているカスタムグループを取得
    my_groups = request.user.groups.all()  # ← Django 標準の Group ではなく
    custom_groups = Group.objects.filter(members=request.user)  # ← `tasks.models.Group` を取得

    return render(request, 'dashboard.html', {'groups': custom_groups})
