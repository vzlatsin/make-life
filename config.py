import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class PostgresConfig(Config):
    try:
        from config_private import PostgresConfig as PrivateConfig
        SQLALCHEMY_DATABASE_URI = PrivateConfig.SQLALCHEMY_DATABASE_URI
    except ImportError:
        SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
    
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
