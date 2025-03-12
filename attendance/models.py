from django.db import models
from django.conf import settings

class AbsenceNotice(models.Model):
    """
    欠席連絡モデル
    生徒が欠席連絡を送信できる
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='absence_notices')
    date = models.DateField()
    reason = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
