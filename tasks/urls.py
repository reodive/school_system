from django.urls import path, include
from . import views

urlpatterns = [
    # HTML 表示用ビュー
    path('', views.task_list, name='task_list'),  # すべての課題一覧
    path('create/', views.create_task, name='create_task'),  # 課題作成
    path('<int:task_id>/submit/', views.submit_task, name='submit_task'),  # 課題提出 (※実装が必要)
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('<int:group_id>/tasks/', views.task_list, name='group_task_list'),  # グループごとの課題一覧

    # API 用エンドポイント（DRF を利用）
    path('api/', views.TaskListAPI.as_view(), name='task_list_api'),
]
