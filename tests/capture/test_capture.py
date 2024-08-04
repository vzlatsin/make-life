import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_capture(client):
    # Follow the redirect for the GET request
    rv = client.get('/capture/', follow_redirects=True)
    assert rv.status_code == 200
    assert b'Capture' in rv.data  # Adjust this to match the expected content in the capture page

    # Test the POST request to /capture
    rv = client.post('/capture', data=dict(content='Test Message'), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Test Message' in rv.data


