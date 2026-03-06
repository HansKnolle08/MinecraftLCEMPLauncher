import logging
from pathlib import Path

# Base directory
BASE_DIR = Path.home() / ".local" / "share" / "lcemp_launcher"

# Launcher folders
INSTALL_DIR = BASE_DIR / "install"
INSTANCES_DIR = BASE_DIR / "instances"
PROTON_DIR = BASE_DIR / "proton"
CONFIG_DIR = BASE_DIR / "config"
LOG_DIR = BASE_DIR / "logs"

logger = logging.getLogger(__name__)

def ensure_directories():
    for path in [BASE_DIR, INSTALL_DIR, INSTANCES_DIR, PROTON_DIR, CONFIG_DIR, LOG_DIR]:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.debug("Created directory: %s", path)