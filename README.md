[![Build](https://img.shields.io/badge/build-pyinstaller%20--noconsole-blue)](https://www.pyinstaller.org/)
[![Status](https://img.shields.io/badge/status-active-critical)](https://github.com/aitji/anti-roblox)
[![Auto-Update](https://img.shields.io/badge/auto--update-enabled-success)](https://raw.githubusercontent.com/aitji/anti-roblox/main/anti_roblox.py)

> [!NOTE]
> If you came here looking for Roblox... go back.

This is a script that:
- Terminates Roblox Player & Studio
- Removes all files, shortcuts, and temp installers
- Silently runs and adds itself to system startup
- Auto-updates from GitHub

> Built for one purpose: clean the system like Roblox never existed.

## Build Instructions

Requires: Python 3.x, `pyinstaller`, `requests`

```bash
pip install requests
pyinstaller --noconsole --onefile anti_roblox.pyw
```

> Output will be at `/dist/anti_roblox.exe`

---

## File Structure

```
aitji/anti-roblox
├── anti_roblox.pyw       # main script (auto-update + uninstall + stealth)
├── README.md             # this file
└── /dist/                # compiled .exe output
```

---

## Auto Update

This script silently updates itself from:

```
https://raw.githubusercontent.com/aitji/anti-roblox/main/anti_roblox.py
```

## Disclaimer

This project is made for fun and local use only.

> Note: If you run this on school computers, you're on your own.  
> Note: If you rename the file, it will silently fix itself.  
> Note: No GUI, no logs, no mercy.