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


src/main.py

Main entry point for the LCEMP Launcher application.
This script initializes the application, sets up logging, and starts the GUI.
"""

"""
IMPORTS
"""
import logging

from lcemplauncher.gui import LauncherGUI
from lcemplauncher.logging_config import setup_logging
from lcemplauncher.paths import ensure_directories

log_file = setup_logging()

"""
MAIN FUNCTION
"""
def main() -> None:
    """Main function to start the LCEMP Launcher."""
    logger = logging.getLogger(__name__)
    logger.info("Starting LCEMP Launcher")
    logger.debug(f"Log file: {log_file}")

    try:
        ensure_directories()
        gui = LauncherGUI()
        gui.run()
    except Exception:
        logger.exception("Application error")
        raise

"""
ENTRY POINT
"""
if __name__ == "__main__":
    main()
