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


src/lcemplauncher/gui.py

Main GUI class for the LCEMP Launcher application.
This module defines the LauncherGUI class, which builds the user interface using Tkinter and handles 
user interactions for managing instances, downloading LCEMP and Proton, and launching the game.
"""

"""
IMPORTS
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import logging
from pathlib import Path
from typing import List, Optional

from .instances import list_instances, create_instance, delete_instance
from .downloader import download_lcemp, download_proton
from .launcher import launch_instance

# Configure logging
logger = logging.getLogger(__name__)

"""
LAUNCHER GUI CLASS
"""
class LauncherGUI:
    """
    Main GUI class for the LCEMP Launcher.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("LCEMP Launcher")
        self.root.geometry("700x600")

        self.selected_instance: Optional[str] = None
        self.versions: List[str] = []

        self._load_versions()
        self.build_ui()
        self.refresh_instances()

    def _load_versions(self) -> None:
        """
        Loads available LCEMP versions from the JSON file.
        """
        versions_file = Path(__file__).parent / "config" / "lcemp_versions.json"
        try:
            with open(versions_file, "r") as f:
                data = json.load(f)
            versions = list(data.get("versions", {}).keys())
            def _parse_version(v: str):
                parts = v.split(".")
                return tuple(int(p) if p.isdigit() else 0 for p in parts)

            self.versions = sorted(versions, key=_parse_version)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load versions: {e}")
            self.versions = []

    def build_ui(self) -> None:
        """
        Builds the main UI components.
        """
        mainframe = ttk.Frame(self.root, padding=10)
        mainframe.pack(fill="both", expand=True)

        # Left side: Instance list
        self._build_instance_list(mainframe)

        # Right side: Instance details and controls
        self._build_right_panel(mainframe)

    def _build_instance_list(self, parent: ttk.Frame) -> None:
        """
        Builds the instance list panel.
        """
        left_frame = ttk.Frame(parent)
        left_frame.pack(side="left", fill="y")

        ttk.Label(left_frame, text="Instances").pack(anchor="w")
        self.instance_list = tk.Listbox(left_frame, height=20)
        self.instance_list.pack(fill="y", expand=True)
        self.instance_list.bind("<<ListboxSelect>>", self.on_select_instance)

        ttk.Button(left_frame, text="New Instance", command=self.create_instance_dialog).pack(fill="x", pady=5)

    def _build_right_panel(self, parent: ttk.Frame) -> None:
        """
        Builds the right panel with instance info and buttons.
        """
        right_frame = ttk.Frame(parent)
        right_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.instance_label = ttk.Label(right_frame, text="No instance selected", font=("Arial", 14))
        self.instance_label.pack(anchor="w", pady=10)

        # Version selection
        self._build_version_selector(right_frame)

        # Action buttons
        self._build_action_buttons(right_frame)

    def _build_version_selector(self, parent: ttk.Frame) -> None:
        """Builds the LCEMP version selector."""
        version_frame = ttk.Frame(parent)
        version_frame.pack(anchor="w", pady=5)

        ttk.Label(version_frame, text="LCEMP Version:").pack(side="left")
        self.version_combo = ttk.Combobox(version_frame, values=self.versions, state="readonly", width=10)
        self.version_combo.pack(side="left", padx=5)
        if self.versions:
            # The list is sorted from oldest to newest; select the newest by default.
            self.version_combo.set(self.versions[-1])

    def _build_action_buttons(self, parent: ttk.Frame) -> None:
        """
        Builds the action buttons.
        """
        button_frame = ttk.Frame(parent)
        button_frame.pack(anchor="w", pady=10)

        ttk.Button(button_frame, text="Install LCEMP", command=self.install_selected).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Download Proton", command=self.download_proton_selected).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Launch", command=self.launch_selected).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_selected).grid(row=0, column=3, padx=5)

    def refresh_instances(self) -> None:
        """
        Refreshes the instance list in the UI.
        """
        self.instance_list.delete(0, tk.END)
        for inst in list_instances():
            self.instance_list.insert(tk.END, inst)

    def on_select_instance(self, event) -> None:
        """
        Handles instance selection from the list.
        """
        selection = self.instance_list.curselection()
        if not selection:
            return

        index = selection[0]
        name = self.instance_list.get(index)
        self.selected_instance = name
        self.instance_label.config(text=f"Instance: {name}")

    def create_instance_dialog(self) -> None:
        """
        Opens a dialog to create a new instance.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("New Instance")
        dialog.geometry("300x100")

        ttk.Label(dialog, text="Instance name").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)

        def create() -> None:
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Name must not be empty")
                return

            try:
                create_instance(name)
                dialog.destroy()
                self.refresh_instances()
                logger.info(f"Instance created: {name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create instance: {str(e)}")
                logger.error(f"Failed to create instance {name}: {e}")

        ttk.Button(dialog, text="Create", command=create).pack(pady=10)

    def install_selected(self) -> None:
        """
        Installs LCEMP for the selected instance.
        """
        if not self.selected_instance:
            messagebox.showerror("Error", "No instance selected")
            return

        version = self.version_combo.get()
        if not version:
            messagebox.showerror("Error", "No version selected")
            return

        try:
            download_lcemp(version, self.selected_instance)
            messagebox.showinfo("Done", f"LCEMP {version} downloaded and extracted")
            logger.info(f"LCEMP {version} installed for instance {self.selected_instance}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.error(f"Failed to install LCEMP {version} for {self.selected_instance}: {e}")

    def download_proton_selected(self) -> None:
        """
        Downloads the default Proton version.
        """
        version = "8-21"
        try:
            download_proton(version)
            messagebox.showinfo("Done", f"Proton {version} downloaded and extracted")
            logger.info(f"Proton {version} downloaded")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.error(f"Failed to download Proton {version}: {e}")

    def launch_selected(self) -> None:
        """
        Launches the selected instance.
        """
        if not self.selected_instance:
            messagebox.showerror("Error", "No instance selected")
            return

        try:
            launch_instance(self.selected_instance)
            messagebox.showinfo("Done", f"{self.selected_instance} was launched")
            logger.info(f"Instance {self.selected_instance} launched")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.error(f"Failed to launch instance {self.selected_instance}: {e}")

    def delete_selected(self) -> None:
        """
        Deletes the selected instance after confirmation.
        """
        if not self.selected_instance:
            return

        confirm = messagebox.askyesno("Delete", f"Delete instance '{self.selected_instance}'?")
        if confirm:
            try:
                delete_instance(self.selected_instance)
                self.selected_instance = None
                self.instance_label.config(text="No instance selected")
                self.refresh_instances()
                logger.info(f"Instance deleted: {self.selected_instance}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
                logger.error(f"Failed to delete instance {self.selected_instance}: {e}")

    def run(self) -> None:
        """
        Starts the GUI main loop.
        """
        self.root.mainloop()
