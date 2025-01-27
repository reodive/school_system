from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', '生徒'),
        ('teacher', '教師'),
        ('admin', '管理者'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
