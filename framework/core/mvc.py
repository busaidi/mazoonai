from jinja2 import Environment, FileSystemLoader
import os

class Model:
    pass

class View:
    def __init__(self, template_folder=None):
        if template_folder is None:
            # Default template folder path relative to the current file
            template_folder = os.path.join(os.path.dirname(__file__), '../../examples/example_app/templates')
        self.env = Environment(loader=FileSystemLoader(template_folder))

    def render(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)

class Controller:
    pass
