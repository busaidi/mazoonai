import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mazoonai_project.settings')

import django
from django.test import Client, TestCase
from unittest.mock import patch


django.setup()


class AppTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MazoonAI Django App')

    def test_health_route(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['framework'], 'Django')

    @patch('chatapp.views.chat_service.chat', return_value='echo:hello')
    def test_chat_route(self, _mock_chat):
        response = self.client.post(
            '/chat',
            data=json.dumps({'message': 'hello', 'history': []}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['reply'], 'echo:hello')

    def test_chat_route_requires_message(self):
        response = self.client.post(
            '/chat', data=json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 405)
