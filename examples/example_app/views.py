from framework.core.mvc import View, Controller
from werkzeug.wrappers import Response

class ExampleController(Controller):
    def index(self, request):
        view = View()
        context = {'message': 'Hello, Mazoonai!'}
        response = Response(view.render('example.html', context), mimetype='text/html')
        return response
