# === Stage 1: install & test ===
FROM python:3.9-slim AS test
WORKDIR /app

# 1. Copy only dependency list and install
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt pytest

# 2. Copy in your code and run tests
COPY . .
RUN pytest --disable-warnings --maxfail=1

# === Stage 2: final runtime ===
FROM python:3.9-slim AS runtime
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
