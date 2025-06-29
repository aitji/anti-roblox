import os, sys, time, json, shutil, threading, urllib.request
import psutil, wmi
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ROBLOX_PROCS = {"RobloxPlayerBeta.exe", "RobloxStudioBeta.exe"}
ROBLOX_DIR = Path.home() / "AppData/Local/Roblox/Versions"
DL_DIR = Path.home() / "Downloads"
APPDIR = Path(os.getenv("LOCALAPPDATA", "")) / "anti-roblox"
EXE_PATH = APPDIR / "anti_roblox.exe"
VERSION_FILE = APPDIR / "version.json"
STARTUP_BAT = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Start Menu/Programs/Startup/anti_roblox.bat"

REMOTE_VERSION = "https://raw.githubusercontent.com/aitji/anti-roblox/main/version.json"
REMOTE_EXE = "https://github.com/aitji/anti-roblox/raw/main/dist/anti_roblox.exe"

def checkUpdate():
    try:
        with urllib.request.urlopen(REMOTE_VERSION, timeout=5) as res:
            remote = json.loads(res.read().decode())
        local = {"version": "0.0"}
        if VERSION_FILE.exists():
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                local = json.load(f)
        local_ver = local.get("version", "0.0")
        if remote["version"] > local_ver:
            tmp = APPDIR / "update.exe"
            urllib.request.urlretrieve(REMOTE_EXE, tmp)
            shutil.move(str(tmp), EXE_PATH)
            with open(VERSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(remote, f)
            os.startfile(EXE_PATH)
            sys.exit()
    except: pass

def killRoblox():
    for proc in psutil.process_iter(['pid', 'name']):
        name = proc.info.get('name')
        if name in ROBLOX_PROCS:
            try: psutil.Process(proc.info['pid']).kill()
            except: pass

def cleanRobloxInstall():
    for f in DL_DIR.glob("RobloxPlayerInstaller-*.exe"):
        try: f.unlink()
        except: pass
    if ROBLOX_DIR.exists():
        try: shutil.rmtree(ROBLOX_DIR, ignore_errors=True)
        except: pass

class RobloxInstallerHandler(FileSystemEventHandler):
    def on_created(self, event):
        name = Path(event.src_path).name
        if name.startswith("RobloxPlayerInstaller") and name.endswith(".exe"):
            try: Path(event.src_path).unlink()
            except: pass

def monitorFiles():
    DL_DIR.mkdir(parents=True, exist_ok=True)
    event_handler = RobloxInstallerHandler()
    observer = Observer()
    observer.schedule(event_handler, str(DL_DIR), recursive=False)
    observer.start()
    return observer

def monitorProcess():
    time.sleep(1)
    try:
        w = wmi.WMI()
        watcher = w.Win32_Process.watch_for("creation")
        while True:
            try:
                proc = watcher()
                if proc.Name in ROBLOX_PROCS:
                    killRoblox()
                    cleanRobloxInstall()
            except: pass
    except: pass

def setupStartup():
    if not EXE_PATH.exists():
        try: shutil.copy2(sys.executable, EXE_PATH)
        except: pass
    if not STARTUP_BAT.exists():
        try:
            with open(STARTUP_BAT, 'w', encoding='utf-8') as f:
                f.write(f'start "" "{EXE_PATH}"\n')
        except: pass
    if not VERSION_FILE.exists():
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            json.dump({"version": "1.0"}, f)

def main():
    APPDIR.mkdir(exist_ok=True)

    setupStartup()
    checkUpdate()
    killRoblox()
    cleanRobloxInstall()
    observer = monitorFiles()
    threading.Thread(target=monitorProcess, daemon=True).start()
    observer.join()

if __name__ == "__main__": main()