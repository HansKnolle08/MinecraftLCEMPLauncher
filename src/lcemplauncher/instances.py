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
import shutil
import logging
from typing import List

from .paths import INSTANCES_DIR

logger = logging.getLogger(__name__)

def list_instances() -> List[str]:
    """
    Lists all instances.

    Returns:
        List[str]: A list of instance names.
    """
    if not INSTANCES_DIR.exists():
        INSTANCES_DIR.mkdir(parents=True)
        logger.info(f"Created instances directory: {INSTANCES_DIR}")

    return [p.name for p in INSTANCES_DIR.iterdir() if p.is_dir()]

def create_instance(name: str) -> None:
    """
    Creates a new instance.

    Args:
        name (str): The name of the instance.
    """
    path = INSTANCES_DIR / name
    path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created instance: {name}")

def delete_instance(name: str) -> None:
    """
    Deletes an instance and all its contents.

    Args:
        name (str): The name of the instance to delete.
    """
    path = INSTANCES_DIR / name
    if path.exists():
        shutil.rmtree(path)
        logger.info(f"Deleted instance: {name}")
    else:
        logger.warning(f"Instance {name} does not exist")
