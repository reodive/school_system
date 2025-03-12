from django.urls import path
from . import views

urlpatterns = [
    path('ai_chat/', views.ai_chat_view, name='ai_chat'),
    path('ai_ask/', views.ai_ask, name='ai_ask'),
]
