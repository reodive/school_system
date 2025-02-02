# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    # ログイン、サインアップ、ログアウトの URL もここに定義するか、Django 標準の auth URL を利用
]
