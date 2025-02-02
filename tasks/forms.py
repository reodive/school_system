# tasks/forms.py
from django import forms
from .models import Task, Announcement

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # 必要なフィールドだけを指定（例として以下を使用）
        fields = ['title', 'description', 'due_date', 'submission_file', 'subject']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        # お知らせ用のフィールド（例としてタイトルと内容）
        fields = ['title', 'content']
