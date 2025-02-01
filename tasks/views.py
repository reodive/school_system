from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskSubmissionForm
from rest_framework import generics
from .serializers import TaskSerializer

# 🔥 課題一覧表示ビュー
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})

# 🔥 課題提出ビュー
def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = '提出済み'  # 🔥 課題の状態を更新
            task.save()
            return redirect('task_list')
    else:
        form = TaskSubmissionForm(instance=task)
    return render(request, 'tasks/submit.html', {'form': form, 'task': task})

# 🔥 課題一覧のAPIビュー
class TaskListAPI(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
