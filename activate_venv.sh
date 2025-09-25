#!/bin/bash
echo "🐍 Activating Python Virtual Environment..."
source venv/bin/activate
echo "✅ Virtual environment activated!"
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo ""
echo "🚀 Starting Saarthi Backend Server..."
echo "Backend will be available at: http://127.0.0.1:8000"
echo "API Documentation: http://127.0.0.1:8000/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
