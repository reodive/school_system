from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    STATUS_CHOICES = [
        ('未提出', '未提出'),
        ('提出済み', '提出済み'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未提出')

    # 🔥 追加: 課題の提出ファイルを管理するフィールド
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)

    # 🔥 追加: 課題を作成した教師
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
