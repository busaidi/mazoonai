from werkzeug.exceptions import HTTPException, MethodNotAllowed, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response


class Router:
    def __init__(self):
        self.url_map = Map()
        self.endpoints = {}

    def add_route(self, rule, endpoint, methods=None, endpoint_name=None):
        endpoint_name = endpoint_name or endpoint.__name__
        methods = methods or ["GET"]
        self.url_map.add(Rule(rule, endpoint=endpoint_name, methods=methods))
        self.endpoints[endpoint_name] = endpoint

    def dispatch(self, request):
        urls = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint_name, args = urls.match()
            return self.endpoints[endpoint_name](request, **args)
        except (NotFound, MethodNotAllowed) as exc:
            return Response(str(exc), status=exc.code, mimetype="text/plain")
        except HTTPException as exc:
            return Response(str(exc), status=exc.code, mimetype="text/plain")

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch(request)
        return response(environ, start_response)
