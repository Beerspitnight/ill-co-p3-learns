import os
import json
import csv
import io
from datetime import datetime, timezone # Import timezone
from pathlib import Path
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash, send_file, Response
from flask_cors import CORS
from dotenv import load_dotenv
# --- Your app module imports ---
from learning_app.scripts.constants import get_all_options
from learning_app.utils.data_loader import get_shuffled_dataset, get_image_by_filename # Ensure these exist
from learning_app.scripts.firebase_service import firebase_client
from learning_app.scripts.auth import login_user, create_user

load_dotenv(dotenv_path="secrets/.env")

# --- Load Admin UID ---
ADMIN_UID = os.getenv("ADMIN_UID")
if not ADMIN_UID:
    print("WARNING: ADMIN_UID environment variable not set or empty. Admin downloads will not work.")
# --- End Load Admin UID ---

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise ValueError("No SECRET_KEY set for Flask application")

options = get_all_options()
ELEMENT = options["ELEMENT"]
PRINCIPLE = options["PRINCIPLE"]

# --- Helper Functions ---
def is_logged_in():
    return "user" in session

def render_instructions_html():
    return """
    <div>
      <strong>How to Tag Images</strong>
      <ul>
        <li>Tag each image using the design principles and elements.</li>
        <li>Leave secondary tags blank if only one applies.</li>
        <li>Reject if low quality, duplicate, or too abstract.</li>
        <li>Offensive if inappropriate content (nudity, violence, hate).</li>
        <li>Your tags auto-save on change.</li>
        <li>Use the sidebar to download your tagged work.</li>
      </ul>
    </div>
    """

# --- Routes ---

@app.route("/")
def index():
    user_id = session.get("user", {}).get("uid") # Example fix
    total_tags = firebase_client.get_total_tagged_count()
    personal_tags = firebase_client.get_user_tagged_count(user_id) if user_id else 0
    return render_template("landing.html", total_tags=total_tags, personal_tags=personal_tags, username=session.get("user", {}).get("email"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        action = request.form.get("action") # 'login' or 'signup'

        user_data = None
        if action == "login":
            user_data = login_user(email, password)
        elif action == "signup":
            display_name = request.form.get("display_name") # Ensure your form has this
            user_data = create_user(email, password, display_name)

        if user_data and user_data.get("localId"): # Check for localId
            session["user"] = {
                "email": email,
                "uid": user_data.get("localId"),
                "display_name": user_data.get("displayName", email) # Store display name or email
            }
            # --- Initialize image queue on login ---
            dataset = get_shuffled_dataset() # Load and shuffle dataset
            session["image_queue"] = [img['image_filename'] for img in dataset] # Store only filenames
            session["image_index"] = 0 # Start at the beginning
            session.modified = True # Ensure session is saved
            # --- End queue initialization ---
            flash("Login successful!", "success")
            return redirect(url_for("tag_image")) # Correct endpoint name
        else:
            error_message = "Login/Signup failed."
            if user_data and user_data.get('error'):
                error_message += f" Reason: {user_data['error'].get('message', 'Unknown error')}"
            flash(error_message, "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("image_queue", None)
    session.pop("image_index", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/tag") # Keep route path as /tag for JS compatibility
def tag_image(): # Keep function name for url_for compatibility
    if not is_logged_in():
        flash("Please log in to start tagging.", "warning")
        return redirect(url_for('login'))

    # --- Initialize queue if missing (e.g., session expired/cleared) ---
    if "image_queue" not in session or "image_index" not in session:
        dataset = get_shuffled_dataset()
        session["image_queue"] = [img['image_filename'] for img in dataset]
        session["image_index"] = 0
        session.modified = True
    # --- End queue initialization ---

    image_queue = session.get("image_queue", [])
    current_index = session.get("image_index", 0)
    queue_len = len(image_queue)

    # --- Handle Navigation ---
    nav_direction = request.args.get("direction") # Changed from 'nav' to 'direction' to match JS
    if nav_direction == "next":
        current_index += 1
    elif nav_direction == "prev":
        current_index -= 1

    # --- Clamp Index and Update Session ---
    if queue_len > 0:
        current_index = max(0, min(current_index, queue_len - 1)) # Clamp index
    else:
        current_index = 0 # Handle empty queue
    session["image_index"] = current_index
    session.modified = True
    # --- End Navigation Handling ---

    # --- Get Image ---
    image = None
    if image_queue and 0 <= current_index < queue_len:
        image_filename = image_queue[current_index]
        image = get_image_by_filename(image_filename) # Load full image data
    # --- End Get Image ---

    if not image:
        flash("Could not load image or queue is empty.", "error")
        # Maybe redirect to index or a 'completed' page
        return redirect(url_for('index'))

    # --- Get User Info, Counts, Instructions ---
    user = session.get("user", {})
    username = user.get("email", "Guest")
    user_id = user.get("uid")
    personal_count = firebase_client.get_user_tagged_count(user_id) if user_id else 0
    global_total = firebase_client.get_total_tagged_count()
    instructions_html = render_instructions_html()

    # --- Get existing tags for this image (if any) ---
    # You might want to load existing tags to pre-fill the form
    # existing_tags = firebase_client.get_tag_for_image(user_id, image['image_filename']) # Example

    # --- Render Template ---
    return render_template(
        "tagging_ui.html",
        image=image,
        elements=ELEMENT,
        principles=PRINCIPLE,
        username=username,
        personal_count=personal_count,
        global_total=global_total,
        instructions_html=instructions_html,
        # existing_tags=existing_tags # Pass existing tags if loaded
        # Add flags for disabling prev/next buttons if needed
        can_go_prev=(current_index > 0),
        can_go_next=(current_index < queue_len - 1)
    )

@app.route("/api/save-tag", methods=["POST"])
def save_tag():
    if not is_logged_in():
        return jsonify({"error": "Not logged in"}), 401
    user_id = session['user']['uid']
    data = request.get_json()
    image_id = data.get("image_id")
    # Use timezone-aware datetime
    timestamp = datetime.now(timezone.utc).isoformat()
    tag_data = {
        "user_id": user_id, # Keep user_id inside tag_data as well, it's good practice
        "timestamp": timestamp,
        "primary_element": data.get("primary_element"),
        "secondary_element": data.get("secondary_element"),
        "primary_principle": data.get("primary_principle"),
        "secondary_principle": data.get("secondary_principle"),
        "notes": data.get("notes"),
        "image_quality": data.get("image_quality"),
        "issues": data.get("issues", []),
        "rejected": data.get("rejected", False),
        "offensive": data.get("offensive", False)
    }
    try:
        # --- Corrected Method Name and Argument Order ---
        # Call save_tag_to_firebase with (image_id, user_id, tag_data)
        firebase_client.save_tag_to_firebase(image_id, user_id, tag_data)
        # --- End Correction ---
        return jsonify({"message": "Tag saved successfully"}), 200
    except AttributeError as ae:
        app.logger.error(f"AttributeError saving tag for {image_id}: {ae}. Check method name in firebase_service.py.")
        return jsonify({"error": f"Server configuration error: {ae}"}), 500
    except Exception as e:
        app.logger.error(f"Error saving tag for {image_id} by user {user_id}: {e}") # Added user_id to log
        return jsonify({"error": str(e)}), 500


# --- Download Routes ---
@app.route("/download-flags")
def download_flagged_tags():
    user = session.get("user")
    if not user or user.get("uid") != ADMIN_UID:
        flash("Access denied.")
        return redirect(url_for("index"))

    data = firebase_client.get_offensive_and_rejected_tags()

    if not data:
        flash("No flagged tags found.")
        return redirect(url_for("index"))

    # Change StringIO to io.StringIO
    si = io.StringIO()
    # Assuming data is a list of dicts and fieldnames can be derived
    if data: # Check if data is not empty before accessing keys
        writer = csv.DictWriter(si, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    else: # Handle empty data case if needed, though checked above
        return Response("", mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=flagged_tags.csv"})


    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=flagged_tags.csv"}
    )

@app.route("/download-success")
def download_success():
    tags = firebase_client.get_successful_tags()  # Should return a list of dicts
    si = io.StringIO()
    cw = csv.DictWriter(si, fieldnames=tags[0].keys())
    cw.writeheader()
    cw.writerows(tags)
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="successful_tags.csv")

@app.route("/download-failed")
def download_failed():
    tags = firebase_client.get_failed_tags()  # Should return a list of dicts
    si = io.StringIO()
    cw = csv.DictWriter(si, fieldnames=tags[0].keys())
    cw.writeheader()
    cw.writerows(tags)
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="failed_tags.csv")

@app.route("/download-success-json")
def download_success_json():
    tags = firebase_client.get_successful_tags()
    return jsonify(tags)

@app.route('/docs')
def docs():
  # You might want to pass some context if needed
  return render_template('docs.html')

# --- Main Execution ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) # Use 0.0.0.0 for Docker
