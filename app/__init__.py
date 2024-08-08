from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from config import DevelopmentConfig, config  # Import the DevelopmentConfig and config dictionary

load_dotenv()  # Load environment variables from .env file

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=DevelopmentConfig):
    try:
        # Ensure config_class defaults to DevelopmentConfig if FLASK_ENV is not set
        env_config_name = os.getenv('FLASK_ENV', 'development')
        print(f"Environment variable FLASK_ENV: {env_config_name}")

        # Update config_class to use the correct configuration from the config dictionary
        config_class = config.get(env_config_name, config_class)
        print(f"Final config class being used: {config_class}")

        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

        print(f"Template directory: {template_dir}")
        print(f"Static directory: {static_dir}")

        app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        app.config.from_object(config_class)

        env = app.config.get('ENV', 'default')
        print(f"Loaded configuration: {config_class}")
        print(f"Environment: {env}")
        print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

        # Ensure SQLALCHEMY_DATABASE_URI is set
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            raise RuntimeError("Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set.")

        db.init_app(app)
        print("Database initialized.")

        migrate.init_app(app, db)
        print("Migration initialized.")

        from .main import main as main_blueprint
        from .capture import capture as capture_blueprint
        from .projects import projects as projects_blueprint
        from .tasks import tasks as tasks_blueprint
        print("Imported blueprints")

        app.register_blueprint(main_blueprint)
        app.register_blueprint(capture_blueprint, url_prefix='/capture')
        app.register_blueprint(projects_blueprint, url_prefix='/projects')
        app.register_blueprint(tasks_blueprint, url_prefix='/tasks')
        print("Registered blueprints")

        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule} -> {rule.endpoint}")

        return app

    except Exception as e:
        print(f"Error during app initialization: {e}")
        raise

if __name__ == "__main__":
    app = create_app()
