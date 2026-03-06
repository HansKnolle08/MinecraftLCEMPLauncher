#!/usr/bin/env bash

set -e

# Default binary name
NAME="lcemp-launcher"

# Use argument if provided
if [ -n "$1" ]; then
    NAME="$1"
fi

# Check project root
if [ ! -d "src" ]; then
    echo "❌ Run this script from the project root (where src/ exists)"
    exit 1
fi

echo "🔧 Building $NAME ..."

# Clean old builds
rm -rf build dist out
mkdir -p out

# PyInstaller command (alles in einer Zeile oder korrekt mit \ ohne Leerzeichen dahinter)
pyinstaller --onefile --windowed \
    --name "$NAME" \
    --hidden-import=tkinter \
    --hidden-import=_tkinter \
    --add-data "src/lcemplauncher/config/lcemp_versions.json:lcemplauncher/config" \
    src/main.py

# Move binary to out/
mv "dist/$NAME" "out/$NAME"

# Cleanup
rm -rf build dist "$NAME.spec"

echo "✅ Build finished"
echo "📦 Binary: out/$NAME"