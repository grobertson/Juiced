#!/usr/bin/env python3
"""Juiced launcher script for Unix systems."""

import sys
import subprocess
from pathlib import Path

# Get script directory
script_dir = Path(__file__).parent
config_file = script_dir / 'configs' / 'config.yaml'

# Check if venv exists
venv_python = script_dir / 'venv' / 'bin' / 'python'

if venv_python.exists():
    print("Starting Juiced with virtual environment...")
    python_cmd = str(venv_python)
else:
    print("Starting Juiced with system Python...")
    print("")
    print("WARNING: No virtual environment found.")
    print("It's recommended to create one with:")
    print("  python3 -m venv venv")
    print("  venv/bin/pip install -r requirements.txt")
    print("")
    print("Attempting to run with system Python...")
    python_cmd = 'python3'

# Run Juiced
try:
    subprocess.run([python_cmd, '-m', 'juiced', str(config_file)])
except KeyboardInterrupt:
    print("\nShutting down...")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
