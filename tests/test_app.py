import unittest

from werkzeug.test import Client
from werkzeug.wrappers import Response

from framework import App
from examples.example_app.views import ExampleController


class StubChatService:
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"

    def chat(self, message, history=None):
        return f"echo:{message}"


class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = App(template_folder="examples/example_app/templates")
        self.controller = ExampleController(self.app, chat_service=StubChatService())

        self.app.add_route("/", self.controller.index, methods=["GET"])
        self.app.add_route("/api", self.controller.health, methods=["GET"])
        self.app.add_route("/chat", self.controller.chat, methods=["POST"])

        self.client = Client(self.app, Response)

    def test_html_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("MazoonAI Framework", response.get_data(as_text=True))

    def test_json_route(self):
        response = self.client.get("/api")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_chat_route(self):
        response = self.client.post("/chat", json={"message": "hello", "history": []})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["reply"], "echo:hello")

    def test_chat_route_requires_message(self):
        response = self.client.post("/chat", json={})
        self.assertEqual(response.status_code, 400)

    def test_not_found(self):
        response = self.client.get("/missing")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
