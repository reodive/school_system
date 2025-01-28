from django.db import models
from users.models import CustomUser  # カスタムユーザーを利用する場合

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', '未提出'),
        ('submitted', '提出済み'),
    ]
    
    title = models.CharField(max_length=255)  # 課題のタイトル
    description = models.TextField()          # 課題の詳細
    due_date = models.DateField()             # 提出期限
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )  # 提出状況
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 作成者（教師）

    def __str__(self):
        return self.title

class Meta:
    ordering = ['due_date']
