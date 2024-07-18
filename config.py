import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class SQLiteConfig(Config):
    """SQLite configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

class PostgresConfig(Config):
    """PostgreSQL configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
    # Attempt to override from config_private if available
    try:
        from config_private import PostgresConfig as PrivateConfig
        SQLALCHEMY_DATABASE_URI = PrivateConfig.SQLALCHEMY_DATABASE_URI
    except ImportError:
        pass

class TestConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
