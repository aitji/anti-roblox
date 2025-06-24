import os, time, subprocess, shutil, psutil, sys, json, urllib.request
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
ROBLOX_PROCESSES = ["RobloxPlayerBeta.exe", "RobloxStudioBeta.exe"]
ROBLOX_DIR = Path(os.getenv("LOCALAPPDATA", "")) / "Roblox" / "Versions"
APPDIR = Path(os.getenv("LOCALAPPDATA", "")) / "anti-roblox"
EXE_NAME = "anti_roblox.exe"
TARGET_EXE = APPDIR / EXE_NAME
STARTUP_BAT = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "anti_roblox.bat"
VERSION_FILE = APPDIR / "version.json"

REMOTE_VERSION_URL = "https://raw.githubusercontent.com/aitji/anti-roblox/main/version.json"
REMOTE_EXE_URL = "https://github.com/aitji/anti-roblox/raw/main/dist/anti_roblox.exe"

def checkUpdate():
    try:
        with urllib.request.urlopen(REMOTE_VERSION_URL, timeout=5) as res:
            remote = json.loads(res.read().decode())
        local = {"version": "0.0"}
        if VERSION_FILE.exists():
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                local = json.load(f)
        if remote["version"] > local["version"]:
            tmp = APPDIR / "update.exe"
            urllib.request.urlretrieve(REMOTE_EXE_URL, tmp)
            shutil.move(str(tmp), TARGET_EXE)
            with open(VERSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(remote, f)
    except: pass

def deleteInstaller():
    for file in DOWNLOADS.glob("RobloxPlayerInstaller-*.exe"):
        try: file.unlink()
        except: pass

def killRoblox():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in ROBLOX_PROCESSES:
            try: proc.kill()
            except: pass

def uninstallRoblox():
    if ROBLOX_DIR.exists():
        try:
            for proc in ROBLOX_PROCESSES:
                subprocess.call(['taskkill', '/f', '/im', proc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            shutil.rmtree(ROBLOX_DIR, ignore_errors=True)
        except: pass

def setupStartup():
    APPDIR.mkdir(exist_ok=True)
    if not TARGET_EXE.exists():
        try: shutil.copy2(sys.executable, TARGET_EXE)
        except: pass
    if not STARTUP_BAT.exists():
        try:
            with open(STARTUP_BAT, 'w', encoding='utf-8') as f:
                f.write(f'start "" "{TARGET_EXE}"\n')
        except: pass
    if not VERSION_FILE.exists():
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            json.dump({"version": "1.0"}, f)

def antiLoop():
    setupStartup()
    checkUpdate()
    while True:
        deleteInstaller()
        killRoblox()
        uninstallRoblox()
        time.sleep(5)

if __name__ == "__main__": antiLoop()
