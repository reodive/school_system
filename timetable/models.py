from django.db import models
from django.conf import settings

class TimetableEntry(models.Model):
    """
    時間割エントリ：授業名、開始時刻、終了時刻、曜日、担当教師などを管理
    """
    DAY_CHOICES = [
        ('Mon', '月'),
        ('Tue', '火'),
        ('Wed', '水'),
        ('Thu', '木'),
        ('Fri', '金'),
        ('Sat', '土'),
        ('Sun', '日'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timetable_entries')
    class_name = models.CharField(max_length=255)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.class_name} ({self.day} {self.start_time}-{self.end_time})"
