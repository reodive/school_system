# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from tasks.models import Group  # tasks/models.py の Group モデルをインポート

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', '生徒'),
        ('teacher', '教師'),
        ('admin', '管理者'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    # ユーザーが複数のグループに所属できる場合
    groups = models.ManyToManyField(Group, related_name='members', blank=True)

    def __str__(self):
        return self.username
