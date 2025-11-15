#!/usr/bin/env bash
# Juiced Setup Script for Unix/Linux/macOS
# This script creates a virtual environment and installs all dependencies

set -e  # Exit on error

echo "===================================================="
echo "Juiced Setup for Unix/Linux/macOS"
echo "===================================================="
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
echo " Virtual environment created"
echo ""

echo "Step 2: Upgrading pip..."
venv/bin/python -m pip install --upgrade pip
echo " pip upgraded"
echo ""

echo "Step 3: Installing dependencies..."
venv/bin/pip install -r requirements.txt
echo " Dependencies installed"
echo ""

echo "Step 4: Setting up config file..."
if [ ! -f "configs/config.yaml" ]; then
    if [ -f "configs/config.yaml.example" ]; then
        cp "configs/config.yaml.example" "configs/config.yaml"
        echo " Created configs/config.yaml from example"
        echo ""
        echo "===================================================="
        echo "Configuration Setup"
        echo "===================================================="
        echo ""
        echo "Please enter your CyTube connection details:"
        echo ""

        read -p "Channel name: " CYTUBE_CHANNEL
        read -p "Username (or press Enter for guest): " CYTUBE_USERNAME

        if [ -n "$CYTUBE_USERNAME" ]; then
            read -sp "Password: " CYTUBE_PASSWORD
            echo ""
        else
            CYTUBE_USERNAME="null"
            CYTUBE_PASSWORD="null"
        fi

        echo ""
        echo "Updating config file..."

        # Escape special characters for sed (/, &, \, newlines)
        escape_sed() {
            printf '%s\n' "$1" | sed -e 's/[\/&]/\\&/g'
        }

        ESCAPED_CHANNEL=$(escape_sed "$CYTUBE_CHANNEL")
        
        if [ "$CYTUBE_USERNAME" != "null" ]; then
            ESCAPED_USERNAME=$(escape_sed "$CYTUBE_USERNAME")
            ESCAPED_PASSWORD=$(escape_sed "$CYTUBE_PASSWORD")
            
            # Combine all sed operations into one atomic command
            sed -i.bak \
                -e "s/\"your-channel-name\"/\"$ESCAPED_CHANNEL\"/" \
                -e "s/\"your-username\"/\"$ESCAPED_USERNAME\"/" \
                -e "s/\"your-password\"/\"$ESCAPED_PASSWORD\"/" \
                "configs/config.yaml"
        else
            # Update channel and comment out user section for guest access
            # More robust than range-based sed which can fail with spacing changes
            sed -i.bak \
                -e "s/\"your-channel-name\"/\"$ESCAPED_CHANNEL\"/" \
                -e "s/^user:/# user:/" \
                -e "s/^  - \"your-username\"/  # - \"your-username\"/" \
                -e "s/^  - \"your-password\"/  # - \"your-password\"/" \
                "configs/config.yaml"
        fi

        # Remove backup file
        rm -f "configs/config.yaml.bak"

        echo " Config file updated with your credentials"
        echo ""
    else
        echo "WARNING: configs/config.yaml.example not found"
    fi
else
    echo " configs/config.yaml already exists (keeping existing config)"
fi
echo ""

echo "Step 5: Making launcher executable..."
chmod +x juiced.py
echo " juiced.py is now executable"
echo ""

echo "===================================================="
echo "Setup Complete!"
echo "===================================================="
echo ""
echo "Next steps:"
echo "  1. Edit configs/config.yaml with your CyTube server and credentials"
echo "  2. Run ./juiced.py to start the application"
echo ""
echo "For help, see README.md or BETA_TESTING.md"
echo ""
