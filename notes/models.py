from django.db import models
from django.conf import settings

class Note(models.Model):
    """
    ノートモデル
    - 生徒や教師が作成するデジタルノート。リッチテキスト、画像、動画、図形、数式などを含めることができる。
    """
    title = models.CharField(max_length=255)
    content = models.TextField()  # CKEditor などでリッチテキスト編集用
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
