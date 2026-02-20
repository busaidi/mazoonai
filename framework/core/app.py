import json

from werkzeug.wrappers import Request, Response

from framework.core.routing import Router
from framework.core.templating import TemplateEngine


class App:
    def __init__(self, template_folder="framework/templates"):
        self.router = Router()
        self.templates = TemplateEngine(template_folder=template_folder)
        self._middleware = []

    def route(self, path, methods=None):
        methods = methods or ["GET"]

        def decorator(func):
            self.router.add_route(path, func, methods=methods)
            return func

        return decorator

    def add_route(self, path, handler, methods=None):
        self.router.add_route(path, handler, methods=methods)

    def add_middleware(self, middleware):
        self._middleware.append(middleware)

    def render_template(self, template_name, context=None, status=200):
        context = context or {}
        content = self.templates.render(template_name, context)
        return Response(content, status=status, mimetype="text/html")

    def json(self, payload, status=200):
        return Response(
            json.dumps(payload), status=status, mimetype="application/json"
        )

    def _run_middleware(self, request):
        def endpoint(req):
            return self.router.dispatch(req)

        handler = endpoint
        for middleware in reversed(self._middleware):
            next_handler = handler
            handler = lambda req, mw=middleware, nxt=next_handler: mw(req, nxt)

        return handler(request)

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self._run_middleware(request)
        return response(environ, start_response)
