import unittest

from werkzeug.test import Client
from werkzeug.wrappers import Response

from framework import App


class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = App(template_folder="examples/example_app/templates")

        @self.app.route("/", methods=["GET"])
        def index(request):
            return self.app.render_template("example.html", {"message": "Hi"})

        @self.app.route("/api", methods=["GET"])
        def api(request):
            return self.app.json({"ok": True})

        self.client = Client(self.app, Response)

    def test_html_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hi", response.get_data(as_text=True))

    def test_json_route(self):
        response = self.client.get("/api")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"ok": True})

    def test_not_found(self):
        response = self.client.get("/missing")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
