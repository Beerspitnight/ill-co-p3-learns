# README: Test Scripts/Suite Instructions

This document explains how to run and maintain the automated test scripts for the Ill‑Co‑P3 rendering application.

---

## 📁 Directory Structure

```
ill-co-p3-render/         # Project root
├── app.py                # Main Flask application
├── tests/                # Automated test suite
│   ├── test_app.py       # Flask endpoint smoke tests
│   ├── test_constants.py # Constants & enum tests
│   ├── test_data_loader.py # Data loader utility tests
│   └── test_auth.py      # Firebase auth mock tests
├── requirements.txt      # Python dependencies (includes pytest)
├── Dockerfile            # Docker build instructions
└── docker-compose.yml    # Container orchestration
```

---

## 💻 Prerequisites

- **Python 3.13** (inside Docker or local venv)
- **pytest** installed (via `requirements.txt`)
- **Docker & Docker Compose** (for containerized testing)

---

## ▶️ Running Tests Locally

1. **Install dependencies** (if not already):
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure** your working directory is the project root:
   ```bash
   cd /path/to/ill-co-p3-render
   ```

3. **Run pytest**:
   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```

---

## ▶️ Running Tests Inside Docker

1. **Bring up the `web` service** (if not already running):
   ```bash
   docker compose up -d
   ```

2. **Install pytest** (only if not included in image):
   ```bash
   docker compose exec web pip install pytest
   ```

3. **Run the test suite**:
   ```bash
   docker compose exec web python -m pytest --maxfail=1 --disable-warnings -q
   ```

4. **Tear down** (optional):
   ```bash
   docker compose down
   ```

---

## 🛠️ Test Descriptions

- **test_app.py**: Verifies key Flask routes (`/`, `/login`, `/api/save-tag`) and response codes.
- **test_constants.py**: Checks that design constants and enums are defined correctly.
- **test_data_loader.py**: Confirms the dataset loader functions return and handle JSON data properly.
- **test_auth.py**: Mocks Firebase REST API calls to validate login success and error handling.

---

## 🔄 Updating or Adding Tests

1. **Create a new file** `tests/test_<feature>.py`.
2. **Write tests** using the `pytest` framework and fixtures from `conftest.py` (if you create one).
3. **Run** `pytest` to ensure all tests pass.
4. **Commit** your new tests to version control.

---

## 📖 Further Reading

- [pytest Documentation](https://docs.pytest.org)
- [Flask Testing Guide](https://flask.palletsprojects.com/en/latest/testing/)

---

*End of README for Test Scripts*

