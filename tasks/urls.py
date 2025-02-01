from django.urls import path
from . import views
from .views import TaskListAPI

urlpatterns = [
    path('', views.task_list, name='task_list'),  # 課題一覧
    path('<int:task_id>/submit/', views.submit_task, name='submit_task'),  # 課題提出
    path('api/v1/tasks/', TaskListAPI.as_view(), name='task_list_api'),  # API のURLを整理
]
