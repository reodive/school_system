from django.db import models  # 🔥 必ず追加する
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('未提出', '未提出'),
        ('提出済み', '提出済み'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未提出')

    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title
