import pytest
from dotenv import load_dotenv
import os
import sys
import subprocess
import time
import requests
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

# Load environment variables from .env file
load_dotenv()

# Set the PYTHONPATH dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.capture.models import CaptureEntry

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='session')
def db_connection(app):
    with app.app_context():
        try:
            connection = db.engine.connect()
            connection.close()
            print("Database connection successful.")
        except OperationalError as e:
            print(f"Database connection failed: {e}")
            pytest.exit("Database connection failed. Exiting pytest.", returncode=1)

@pytest.fixture(scope='function')
def clear_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app, db_connection):
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app, db_connection):
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def clear_messages(app):
    with app.app_context():
        db.session.query(CaptureEntry).delete()
        db.session.commit()
    yield
    with app.app_context():
        db.session.query(CaptureEntry).delete()
        db.session.commit()

@pytest.fixture(scope='module')
def start_flask_server():
    process = subprocess.Popen(['flask', 'run', '--no-debugger'])
    time.sleep(5)

    try:
        response = requests.get('http://localhost:5000')
        if response.status_code != 200:
            raise RuntimeError("Flask server not running as expected.")
    except Exception as e:
        process.terminate()
        print(f"Failed to start Flask server: {e}")
        sys.exit(1)
    yield
    process.terminate()
