from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'created_by')  # 🔥 `created_by` を表示
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'description')

admin.site.register(Task, TaskAdmin)