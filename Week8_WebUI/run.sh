#!/bin/bash

# Underwater Animal Detection Web UI - Quick Start Script

echo "🐠 Underwater Animal Detection Web UI"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if model exists
MODEL_PATH="../week6_ModelTraining/outputs/mobilenet_model.h5"
if [ ! -f "$MODEL_PATH" ]; then
    echo "⚠️  Warning: Trained model not found at $MODEL_PATH"
    echo "Please train the model first:"
    echo "  cd ../week6_ModelTraining"
    echo "  python train_mobilenet.py"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Model found: $MODEL_PATH"
fi

echo ""

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip install flask werkzeug
    echo ""
fi

# Check for OpenAI (optional)
if python3 -c "import openai" &> /dev/null; then
    echo "✅ OpenAI package found (optional)"
else
    echo "ℹ️  OpenAI package not found (optional - will use fallback descriptions)"
fi

echo ""
echo "🚀 Starting web server..."
echo "📍 Access the app at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "======================================"
echo ""

# Run the Flask app
python3 app.py

# Made with Bob
