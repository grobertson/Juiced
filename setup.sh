#!/usr/bin/env bash
# Juiced Setup Script for Unix/Linux/macOS
# This script creates a virtual environment and installs all dependencies

set -e  # Exit on error

echo "========================================"
echo "Juiced Setup for Unix/Linux/macOS"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from your package manager"
    echo ""
    exit 1
fi

echo "Using Python: $(python3 --version)"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

echo "Step 2: Upgrading pip..."
venv/bin/python -m pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

echo "Step 3: Installing dependencies..."
venv/bin/pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

echo "Step 4: Setting up config file..."
if [ ! -f "configs/config.yaml" ]; then
    if [ -f "configs/config.yaml.example" ]; then
        cp "configs/config.yaml.example" "configs/config.yaml"
        echo "✓ Created configs/config.yaml from example"
        echo ""
        echo "IMPORTANT: Edit configs/config.yaml with your CyTube credentials"
    else
        echo "WARNING: configs/config.yaml.example not found"
    fi
else
    echo "✓ configs/config.yaml already exists"
fi
echo ""

echo "Step 5: Making launcher executable..."
chmod +x juiced.py
echo "✓ juiced.py is now executable"
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Edit configs/config.yaml with your CyTube server and credentials"
echo "  2. Run ./juiced.py to start the application"
echo ""
echo "For help, see README.md or BETA_TESTING.md"
echo ""
