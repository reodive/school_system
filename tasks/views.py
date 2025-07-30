import logging
import datetime
from datetime import timedelta
from datetime import datetime
import calendar

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.views.decorators.http import require_POST

from .models import Task, Announcement, Submission, Group
from .forms import TaskForm, AnnouncementForm, TaskSubmissionForm
from .utils import add_calendar_event
from users.models import CustomUser
from users.decorators import role_required
from users.serializers import UserSerializer
from .serializers import TaskSerializer, AnnouncementSerializer

logger = logging.getLogger(__name__)

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    tasks = group.task_set.all()
    announcements = group.announcements.all().order_by('-created_at')
    return render(request, 'tasks/group_detail.html', {
        'group': group,
        'tasks': tasks,
        'announcements': announcements,
    })

def timer_view(request):
    return render(request, 'tasks/timer.html')

def group_selection(request):
    groups = Group.objects.all()
    return render(request, 'tasks/group_selection.html', {'groups': groups})

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"

def home(request):
    # ■ 日付・時刻情報
    now = datetime.now()
    today = now.date()

    # ■ カレンダー用：今月の日にちリスト
    last_day = calendar.monthrange(today.year, today.month)[1]
    days_in_month = list(range(1, last_day + 1))

    # ■ Next Class 用：次の授業開始時刻との差分（分単位）
    minutes_left = 5  # 実装に合わせて動的に取得してください

    # ■ 天気情報（仮置き。API連携があれば読み替え）
    weather = {
        'city': 'Tokyo',
        'temp': 24,
    }

    # ■ ToDo リスト：担当ユーザーで絞り込み、締切日でソート
    tasks = (
        Task.objects
            .filter(assigned_to=request.user)
            .order_by('deadline')   # ← ここを 'id' や 'priority' に変えてもOK
    )

    context = {
        'now': now,
        'today': today,
        'days_in_month': days_in_month,
        'minutes_left': minutes_left,
        'weather': weather,
        'tasks': tasks,
    }
    return render(request, 'home.html', context)

def progress_api(request):
    # 例: ユーザーの完了済みタスク数と総タスク数を取得
    completed = Task.objects.filter(user=request.user, done=True).count()
    total     = Task.objects.filter(user=request.user).count()
    return JsonResponse({'completed': completed, 'total': total})


@login_required
def task_list(request):
    sort_by = request.GET.get('sort', 'deadline')
    group_filter = request.GET.get('group', None)
    query = request.GET.get('q', '')

    tasks = Task.objects.all()
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if group_filter:
        tasks = tasks.filter(group__id=group_filter)
    if sort_by in ['deadline', 'title', 'priority']:
        tasks = tasks.order_by(sort_by)
    else:
        tasks = tasks.order_by('deadline')

    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    groups = Group.objects.all()

    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'groups': groups,
        'current_group': group_filter,
        'query': query,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, "tasks/task_detail.html", {"task": task})

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save()
            messages.success(request, "課題が作成されました。")
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
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.user = request.user
            submission.save()
            task.status = '提出済み'
            task.save()
            messages.success(request, "課題を提出しました。")
            return redirect('task_list')
    else:
        form = TaskSubmissionForm()
    return render(request, 'tasks/submit.html', {'form': form, 'task': task})

@login_required
def announcement_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    announcements = Announcement.objects.filter(group=group).order_by('-created_at')
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
            messages.success(request, f"{group.name} へのお知らせを投稿しました。")
            return redirect('announcement_list', group_id=group.id)
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = AnnouncementForm()
    return render(request, 'tasks/announcement_form.html', {
        'form': form,
        'group': group
    })

def add_to_calendar(task):
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

class TaskListAPI(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskDetailAPI(APIView):
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

@login_required
def group_stream(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    announcements = Announcement.objects.filter(group=group)
    tasks_in_group = group.tasks.all()
    submissions = Submission.objects.filter(task__in=tasks_in_group)
    stream_items = []
    for ann in announcements:
        stream_items.append({
            'type': 'announcement',
            'title': ann.title,
            'content': ann.content,
            'created_at': ann.created_at,
            'user': ann.created_by,
        })
    for sub in submissions:
        stream_items.append({
            'type': 'submission',
            'task_title': sub.task.title,
            'comment': getattr(sub, 'comment', ''),
            'file': sub.file.url if sub.file else None,
            'created_at': sub.created_at,
            'user': sub.user,
        })
    stream_items = sorted(stream_items, key=lambda x: x['created_at'], reverse=True)
    context = {
        'group': group,
        'stream_items': stream_items,
    }
    return render(request, 'tasks/group_stream.html', context)

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def group_roster(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    members = group.members.all()
    roster = []
    tasks = group.tasks.all()
    for member in members:
        submitted_count = sum(1 for task in tasks if task.submissions.filter(user=member).exists())
        total_count = tasks.count()
        roster.append({
            'member': member,
            'submitted_count': submitted_count,
            'total_count': total_count,
        })
    context = {
        'group': group,
        'roster': roster,
    }
    return render(request, 'tasks/group_roster.html', context)

@login_required
@role_required(allowed_roles=['teacher', 'admin'])
def tasks_dashboard(request):
    tasks = Task.objects.all().order_by('subject', 'deadline')
    tasks_by_subject = {}
    for task in tasks:
        subject = task.subject if task.subject else "未設定"
        tasks_by_subject.setdefault(subject, []).append(task)
    groups = Group.objects.all()
    groups_info = [{
        'group': group,
        'member_count': group.members.count(),
    } for group in groups]
    context = {
        'tasks_by_subject': tasks_by_subject,
        'groups_info': groups_info,
    }
    return render(request, 'tasks/teacher_dashboard.html', context)

@login_required
def tasks_by_subject(request):
    tasks = Task.objects.all().order_by('subject', 'deadline')
    tasks_by_subject = {}
    for task in tasks:
        subject = task.subject if task.subject else "未設定"
        tasks_by_subject.setdefault(subject, []).append(task)
    context = {
        'tasks_by_subject': tasks_by_subject,
    }
    return render(request, 'tasks/tasks_by_subject.html', context)

@require_POST
def toggle_task(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        raise Http404
    task.done = not task.done
    task.save()
    return JsonResponse({'pk': pk, 'done': task.done})