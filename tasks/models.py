from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    """
    課題モデル：課題の基本情報や提出状況を管理
    """

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)  # ✅ 'due_date' ではなく 'deadline' を使用

    STATUS_CHOICES = [
        ('未提出', '未提出'),
        ('提出済み', '提出済み'),
        ('添削中', '添削中'),
        ('再提出', '再提出'),
        ('完了', '完了'),
    ]
    status = models.CharField(max_length=10, choices=[('未提出', '未提出'), ('提出済み', '提出済み'), ('添削中', '添削中'), ('再提出', '再提出'), ('完了', '完了')], default='未提出')
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')

    # 課題が割り当てられたユーザー（生徒）を管理したい場合
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    # 科目や得点、教師コメントなど
    subject = models.CharField(max_length=100, blank=True)
    score = models.IntegerField(null=True, blank=True)
    teacher_comment = models.TextField(blank=True)

    # 課題の優先順位を管理したい場合（1が最優先）
    priority = models.PositiveIntegerField(
        default=3,
        help_text="課題の優先順位。数値が小さいほど優先度が高い。"
    )

    class Meta:
        ordering = ['deadline']  # 締切日でソート

    def __str__(self):
        return self.title

    @property
    def progress(self):
        """
        提出状況に応じた進捗率のサンプル計算。
        実際には提出数や添削状況などに合わせてロジックを拡張できます。
        """
        if self.status == '提出済み':
            return 100
        elif self.status == '添削中':
            return 75
        elif self.status == '再提出':
            return 50
        elif self.status == '完了':
            return 100
        else:
            return 0


class Submission(models.Model):
    """
    提出モデル：生徒が提出したファイルやコメントを管理
    """
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    comment = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user} for {self.task}"


class Group(models.Model):
    """
    学生グループやクラスを管理するモデル
    """
    name = models.CharField(max_length=100)
    # 例: グループのメンバー
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="custom_user_groups",
        blank=True
    )

    def __str__(self):
        return self.name
    
class Announcement(models.Model):
    """
    グループ向けのお知らせやアナウンスを管理するモデル
    """
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='announcements'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.group.name})"


class Feedback(models.Model):
    """
    フィードバックモデル：教師が課題に対してコメントや点数を付ける場合に使用
    """
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.teacher} on {self.task}"
