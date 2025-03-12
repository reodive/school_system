from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    """
    学生グループやクラスを管理するモデル
    - name: グループ名
    - members: グループに所属するユーザー（通常は生徒）
    """
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="custom_user_groups",
        blank=True
    )

    def __str__(self):
        return self.name

class Task(models.Model):
    """
    課題モデル：
    - グループに紐づく場合、どのグループ向けの課題かを管理（group）
    - title, description, deadline, status, subject などを管理
    - created_by: 課題を作成した教師
    - assigned_to: 課題が割り当てられた生徒（任意）
    - priority: 課題の優先順位（1が最優先）
    """
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    
    STATUS_CHOICES = [
        ('未提出', '未提出'),
        ('提出済み', '提出済み'),
        ('添削中', '添削中'),
        ('再提出', '再提出'),
        ('完了', '完了'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未提出')
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    subject = models.CharField(max_length=100, blank=True)  # 教科情報
    score = models.IntegerField(null=True, blank=True)
    teacher_comment = models.TextField(blank=True)
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
        提出状況に応じた進捗率を計算するプロパティ
        ※ 状態に合わせたサンプルロジック。必要に応じて拡張してください。
        """
        if self.status == '提出済み' or self.status == '完了':
            return 100
        elif self.status == '添削中':
            return 75
        elif self.status == '再提出':
            return 50
        else:
            return 0

class Submission(models.Model):
    """
    提出モデル：
    - 生徒が課題に対して提出したファイル、コメント、デジタルノート形式の記録を管理
    """
    task = models.ForeignKey(
        Task,
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

class Announcement(models.Model):
    """
    お知らせモデル：
    - グループ向けのお知らせ、資料、定期考査範囲などの告知を管理
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
    フィードバックモデル：
    - 教師が課題に対してコメントや点数を付けるための記録
    """
    task = models.ForeignKey(
        Task,
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
