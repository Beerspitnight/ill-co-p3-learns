"""
Constants for the image tagging application.
"""

import logging
from enum import Enum

# Removed streamlit import as it's only used in a function that might be removed or simplified

# Configure module-level logger
logger = logging.getLogger(__name__)

class Icons(str, Enum):
    BACK = "back.svg"
    NEXT = "next.svg"
    SAVE = "save.svg"
    DOWNLOAD = "download.svg"

# Define the primary constants directly
ELEMENT_OPTIONS = [
    "Line", "Shape", "Form", "Color", "Value", "Space", "Texture"
]
logger.info(f"Defined ELEMENT_OPTIONS: {ELEMENT_OPTIONS}")

PRINCIPLE_OPTIONS = [
    "Balance", "Emphasis", "Movement", "Pattern & Repetition",
    "Rhythm", "Proportion", "Variety", "Unity"
]
logger.info(f"Defined PRINCIPLE_OPTIONS: {PRINCIPLE_OPTIONS}")

# --- Removed Fallback Logic ---
# FALLBACK_ELEMENT_OPTIONS = [...] # Removed
# FALLBACK_PRINCIPLE_OPTIONS = [...] # Removed
# USING_FALLBACK_CONSTANTS = False # Removed
# IMPORT_ERROR_MESSAGE = None # Removed
# try...except ImportError block removed entirely

# Additional helper functions for constants
def get_all_options():
    """Return all element and principle options as a single list"""
    return {
        "ELEMENT": ["Line", "Shape", "Form", "Color", "Value", "Space", "Texture"],
        "PRINCIPLE": ["Balance", "Emphasis", "Movement", "Pattern", "Rhythm", "Proportion", "Unity"]
    }


# --- Simplified/Removed Fallback-related Functions ---
# def is_using_fallbacks(): # Removed - No longer relevant
#     """Check if fallback constants are being used"""
#     return False # Always false now

# def show_warnings_if_needed(): # Removed - No longer relevant
#     """Show warnings in the Streamlit UI if we're using fallbacks"""
#     # This function will no longer do anything as fallbacks are removed
#     pass