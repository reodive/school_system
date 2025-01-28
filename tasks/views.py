from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskSubmissionForm

def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = '提出済み'  # 提出後、ステータスを変更
            form.save()
            return redirect('task_list')  # 提出後に課題一覧ページへリダイレクト
    else:
        form = TaskSubmissionForm()
    return render(request, 'tasks/submit.html', {'form': form, 'task': task})
