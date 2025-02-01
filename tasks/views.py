from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskSubmissionForm

def create_task(request):
    if request.method == "POST":
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("task_list")  # 課題一覧ページへリダイレクト
    else:
        form = TaskSubmissionForm()

    return render(request, "tasks/create_task.html", {"form": form})
