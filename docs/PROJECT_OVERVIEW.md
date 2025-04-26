Project Overview 

📁 Project Root
📦 ill-co-p3-learns/

ill-co-p3-learns/
├── README.md                  ← Main project description
├── requirements.txt           ← Python dependencies
├── .gitignore                 ← Ignore venvs, caches, secrets
├── pytest.ini                 ← Pytest marker configuration
├── landing_page.py            ← Streamlit landing page
├── login_page.py              ← Streamlit login/signup page
├── tagging_ui.py              ← Fully styled tagging interface
├── main_learns.py             ← [LEGACY] Original main app script
├── .streamlit/
│   └── secrets.toml           ← Firebase + app secrets for Streamlit Cloud
├── assets/
│   ├── logo_orange.png        ← Branding logo
│   ├── buk_sidebar.png        ← Sidebar image (Bukowski sketch)
│   └── *.svg                  ← Icons for nav buttons
├── docs/
│   ├── PROJECT_OVERVIEW.md    ← (You are here) Full file tree + annotations
│   └── TAGGING_INSTRUCTIONS.md ← Tagging definitions for contributors
├── learning_app/
│   ├── __init__.py
│   ├── data/                  ← Image input sources
│   ├── output/
│   │   ├── app_tagged_results/← Output from tagging sessions
│   │   └── pairs/             ← Output from pairing logic
│   ├── scripts/
│   │   ├── auth.py            ← Auth functions and login logic
│   │   ├── firebase_service.py← Firebase client ops (tag saving, loading)
│   │   ├── constants.py       ← App paths, get_icon_path(), etc.
│   │   ├── settings.py        ← Secure config handling (env + secrets)
│   │   └── main_learns.py     ← Legacy app logic
│   ├── styles/
│   │   └── styles.css         ← Legacy CSS file (optional now)
│   ├── templates/             ← (Future) For multipage or Jinja templates
│   └── utils/
│       ├── __init__.py
│       └── ui.py              ← Custom UI components for Streamlit
├── learning_app/test_scripts/
│   ├── test_auth_login.py     ← Tests failed logins (raises AuthError)
│   ├── test_firebase.py       ← Verifies Firebase init logic
│   ├── test_dataset_load.py   ← Validates dataset formats
│   ├── test_export_logic.py   ← Confirms JSON export loads properly
│   ├── test_tagging_flow.py   ← Tests Streamlit state interactions
│   ├── check_secrets.py       ← Utility to verify secret keys exist
│   └── README_TEST_SCRIPTS.md ← Test instructions for devs

Legend:
✅ = Streamlit-ready and styled
🔐 = Secure / secrets
🧪 = Covered by test
🕐 = Needs cleanup or final routing


Copy
Edit


File/Folder	Purpose
README.md	Top-level project info or instructions
requirements.txt	All Python dependencies for app + tests
landing_page.py	Streamlit landing UI (adapted from landing.html)
login_page.py	Streamlit login/signup interface (adapted from login.html)
tagging_ui.py	Fully-styled Streamlit tagging interface with sidebar
main_learns.py	[ARCHIVE/LEGACY] Initial main UI for tagging, now modularized
secrets/	Folder for TOML files (e.g. API keys) - DO NOT COMMIT
.gitignore	Ignores venv, __pycache__, etc.
.streamlit/secrets.toml	Secure secrets for Streamlit Cloud — NOT in Git
📁 assets/

File	Purpose
logo_orange.png	App branding for sidebar and landing
buk_sidebar.png	Sidebar image (Bukowski sketch)
*.svg icons	Navigation (next, back, save, download) — used in tagging UI
📁 docs/

File	Purpose
PROJECT_OVERVIEW.md	This file — annotated tree of current structure
TAGGING_INSTRUCTIONS.md	Tagger-facing instructions, roles, and definitions
📁 learning_app/
Top-level app logic, scripts, data, and outputs

📂 learning_app/data/
Source content: image inputs, references, design guides

📂 learning_app/output/
All tagging and enrichment outputs


Folder	Contents
app_tagged_results/	Exports made through Streamlit UI
pairs/	Output from image pair generation scripts
📂 learning_app/scripts/

Script	Purpose
auth.py	Auth logic — login, session storage, token validation
firebase_service.py	Firebase backend access methods (save, load, etc.)
constants.py	Global paths, icon loader
settings.py	Pulls secrets.toml + config handling
main_learns.py	[Legacy] Previously main UI script — now broken into pages
__init__.py	Allows import as a Python package
📂 learning_app/styles/
Currently contains: styles.css (for legacy non-Streamlit HTML rendering)

📂 learning_app/templates/
Reserved for future Jinja/HTML templates or multipage assets

📂 learning_app/utils/

File	Purpose
ui.py	Custom Streamlit UI components (secure_input, layout helpers)
__init__.py	Enables package import of utils
📂 learning_app/test_scripts/
Test suite for all major modules and flows


File	Purpose
pytest.ini	Configures test markers (integration, etc.)
test_auth_login.py	Tests authenticate_user() failure handling
test_firebase.py	Tests Firebase init/imports without real write
test_dataset_load.py	Loads and validates data format
test_export_logic.py	Verifies tagged export is readable
test_tagging_flow.py	Covers Streamlit session + UI logic
check_secrets.py	Dev tool to confirm secret keys exist
backup_illcop3.sh	Dev shell script for snapshot backups
README_TEST_SCRIPTS.md	Dev instructions on test layout
✅ Key Concepts
✅ Streamlit Modular Pages: landing_page.py, login_page.py, tagging_ui.py

✅ All styles injected inline in .py pages — no external CSS needed at runtime

✅ Firebase ready (auth + tagging) — logic lives in firebase_service.py and auth.py

✅ Secrets secure via secrets.toml

✅ Testing structured under learning_app/test_scripts