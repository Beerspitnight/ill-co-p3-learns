import os
import requests
import logging
from learning_app.scripts.settings import FIREBASE_API_KEY, FIREBASE_DB_URL
from learning_app.scripts.firebase_service import initialize_firebase

logger = logging.getLogger(__name__)

FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
FIREBASE_UPDATE_PROFILE_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={FIREBASE_API_KEY}"

def login_user(email, password):
    """Authenticate a user using Firebase Authentication REST API."""
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(FIREBASE_AUTH_URL, json=payload)
        response.raise_for_status()
        user_data = response.json()
        logger.info(f"✅ Login successful for {email}")
        return user_data
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Login failed: {e}")
        return None


def create_user(email, password, display_name):
    """Create a new user and set their display name in Firebase Authentication."""
    signup_payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        # First: Create the user
        signup_response = requests.post(FIREBASE_SIGNUP_URL, json=signup_payload)
        signup_response.raise_for_status()
        signup_data = signup_response.json()
        id_token = signup_data.get("idToken")

        # Second: Update display name
        update_payload = {
            "idToken": id_token,
            "displayName": display_name,
            "returnSecureToken": True
        }
        update_response = requests.post(FIREBASE_UPDATE_PROFILE_URL, json=update_payload)
        update_response.raise_for_status()

        logger.info(f"✅ User created and name set: {email}")
        return signup_data
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Account creation failed: {e}")
        return None
