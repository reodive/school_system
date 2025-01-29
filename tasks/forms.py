from django import forms
from .models import Task

class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['submission_file']  # 🔥 `models.FileField` ではなく `forms.FileField` を使用！
