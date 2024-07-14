from flask import Blueprint

inbox = Blueprint('inbox', __name__, template_folder='templates')

from . import routes

