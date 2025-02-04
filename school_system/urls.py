from django.contrib import admin
from django.urls import path, include
from tasks.views import home  # 例: tasks/views.py に home を定義している場合

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # ルートURLに home ビューを割り当て
    path('users/', include('users.urls')),  # ユーザー関連のURL
    path('tasks/', include('tasks.urls')),  # タスク関連のURLなど
    path('notifications/', include('notifications.urls')),
]