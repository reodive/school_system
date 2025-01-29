from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskSubmissionForm

# 🔥 課題一覧API（修正ポイント）
class TaskListAPI(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# 課題一覧ビュー
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})

# 課題提出ビュー
def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = '提出済み'  # ステータスを「提出済み」に変更
            form.save()
            return redirect('task_list')
    else:
        form = TaskSubmissionForm()
    return render(request, 'tasks/submit.html', {'form': form, 'task': task})
