from django import forms
from .models import Task

class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['submission_file']
        submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
