from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings  # 🔥 メディアファイル対応
from django.conf.urls.static import static  # 🔥 メディアファイル対応

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('tasks/', include('tasks.urls')),  # tasksアプリのURLをインクルード
    path('users/', include('users.urls')),  # 🔥 追加: ユーザー認証関連のURLを統合
]

# 🔥 メディアファイルの設定（開発環境用）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
