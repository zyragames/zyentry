# ZyEntry

**ZyEntry** is a small, modern Linux desktop utility for creating `.desktop` files without editing config files by hand.

It helps you add AppImages, binaries, scripts, launchers, and custom applications to your Linux application menu in a clean and beginner-friendly way.

Built with **Python** and **PySide6**.

---

## ✨ Features

- Create Linux `.desktop` launchers through a simple GUI
- Step-by-step workflow
- Validation for required fields
- Preview generated `.desktop` files before installing
- User-level installation only — no `sudo` required
- Adds launchers to:

```text
~/.local/share/applications/
```

- Supports common freedesktop categories:
  - Utility
  - Development
  - Game
  - Graphics
  - AudioVideo
  - Office
  - Network
  - System
  - Settings
  - Education
- Optional terminal launch mode
- Dark mode and light mode
- Language support:
  - German
  - English
  - French
- Settings are saved locally as JSON:

```text
~/.config/zyentry/settings.json
```

---

## 🖥️ What does it do?

Instead of manually writing files like this:

```ini
[Desktop Entry]
Type=Application
Name=My App
Comment=My custom launcher
Exec=/home/user/Applications/MyApp.AppImage
Icon=my-app
Terminal=false
Categories=Utility;
StartupNotify=true
```

ZyEntry lets you create them through a clean graphical interface.

The generated launcher appears in compatible Linux desktop environments such as:

- KDE Plasma
- GNOME
- XFCE
- Cinnamon
- MATE
- LXQt

---

## 📦 Current status

ZyEntry is currently in early development.

The local Python app is the main focus right now. Packaging as an **AppImage** and adding an installer script is planned for a later stage.

---

## 🚀 Requirements

- Linux
- Python **3.11+**
- PySide6

Check your Python version:

```bash
python3 --version
```

If you have multiple Python versions installed, you can check them like this:

```bash
python3.12 --version
python3.11 --version
python3 --version
```

---

## 🔧 Run from source

Clone the repository:

```bash
git clone https://github.com/zyrano84/zyentry.git
cd zyentry
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

If `python3.12` is not available, use Python 3.11 or newer:

```bash
python3.11 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install ZyEntry in editable mode:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Start the app:

```bash
python -m zyentry
```

---

## 🧭 Basic workflow

1. Choose an application, AppImage, binary, or script
2. Enter a name and optional description
3. Select an icon
4. Choose a desktop menu category
5. Preview and create the launcher

ZyEntry writes the generated `.desktop` file to your local user applications directory:

```text
~/.local/share/applications/
```

No system-wide installation is required.

---

## 🌓 Themes

ZyEntry includes:

- Dark mode
- Light mode

The selected theme is saved automatically and restored on the next start.

---

## 🌍 Languages

ZyEntry currently supports:

- 🇩🇪 German
- 🇬🇧 English
- 🇫🇷 French

The selected language is saved automatically.

---

## 🔐 Privacy

ZyEntry does not use:

- cloud services
- tracking
- telemetry
- online accounts
- external APIs

Everything happens locally on your machine.

---

## 🗂️ Project structure

```text
zyentry/
├── pyproject.toml
├── README.md
└── src/
    └── zyentry/
        ├── app.py
        ├── __main__.py
        ├── core/
        ├── ui/
        └── resources/
```

---

## 🛠️ Development notes

ZyEntry follows a simple principle:

> Make Linux desktop launchers easy, without hiding what is being generated.

The app is intentionally small, local-first, and user-level only.

---

## 📌 Planned

- AppImage build
- Installer script for easy desktop integration
- Better icon handling
- Optional launcher editing
- Optional launcher removal
- More desktop environment polish

---

## 🤝 Contributing

Contributions are welcome.

Good areas for contributions:

- UI polish
- Linux desktop compatibility
- translations
- packaging
- AppImage support
- bug fixes

Please keep changes focused and avoid unnecessary complexity.

---

## 📄 License

License not selected yet.

If you want to use or contribute to ZyEntry, please check back once a license has been added.
