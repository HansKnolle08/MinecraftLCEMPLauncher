# LCEMP Launcher
---
A Python-based GUI launcher for managing and running Minecraft LCEMP on Linux with the Proton compatibility layer.

## Features
---

- **Instance Management**: Create, list, and delete LCEMP instances
- **Version Control**: Easy selection and installation of different LCEMP versions
- **Proton Integration**: Download and use Proton for running LCEMP on Linux
- **GUI Interface**: User-friendly tkinter-based interface for all operations

## Requirements
---

- Python 3.11+
- tkinter
- requests library
- bs4 library
- Linux-based OS

## Installation
---

1. Clone or download this repository
2. Install Libraies:

Ubuntu:
```bash
sudo apt update
sudo apt install python3-tk python3-requests python3-bs4
```
Fedora:
```bash
sudo dnf update
sudo dnf install python3-tk python3-requests python3-bs4
```
Arch:
```bash
sudo pacman -Syu python3-tk python3-requests python3-bs4
```

## Usage
---

### Running the Launcher

```bash
python src/main.py
```
or
```bash
python3 src/main.py
```

### Creating an Instance

1. Click on the "New Instance" button
2. Enter a name for your instance
3. Click "Create"

### Installing LCEMP

1. Select an instance from the list
2. Choose a version from the dropdown
3. Click "Install LCEMP"

### Downloading Proton

Click "Download Proton" to download the default Proton version (8-21) needed to run the game.

### Launching a Game

1. Select an instance
2. Click "Launch" to start the game with Proton

### Deleting an Instance

1. Select an instance
2. Click "Delete" and confirm the deletion

## Configuration
---

LCEMP versions are defined in `lcemp_versions.json`. You can add new versions by updating this file with version numbers and download URLs.

## License
---

MIT License - See LICENSE file for details

## Contributing
---

Contributions are welcome! Feel free to submit issues or pull requests.
