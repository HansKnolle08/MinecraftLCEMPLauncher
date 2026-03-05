from pathlib import Path

# Base directory
BASE_DIR = Path.home() / ".lcemp_launcher"

# Launcher folders
INSTALL_DIR = BASE_DIR / "install"
INSTANCES_DIR = BASE_DIR / "instances"
PROTON_DIR = BASE_DIR / "proton"
CONFIG_DIR = BASE_DIR / "config"

def ensure_directories():
    for path in [BASE_DIR, INSTALL_DIR, INSTANCES_DIR, PROTON_DIR, CONFIG_DIR]:
        path.mkdir(parents=True, exist_ok=True)