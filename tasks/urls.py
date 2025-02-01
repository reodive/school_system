from django.urls import path
from . import views  # ✅ `views` モジュール全体をインポート

urlpatterns = [
    path('', views.task_list, name='task_list'),  # ✅ `views.task_list` で呼び出す
    path('<int:task_id>/submit/', views.submit_task, name='submit_task'),
    path('api/v1/tasks/', views.TaskListAPI.as_view(), name='task_list_api'),
]
