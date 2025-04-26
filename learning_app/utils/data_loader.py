from pathlib import Path
import json
import random
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # 🔁 This goes from utils → scripts → root
DATA_PATH = BASE_DIR / "data" / "combined_pairs_sampled_for_gpt.json"

def load_dataset():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_shuffled_dataset():
    # Remove redundant imports inside function
    # Use DATA_PATH instead of hardcoded relative path
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        random.shuffle(data)
        # Optionally filter out invalid images here
        return data
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}")
        return [] # Return empty list on error
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {DATA_PATH}")
        return [] # Return empty list on error
    except Exception as e:
        print(f"An unexpected error occurred in get_shuffled_dataset: {e}")
        return [] # Return empty list on error


def get_image_by_filename(filename):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for img in data:
        if img["image_filename"] == filename:
            return img
    return None