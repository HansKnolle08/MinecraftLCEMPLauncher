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
This script initializes the application, sets up logging, and handles the main window.
"""

"""
IMPORTS
"""
import logging
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from lcemplauncher.logging_config import setup_logging
from lcemplauncher.paths import ensure_directories

from lcemplauncher.ui.main.ui_form import Ui_LauncherMain
from lcemplauncher.ui.settings.ui_form import Ui_SettingsMain


log_file = setup_logging()

"""
SETUP UI
"""
class LauncherMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LauncherMain()
        self.ui.setupUi(self)

        self.connect_ui()

    def connect_ui(self):
        self.ui.SettingsButton.clicked.connect(self.open_settings)
        self.ui.LaunchButtonMain.clicked.connect(self.launch_instance)
        self.ui.LaunchButtonMain_2.clicked.connect(self.new_instance)

    def new_instance(self):
        logger = logging.getLogger(__name__)
        logger.info("Creating new instance")
        print("New instance button clicked")

    def launch_instance(self):
        logger = logging.getLogger(__name__)
        logger.info("Launching instance")
        print("Launch button clicked")

    def open_settings(self):
        logger = logging.getLogger(__name__)
        logger.info("Opening settings")

        self.settings_window = QMainWindow()
        self.settings_ui = Ui_SettingsMain()
        self.settings_ui.setupUi(self.settings_window)

        self.settings_window.show()

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
        app = QApplication(sys.argv)
        widget = LauncherMain()
        widget.show()
        sys.exit(app.exec())
    except Exception:
        logger.exception("Application error")
        raise

"""
ENTRY POINT
"""
if __name__ == "__main__":
    main()
