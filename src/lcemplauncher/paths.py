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


src/lcemplauncher/paths.py

This module defines the directory structure and paths used by the LCEMP Launcher. 
It sets up the base directory in the user's home folder and defines subdirectories for 
installations, instances, Proton versions, configuration, and users. 
"""

"""
IMPORTS
"""

# Standard library imports
from pathlib import Path
import shutil

# Base directory
BASE_DIR = Path.home() / ".local" / "share" / "lcemp_launcher" # ~/.local/share/lcemp_launcher/

# Internal Config directory
INTERNAL_CONFIG_DIR = Path(__file__).parent / "config"

# Launcher folders
INSTALL_DIR = BASE_DIR / "install" # Temporary directory for installations and downloads
INSTANCES_DIR = BASE_DIR / "instances" # Directory where all instances are stored, each instance gets its own subdirectory
PROTON_DIR = BASE_DIR / "proton" # Directory where all Proton versions are stored, each version gets its own subdirectory
CONFIG_DIR = BASE_DIR / "config" # Directory for configuration files, currently not in use
USER_DIR = BASE_DIR / "user" # Directory for user-specific data

# Ensure all necessary directories exist and create them if they don't
def ensure_directories():
    for path in [BASE_DIR, INSTALL_DIR, INSTANCES_DIR, PROTON_DIR, CONFIG_DIR, USER_DIR]:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
    
    # Initialize JSON config files if they don't exist
    if USER_DIR.exists() and not (USER_DIR / "users.json").exists():
        _initiate_json_configs()

# Initialize JSON config files if they don't exist
def _initiate_json_configs():
    users_config = INTERNAL_CONFIG_DIR / "users.json"
    users_target = USER_DIR / "users.json"

    if not users_target.exists():
        shutil.copy(users_config, users_target)