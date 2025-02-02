# tasks/forms.py
from django import forms
from .models import Task, Announcement

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'submission_file', 'subject']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']

class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = Task
        # 提出ファイルのみ更新する例です。必要に応じて他のフィールドを追加してください。
        fields = ['submission_file']
