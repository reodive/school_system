from .models import Task

class TaskModelTest(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            due_date="2025-12-31",
            status="pending"
        )
        self.assertEqual(str(task), "Test Task")