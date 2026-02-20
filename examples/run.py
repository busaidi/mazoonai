import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from framework import App
from example_app.views import ExampleController


def create_app():
    app = App(template_folder="examples/example_app/templates")
    controller = ExampleController(app)

    app.add_route("/", controller.index)
    app.add_route("/health", controller.health)
    return app


app = create_app()

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 4000, app)
