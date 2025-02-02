# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # 他のユーザー関連の URL（ログイン、サインアップなど）
]
