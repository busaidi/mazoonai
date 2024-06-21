from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

class Router:
    def __init__(self):
        self.url_map = Map()
        self.endpoints = {}

    def add_route(self, rule, endpoint):
        endpoint_name = endpoint.__name__
        self.url_map.add(Rule(rule, endpoint=endpoint_name))
        self.endpoints[endpoint_name] = endpoint

    def dispatch(self, request):
        urls = self.url_map.bind_to_environ(request.environ)
        endpoint_name, args = urls.match()
        return self.endpoints[endpoint_name](request, **args)

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch(request)
        return response(environ, start_response)
