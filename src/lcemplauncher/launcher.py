import subprocess
import os
from pathlib import Path
from .paths import INSTANCES_DIR, PROTON_DIR


def launch_instance(instance_name, proton_version="8-21"):
    game_dir = INSTANCES_DIR / instance_name / "game"
    if not game_dir.exists():
        raise ValueError("Game not installed for this instance")

    proton_dir = PROTON_DIR / f"GE-Proton{proton_version}"
    if not proton_dir.exists():
        raise ValueError(f"Proton {proton_version} not downloaded")

    # Find the exe - assume it's LCEMP.exe or search for .exe
    exe_files = list(game_dir.glob("*.exe"))
    if not exe_files:
        raise ValueError("No executable found in game directory")

    exe_path = exe_files[0]  # Take the first one

    # Set up Wine prefix for this instance
    wineprefix_path = INSTANCES_DIR / instance_name / "wineprefix"
    wineprefix_path.mkdir(parents=True, exist_ok=True)

    print(f"Launching {exe_path} with Proton {proton_version} using prefix {wineprefix_path}")

    # Command: proton run exe_path
    cmd = [str(proton_dir / "proton"), "run", str(exe_path)]

    # Environment with STEAM_COMPAT_DATA_PATH and STEAM_COMPAT_CLIENT_INSTALL_PATH
    env = os.environ.copy()
    env["STEAM_COMPAT_DATA_PATH"] = str(wineprefix_path)
    env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = str(proton_dir)

    # Change to game directory
    os.chdir(game_dir)

    # Run in background? For now, run and wait
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        raise ValueError(f"Launch failed with return code {result.returncode}")


    