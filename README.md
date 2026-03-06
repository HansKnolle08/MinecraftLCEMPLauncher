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

## Installation and Running
---

1. Clone or download this repository
2. Move into run/
3. Choose the correct run_{your_os}.sh for your os
4. Run
```bash
chmod +x run_{your_os}.sh
```
5. Start the Launcher
```bash
./run_{your_os}.sh
```

## Usage
---

### Creating an Instance

1. Click the **"Create Instance"** button in the main window.
2. Enter a name for the instance and click **"Create"**.
3. The instance will appear in the list.

### Managing an Instance

1. Select an instance from the list.
2. Double-click the instance to open the instance detail window.

### Installing LCEMP

1. In the instance detail window, pick a version from the **"LCEMP Version"** dropdown.
2. Click **"Download LCEMP"**.
3. The launcher will download and extract LCEMP into the instance folder.

### Downloading Proton

1. On the main Window click on Settings and then you should see the Settings Windows with the Proton Manager inside it
2. In the Textfield enter the Proton Version you want to download (e.g. 8-32, 9-16, ...) and click on Download. 
3. The selected Proton version will be downloaded and extracted inside the lcemp_launcher folder

### Launching a Game

1. In the instance detail window, select the desired Proton version.
2. Click **"Launch"** in the instance detail window or **"Launch Instance"** in the main window to start the game using the selected Proton build.

### Deleting an Instance

1. In the instance detail window, click **"Delete Instance"**.
2. Confirm the deletion when prompted.

## Configuration
---

LCEMP versions are defined in `lcemp_versions.json`. You can add new versions by updating this file with version numbers and download URLs.

## License
---

MIT License - See LICENSE file for details

## Contributing
---

Contributions are welcome! Feel free to submit issues or pull requests.
