# calendarapp/models.py
from django.db import models
from django.conf import settings

class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
