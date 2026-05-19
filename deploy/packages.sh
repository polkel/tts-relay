#!/usr/bin/env bash

set -Eeuo pipefail

echo "Starting generate packages script..."

ROOT_DIR="$(cd "$(dirname ${BASH_SOURCE[0]})" && cd .. && pwd)"
TARGET_DIR="$ROOT_DIR/.venv"

if [[ -d "$TARGET_DIR" || -f "$TARGET_DIR" ]]; then
    echo "Deleting existing .venv"
    rm -rf "$TARGET_DIR"
fi

echo "Making new virtual environment"
python3 -m venv "$TARGET_DIR"
source "$TARGET_DIR/bin/activate"

echo "Installing packages..."
pip install -r "$ROOT_DIR/requirements.txt"
deactivate

echo "Finished generate packages script..."



