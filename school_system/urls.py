from django.contrib import admin
from django.urls import path, include
from tasks.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path('notifications/', include('notifications.urls')),
    path('dm/', include('dm.urls')),
    path('calendar/', include('calendarapp.urls')),
    path('', include('tasks.urls')),
]
