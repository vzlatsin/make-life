from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

    print(f"Template directory: {template_dir}")  # Debug print statement
    print(f"Static directory: {static_dir}")  # Debug print statement

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # Ensure 'ENV' key is in app.config and provide default value
    env = app.config.get('ENV', 'default')
    print(f"Loaded configuration: {config_class}")
    print(f"Environment: {env}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    if config_class == 'config.PostgresConfig':
        print("Using PostgreSQL configuration.")
    else:
        print("Using SQLite configuration.")

    # Initialize database with the app
    db.init_app(app)
    print("Database initialized.")
    migrate.init_app(app, db)
    print("Migration initialized.")

    from .main import main as main_blueprint
    from .inbox import inbox as inbox_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(inbox_blueprint, url_prefix='/inbox')
    print("Blueprints registered.")

    # Print all registered routes for debugging
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")

    return app
