from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskSubmissionForm

# 課題一覧を表示
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})

# 課題提出機能
def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)  # 該当する課題を取得
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = '提出済み'  # ステータスを更新
            form.save()
            return redirect('task_list')  # 提出後に課題一覧ページへリダイレクト
    else:
        form = TaskSubmissionForm()

    return render(request, 'tasks/submit.html', {'form': form, 'task': task})
