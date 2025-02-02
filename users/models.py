from django.contrib.auth.models import AbstractUser
from django.db import models

# カスタムユーザーモデル（生徒・教師の役割を追加）
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', '生徒'),
        ('teacher', '教師'),
        ('admin', '管理者'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username
    
    groups = models.ManyToManyField('tasks.Group', blank=True, related_name='students')
    ...
