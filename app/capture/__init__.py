from flask import Blueprint

capture = Blueprint('capture', __name__, template_folder='templates', static_folder='static')

from . import routes
