from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),  # ✅ これが正しく登録されているか確認
    path("users/", include("users.urls")),
]
