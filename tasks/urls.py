from django.urls import path
from . import views
from .views import home, TaskDetailAPI, TaskListAPI, submit_task

urlpatterns = [
    # ホームページ
    path("", home, name="home"),

    # 課題関連
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/submit/", submit_task, name="submit_task"),

    # お知らせ関連
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("announcements/create/", views.announcement_create, name="announcement_create"),

    # グループごとの課題一覧（例: 特定グループの課題一覧を表示）
    path("groups/<int:group_id>/tasks/", views.task_list, name="group_task_list"),
    path('group/<int:group_id>/announcements/', views.announcement_list, name='announcement_list'),
    path('group/<int:group_id>/announcements/create/', views.announcement_create, name='announcement_create'),
    path('group/<int:group_id>/stream/', views.group_stream, name='group_stream'),

    # REST API
    path("api/tasks/", TaskListAPI.as_view(), name="task_list_api"),
    path("api/tasks/<int:task_id>/", TaskDetailAPI.as_view(), name="task_detail_api"),
    path('group/<int:group_id>/roster/', views.group_roster, name='group_roster'),
    path('teacher_dashboard/', views.tasks_dashboard, name='teacher_dashboard'),
    path('tasks_by_subject/', views.tasks_by_subject, name='tasks_by_subject'),
    path('group/<int:group_id>/roster/', views.group_roster, name='group_roster'),
    path('group/<int:group_id>/stream/', views.group_stream, name='group_stream'),
    path('group/selection/', views.group_selection, name='group_selection'),

]
