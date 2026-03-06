#!/usr/bin/env bash
set -e

# -------------------------------
# Fedora Launcher Runner
# -------------------------------

PYTHON_CMD=$(command -v python3 || true)
PYTHON_VER=0
if [[ -n "$PYTHON_CMD" ]]; then
    PYTHON_VER=$($PYTHON_CMD -V | awk '{print $2}' | cut -d. -f1,2 | awk -F. '{print $1*10+$2}')
fi

if [[ -z "$PYTHON_CMD" ]] || [[ $PYTHON_VER -lt 31 ]]; then
    echo " Installing Python 3.11+ ..."
    sudo dnf check-update -y
    sudo dnf install -y python3 python3-pip python3-tkinter
    PYTHON_CMD=python3
fi

$PYTHON_CMD -m pip install --user --upgrade pip
$PYTHON_CMD -m pip install --user beautifulsoup4 requests

echo "Launching LCEMP Launcher..."
$PYTHON_CMD ../src/main.py