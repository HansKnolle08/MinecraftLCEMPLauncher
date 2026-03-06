#!/usr/bin/env bash
set -e

# -------------------------------
# Arch / Manjaro Launcher Runner
# -------------------------------

PYTHON_CMD=$(command -v python3 || true)
PYTHON_VER=0
if [[ -n "$PYTHON_CMD" ]]; then
    PYTHON_VER=$($PYTHON_CMD -V | awk '{print $2}' | cut -d. -f1,2 | awk -F. '{print $1*10+$2}')
fi

if [[ -z "$PYTHON_CMD" ]] || [[ $PYTHON_VER -lt 31 ]]; then
    echo "Installing Python 3.11+ ..."
    sudo pacman -Syu --noconfirm python
    PYTHON_CMD=python3
fi

sudo pacman -S --noconfirm tk python-beautifulsoup4 python-requests

echo "Launching LCMPE Launcher..."
$PYTHON_CMD ../src/main.py