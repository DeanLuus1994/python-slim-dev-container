#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Ensure Python is installed for config generation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Installing..."
    apt-get update && apt-get install -y python3 python3-pip
fi

# Install tomli for TOML parsing
pip3 install tomli

# Run config generation script
python3 $PROJECT_ROOT/scripts/generate_config.py

# Verify .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "ERROR: .env file was not generated."
    exit 1
fi

echo "Pre-build hook completed successfully."