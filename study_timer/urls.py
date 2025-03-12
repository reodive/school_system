from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_timer, name='start_timer'),
    path('stop/', views.stop_timer, name='stop_timer'),
]
