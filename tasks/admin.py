from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_due_date', 'status', 'created_by')  # 🔥 修正
    list_filter = ('status',)  # 🔥 'due_date' を削除
    search_fields = ('title', 'description')

    def get_due_date(self, obj):
        return obj.due_date  # 🔥 due_date を取得するメソッドを追加
    get_due_date.short_description = 'Due Date'  # 管理画面のカラム名

admin.site.register(Task, TaskAdmin)
