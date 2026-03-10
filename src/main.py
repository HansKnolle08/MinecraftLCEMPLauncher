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

# Standard library imports
import logging
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
import json

# Local imports
from lcemplauncher.logging_config import setup_logging
from lcemplauncher.paths import *
from lcemplauncher.launcher import launch_instance

# UI imports
from lcemplauncher.ui.main.ui_form import Ui_LauncherMain
from lcemplauncher.ui.settings.ui_form import Ui_SettingsMain
from lcemplauncher.ui.dialog.ui_form import Ui_NewInstanceMain

# Setup logging
log_file = setup_logging()

"""
SETUP UI
"""
class LauncherMain(QMainWindow):
    """Main window for the LCEMP Launcher"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LauncherMain()
        self.ui.setupUi(self)

        self.connect_ui()
        self.load_instances()
        self.load_users()

    # Connect UI signals to logic
    def connect_ui(self):
        self.ui.SettingsButton.clicked.connect(self.open_settings_button)
        self.ui.LaunchButtonMain.clicked.connect(self.launch_instance_button)
        self.ui.LaunchButtonMain_2.clicked.connect(self.new_instance_button)

    # UI button handlers
    def new_instance_button(self):
        logger = logging.getLogger(__name__)
        logger.info("Creating new instance")
        
        self.new_instance_dialog = QMainWindow()
        self.new_instance_ui = Ui_NewInstanceMain()
        self.new_instance_ui.setupUi(self.new_instance_dialog)

        self.new_instance_dialog.show()

    def launch_instance_button(self):
        logger = logging.getLogger(__name__)
        logger.info("Launching instance")

        item = self.ui.InstanceList.currentItem()

        if item is None:
            logger.warning("No instance selected")
            return

        instance_name = item.text()

        # Currently hardcoded, will be selectable in the future
        proton_version = "10-25"

        logger.info(f"Launching instance: {instance_name} with Proton {proton_version}")

        launch_instance(instance_name, proton_version)

    def open_settings_button(self):
        logger = logging.getLogger(__name__)
        logger.info("Opening settings")

        self.settings_window = QMainWindow()
        self.settings_ui = Ui_SettingsMain()
        self.settings_ui.setupUi(self.settings_window)

        self.settings_window.show()

    # Load instances from the instances directory and show them in the UI list
    def load_instances(self):
        logger = logging.getLogger(__name__)
        logger.info("Loading instances")

        self.ui.InstanceList.clear()

        if not INSTANCES_DIR.exists():
            return

        for instance in sorted(INSTANCES_DIR.iterdir()):
            if instance.is_dir():
                self.ui.InstanceList.addItem(instance.name)

    def load_users(self):
        logger = logging.getLogger(__name__)
        logger.info("Loading users")

        self.ui.comboBox.clear()

        try:
            with open(USER_DIR / "users.json", "r") as f:
                data = json.load(f)

            users = data.get("Users", {})

            for user_id, user_data in users.items():
                username = user_data.get("Username", "Unknown")
                self.ui.comboBox.addItem(username)

        except Exception:
            logger.exception("Failed to load users")

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
        initiate_json_configs()
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
