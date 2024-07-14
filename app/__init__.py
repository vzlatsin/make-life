from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.inbox import inbox as inbox_bp
    app.register_blueprint(inbox_bp)

    return app
