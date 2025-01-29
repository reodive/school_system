from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    
    STATUS_CHOICES = [
        ('未提出', '未提出'),
        ('提出済み', '提出済み'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未提出')

    # 課題提出用のファイルフィールド
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)

    def __str__(self):
        return self.title
