from lcemplauncher.paths import ensure_directories
from lcemplauncher.launcher import Launcher

def main():
    ensure_directories()

    launcher = Launcher()
    launcher.start()

if __name__ == "__main__":
    main()