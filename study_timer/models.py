from django.db import models
from django.conf import settings

class StudySession(models.Model):
    """
    勉強タイマー機能用のモデル
    ユーザーが勉強したセッションの開始時間、終了時間、計測時間を記録
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)  # end_time - start_time

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: {self.start_time} ~ {self.end_time}"
