from lcemplauncher.gui import LauncherGUI
from lcemplauncher.paths import ensure_directories


def main():
    ensure_directories()

    gui = LauncherGUI()
    gui.run()


if __name__ == "__main__":
    main()