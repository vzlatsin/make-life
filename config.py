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
    if 'DATABASE_URL' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")
    else:
        try:
            from config_private import PostgresConfig as PrivateConfig
            SQLALCHEMY_DATABASE_URI = PrivateConfig.SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://")
        except ImportError:
            SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'

class TestConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
