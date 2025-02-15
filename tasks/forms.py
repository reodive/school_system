# tasks/forms.py
from django import forms
from .models import Task, Announcement

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "deadline"]  # 👈 deadline を追加
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']

class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['submission_file', 'status']  # ステータスを追加
