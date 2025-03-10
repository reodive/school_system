from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class UserTests(TestCase):
    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'student',
            'password1': 'ComplexPassword123',
            'password2': 'ComplexPassword123'
        })
        self.assertEqual(response.status_code, 302)
