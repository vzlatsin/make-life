from flask import Blueprint

projects = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

print("Blueprint name:", projects.name)
print("Blueprint template folder:", projects.template_folder)
print("Blueprint static folder:", projects.static_folder)

from . import routes
