# framework/core/templating.py
from jinja2 import Environment, FileSystemLoader


class TemplateEngine:
    def __init__(self, template_folder='framework/templates'):
        self.env = Environment(loader=FileSystemLoader(template_folder))

    def render(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)
