import os, sys, time, json, shutil, threading, urllib.request, fnmatch
import psutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from packaging import version

ROBLOX_PROCS = {"RobloxPlayerBeta.exe", "RobloxStudioBeta.exe"}
DL_DIR = Path.home() / "Downloads"
APPDIR = Path(os.getenv("LOCALAPPDATA", "")) / "anti-roblox"
EXE_PATH = APPDIR / "anti_roblox.exe"
VERSION_FILE = APPDIR / "version.json"
STARTUP_BAT = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Start Menu/Programs/Startup/anti_roblox.bat"

LOCAL_ROBLOX_DIR = Path.home() / "AppData/Local/Roblox"
STARTMENU_ROBLOX_DIR = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Roblox"
DESKTOP_PATHS = [
    Path(os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")),
    Path("E:/Desktop/Folder/shortcut")
    # open issuse/pull request to add more paths btw!
]

REMOTE_VERSION = "https://raw.githubusercontent.com/aitji/anti-roblox/main/version.json"
REMOTE_EXE = "https://github.com/aitji/anti-roblox/raw/main/dist/anti_roblox.exe"

def isUpdate():
    try:
        with urllib.request.urlopen(REMOTE_VERSION, timeout=5) as res:
            remote = json.loads(res.read().decode())
        local = {"version": "0.0"}
        if VERSION_FILE.exists():
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                local = json.load(f)
        if version.parse(remote["version"]) > version.parse(local.get("version", "0.0")):
            tmp = APPDIR / "update.exe"
            urllib.request.urlretrieve(REMOTE_EXE, tmp)
            shutil.move(str(tmp), EXE_PATH)
            with open(VERSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(remote, f)
            os.startfile(EXE_PATH)
            sys.exit()
    except:
        pass

def killRoblox():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info.get('name') in ROBLOX_PROCS:
            try: proc.kill()
            except: pass

def clean_RobloxInstall():
    for f in DL_DIR.glob("*.exe"):
        if fnmatch.fnmatch(f.name, "RobloxPlayerInstaller-*.exe"):
            try: f.unlink()
            except: pass

    for path in [
        LOCAL_ROBLOX_DIR,
        STARTMENU_ROBLOX_DIR,
        Path("C:/Program Files/Roblox"),
        Path("C:/Program Files (x86)/Roblox")
    ]:
        if path.exists():
            try: shutil.rmtree(path, ignore_errors=True)
            except: pass

    for desktop in DESKTOP_PATHS:
        if desktop.exists():
            for f in desktop.glob("**/*"):
                if f.is_file() and f.suffix.lower() == ".lnk":
                    if any(name in f.name for name in ["Roblox", "Roblox Player", "Roblox Studio"]):
                        try: f.unlink()
                        except: pass

class RobloxInstallerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if fnmatch.fnmatch(Path(event.src_path).name, "RobloxPlayerInstaller-*.exe"):
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
    while True:
        for proc in psutil.process_iter(['name']):
            if proc.info.get('name') in ROBLOX_PROCS:
                try: proc.kill()
                except: pass
                clean_RobloxInstall()
        time.sleep(0.5)

def setupStart():
    if not EXE_PATH.exists():
        try: shutil.copy2(sys.executable, EXE_PATH)
        except: pass

    startup_folder = STARTUP_BAT.parent
    if not startup_folder.exists():
        try: startup_folder.mkdir(parents=True, exist_ok=True)
        except: pass

    if not STARTUP_BAT.exists():
        try:
            with open(STARTUP_BAT, 'w', encoding='utf-8') as f: f.write(f'start "" "{EXE_PATH}"\n')
        except: pass

    if not VERSION_FILE.exists():
        with open(VERSION_FILE, 'w', encoding='utf-8') as f: json.dump({"version": "1.0"}, f)

def main():
    APPDIR.mkdir(exist_ok=True)
    setupStart()
    isUpdate()
    killRoblox()
    clean_RobloxInstall()
    observer = monitorFiles()
    threading.Thread(target=monitorProcess, daemon=True).start()
    observer.join()

if __name__ == "__main__": main()