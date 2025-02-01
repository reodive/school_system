from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
    path("users/", include("users.urls")),  # 🔥 追加
    path("", include("dashboard.urls")),  # 🔥 ダッシュボードを後で作成
]
