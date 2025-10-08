#!/usr/bin/env bash
#
# Quick start script for Tech Trends Harvester
# Handles setup and launch
#

set -e

echo "Tech Trends Harvester - Quick Start"
echo "========================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "[ERROR] uv is not installed"
    echo ""
    echo "Install it with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Or use pip:"
    echo "  python -m pip install uv"
    exit 1
fi

echo "[OK] uv is installed"

# Check if .venv exists, if not create it
if [ ! -d ".venv" ]; then
    echo "[SETUP] Setting up virtual environment..."
    uv venv
fi

echo "[OK] Virtual environment ready"

# Sync dependencies
echo "[SETUP] Installing dependencies..."
uv sync

echo "[OK] Dependencies installed"
echo ""
echo "[LAUNCH] Starting application..."
echo ""

# Run the app
uv run python run_app.py

