from flask import Blueprint

inbox = Blueprint('inbox', __name__, template_folder='templates', static_folder='static')

from . import routes
