from django.urls import path 
from . import views
from .views import UserProfileAPI
from django.contrib.auth import views as auth_views

urlpatterns = [
    # API エンドポイント
    path('api/profile/', UserProfileAPI.as_view(), name='user_profile_api'),
    
    # ダッシュボードとグループ詳細
    path('dashboard/', views.dashboard, name='dashboard'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    
    # 認証関連のURL
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    
    # パスワードリセット関連
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    # ここに生徒ダッシュボードのURLパターンを追加
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]
