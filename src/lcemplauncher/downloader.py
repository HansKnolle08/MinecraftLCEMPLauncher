import requests
import json
import tarfile
import zipfile
import os
from pathlib import Path
from .paths import PROTON_DIR, INSTALL_DIR, INSTANCES_DIR


VERSIONS_FILE = Path(__file__).parent / "lcemp_versions.json"


def download_file(url, output_path):
    print(f"Starting download from {url}")
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    content_length = response.headers.get('content-length')
    if content_length:
        print(f"Expected file size: {content_length} bytes")
    else:
        print("Content-Length header not provided")

    downloaded_size = 0
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)

    actual_size = output_path.stat().st_size
    print(f"Downloaded {downloaded_size} bytes, file size on disk: {actual_size} bytes")

    if content_length and int(content_length) != actual_size:
        print(f"Warning: Downloaded size ({actual_size}) does not match expected size ({content_length})")

def download_proton(version):
    downloading_dir = PROTON_DIR / "downloading"
    downloading_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{version}/GE-Proton{version}.tar.gz"
    archive = downloading_dir / f"{version}.tar.gz"

    print(f"Downloading Proton {version}")

    download_file(url, archive)

    print(f"Extracting Proton {version}")

    extract_path = PROTON_DIR / f"GE-Proton{version}"
    with tarfile.open(archive, 'r:gz') as tar:
        tar.extractall(PROTON_DIR)

    os.remove(archive)

    print(f"Proton {version} extracted to {extract_path}")

def download_lcemp(version, instance_name):
    print(f"Downloading LCEMP version {version} for instance {instance_name}")

    # JSON laden
    with open(VERSIONS_FILE, "r") as f:
        data = json.load(f)

    versions = data["versions"]

    if version not in versions:
        raise ValueError(f"Version {version} not found in lcemp_versions.json")

    download_url = versions[version]

    output = INSTALL_DIR / f"lcemp_{version}.zip"

    download_file(download_url, output)

    if not output.exists() or output.stat().st_size == 0:
        raise ValueError(f"Download failed: {output} not found or empty")

    print(f"Extracting LCEMP {version} to instance {instance_name}")

    extract_path = INSTANCES_DIR / instance_name / "game"
    extract_path.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        raise ValueError(f"Downloaded file is not a valid ZIP archive. Download may be incomplete or corrupted. File size: {output.stat().st_size} bytes")

    os.remove(output)

    print(f"LCEMP {version} extracted to {extract_path}")