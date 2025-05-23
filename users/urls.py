from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm
from notifications.views import get_notifications
from tasks.views import group_detail

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'), name='logout' ),
    path('signup/', views.signup, name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),

    # API Endpoints
    path('api/profile/', views.UserProfileAPI.as_view(), name='user_profile_api'),

    # Dashboard and Group Details
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),

    # Notifications
    path('notifications/', get_notifications, name='get_notifications'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('settings/notifications/', views.notification_settings, name='notification_settings'),    

    path('switch_mode/<str:mode>/', views.switch_mode, name='switch_mode'),
    path('group/<int:group_id>/', group_detail, name='group_detail'),
]
