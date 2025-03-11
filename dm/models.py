# dm/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

# --- 既存のDMモデル（参考） ---
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.created_at}"

# --- グループチャット用モデル ---
class GroupChatRoom(models.Model):
    """
    グループチャットルームを管理するモデル
    - ルーム名は教師が作成するか、生徒グループ単位で自動生成するなど用途に合わせて設定可能
    - 複数のユーザーが参加できる
    """
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupChatMessage(models.Model):
    """
    グループチャットルーム内の各メッセージを管理するモデル
    """
    room = models.ForeignKey(
        GroupChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message by {self.sender} in {self.room} at {self.created_at}"