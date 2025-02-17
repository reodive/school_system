from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from .models import Task

@receiver(pre_save, sender=Task)
def send_task_reminder(sender, instance, **kwargs):
    """提出期限の3時間前に通知を送る"""
    if instance.due_date - timedelta(hours=3) <= now():
        recipients = [instance.created_by.email]  # 作成者（教師）
        recipients += [submission.submitted_by.email for submission in instance.submissions.all()]  # 提出者（生徒）

        send_mail(
            '【リマインド】課題の提出期限が近づいています',
            f'課題 "{instance.title}" の提出期限が {instance.due_date} に迫っています。',
            'noreply@school-system.com',
            recipients,
            fail_silently=True,
        )
