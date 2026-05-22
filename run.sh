#!/bin/bash

echo "================================================"
echo "  Flask Portfolio Server - Linux/Mac Launcher"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3 first"
    exit 1
fi

echo "[INFO] Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
    echo "[SUCCESS] Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install/Update dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt
echo ""

# Start the Flask server
echo "================================================"
echo "  Starting Flask Server..."
echo "  Press Ctrl+C to stop the server"
echo "================================================"
echo ""
python app.py
