from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from tasks.models import Group

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
    # ユーザーが所属するグループを両方（教師、学生）から取得
    my_groups = request.user.groups.all()
    return render(request, 'dashboard.html', {'groups': my_groups})
