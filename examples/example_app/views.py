from framework.core.ai import QwenChatService
from framework.core.mvc import Controller


class ExampleController(Controller):
    def __init__(self, app, chat_service=None):
        self.app = app
        self.chat_service = chat_service or QwenChatService()

    def index(self, request):
        context = {"message": "MazoonAI Framework", "model": self.chat_service.model_name}
        return self.app.render_template("example.html", context)

    def health(self, request):
        return self.app.json({"status": "ok", "model": self.chat_service.model_name})

    def chat(self, request):
        payload = request.get_json(silent=True) or {}
        message = payload.get("message", "").strip()
        history = payload.get("history", [])

        if not message:
            return self.app.json({"error": "message is required"}, status=400)

        try:
            answer = self.chat_service.chat(message, history=history)
        except RuntimeError as exc:
            return self.app.json(
                {
                    "error": str(exc),
                    "hint": "Install dependencies and run once to download Qwen model.",
                },
                status=503,
            )

        return self.app.json({"reply": answer, "model": self.chat_service.model_name})
