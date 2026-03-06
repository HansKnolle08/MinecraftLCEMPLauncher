#!/usr/bin/env bash
set -e

# -------------------------------
# Ubuntu / Debian Launcher Runner
# -------------------------------

# Prüfen auf Python >= 3.11
PYTHON_CMD=$(command -v python3 || true)
if [[ -z "$PYTHON_CMD" ]] || [[ $($PYTHON_CMD -V | awk '{print $2}' | cut -d. -f1,2 | awk -F. '{print $1*10+$2}') -lt 31 ]]; then
    echo "Installing Python 3.11+ ..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-tk python3-requests
    PYTHON_CMD=python3
fi

sudo apt install -y python3-bs4 python3-tk python3-requests

echo "Running LCEMP Launcher..."
$PYTHON_CMD ../src/main.py