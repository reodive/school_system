# dm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_list, name='message_list'),  # /dm/
    path('<int:user_id>/', views.message_detail, name='message_detail'),  # /dm/2/]
    path('rooms/', views.group_chat_room_list, name='group_chat_room_list'),
    path('rooms/<int:room_id>/', views.group_chat_room_detail, name='group_chat_room_detail'),
]
