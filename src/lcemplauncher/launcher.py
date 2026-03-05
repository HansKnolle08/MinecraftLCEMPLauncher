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

Launcher functions for the LCEMP Launcher application.
This module provides the main functions to launch the game using Proton, as well as 
helper functions for downloading and installing LCEMP and Proton.
"""

"""
IMPORTS
"""
import subprocess
import os
import logging

from .paths import INSTANCES_DIR, PROTON_DIR

# Configure logging
logger = logging.getLogger(__name__)


def launch_instance(instance_name: str, proton_version: str = "8-21") -> None:
    """
    Launches the LCEMP game for the specified instance using Proton.

    Args:
        instance_name (str): The name of the instance to launch.
        proton_version (str): The Proton version to use (default: "8-21").

    Raises:
        ValueError: If the game is not installed, Proton is not downloaded, or no executable is found.
        subprocess.CalledProcessError: If the launch command fails.
    """
    game_dir = INSTANCES_DIR / instance_name / "game"
    if not game_dir.exists():
        raise ValueError("Game not installed for this instance")

    proton_dir = PROTON_DIR / f"GE-Proton{proton_version}"
    if not proton_dir.exists():
        raise ValueError(f"Proton {proton_version} not downloaded")

    # Find the executable file
    exe_files = list(game_dir.glob("*.exe"))
    if not exe_files:
        raise ValueError("No executable found in game directory")

    exe_path = exe_files[0]  # Use the first .exe file found

    # Set up Wine prefix for this instance
    wineprefix_path = INSTANCES_DIR / instance_name / "wineprefix"
    wineprefix_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"Launching {exe_path} with Proton {proton_version} using prefix {wineprefix_path}")

    # Prepare the Proton command
    cmd = [str(proton_dir / "proton"), "run", str(exe_path)]

    # Set environment variables required by Proton
    env = os.environ.copy()
    env["STEAM_COMPAT_DATA_PATH"] = str(wineprefix_path)
    env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = str(proton_dir)

    # Change to the game directory before launching
    os.chdir(game_dir)

    # Launch the game
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        raise ValueError(f"Launch failed with return code {result.returncode}")
