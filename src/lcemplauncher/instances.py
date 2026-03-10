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


src/lcemplauncher/instances.py

Instance management functions for the LCEMP Launcher application.
This module provides functions to list, create, and delete instances.
"""

"""
IMPORTS
"""

# Standard library imports
import shutil
from typing import List
import json

# Local imports
from .paths import INSTANCES_DIR, INTERNAL_CONFIG_DIR

# Lists all instances and returns their names as a list of strings.
def list_instances() -> List[str]:
    if not INSTANCES_DIR.exists():
        INSTANCES_DIR.mkdir(parents=True)

    return [p.name for p in INSTANCES_DIR.iterdir() if p.is_dir()]

# Creates a new instance with the given name. It creates a new directory for the instance and copies a template configuration file into it.
def create_instance(name: str) -> None:
    path = INSTANCES_DIR / name
    path.mkdir(parents=True, exist_ok=True)

    template = INTERNAL_CONFIG_DIR / "instance.json"
    target = path / "instance.json"

    if not target.exists():
        shutil.copy(template, target)

        with open(target, "r") as f:
            data = json.load(f)

        data["instance"]["Name"] = name

        with open(target, "w") as f:
            json.dump(data, f, indent=4)

# Loads the configuration of an instance and returns it as a dictionary. It reads the instance.json file from the instance's directory.
def load_instance_config(name: str) -> dict:
    config_path = INSTANCES_DIR / name / "instance.json"

    if not config_path.exists():
        raise ValueError("Instance config missing")

    with open(config_path, "r") as f:
        data = json.load(f)

    return data["instance"]

def delete_instance(name: str) -> None:
    """
    Deletes an instance and all its contents.

    Args:
        name (str): The name of the instance to delete.
    """
    path = INSTANCES_DIR / name
    if path.exists():
        shutil.rmtree(path)
    else:
        print(f"Instance '{name}' does not exist.")
