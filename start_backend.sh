#!/bin/bash

# Backend Startup Script
echo "🚀 Starting Career Guidance Backend Server..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing Python dependencies..."
    pip install -r requirements-minimal.txt
fi

# Check if ML models exist
if [ ! -f "ml/models/classifier.joblib" ]; then
    echo "🤖 Training ML models (first time only)..."
    echo "   This may take 5-10 minutes..."
    python scripts/create_and_train_datasets.py
fi

# Start the server
echo ""
echo "✅ Starting Flask server on http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""
python run.py

