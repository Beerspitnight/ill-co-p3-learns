#!/usr/bin/env bash
set -e

echo "📦 Building & starting containers..."
docker-compose up --build -d

echo "🔍 Waiting a moment for the app to spin up..."
sleep 3

echo "✅ Running all pytest suites..."
pytest -q

echo "🛑 Tearing down containers..."
docker-compose down

echo "🎉 All tests passed!"

