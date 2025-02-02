# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # 課題一覧（ルート URL で表示）
    path('create/', views.create_task, name='create_task'),  # 課題作成
    path('<int:task_id>/submit/', views.submit_task, name='submit_task'),  # 課題提出
    path('api/', views.TaskListAPI.as_view(), name='task_list_api'),  # API用エンドポイント
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('<int:group_id>/tasks/', views.task_list, name='group_task_list'),  # グループごとの課題一覧
]
