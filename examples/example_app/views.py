from framework.core.mvc import Controller


class ExampleController(Controller):
    def __init__(self, app):
        self.app = app

    def index(self, request):
        context = {"message": "Hello, Mazoonai!"}
        return self.app.render_template("example.html", context)

    def health(self, request):
        return self.app.json({"status": "ok"})
