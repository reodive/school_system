# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class LoginHistory(models.Model):
    """
    ユーザーのログイン履歴を記録するモデル
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='login_histories')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', '生徒'),
        ('teacher', '教師'),
        ('admin', '管理者'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username

class NotificationSetting(models.Model):
    """
    ユーザーごとの通知設定を管理するモデル
    """
    NOTIF_CHOICES = (
        ('on', 'ON'),
        ('off', 'OFF'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_setting')
    # 各通知項目: 課題リマインダー、チャット、アナウンス
    assignment_reminder = models.CharField(max_length=3, choices=NOTIF_CHOICES, default='on')
    chat_notification = models.CharField(max_length=3, choices=NOTIF_CHOICES, default='on')
    announcement_notification = models.CharField(max_length=3, choices=NOTIF_CHOICES, default='on')
    # 各通知の頻度（例：分、時間単位のオプションなど）
    reminder_frequency = models.IntegerField(default=24)  # 例: 24時間前通知

    def __str__(self):
        return f"{self.user.username} の通知設定"