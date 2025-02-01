from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'priority')
    list_filter = ('status', 'due_date', 'priority')

admin.site.register(Task, TaskAdmin)