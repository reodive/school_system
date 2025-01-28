from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # 課題一覧ページ
    path('<int:task_id>/submit/', views.submit_task, name='submit_task'),  # 課題の提出ページ
]
