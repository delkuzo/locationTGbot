#!/bin/bash

echo "Starting Location TG Bot..."
echo "Python version:"
python --version
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la
echo "Environment variables:"
echo "PORT=${PORT}"
echo "TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN:0:10}..."
echo "OPENAI_API_KEY=${OPENAI_API_KEY:0:10}..."

# Start the application
exec python -m uvicorn bot.main:app --host 0.0.0.0 --port ${PORT:-8000} 