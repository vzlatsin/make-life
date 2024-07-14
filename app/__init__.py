from flask import Flask
import os

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    from .main import main as main_blueprint
    from .inbox import inbox as inbox_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(inbox_blueprint)

    return app
