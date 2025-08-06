[![Status](https://img.shields.io/badge/status-active-critical)](https://github.com/aitji/anti-roblox)
[![Auto-Update](https://img.shields.io/badge/auto--update-enabled-success)](https://raw.githubusercontent.com/aitji/anti-roblox/main/anti_roblox.pyw)

> [!NOTE]
> If you came here looking for Roblox... go back.

This is a script that:
- Terminates Roblox Player & Studio
- Removes all files, shortcuts, and temp installers
- Silently runs and adds itself to system startup: `shell:startup`
- Auto-updates from GitHub

> Built for one purpose: clean the system like Roblox never existed.


Requires: Python 3.x, `pyinstaller`, `requests`, `watchdog`

```bash
pip install requests watchdog
pyinstaller --noconsole --onefile anti_roblox.pyw
```

> Output will be at `/dist/anti_roblox.exe`

---


```
aitji/anti-roblox
├── anti_roblox.pyw       # main script (auto-update + uninstall + stealth)
├── README.md             # this file
├── version.json          # auto update version file
└── /dist/*.exe           # compiled .exe output
```

---


This script silently updates itself from:

```
https://raw.githubusercontent.com/aitji/anti-roblox/main/anti_roblox.pyw
```

> [!WARNING]
> Disclaimer
> This project is made for fun and local use only.
> 
> If you run this on school computers, you're on your own.
> 
> If you rename the file, it will silently fix itself.
> 
> No GUI, no logs, no mercy.