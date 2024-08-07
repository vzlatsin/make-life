import pytest
from dotenv import load_dotenv
import os
import sys
import subprocess
import time

# Load environment variables from .env file
load_dotenv()

# Set the PYTHONPATH dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.capture.models import CaptureEntry

@pytest.fixture(scope='module')
def app():
    # Set up the Flask application for testing
    app = create_app('testing')
    app.config['TESTING'] = True

    with app.app_context():
        # Create the database and tables
        db.create_all()
        yield app
        # Drop the database and tables
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='module')
def start_flask_server():
    # Start the Flask server
    process = subprocess.Popen(['flask', 'run'])
    time.sleep(5)  # Give the server time to start
    yield
    process.terminate()

@pytest.fixture
def clear_messages(app):
    with app.app_context():
        db.session.query(CaptureEntry).delete()
        db.session.commit()
    yield
    with app.app_context():
        db.session.query(CaptureEntry).delete()
        db.session.commit()
