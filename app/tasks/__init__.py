from flask import Blueprint

tasks = Blueprint('tasks', __name__, template_folder='templates', static_folder='static')


from . import routes
