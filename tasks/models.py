from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    
    STATUS_CHOICES = [
        ('未提出', '未提出'),
        ('提出済み', '提出済み'),
        ('添削中', '添削中'),
        ('再提出', '再提出'),
        ('完了', '完了'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未提出')
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    subject = models.CharField(max_length=100, blank=True)
    score = models.IntegerField(null=True, blank=True)
    teacher_comment = models.TextField(blank=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title

class Submission(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user} for {self.task}"

from django.contrib.auth.models import User
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="groups")  # 修正

    def __str__(self):
        return self.name

class Announcement(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="feedbacks")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 修正
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.teacher} on {self.task}"
