# Screen Sharing App

## Description

**Screen Sharing App** is a Python application that allows you to capture and share your screen on **Ubuntu 24.04** with GNOME. The app lets you select a **monitor** or a **specific window** and provides a **dynamic real-time preview at 720p resolution**, ensuring a high-quality viewing experience.

The application uses technologies such as:

- **PyGObject**: To capture the screen and manage monitors in GNOME.
- **xwininfo** and **xwd**: To obtain information and screenshots of specific windows in X11 systems.
- **PyQt5**: For the graphical user interface.
- **QTimer**: To update the real-time preview.

### Demo Video

[![Screen Sharing Demo](./media/Screencast from 2024-12-17 15-05-29.webm)

---

## Features

- 🖥 **Source Selection**: Choose between **monitors** or **active windows** to share.
- 🔍 **Dynamic Preview**: Displays the screen capture in **real-time** at a resolution of **1280x720 (720p)**.
- 🚀 **Intuitive Interface**: Built with **PyQt5** for easy and modern navigation.
- 🛠 **Optimization**: The image is dynamically resized to maintain quality without losing aspect ratio.

---

## System Requirements

- **Operating System**: Ubuntu 24.04 (GNOME)
- **X11 Environment** (Not yet compatible with Wayland)
- **Python 3.8+**
- Additional dependencies:
  - PyGObject
  - PyQt5
  - xwininfo
  - xwd

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/screen-sharing-app.git
cd screen-sharing-app
```

### 2. Install dependencies

Run the following command to install the required packages:

```bash
sudo apt update
sudo apt install python3-venv python3-pip x11-utils x11-apps

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Execution

1. Activate the virtual environment if it's not already active:

```bash
source venv/bin/activate
```

2. Run the main application:

```bash
python src/main.py
```

---

## Usage

1. When you start the application, a main window will appear with two buttons:

   - **"Start Sharing"**: Opens a dialog to select a **monitor** or a **specific window**.
   - **"Stop Sharing"**: Closes the preview and stops the capture.

2. Select a source (monitor or window) from the popup dialog.

3. Once the source is selected, a **dynamic real-time preview** will appear at **720p resolution**.

4. To stop sharing, click on the **"Stop Sharing"** button.

---

## Screenshots

### Monitor or Window Selection

![Monitor or Window Selection](docs/select_window.png)

### Real-Time Preview

![Real-Time Preview](docs/preview_screen.png)

---

## Project Architecture

The project file structure is as follows:

```bash
screen-sharing-app/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── __init__.py
│   ├── main.py          # Main entry point
│   ├── capture.py       # Functions to capture monitors and windows
│   ├── compression.py   # (Optional) Logic for image compression
│   └── ui.py            # Graphical user interface
├── tests/               # Unit tests
└── docs/
    ├── select_window.png
    └── preview_screen.png
```

---

## Common Issues

### 1. **Wayland Error**

- The application requires **X11**. If you are using **Wayland**, log into **Xorg** from the login screen.

### 2. **xwininfo or xwd Not Found**

- Ensure you have X11 tools installed:
  ```bash
  sudo apt install x11-utils x11-apps
  ```

---

## Contribution

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```
4. Open a Pull Request.

---

## License

This project is licensed under the **MIT License**.

---

## Author

Developed by **[Your Name]**. If you have questions or suggestions, feel free to contact me.

---

## Future Improvements

- 🔧 Support for **Wayland** environments using PipeWire.
- 🎥 Screen streaming through **WebRTC**.
- 💾 Screen recording in video format.
