from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
]

from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('tasks/', include('tasks.urls')),
]
