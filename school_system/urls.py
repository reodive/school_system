from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # ✅ テンプレートビューを追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('', TemplateView.as_view(template_name="index.html"), name="home"),  # ✅ 追加
]
