from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),  # ルート URL は tasks アプリの URL 定義を利用
    path('users/', include('users.urls')),  # ユーザー関連の URL
]
