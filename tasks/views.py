# tasks/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import models  # ✅ `models` を追加
from .models import Task, Feedback  # ✅ `Task` や `Feedback` を正しくインポート


SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # Google API の認証情報

def add_to_calendar(task):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": task.title,
        "description": task.description,
        "start": {"date": str(task.due_date)},
        "end": {"date": str(task.due_date)},
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    return event

def task_list(request):
    tasks = Task.objects.all()  # すべての課題を取得
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def create_task(request):
    # ロールがteacher/adminのユーザーだけがアクセス可能
    ...


@login_required
def announcement_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    announcements = group.announcements.order_by('-created_at')
    return render(request, 'tasks/announcement_list.html', {
        'group': group,
        'announcements': announcements,
    })

@login_required
def announcement_create(request, group_id):
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
        form = AnnouncementForm()
    return render(request, 'tasks/announcement_form.html', {
        'group': group,
        'form': form,
    })

class Feedback(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="feedbacks")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
