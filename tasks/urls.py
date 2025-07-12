from django.urls import path
from . import views
from .views import home, TaskDetailAPI, TaskListAPI, submit_task
from .views import progress_api
from django.contrib.auth.decorators import login_required
from .views import task_list

urlpatterns = [
    path("tasks/", login_required(task_list), name="task_list"),
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

    # グループ関連
    path("groups/<int:group_id>/tasks/", views.task_list, name="group_task_list"),
    path("group/<int:group_id>/announcements/", views.announcement_list, name="announcement_list"),
    path("group/<int:group_id>/announcements/create/", views.announcement_create, name="announcement_create"),
    path("group/<int:group_id>/stream/", views.group_stream, name="group_stream"),
    path("group/<int:group_id>/roster/", views.group_roster, name="group_roster"),
    path("group/selection/", views.group_selection, name="group_selection"),

    # REST API
    path("api/tasks/", TaskListAPI.as_view(), name="task_list_api"),
    path("api/tasks/<int:task_id>/", TaskDetailAPI.as_view(), name="task_detail_api"),

    # 教師用ダッシュボードと教科別課題
    path("teacher_dashboard/", views.tasks_dashboard, name="teacher_dashboard"),
    path("tasks_by_subject/", views.tasks_by_subject, name="tasks_by_subject"),
    path('timer/', views.timer_view, name='timer_view'),
    # urls.py
    path('api/progress/', progress_api, name='progress_api'),

]
