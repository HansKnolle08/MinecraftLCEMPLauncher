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

- Python 3.7+
- tkinter (usually included with Python)
- requests library
- bs4 library
- Linux-based OS

## Installation
---

1. Clone or download this repository

## Usage
---

### Running the Launcher

```bash
python src/main.py
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
