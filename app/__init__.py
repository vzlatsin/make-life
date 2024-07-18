from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import subprocess
import sys
from config import Config, PostgresConfig, TestConfig  # Import configuration classes

db = SQLAlchemy()
migrate = Migrate()

def check_postgres():
    try:
        result = subprocess.run(["pg_ctl", "status"], capture_output=True, text=True)
        if "no server running" in result.stdout:
            print("PostgreSQL server is not running.")
            return False
        else:
            print("PostgreSQL server is running.")
            return True
    except Exception as e:
        print(f"Error checking PostgreSQL status: {e}")
        return False

def create_app(config_class='config.Config'):
    try:
        print(f"Passed config class: {config_class}")

        env_config_class = os.getenv('FLASK_CONFIG')
        print(f"Environment variable FLASK_CONFIG: {env_config_class}")

        # Prioritize command-line argument over the environment variable
        if config_class == 'config.Config' and env_config_class:
            config_class = env_config_class

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

        if config_class == 'config.PostgresConfig' or config_class == PostgresConfig:
            print("Using PostgreSQL configuration.")
            if not check_postgres():
                print("Exiting application due to PostgreSQL server not running.")
                sys.exit(1)
        else:
            print("Using SQLite configuration.")

        db.init_app(app)
        print("Database initialized.")

        with app.app_context():
            try:
                connection = db.engine.connect()
                connection.close()
                print("Database connection successful.")
            except Exception as e:
                print(f"Database connection failed: {e}")
                print("Exiting application due to database connection failure.")
                sys.exit(1)


        migrate.init_app(app, db)
        print("Migration initialized.")

        from .main import main as main_blueprint
        from .inbox import inbox as inbox_blueprint

        app.register_blueprint(main_blueprint)
        app.register_blueprint(inbox_blueprint, url_prefix='/inbox')
        print("Blueprints registered.")

        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule} -> {rule.endpoint}")

        return app

    except Exception as e:
        print(f"Error during app initialization: {e}")
        raise
