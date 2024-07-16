from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

    print(f"Template directory: {template_dir}")  # Debug print statement
    print(f"Static directory: {static_dir}")  # Debug print statement

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object('config.Config')  # Assuming you have a Config class in config.py

    # Initialize database with the app
    db.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    from .inbox import inbox as inbox_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(inbox_blueprint, url_prefix='/inbox')

    # Print all registered routes for debugging
    if __name__ == "__main__":
        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule} -> {rule.endpoint}")

    return app
