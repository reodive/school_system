from django.db import models  # 🔥 必ず追加する
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=100)
    # 例: grade, subjectなども
    # teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teaching_groups', blank=True)
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
    ('未提出', '未提出'),
    ('提出済み', '提出済み'),
    ('添削中', '添削中'),
    ('再提出', '再提出'),
    ('完了', '完了'),
]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未提出')
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    subject = models.CharField(max_length=100, blank=True)
    score = models.IntegerField(null=True, blank=True)
    teacher_comment = models.TextField(blank=True)



    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title
    
class Announcement(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
