from pathlib import Path
import shutil
from .paths import INSTANCES_DIR


def list_instances():

    if not INSTANCES_DIR.exists():
        INSTANCES_DIR.mkdir(parents=True)

    return [
        p.name for p in INSTANCES_DIR.iterdir()
        if p.is_dir()
    ]


def create_instance(name):

    path = INSTANCES_DIR / name
    path.mkdir(parents=True, exist_ok=True)


def delete_instance(name):

    path = INSTANCES_DIR / name

    if path.exists():
        shutil.rmtree(path)