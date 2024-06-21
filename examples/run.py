import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.core.routing import Router
from example_app.views import ExampleController

def create_app():
    router = Router()
    controller = ExampleController()
    router.add_route('/', controller.index)
    return router

app = create_app()

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, app)
