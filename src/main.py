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

Main entry point for the LCEMP Launcher.
This script initializes the application, sets up logging, and handles the main window.
"""

"""
IMPORTS
"""

# Standard library imports
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
import json
import threading

# Local imports
from lcemplauncher.paths import *
from lcemplauncher.launcher import launch_instance
from lcemplauncher.instances import load_instance_config

# UI imports
from lcemplauncher.ui.main.ui_form import Ui_LauncherMain
from lcemplauncher.ui.settings.ui_form import Ui_SettingsMain
from lcemplauncher.ui.dialog.ui_form import Ui_NewInstanceMain

"""
LAUNCHER MAIN WINDOW
"""
class LauncherMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LauncherMain()
        self.ui.setupUi(self)

        self.connect_ui()
        self._load_instances()
        self._load_users()

        self.ui.InstanceSettingsFrame.hide()

    # Connect UI signals to logic
    def connect_ui(self):
        self.ui.SettingsButton.clicked.connect(self._open_settings_button)
        self.ui.LaunchButton.clicked.connect(self._launch_instance_button)
        self.ui.NewInstanceButton.clicked.connect(self._new_instance_button)
        self.ui.InstanceList.currentItemChanged.connect(self._instance_selected)

    # UI button handlers
    def _new_instance_button(self):
        self.new_instance_dialog = QMainWindow()
        self.new_instance_ui = Ui_NewInstanceMain()
        self.new_instance_ui.setupUi(self.new_instance_dialog)

        self.new_instance_dialog.show()

    def _launch_instance_button(self):
        item = self.ui.InstanceList.currentItem()
        username = self.ui.UserSelectBox.currentText()
        ip_address = "192.168.1.99"

        if item is None:
            return

        instance_name = item.text()
        proton_version = self.ui.ProtonSelectBox.currentText().replace("GE-Proton", "")

        thread = threading.Thread(
            target=launch_instance,
            args=(instance_name, username, ip_address, proton_version),
            daemon=True
        )
        thread.start()

    def _open_settings_button(self):
        self.settings_window = QMainWindow()
        self.settings_ui = Ui_SettingsMain()
        self.settings_ui.setupUi(self.settings_window)

        self.settings_window.show()

    # Load instances from the instances directory and show them in the UI list
    def _load_instances(self):
        self.ui.InstanceList.clear()

        if not INSTANCES_DIR.exists():
            return

        for instance in sorted(INSTANCES_DIR.iterdir()):
            if instance.is_dir():
                self.ui.InstanceList.addItem(instance.name)

    def _instance_selected(self, item):
        if item is None:
            return
        
        self.ui.InstanceSettingsFrame.show()

        name = item.text()

        config = load_instance_config(name)

        self.ui.InstanceName.setText(config["Name"])
        self.ui.IPAddressInput.setText(config["IPAddress"] or "")

        self.ui.ProtonSelectBox.clear()
        for ver in self._list_proton_versions():
            if not ver == "downloading":
                self.ui.ProtonSelectBox.addItem(ver)

        playtime = config["Playtime"] or "0d 0h 0m"
        self.ui.PlaytimeLabel.setText(f"Playtime: {playtime}")

    # Load users from the users.json file and show them in the UI combo box
    def _load_users(self):
        self.ui.UserSelectBox.clear()

        try:
            with open(USER_DIR / "users.json", "r") as f:
                data = json.load(f)

            users = data.get("Users", {})

            for _user_id, user_data in users.items():
                username = user_data.get("Username", "Unknown")
                self.ui.UserSelectBox.addItem(username)

        except Exception:
            print("Failed to load users.json")

    @staticmethod
    def _list_proton_versions():
        if not PROTON_DIR.exists():
            PROTON_DIR.mkdir(parents=True)
        return [p.name for p in PROTON_DIR.iterdir() if p.is_dir()]

"""
MAIN FUNCTION
"""
def main() -> None:
    try:
        ensure_directories()
        app = QApplication(sys.argv)
        widget = LauncherMain()
        widget.show()
        sys.exit(app.exec())
    except Exception:
        raise

"""
ENTRY POINT
"""
if __name__ == "__main__":
    main()
