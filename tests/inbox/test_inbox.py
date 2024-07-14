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

def test_inbox(client):
    rv = client.get('/inbox')
    assert b'Inbox' in rv.data
    rv = client.post('/inbox', data=dict(message='Test Message'), follow_redirects=True)
    assert b'Test Message' in rv.data
