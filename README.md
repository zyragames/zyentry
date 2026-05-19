# ZyEntry

ZyEntry is a modern Linux desktop app for creating, validating, previewing, and installing user-level `.desktop` files for KDE/GNOME/XFCE-compatible application menus.

`mockup.png` in the project root is the visual UI reference. AppImage packaging and installers are planned for a later phase and are intentionally not part of this local app build.

## Requirements

- Linux desktop environment
- Python 3.11 or newer, recommended: Python 3.11+
- PySide6, installed through the project dependencies

Check available Python versions:

```bash
python3 --version
python3.12 --version
python3.11 --version
```

## Setup

```bash
./scripts/dev_setup.sh
```

The script checks `python3.12`, `python3.11`, then `python3`, creates `.venv` if needed, updates pip, and installs the project in editable dev mode.

## Start

```bash
./scripts/dev_run.sh
```

Manual alternative:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m zyentry
```

If Python 3.12 is not available, use Python 3.11:

```bash
python3.11 -m venv .venv
```

## Tests

```bash
./scripts/dev_test.sh
```

Or manually:

```bash
source .venv/bin/activate
python -m pytest
python -c "import zyentry; print('ok')"
```

## User-Level Behavior

ZyEntry writes application menu entries only to the current user directory:

```text
~/.local/share/applications
```

Settings are saved as JSON at:

```text
~/.config/zyentry/settings.json
```

No `sudo`, system-wide installation, database, web service, Docker, AppImage, or installer is used in this phase.
