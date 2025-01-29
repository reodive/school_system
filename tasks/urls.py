from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # 課題一覧が表示
    path('<int:task_id>/submit/', views.submit_task, name='submit_task'),
    path('api/', views.TaskListAPI.as_view(), name='task_list_api'),
]
