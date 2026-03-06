#!/usr/bin/env bash

set -e

NAME="lcemp-launcher"

if [ -n "$1" ]; then
    NAME="$1"
fi

if [ ! -d "src" ]; then
    echo "❌ Run this script from the project root (where src/ exists)"
    exit 1
fi

echo "🔧 Building $NAME ..."

rm -rf build dist out
mkdir -p out

pyinstaller --onefile --windowed \
    --name "$NAME" \
    --hidden-import=tkinter \
    --hidden-import=_tkinter \
    --add-data "src/lcemplauncher/config/lcemp_versions.json:lcemplauncher/config" \
    src/main.py

mv "dist/$NAME" "out/$NAME"

rm -rf build dist "$NAME.spec"

echo "✅ Build finished"
echo "📦 Binary: out/$NAME"