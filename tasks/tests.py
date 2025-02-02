# tasks/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class TaskTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher1', password='pass', role='teacher')
        self.task = Task.objects.create(title="テスト課題", description="テスト内容", created_by=self.teacher)

    def test_task_list_view(self):
        self.client.login(username='teacher1', password='pass')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "テスト課題")
