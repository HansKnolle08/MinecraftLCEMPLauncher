"""
MIT License

Copyright (c) 2026 [HansKnolle08]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


src/lcemplauncher/launcher.py

Launcher functions for the LCEMP Launcher.
Handles starting LCEMP instances through Proton.
"""

"""
IMPORTS
"""

# Standard library imports
import subprocess
import os
from pathlib import Path

# Local imports
from .paths import INSTANCES_DIR, PROTON_DIR

# Finds the Minecraft.Cient.exe in the given game directory
def _find_executable(game_dir: Path) -> Path:
    # Searches specifically for Minecraft.Client.exe, to prevent executing malicious files that may be present in the game directory
    exe_files = list(game_dir.glob("Minecraft.Client.exe"))

    if not exe_files:
        raise ValueError("Minecraft.Client.exe not found in game directory")

    return exe_files[0]

# Prepares environment variables for Proton
def _prepare_environment(wineprefix_path: Path, proton_dir: Path) -> dict:
    env = os.environ.copy() # Copy of the current environment

    # Set Proton-specific environment variables
    env["STEAM_COMPAT_DATA_PATH"] = str(wineprefix_path)
    env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = str(proton_dir)

    return env

# Launches the specified instance with the given player name and Proton version
def launch_instance(instance_name: str, player_name: str, ip_address: str, proton_version: str = "8-21") -> subprocess.Popen:
    # Preparing directories and paths
    instance_dir = INSTANCES_DIR / instance_name
    game_dir = instance_dir / "game"

    if not game_dir.exists():
        raise ValueError(f"Game not installed for instance: {instance_name}")

    # Proton directory
    proton_dir = PROTON_DIR / f"GE-Proton{proton_version}"

    if not proton_dir.exists():
        raise ValueError(f"Proton {proton_version} not installed")

    # Find executable
    exe_path = _find_executable(game_dir)

    # Wine prefix
    wineprefix_path = instance_dir / "wineprefix"
    wineprefix_path.mkdir(parents=True, exist_ok=True)

    # Proton command
    cmd = [
        str(proton_dir / "proton"),
        "run",
        str(exe_path),
        "-name",
        player_name,
        "-ip",
        ip_address
    ]

    # Environment
    env = _prepare_environment(wineprefix_path, proton_dir)

    # Launch game
    process = subprocess.Popen(
        cmd,
        cwd=game_dir,
        env=env
    )

    return process