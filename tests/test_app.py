# tests/test_app.py
import os
import pytest
from app import app as flask_app  # this loads your app.py

@pytest.fixture
def client():
    # Provide dummy env for Firebase init
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/ill-co-p3-learns-firebase-adminsdk.json'
    os.environ['FIREBASE_DB_URL'] = 'https://dummy.firebaseio.com'
    os.environ['FIREBASE_API_KEY'] = 'dummy_key'
    flask_app.config['TESTING'] = True
    return flask_app.test_client()

def test_homepage_loads(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Login' in resp.data

def test_login_page_loads(client):
    resp = client.get('/login')
    assert resp.status_code == 200
    assert b'email' in resp.data.lower()

def test_save_tag_requires_login(client):
    resp = client.post('/api/save-tag', json={})
    assert resp.status_code == 401
    assert b'Not logged in' in resp.data
