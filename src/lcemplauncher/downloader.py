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
from typing import Callable, Optional
from pathlib import Path
from bs4 import BeautifulSoup

from .paths import PROTON_DIR, INSTALL_DIR, INSTANCES_DIR

VERSIONS_FILE = Path(__file__).parent / "config" / "lcemp_versions.json"

def download_file(
    url: str,
    output_path: Path,
    progress_callback: Optional[Callable[[int, Optional[int]], None]] = None,
) -> None:
    """Downloads a file from a URL (MediaFire) to the specified output path.

    Args:
        url: The URL to download.
        output_path: Path to save the downloaded file.
        progress_callback: Optional callback with signature (downloaded_bytes, total_bytes).
    """
    if "mediafire.com/file/" in url:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        download_button = soup.find("a", id="downloadButton")
        if download_button:
            url = download_button["href"]
        else:
            raise ValueError("MediaFire download button not found")

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    content_length: Optional[str] = response.headers.get("content-length")
    total_bytes: Optional[int] = int(content_length) if content_length and content_length.isdigit() else None
    if total_bytes:
        print(f"Total file size: {total_bytes} bytes")
    else:
        print("Total file size: unknown")

    downloaded_size = 0
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                if progress_callback:
                    progress_callback(downloaded_size, total_bytes)

    actual_size = output_path.stat().st_size

    if total_bytes and total_bytes != actual_size:
        print(f"Warning: Downloaded file size {actual_size} bytes does not match expected size {total_bytes} bytes")

def download_proton(version: str, progress_callback: Optional[Callable[[int, Optional[int]], None]] = None) -> None:
    """Downloads and extracts the specified Proton version.

    Args:
        version (str): The Proton version to download (e.g., "8-21").
        progress_callback: Optional callback called with (downloaded_bytes, total_bytes).

    Raises:
        ValueError: If extraction fails.
    """
    downloading_dir = PROTON_DIR / "downloading"
    downloading_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{version}/GE-Proton{version}.tar.gz"
    archive = downloading_dir / f"{version}.tar.gz"

    download_file(url, archive, progress_callback=progress_callback)

    extract_path = PROTON_DIR / f"GE-Proton{version}"

    try:
        with tarfile.open(archive, 'r:gz') as tar:
            tar.extractall(PROTON_DIR)
    except tarfile.TarError as e:
        raise ValueError(f"Failed to extract Proton archive: {e}")

    try:
        os.remove(archive)
    except Exception:
        print(f"Failed to remove temporary Proton archive: {archive}")

def download_lcemp(
    version: str,
    instance_name: str,
    progress_callback: Optional[Callable[[int, Optional[int]], None]] = None,
) -> None:
    """Downloads and extracts the specified LCEMP version for the given instance.

    Args:
        version (str): The LCEMP version to download (e.g., "1.0.1").
        instance_name (str): The name of the instance to install to.
        progress_callback: Optional callback called with (downloaded_bytes, total_bytes).

    Raises:
        ValueError: If the version is not found, download fails, or extraction fails.
    """

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
    download_file(download_url, output, progress_callback=progress_callback)

    if not output.exists() or output.stat().st_size == 0:
        raise ValueError(f"Download failed: {output} not found or empty")

    extract_path = INSTANCES_DIR / instance_name / "game"
    extract_path.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile as e:
        raise ValueError(
            f"Downloaded file is not a valid ZIP archive. Download may be incomplete or corrupted. File size: {output.stat().st_size} bytes. Error: {e}"
        )

    try:
        os.remove(output)
    except Exception:
        print(f"Failed to remove temporary LCEMP archive: {output}")

    print(f"LCEMP version {version} downloaded and extracted to instance '{instance_name}'")
