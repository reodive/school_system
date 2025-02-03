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
        fields = ['submission_file', 'status']  # ステータスを追加
