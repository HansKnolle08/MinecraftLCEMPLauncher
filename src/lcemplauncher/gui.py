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
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional

from .instances import list_instances, create_instance, delete_instance
from .downloader import download_lcemp, download_proton
from .launcher import launch_instance
from .paths import INSTANCES_DIR, PROTON_DIR

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
        self.root.minsize(760, 520)

        # Use a modern theme when possible
        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Status bar variable
        self.status_var = tk.StringVar(value="Ready")

        # Set the window icon from the project root (favicon.png / favicon.ico)
        self.icon_path = self._find_project_icon()
        if self.icon_path:
            try:
                if self.icon_path.suffix.lower() in {".png", ".gif"}:
                    # Works on all platforms
                    icon_img = tk.PhotoImage(file=str(self.icon_path))
                    self.root.iconphoto(False, icon_img)
                else:
                    # .ico works on Windows; on Linux, iconbitmap may fail.
                    self.root.iconbitmap(str(self.icon_path))
            except Exception as e:
                logger.debug("Failed to set window icon; this is non-fatal: %s", e)

        self.selected_instance: Optional[str] = None
        self.versions: List[str] = []

        self._load_versions()
        self.build_ui()
        self.refresh_instances()

    def _get_installed_proton_versions(self) -> list[str]:
        """Returns a sorted list of installed Proton versions found in the Proton folder."""
        if not PROTON_DIR.exists():
            return []

        versions = []
        for path in PROTON_DIR.iterdir():
            if path.is_dir() and path.name.startswith("GE-Proton"):
                versions.append(path.name.replace("GE-Proton", ""))

        def _parse(v: str):
            parts = v.split("-")
            return tuple(int(p) if p.isdigit() else 0 for p in parts)

        return sorted(versions, key=_parse)

    def _get_default_proton_version(self) -> str:
        """Returns the best available Proton version to use by default."""
        versions = self._get_installed_proton_versions()
        if versions:
            return versions[-1]
        return "8-21"

    def _find_project_icon(self) -> Optional[Path]:
        """Finds the nearest favicon file by walking up from this file.

        Supports `favicon.png`, `favicon.gif`, and `favicon.ico` (Windows only).
        """
        current = Path(__file__).resolve().parent
        # Walk up a few levels to allow running from different working directories.
        for _ in range(6):
            for name in ("favicon.png", "favicon.gif", "favicon.ico"):
                icon_path = current / name
                if icon_path.exists():
                    return icon_path
            current = current.parent

        logger.warning("Project icon not found (searched up from %s)", Path(__file__).resolve())
        return None

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
        mainframe = ttk.Frame(self.root, padding=12)
        mainframe.pack(fill="both", expand=True)

        # Allow each panel to grow
        mainframe.columnconfigure(0, weight=1, uniform="a")
        mainframe.columnconfigure(1, weight=2, uniform="a")
        mainframe.rowconfigure(0, weight=1)

        # Left side: Instance list
        self._build_instance_list(mainframe)

        # Right side: Instance details and controls
        self._build_right_panel(mainframe)

        # Status bar
        status_bar = ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken")
        status_bar.pack(side="bottom", fill="x")

    def _build_instance_list(self, parent: ttk.Frame) -> None:
        """
        Builds the instance list panel.
        """
        left_frame = ttk.LabelFrame(parent, text="Instances")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)
        parent.columnconfigure(0, weight=1)

        self.instance_list = tk.Listbox(left_frame, height=20, activestyle="dotbox", highlightthickness=0)
        self.instance_list.grid(row=0, column=0, sticky="nsew", padx=4, pady=(6, 2))
        self.instance_list.bind("<<ListboxSelect>>", self.on_select_instance)
        self.instance_list.bind("<Double-Button-1>", self.on_double_click_instance)

        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.instance_list.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=(6, 2))
        self.instance_list.config(yscrollcommand=scrollbar.set)

        ttk.Button(left_frame, text="Create Instance", command=self.create_instance_dialog).grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)
        left_frame.rowconfigure(0, weight=1)

    def _build_right_panel(self, parent: ttk.Frame) -> None:
        """
        Builds the right panel with instance info and the main action buttons.
        """
        right_frame = ttk.Frame(parent)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)
        parent.columnconfigure(1, weight=2)

        self.instance_label = ttk.Label(right_frame, text="No instance selected", font=("Segoe UI", 14, "bold"))
        self.instance_label.grid(row=0, column=0, sticky="w", pady=(4, 12))

        # Primary actions on the main page
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=1, column=0, sticky="w", pady=10)

        ttk.Button(button_frame, text="Launch Instance", command=self.launch_selected, width=16).grid(row=0, column=0, padx=4)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_instances, width=16).grid(row=0, column=1, padx=4)
        ttk.Button(button_frame, text="Settings", command=self.open_settings_window, width=16).grid(row=0, column=2, padx=4)

        # Keep some vertical spacing at the bottom
        right_frame.rowconfigure(2, weight=1)


    def refresh_instances(self) -> None:
        """
        Refreshes the instance list in the UI.
        """
        self.instance_list.delete(0, tk.END)
        for inst in list_instances():
            self.instance_list.insert(tk.END, inst)
        self.status_var.set("Instances refreshed")

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
        self.instance_label.config(text=f"Selected Instance: {name}")
        self.status_var.set(f"Selected '{name}'")

    def on_double_click_instance(self, event) -> None:
        """Opens the instance context window on double click."""
        # Ensure selection is updated before opening the context window
        self.on_select_instance(event)
        if not self.selected_instance:
            return
        self.open_instance_window(self.selected_instance)

    def create_instance_dialog(self) -> None:
        """Opens a dialog to create a new instance."""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Instance")
        dialog.geometry("300x150")

        ttk.Label(dialog, text="Instance name").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)

        def create() -> None:
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Name must not be empty", parent=dialog)
                return

            try:
                create_instance(name)
                dialog.destroy()
                self.refresh_instances()
                self.status_var.set(f"Created instance '{name}'")
                logger.info(f"Instance created: {name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create instance: {str(e)}", parent=dialog)
                self.status_var.set("Failed to create instance")
                logger.error(f"Failed to create instance {name}: {e}")

        if self.icon_path:
            try:
                if self.icon_path.suffix.lower() in {".png", ".gif"}:
                    icon_img = tk.PhotoImage(file=str(self.icon_path))
                    dialog.iconphoto(False, icon_img)
                else:
                    dialog.iconbitmap(str(self.icon_path))
            except Exception as e:
                logger.debug("Failed to set dialog icon (non-fatal): %s", e)

        ttk.Button(dialog, text="Create", command=create).pack(pady=10)

    def open_instance_window(self, instance_name: str) -> None:
        """Opens a detail/context window for the selected instance."""
        window = tk.Toplevel(self.root)
        window.title(f"Instance: {instance_name}")
        window.minsize(420, 260)

        if self.icon_path:
            try:
                if self.icon_path.suffix.lower() in {".png", ".gif"}:
                    icon_img = tk.PhotoImage(file=str(self.icon_path))
                    window.iconphoto(False, icon_img)
                else:
                    window.iconbitmap(str(self.icon_path))
            except Exception:
                pass

        info_label = ttk.Label(window, text=f"Instance: {instance_name}", font=("Segoe UI", 12, "bold"))
        info_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 6))

        # Rename
        ttk.Label(window, text="Rename:").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        rename_entry = ttk.Entry(window, width=26)
        rename_entry.insert(0, instance_name)
        rename_entry.grid(row=1, column=1, sticky="w", pady=4)
        ttk.Button(window, text="Rename", command=lambda: self._rename_instance(instance_name, rename_entry.get().strip(), window)).grid(row=1, column=2, padx=10, pady=4)

        # Open folder
        ttk.Button(window, text="Open Folder", command=lambda: self._open_instance_folder(instance_name, parent=window)).grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=4)

        # Game version selector and install
        ttk.Label(window, text="LCEMP Version:").grid(row=3, column=0, sticky="w", padx=10, pady=(12, 4))
        version_combo = ttk.Combobox(window, values=self.versions, state="readonly", width=18)
        version_combo.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=(12, 4))
        if self.versions:
            version_combo.set(self.versions[-1])

        # Proton selector
        ttk.Label(window, text="Proton Version:").grid(row=4, column=0, sticky="w", padx=10, pady=(8, 4))
        proton_versions = self._get_installed_proton_versions()
        proton_combo = ttk.Combobox(window, values=proton_versions, state="readonly", width=18)
        proton_combo.grid(row=4, column=1, columnspan=2, sticky="w", padx=10, pady=(8, 4))
        if proton_versions:
            proton_combo.set(proton_versions[-1])

        action_frame = ttk.Frame(window)
        action_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=6)
        action_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(action_frame, text="Download LCEMP", command=lambda: self.install_selected(instance_name, version_combo.get(), parent=window)).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(action_frame, text="Delete Instance", command=lambda: self._delete_instance_confirm(instance_name, window)).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(action_frame, text="Launch", command=lambda: self._launch_instance_with_proton(instance_name, proton_combo.get(), parent=window)).grid(row=0, column=2, sticky="ew", padx=4)

        window.transient(self.root)
        window.update_idletasks()
        window.wait_visibility()
        try:
            window.grab_set()
        except tk.TclError:
            # Some window managers may not allow grab immediately; ignore.
            pass
        window.focus_force()

    def _rename_instance(self, old_name: str, new_name: str, window: tk.Toplevel) -> None:
        """Renames an instance directory and updates the UI."""
        if not new_name:
            messagebox.showerror("Error", "Name must not be empty", parent=window)
            return
        if new_name == old_name:
            return

        old_path = INSTANCES_DIR / old_name
        new_path = INSTANCES_DIR / new_name
        if new_path.exists():
            messagebox.showerror("Error", f"An instance named '{new_name}' already exists", parent=window)
            return

        try:
            old_path.rename(new_path)
            self.selected_instance = new_name
            self.refresh_instances()
            self.instance_label.config(text=f"Selected Instance: {new_name}")
            self.status_var.set(f"Renamed instance to '{new_name}'")
            window.title(f"Instance: {new_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename: {e}")
            self.status_var.set("Rename failed")

    def _open_instance_folder(self, instance_name: str, parent: Optional[tk.Toplevel] = None) -> None:
        """Opens the instance folder in the system file explorer."""
        parent = parent or self.root
        instance_path = INSTANCES_DIR / instance_name
        if not instance_path.exists():
            messagebox.showerror("Error", "Instance folder does not exist", parent=parent)
            return
        try:
            subprocess.Popen(["xdg-open", str(instance_path)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}", parent=parent)

    def _delete_instance_confirm(self, instance_name: str, window: tk.Toplevel) -> None:
        """Asks for confirmation and deletes the instance."""
        confirm = messagebox.askyesno("Delete", f"Delete instance '{instance_name}'?", parent=window)
        if confirm:
            try:
                delete_instance(instance_name)
                self.selected_instance = None
                self.instance_label.config(text="No instance selected")
                self.refresh_instances()
                self.status_var.set("Instance deleted")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}", parent=window)
                self.status_var.set("Delete failed")
        """
        Opens a dialog to create a new instance.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("New Instance")
        dialog.geometry("300x150")

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
                self.status_var.set(f"Created instance '{name}'")
                logger.info(f"Instance created: {name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create instance: {str(e)}")
                self.status_var.set("Failed to create instance")
                logger.error(f"Failed to create instance {name}: {e}")

        if self.icon_path:
            try:
                dialog.iconbitmap(str(self.icon_path))
            except Exception as e:
                logger.warning(f"Failed to set dialog icon: {e}")

        ttk.Button(dialog, text="Create", command=create).pack(pady=10)

    def install_selected(self, instance_name: Optional[str] = None, version: Optional[str] = None, parent: Optional[tk.Toplevel] = None) -> None:
        """Installs LCEMP for the given instance."""
        instance = instance_name or self.selected_instance
        if not instance:
            messagebox.showerror("Error", "No instance selected", parent=parent or self.root)
            return

        if not version:
            messagebox.showerror("Error", "No version selected", parent=parent or self.root)
            return

        # Confirm overwrite if a game directory already exists
        game_dir = INSTANCES_DIR / instance / "game"
        if game_dir.exists() and any(game_dir.iterdir()):
            confirm = messagebox.askyesno(
                "Overwrite existing installation",
                f"Instance '{instance}' already has a game installed. Overwrite with LCEMP {version}?",
                parent=parent or self.root,
            )
            if not confirm:
                self.status_var.set("LCEMP install canceled")
                return

            try:
                shutil.rmtree(game_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove existing installation: {e}", parent=parent or self.root)
                self.status_var.set("LCEMP install failed")
                logger.error(f"Failed to remove existing game folder for {instance}: {e}")
                return

        try:
            self.status_var.set(f"Installing LCEMP {version}...")

            def action(progress_cb):
                download_lcemp(version, instance, progress_callback=progress_cb)

            self._run_with_progress(f"Downloading LCEMP {version}", action, parent=parent)

            messagebox.showinfo("Done", f"LCEMP {version} downloaded and extracted", parent=parent or self.root)
            self.status_var.set(f"Installed LCEMP {version} for '{instance}'")
            logger.info(f"LCEMP {version} installed for instance {instance}")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=parent or self.root)
            self.status_var.set("LCEMP install failed")
            logger.error(f"Failed to install LCEMP {version} for {instance}: {e}")

    def _run_with_progress(self, title: str, action, parent: Optional[tk.Widget] = None) -> None:
        """Run a long-running action while showing a progress dialog."""
        parent = parent or self.root
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.attributes("-topmost", True)
        dialog.grab_set()

        ttk.Label(dialog, text=title, font=("Segoe UI", 11, "bold")).pack(padx=12, pady=(12, 6))
        progress_bar = ttk.Progressbar(dialog, mode="determinate", length=360)
        progress_bar.pack(fill="x", padx=12, pady=6)

        status_var = tk.StringVar(value="Starting...")
        ttk.Label(dialog, textvariable=status_var).pack(padx=12, pady=(0, 12))

        indeterminate_started = {"value": False}

        def progress_callback(downloaded: int, total: Optional[int]) -> None:
            if total and total > 0:
                progress_bar.config(mode="determinate", maximum=total)
                progress_bar["value"] = min(downloaded, total)
                status_var.set(f"{downloaded}/{total} bytes ({downloaded/total*100:.1f}%)")
            else:
                if not indeterminate_started["value"]:
                    progress_bar.config(mode="indeterminate")
                    progress_bar.start(10)
                    indeterminate_started["value"] = True
                status_var.set(f"{downloaded} bytes downloaded")
            dialog.update_idletasks()

        try:
            action(progress_callback)
        finally:
            try:
                progress_bar.stop()
            except Exception:
                pass
            dialog.destroy()

    def download_proton_selected(self, instance_name: Optional[str] = None, version: Optional[str] = None, parent: Optional[tk.Toplevel] = None) -> None:
        """Downloads a specified Proton version."""
        if not version:
            messagebox.showerror("Error", "No Proton version selected", parent=parent or self.root)
            return

        try:
            self.status_var.set(f"Downloading Proton {version}...")

            def action(progress_cb):
                download_proton(version, progress_callback=progress_cb)

            self._run_with_progress(f"Downloading Proton {version}", action, parent=parent)

            messagebox.showinfo("Done", f"Proton {version} downloaded and extracted", parent=parent or self.root)
            self.status_var.set(f"Proton {version} downloaded")
            logger.info(f"Proton {version} downloaded")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=parent or self.root)
            self.status_var.set("Proton download failed")
            logger.error(f"Failed to download Proton {version}: {e}")

    def _launch_instance_with_proton(self, instance_name: str, proton_version: str, parent: Optional[tk.Toplevel] = None) -> None:
        """Launches an instance using a specific Proton version."""
        parent = parent or self.root

        if not instance_name:
            messagebox.showerror("Error", "No instance selected", parent=parent)
            return

        if not proton_version:
            messagebox.showerror("Error", "No Proton version selected", parent=parent)
            return

        try:
            self.status_var.set(f"Launching '{instance_name}' with Proton {proton_version}...")
            launch_instance(instance_name, proton_version=proton_version)
            messagebox.showinfo("Done", f"{instance_name} was launched", parent=parent)
            self.status_var.set(f"Launched '{instance_name}'")
            logger.info(f"Instance {instance_name} launched")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=parent)
            self.status_var.set("Launch failed")
            logger.error(f"Failed to launch instance {instance_name}: {e}")

    def open_settings_window(self) -> None:
        """Opens the settings window for managing Proton."""
        window = tk.Toplevel(self.root)
        window.title("Settings")
        window.minsize(440, 320)

        if self.icon_path:
            try:
                window.iconbitmap(str(self.icon_path))
            except Exception:
                pass

        title = ttk.Label(window, text="Proton Manager", font=("Segoe UI", 12, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(12, 8))

        ttk.Label(window, text="Proton Version:").grid(row=1, column=0, sticky="w", padx=12)
        version_entry = ttk.Entry(window, width=18)
        version_entry.insert(0, self._get_default_proton_version())
        version_entry.grid(row=1, column=1, sticky="w", padx=(4, 0))

        def refresh_proton_list() -> None:
            proton_list.delete(0, tk.END)
            for v in self._get_installed_proton_versions():
                proton_list.insert(tk.END, v)

        ttk.Button(window, text="Download", command=lambda: [
            self.download_proton_selected(version=version_entry.get().strip(), parent=window),
            refresh_proton_list(),
        ]).grid(row=1, column=2, padx=12)

        ttk.Separator(window, orient="horizontal").grid(row=2, column=0, columnspan=3, sticky="ew", padx=12, pady=10)

        ttk.Label(window, text="Installed Proton Versions:").grid(row=3, column=0, columnspan=3, sticky="w", padx=12)

        proton_list_frame = ttk.Frame(window)
        proton_list_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=12, pady=(4, 0))
        window.rowconfigure(4, weight=1)

        proton_list = tk.Listbox(proton_list_frame, height=8)
        proton_list.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(proton_list_frame, orient="vertical", command=proton_list.yview)
        scrollbar.pack(side="right", fill="y")
        proton_list.config(yscrollcommand=scrollbar.set)

        for v in self._get_installed_proton_versions():
            proton_list.insert(tk.END, v)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=12, pady=10)
        btn_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(btn_frame, text="Delete", command=lambda: self._delete_proton_version(proton_list)).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(btn_frame, text="Open Folder", command=self._open_proton_folder).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(btn_frame, text="Close", command=window.destroy).grid(row=0, column=2, sticky="ew", padx=4)

        window.transient(self.root)
        window.grab_set()
        window.focus_force()

    def _open_proton_folder(self) -> None:
        """Opens the Proton install folder in the file explorer."""
        try:
            subprocess.Popen(["xdg-open", str(PROTON_DIR)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Proton folder: {e}")

    def _delete_proton_version(self, proton_list: tk.Listbox) -> None:
        """Deletes the selected Proton version from disk."""
        selection = proton_list.curselection()
        if not selection:
            return

        version = proton_list.get(selection[0])
        confirm = messagebox.askyesno("Delete", f"Delete Proton {version}?", parent=proton_list)
        if not confirm:
            return

        proton_path = PROTON_DIR / f"GE-Proton{version}"
        try:
            shutil.rmtree(proton_path)
            proton_list.delete(selection[0])
            self.status_var.set(f"Deleted Proton {version}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete Proton {version}: {e}", parent=proton_list)
            self.status_var.set("Delete failed")

    def launch_selected(self) -> None:
        """Launches the selected instance."""
        if not self.selected_instance:
            messagebox.showerror("Error", "No instance selected")
            return

        proton_version = self._get_default_proton_version()

        try:
            self.status_var.set(f"Launching '{self.selected_instance}' with Proton {proton_version}...")
            launch_instance(self.selected_instance, proton_version=proton_version)
            messagebox.showinfo("Done", f"{self.selected_instance} was launched")
            self.status_var.set(f"Launched '{self.selected_instance}'")
            logger.info(f"Instance {self.selected_instance} launched")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Launch failed")
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
                self.status_var.set("Instance deleted")
                logger.info(f"Instance deleted: {self.selected_instance}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
                self.status_var.set("Delete failed")
                logger.error(f"Failed to delete instance {self.selected_instance}: {e}")

    def run(self) -> None:
        """
        Starts the GUI main loop.
        """
        self.root.mainloop()
