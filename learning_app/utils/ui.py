
import re
import uuid

# Form Inputs
def sanitize_text(text: str) -> str:
    """Basic sanitization: trim whitespace."""
    return text.strip() if isinstance(text, str) else ""

def secure_input(label: str, type: str = "default", placeholder: str = "", key: str = None) -> str:
    """Streamlit wrapper for text or password input with built-in email and length validation."""
    # For password inputs, generate a new key to avoid caching the value
    widget_key = str(uuid.uuid4()) if type == "password" else key
    raw = st.text_input(label, type=type, placeholder=placeholder, key=widget_key)
    text = sanitize_text(raw)
    if "email" in label.lower():
        # Validate against basic email pattern
        if text and not re.match(r"[^@]+@[^@]+\.[^@]+", text):
            st.warning("Invalid email format.")
    if "password" in label.lower():
        if text and len(text) < 6:
            st.warning("Password must be at least 6 characters long.")
    return text

# Display Blocks
from learning_app.scripts.settings import get_icon_path

def labeled_icon(icon_filename: str, width: int = 20) -> None:
    """Streamlit helper to display an SVG icon and warn if the file is missing."""
    try:
        st.image(get_icon_path(icon_filename), width=width)
    except FileNotFoundError:
        st.warning(f"Missing icon '{icon_filename}'.")
