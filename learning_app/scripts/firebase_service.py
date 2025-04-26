import os
import json
import requests
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, initialize_app, db
#from dotenv import load_dotenv

#load_dotenv(dotenv_path="secrets/.env")
#FIREBASE_APP = None

def initialize_firebase():
    global FIREBASE_APP
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        db_url = os.getenv("FIREBASE_DB_URL")

        print("🔥 Initializing Firebase Admin SDK")
        cred = credentials.Certificate(cred_path)
        FIREBASE_APP = firebase_admin.initialize_app(cred, {
            "databaseURL": db_url
        })
    else:
        FIREBASE_APP = firebase_admin.get_app()

    return FIREBASE_APP

def sanitize_path(s):
    return s.replace(".", "_").replace("/", "_")

class FirebaseClient:
    def __init__(self):
        self.db_url = os.getenv("FIREBASE_DB_URL")
        initialize_firebase()  # ✅ Ensures Firebase SDK is ready

    def _execute(self, func, fallback=None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                print(f"[WARN] Attempt {attempt+1}/{max_attempts} failed in {func.__name__}: {e}")
        return fallback

    def save_tag_to_firebase(self, image_id, user_id, tag_data):
        safe_image_id = sanitize_path(image_id)
        safe_user_id = sanitize_path(user_id)
        full_path = f"tags/{safe_image_id}/{safe_user_id}"

        print("🧪 Saving to Firebase path:", full_path)
        print("🧪 Tag data:", tag_data)

        return self._execute(lambda: db.reference(full_path).set(tag_data) or True)

    def get_tags_for_image(self, image_id):
        safe_image_id = sanitize_path(image_id)
        return self._execute(lambda: db.reference(f"tags/{safe_image_id}").get(), fallback={})

    def get_total_tagged_count(self):
        all_tags = self._execute(lambda: db.reference("tags").get(), fallback={})
        return sum(len(t) for t in all_tags.values())

    def get_user_tagged_count(self, user_id):
        # This method seems incorrect based on your save path `tags/{image_id}/{user_id}`
        # It reads `tags/{user_id}` which likely doesn't exist or isn't structured as expected.
        # Let's redefine it to count correctly based on the assumed structure.
        if not user_id:
            return 0
        safe_user_id = sanitize_path(user_id)
        all_tags = self._execute(lambda: db.reference("tags").get(), fallback={})
        count = 0
        if all_tags:
            for image_id, tagset in all_tags.items():
                if isinstance(tagset, dict) and safe_user_id in tagset:
                    count += 1
        return count

    def get_tagged_image_filenames_for_user(self, user_id):
        """Retrieves a set of image filenames already tagged by the user."""
        if not user_id:
            return set()
        safe_user_id = sanitize_path(user_id)
        # Fetch all tags. This might be inefficient for very large datasets.
        # Consider restructuring data or using queries if performance becomes an issue.
        all_tags = self._execute(lambda: db.reference("tags").get(), fallback={})
        tagged_filenames = set()
        if all_tags:
            for image_id, tagset in all_tags.items():
                # Check if tagset is a dictionary (representing users who tagged this image)
                # and if the specific user is in that dictionary
                if isinstance(tagset, dict) and safe_user_id in tagset:
                    # Note: image_id here is the *sanitized* filename from the DB path
                    # If you need the original filename, you might need to store it
                    # within the tag data itself or reverse the sanitization if possible.
                    # Assuming image_id IS the filename needed for filtering:
                    tagged_filenames.add(image_id)
        print(f"Found {len(tagged_filenames)} tagged images for user {user_id}") # Added print for debugging
        return tagged_filenames

    def get_offensive_and_rejected_tags(self):
        all_tags = self._execute(lambda: db.reference("tags").get(), fallback={})
        flagged = []
        for img_id, tag_group in all_tags.items():
            for user_id, tag in tag_group.items():
                if tag.get("offensive") or tag.get("rejected"):
                    flagged.append({
                        "image_id": img_id,
                        "user_id": user_id,
                        **tag
                    })
        return flagged

    def get_successful_tags(self):
        all_tags = self.get_all_tags()
        successful = [
            tag for tag in all_tags
            if not tag.get("rejected", False) and not tag.get("offensive", False)
        ]
        return successful

    def get_failed_tags(self):
        all_tags = self.get_all_tags()
        failed = [
            tag for tag in all_tags
            if tag.get("rejected", False) or tag.get("offensive", False)
        ]
        return failed

    def get_all_tags(self):
        all_tags = self._execute(lambda: db.reference("tags").get(), fallback={})
        flat = []
        for image_id, tag_group in all_tags.items():
            for user_id, tag_data in tag_group.items():
                flat.append({
                    "image_id": image_id,
                    "user_id": user_id,
                    **tag_data
                })
        return flat


# Singleton instance
firebase_client = FirebaseClient()

# Backward-compatible alias
def save_tag_to_firebase(image_id, user_id, tag_data):
    return firebase_client.save_tag_to_firebase(image_id, user_id, tag_data)
