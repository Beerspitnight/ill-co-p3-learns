from pathlib import Path

# Define the export script contents
export_script_code = """
import firebase_admin
from firebase_admin import credentials, db
import json
import csv
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("secrets/ill-co-p3-learns-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ill-co-p3-learns-default-rtdb.firebaseio.com'
})

# Reference to tags node
ref = db.reference("tags")
tags_data = ref.get()

# Output containers
by_user = {}

# Process all tags grouped by user
for image_id, user_entries in tags_data.items():
    for user_id, tag_data in user_entries.items():
        if user_id not in by_user:
            by_user[user_id] = {
                "tags": []
            }
        # Add the image ID to the tag data
        tag_data["image_id"] = image_id
        by_user[user_id]["tags"].append(tag_data)

# Save JSON output
json_path = "learning_app/output/app_tagged_results/tagged_results_by_user.json"
Path(json_path).parent.mkdir(parents=True, exist_ok=True)
with open(json_path, "w") as jf:
    json.dump(by_user, jf, indent=2)

# Save CSV output (flat list, all users)
csv_path = "learning_app/output/app_tagged_results/tagged_results_by_user.csv"
flat_rows = []
for user_id, content in by_user.items():
    for tag in content["tags"]:
        flat_rows.append({
            "user_id": user_id,
            "image_id": tag.get("image_id", ""),
            "primary_element": tag.get("primary_element", ""),
            "secondary_element": tag.get("secondary_element", ""),
            "primary_principle": tag.get("primary_principle", ""),
            "secondary_principle": tag.get("secondary_principle", ""),
            "issues": ", ".join(tag.get("issues", [])),
            "quality_rating": tag.get("quality_rating", ""),
            "notes": tag.get("notes", ""),
            "is_rejected": tag.get("is_rejected", False),
            "is_offensive": tag.get("is_offensive", False)
        })

with open(csv_path, "w", newline="") as cf:
    writer = csv.DictWriter(cf, fieldnames=flat_rows[0].keys())
    writer.writeheader()
    writer.writerows(flat_rows)

print(f"✅ Export complete. Saved to:\\n{json_path}\\n{csv_path}")
"""

# Save the script
script_path = Path("learning_app/scripts/export_firebase_tags_by_user.py")
script_path.parent.mkdir(parents=True, exist_ok=True)
script_path.write_text(export_script_code)

# Confirm file path to user
script_path.name
