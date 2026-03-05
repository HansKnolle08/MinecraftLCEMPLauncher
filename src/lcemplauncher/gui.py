import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

from .instances import (
    list_instances,
    create_instance,
    delete_instance,
)

from .downloader import download_lcemp, download_proton
from .launcher import launch_instance


class LauncherGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LCEMP Launcher")
        self.root.geometry("700x400")

        self.selected_instance = None

        # Load LCEMP versions
        versions_file = Path(__file__).parent / "lcemp_versions.json"
        with open(versions_file, "r") as f:
            data = json.load(f)
        self.versions = list(data["versions"].keys())

        self.build_ui()
        self.refresh_instances()

    # -------------------------
    # UI LAYOUT
    # -------------------------

    def build_ui(self):

        mainframe = ttk.Frame(self.root, padding=10)
        mainframe.pack(fill="both", expand=True)

        # LEFT SIDE (INSTANCE LIST)

        left_frame = ttk.Frame(mainframe)
        left_frame.pack(side="left", fill="y")

        ttk.Label(left_frame, text="Instanzen").pack(anchor="w")

        self.instance_list = tk.Listbox(left_frame, height=20)
        self.instance_list.pack(fill="y", expand=True)
        self.instance_list.bind("<<ListboxSelect>>", self.on_select_instance)

        ttk.Button(
            left_frame,
            text="Neue Instanz",
            command=self.create_instance_dialog
        ).pack(fill="x", pady=5)

        # RIGHT SIDE

        right_frame = ttk.Frame(mainframe)
        right_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.instance_label = ttk.Label(
            right_frame,
            text="Keine Instanz ausgewählt",
            font=("Arial", 14)
        )
        self.instance_label.pack(anchor="w", pady=10)

        # Version selection
        version_frame = ttk.Frame(right_frame)
        version_frame.pack(anchor="w", pady=5)

        ttk.Label(version_frame, text="LCEMP Version:").pack(side="left")
        self.version_combo = ttk.Combobox(version_frame, values=self.versions, state="readonly", width=10)
        self.version_combo.pack(side="left", padx=5)
        self.version_combo.set(self.versions[0])  # Default to first version

        # Buttons

        button_frame = ttk.Frame(right_frame)
        button_frame.pack(anchor="w", pady=10)

        ttk.Button(
            button_frame,
            text="Install LCEMP",
            command=self.install_selected
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Download Proton",
            command=self.download_proton_selected
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="Launch",
            command=self.launch_selected
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_selected
        ).grid(row=0, column=3, padx=5)

    # -------------------------
    # INSTANCE LIST
    # -------------------------

    def refresh_instances(self):

        self.instance_list.delete(0, tk.END)

        for inst in list_instances():
            self.instance_list.insert(tk.END, inst)

    def on_select_instance(self, event):

        selection = self.instance_list.curselection()

        if not selection:
            return

        index = selection[0]
        name = self.instance_list.get(index)

        self.selected_instance = name

        self.instance_label.config(text=f"Instanz: {name}")

    # -------------------------
    # CREATE INSTANCE
    # -------------------------

    def create_instance_dialog(self):

        dialog = tk.Toplevel(self.root)
        dialog.title("Neue Instanz")

        ttk.Label(dialog, text="Instanzname").pack(pady=5)

        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)

        def create():

            name = name_entry.get().strip()

            if not name:
                messagebox.showerror("Error", "Name darf nicht leer sein")
                return

            try:
                create_instance(name)
                dialog.destroy()
                self.refresh_instances()
            except Exception as e:
                messagebox.showerror("Error", f"Fehler beim Erstellen der Instanz: {str(e)}")

        ttk.Button(
            dialog,
            text="Erstellen",
            command=create
        ).pack(pady=10)

    # -------------------------
    # INSTALL
    # -------------------------

    def install_selected(self):

        if not self.selected_instance:
            messagebox.showerror("Error", "Keine Instanz ausgewählt")
            return

        version = self.version_combo.get()
        if not version:
            messagebox.showerror("Error", "Keine Version ausgewählt")
            return

        try:
            download_lcemp(version, self.selected_instance)
            messagebox.showinfo("Done", f"LCEMP {version} wurde heruntergeladen und entpackt")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------------
    # DOWNLOAD PROTON
    # -------------------------

    def download_proton_selected(self):

        version = "8-21"

        try:
            download_proton(version)
            messagebox.showinfo("Done", f"Proton {version} wurde heruntergeladen und entpackt")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------------
    # LAUNCH
    # -------------------------

    def launch_selected(self):

        if not self.selected_instance:
            messagebox.showerror("Error", "Keine Instanz ausgewählt")
            return

        try:
            launch_instance(self.selected_instance)
            messagebox.showinfo("Done", f"{self.selected_instance} wurde gestartet")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------------
    # DELETE
    # -------------------------

    def delete_selected(self):

        if not self.selected_instance:
            return

        confirm = messagebox.askyesno(
            "Delete",
            f"Instanz '{self.selected_instance}' löschen?"
        )

        if confirm:
            delete_instance(self.selected_instance)
            self.selected_instance = None
            self.instance_label.config(text="Keine Instanz ausgewählt")
            self.refresh_instances()

    # -------------------------

    def run(self):
        self.root.mainloop()