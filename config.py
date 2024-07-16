import os  # Import the os module to interact with the operating system
basedir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the directory where this file is located

class Config:
    # Set the database URI for SQLAlchemy. This tells SQLAlchemy where the database is located.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Disable SQLAlchemy modification tracking, which is not needed and adds extra overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True  # Enable testing mode for the app
    # Use an in-memory SQLite database for testing, which is fast and doesn't require a file.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'