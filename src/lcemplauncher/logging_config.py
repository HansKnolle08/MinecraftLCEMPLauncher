from __future__ import annotations

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


src/lcemplauncher/logging_config.py

Logging configuration for the LCEMP Launcher application.
This module sets up logging for the console.
"""

"""
IMPORTS
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .paths import BASE_DIR

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "launcher.log"

def setup_logging(level: str | int | None = None) -> Path:
    """Configure logging for the application.

    This configures both a console handler and a rotating file handler.

    Args:
        level: Optional logging level (e.g. "DEBUG", "INFO", logging.DEBUG).
            If not provided, the environment variable LCEMP_LOG_LEVEL is used.

    Returns:
        Path: The path to the log file.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Determine log level
    if level is None:
        level_env = os.getenv("LCEMP_LOG_LEVEL", "INFO")
        if isinstance(level_env, str):
            level_env = level_env.strip().upper()
        try:
            level = getattr(logging, level_env)
        except Exception:
            level = logging.INFO

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove any handlers added by default
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    root_logger.debug("Logging configured. Log file: %s", LOG_FILE)
    return LOG_FILE
