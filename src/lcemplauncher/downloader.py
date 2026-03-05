import requests
import json
from pathlib import Path
from .paths import PROTON_DIR, INSTALL_DIR


VERSIONS_FILE = Path(__file__).parent / "lcemp_versions.json"


def download_file(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)

def download_proton(version):
    url = f"https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton{version}/GE-Proton{version}.tar.gz"
    archive = PROTON_DIR / f"{version}.tar.gz"

    print(f"Downloading Proton {version}")

    download_file(url, archive)

def download_lcemp(version):
    print(f"Downloading LCEMP version {version}")

    # JSON laden
    with open(VERSIONS_FILE, "r") as f:
        data = json.load(f)

    versions = data["versions"]

    if version not in versions:
        raise ValueError(f"Version {version} not found in lcemp_versions.json")

    download_url = versions[version]

    output = INSTALL_DIR / f"lcemp_{version}.zip"

    download_file(download_url, output)

    print(f"Downloaded LCEMP {version} to {output}")