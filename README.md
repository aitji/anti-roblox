[![Status](https://img.shields.io/badge/status-active-critical)](https://github.com/aitji/anti-roblox)
[![Auto-Update](https://img.shields.io/badge/auto--update-enabled-success)](https://raw.githubusercontent.com/aitji/anti-roblox/main/anti_roblox.pyw)

> [!NOTE]
> If you came here looking for Roblox... go back.

This is a script that:
- Terminates Roblox Player & Studio
- Removes all\* files, shortcuts, and temp installers
- Silently runs and adds itself to system startup: `shell:startup`
- Auto-updates from this GitHub

> Built for one purpose: clean the system like Roblox never existed.


Requires: Python 3.x, `psutil`, `watchdog`, `numba`, `pywin32`

```bash
pip install -r requirements.txt
```

you can direct load python module by this below command!

```bash
pip install psutil watchdog numba pywin32
```

## Build Python to EXE

```bash
pyinstaller --noconsole --onefile anti_roblox.pyw
```

> You should grab "anti_roblox.spec" too
> 
> Output will be at `/dist/anti_roblox.exe`

---


```
aitji/anti-roblox
├── anti_roblox.pyw       # main snip
├── isItonMyPc.py         # check anti roblox snip
├── version.json          # auto update version file
├── anti_roblox.spec      # spec to build exe
├── README.md             # this file
└── /dist/*.exe           # compiled .exe output
```

---


This script silently updates itself from:

```
https://raw.githubusercontent.com/aitji/anti-roblox/main/anti_roblox.pyw
```

> [!WARNING]
> Disclaimer
> This project is made for fun and local use only, If you run this on school computers, you're on your own.
>
> If you rename the file, it will silently fix itself. (No GUI, no logs, no mercy)

## Star History

<a href="https://www.star-history.com/#aitji/anti-roblox&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=aitji/anti-roblox&type=date&theme=dark&legend=bottom-right" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=aitji/anti-roblox&type=date&legend=bottom-right" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=aitji/anti-roblox&type=date&legend=bottom-right" />
 </picture>
</a>
