#settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Firebase Admin SDK
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# 🌐 Firebase Realtime Database
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

# 🔑 Firebase Auth & REST APIs
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# 📦 Firebase Storage (if needed)
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")

# 👤 Optional: Admin user ID
ADMIN_UID = os.getenv("ADMIN_UID")

# 🖼️ Icons & Assets directory
ASSETS_DIR = BASE_DIR / "static"

def get_icon_path(icon_name):
    """
    Returns full path to an icon in the static directory.
    Example: get_icon_path('logo_orange.png')
    """
    return ASSETS_DIR / icon_name
