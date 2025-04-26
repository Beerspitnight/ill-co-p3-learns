# tests/test_auth.py
import pytest
import requests
from learning_app.scripts.auth import login_user, FIREBASE_SIGNUP_URL

class DummyResponse:
    def __init__(self, url):
        self.url = url
    def raise_for_status(self):
        pass
    def json(self):
        if self.url == FIREBASE_SIGNUP_URL:
            return {'idToken': 'token123', 'localId': 'uid123'}
        return {'displayName': 'Test User'}

def test_login_user_success(monkeypatch):
    def fake_post(url, json):
        return DummyResponse(url)
    monkeypatch.setattr(requests, 'post', fake_post)
    user_data = login_user('test@example.com', 'password')
    assert isinstance(user_data, dict)
    assert user_data.get('idToken') == 'token123'

def test_login_user_failure(monkeypatch):
    class ErrorResponse:
        def raise_for_status(self):
            raise requests.HTTPError('Unauthorized')
    def fake_post_error(url, json):
        return ErrorResponse()
    monkeypatch.setattr(requests, 'post', fake_post_error)
    with pytest.raises(requests.HTTPError):
        login_user('test@example.com', 'wrongpassword')
