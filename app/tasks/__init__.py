from flask import Blueprint

tasks = Blueprint('tasks', __name__, template_folder='templates', static_folder='static')

print("Blueprint name:", tasks.name)
print("Blueprint template folder:", tasks.template_folder)
print("Blueprint static folder:", tasks.static_folder)


from . import routes
