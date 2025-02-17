from django.urls import path
from . import views
from .views import home
from .views import TaskDetailAPI, TaskListAPI
from .views import submit_task

urlpatterns = [
    path("", home, name="home"),
    path("", views.task_list, name="task_list"),
    path("<int:task_id>/", views.task_detail, name="task_detail"),
    path('tasks/create/', views.create_task, name='create_task'),
    path('<int:task_id>/submit/', views.submit_task, name='submit_task'),  # 課題提出（実装済み）
    # お知らせ関連
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),  # お知らせ投稿
    
    # グループごとの課題一覧
    path('<int:group_id>/tasks/', views.task_list, name='group_task_list'),
    
    # REST API
    path('api/tasks/', TaskListAPI.as_view(), name='task_list_api'),
    path('api/tasks/<int:task_id>/', TaskDetailAPI.as_view(), name='task_detail_api'),
]