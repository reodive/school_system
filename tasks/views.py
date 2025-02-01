from django.shortcuts import render, get_object_or_404
from .models import Task
from .forms import TaskSubmissionForm
from rest_framework import generics
from .serializers import TaskSerializer

# 🔥 追加: 課題一覧を表示するビュー
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})

# API ビュー
class TaskListAPI(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# 課題の提出ビュー
def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)  # IDで課題を取得
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = '提出済み'  # ステータスを更新
            task.save()
            return redirect('task_list')  # 提出後にリダイレクト
    else:
        form = TaskSubmissionForm(instance=task)

    return render(request, 'tasks/submit.html', {'form': form, 'task': task})
