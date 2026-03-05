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


src/lcemplauncher/downloader.py

Downloader functions for the LCEMP Launcher application.
This module provides functions to download and extract LCEMP and Proton versions.
"""

"""
IMPORTS
"""
import requests
import json
import tarfile
import zipfile
import os
import logging
from pathlib import Path
from typing import Optional

from .paths import PROTON_DIR, INSTALL_DIR, INSTANCES_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

VERSIONS_FILE = Path(__file__).parent / "config" / "lcemp_versions.json"

def download_file(url: str, output_path: Path) -> None:
    """
    Downloads a file from the given URL to the specified output path.

    Args:
        url (str): The URL to download from.
        output_path (Path): The path where the file will be saved.
    """
    logger.info(f"Starting download from {url}")
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    content_length: Optional[str] = response.headers.get('content-length')
    if content_length:
        logger.info(f"Expected file size: {content_length} bytes")
    else:
        logger.warning("Content-Length header not provided")

    downloaded_size = 0
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)

    actual_size = output_path.stat().st_size
    logger.info(f"Downloaded {downloaded_size} bytes, file size on disk: {actual_size} bytes")

    if content_length and int(content_length) != actual_size:
        logger.warning(f"Downloaded size ({actual_size}) does not match expected size ({content_length})")

def download_proton(version: str) -> None:
    """
    Downloads and extracts the specified Proton version.

    Args:
        version (str): The Proton version to download (e.g., "8-21").

    Raises:
        ValueError: If extraction fails.
    """
    downloading_dir = PROTON_DIR / "downloading"
    downloading_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{version}/GE-Proton{version}.tar.gz"
    archive = downloading_dir / f"{version}.tar.gz"

    logger.info(f"Downloading Proton {version}")
    download_file(url, archive)

    logger.info(f"Extracting Proton {version}")
    extract_path = PROTON_DIR / f"GE-Proton{version}"
    try:
        with tarfile.open(archive, 'r:gz') as tar:
            tar.extractall(PROTON_DIR)
    except tarfile.TarError as e:
        raise ValueError(f"Failed to extract Proton archive: {e}")

    os.remove(archive)
    logger.info(f"Proton {version} extracted to {extract_path}")

def download_lcemp(version: str, instance_name: str) -> None:
    """
    Downloads and extracts the specified LCEMP version for the given instance.

    Args:
        version (str): The LCEMP version to download (e.g., "1.0.1").
        instance_name (str): The name of the instance to install to.

    Raises:
        ValueError: If the version is not found, download fails, or extraction fails.
    """
    logger.info(f"Downloading LCEMP version {version} for instance {instance_name}")

    try:
        with open(VERSIONS_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to load versions file: {e}")

    versions = data.get("versions", {})
    if version not in versions:
        raise ValueError(f"Version {version} not found in lcemp_versions.json")

    download_url = versions[version]
    output = INSTALL_DIR / f"lcemp_{version}.zip"

    download_file(download_url, output)

    if not output.exists() or output.stat().st_size == 0:
        raise ValueError(f"Download failed: {output} not found or empty")

    logger.info(f"Extracting LCEMP {version} to instance {instance_name}")
    extract_path = INSTANCES_DIR / instance_name / "game"
    extract_path.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile as e:
        raise ValueError(f"Downloaded file is not a valid ZIP archive. Download may be incomplete or corrupted. File size: {output.stat().st_size} bytes. Error: {e}")

    os.remove(output)
    logger.info(f"LCEMP {version} extracted to {extract_path}")
