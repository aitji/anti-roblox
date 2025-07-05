import os
import sys
import time
import json
import shutil
import threading
import urllib.request
import fnmatch
import psutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from packaging import version
import winreg

ROBLOX_PROCS = {"RobloxPlayerBeta.exe", "RobloxStudioBeta.exe"}
DL_DIR = Path.home() / "Downloads"
APPDIR = Path(os.getenv("LOCALAPPDATA", "")) / "anti-roblox"
EXE_PATH = APPDIR / "anti_roblox.exe"
VERSION_FILE = APPDIR / "version.json"
STARTUP_BAT = Path(os.getenv("APPDATA")) / \
    "Microsoft/Windows/Start Menu/Programs/Startup/anti_roblox.bat"

LOCAL_ROBLOX_DIR = Path.home() / "AppData/Local/Roblox"
STARTMENU_ROBLOX_DIR = Path.home(
) / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Roblox"

ROBLOX_SHORTCUT_NAMES = [
    "Roblox", "Roblox Player", "Roblox Studio",
    "RobloxPlayerBeta", "RobloxStudioBeta",
    "Roblox Corporation"
]


def unpinRoblox():
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
            try: favorites_data, _ = winreg.QueryValueEx(key, "Favorites")
            except: pass
            winreg.CloseKey(key)
        except: pass

        quick_launch_paths = [
            Path.home() / "AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar",
            Path.home() / "AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/StartMenu",
            Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
        ]

        for path in quick_launch_paths:
            if path.exists():
                for f in path.rglob("*.lnk"):
                    if f.is_file():
                        if any(name.lower() in f.name.lower() for name in ROBLOX_SHORTCUT_NAMES):
                            try: f.unlink()
                            except: pass
    except: pass


def resetExplor():
    try:
        import subprocess
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, check=False)
        time.sleep(1)
        subprocess.run(["explorer.exe"], capture_output=True, check=False)
    except: pass
    paths = []

    user_desktop = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
    if user_desktop.exists(): paths.append(user_desktop)

    public_desktop = Path(os.environ.get("PUBLIC", "")) / "Desktop"
    if public_desktop.exists(): paths.append(public_desktop)

    for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_desktop = Path(f"{drive}:/Desktop")
        if drive_desktop.exists():
            paths.append(drive_desktop)

            for subfolder in ["Folder", "shortcuts", "shortcut", "Games"]:
                sub_path = drive_desktop / subfolder
                if sub_path.exists(): paths.append(sub_path)

    return paths


def unpinRoblox():
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)

            try: favorites_data, _ = winreg.QueryValueEx(key, "Favorites")
            except: pass

            winreg.CloseKey(key)
        except: pass

        quick_launch_paths = [
            Path.home() / "AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar",
            Path.home() / "AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/StartMenu",
            Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
        ]

        for path in quick_launch_paths:
            if path.exists():
                for f in path.rglob("*.lnk"):
                    if f.is_file():
                        if any(name.lower() in f.name.lower() for name in ROBLOX_SHORTCUT_NAMES):
                            try:
                                f.unlink()
                            except: pass
    except: pass


def resetExplor():
    try:
        import subprocess
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, check=False)
        time.sleep(1)
        subprocess.run(["explorer.exe"], capture_output=True, check=False)
    except: pass


REMOTE_VERSION = "https://raw.githubusercontent.com/aitji/anti-roblox/main/version.json"
REMOTE_EXE = "https://github.com/aitji/anti-roblox/raw/main/dist/anti_roblox.exe"


def isUpdate():
    try:
        with urllib.request.urlopen(REMOTE_VERSION, timeout=5) as res: remote = json.loads(res.read().decode())
        local = {"version": "0.0"}
        if VERSION_FILE.exists():
            with open(VERSION_FILE, 'r', encoding='utf-8') as f: local = json.load(f)
        if version.parse(remote["version"]) > version.parse(local.get("version", "0.0")):
            tmp = APPDIR / "update.exe"
            urllib.request.urlretrieve(REMOTE_EXE, tmp)
            shutil.move(str(tmp), EXE_PATH)
            with open(VERSION_FILE, 'w', encoding='utf-8') as f: json.dump(remote, f)
            os.startfile(EXE_PATH)
            sys.exit()
    except: pass


def delRoblox():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info.get('name') in ROBLOX_PROCS:
            try: proc.kill()
            except: pass


def getDeskPath():
    paths = []

    user_desktop = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
    if user_desktop.exists(): paths.append(user_desktop)

    public_desktop = Path(os.environ.get("PUBLIC", "")) / "Desktop"
    if public_desktop.exists(): paths.append(public_desktop)

    for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_desktop = Path(f"{drive}:/Desktop")
        if drive_desktop.exists():
            paths.append(drive_desktop)

            for subfolder in [
                "Folder", "shortcuts", "shortcut", "Games", "Programs",
                "Utilities", "Apps", "Applications", "Tools", "Game Shortcuts", "My Games", ""
            ]: # pr to add more subfolders btw
                sub_path = drive_desktop / subfolder
                if sub_path.exists(): paths.append(sub_path)

    return paths


def isRobloxOn():
    for f in DL_DIR.glob("*.exe"):
        if fnmatch.fnmatch(f.name, "RobloxPlayerInstaller-*.exe"):
            try:
                f.unlink()
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

    desktop_paths = getDeskPath()
    for desktop in desktop_paths:
        try:
            for f in desktop.rglob("*.lnk"):
                if f.is_file():
                    if any(name.lower() in f.name.lower() for name in ROBLOX_SHORTCUT_NAMES):
                        try: f.unlink()
                        except: pass

            for f in desktop.rglob("*.exe"):
                if f.is_file():
                    if any(name.lower() in f.name.lower() for name in ROBLOX_SHORTCUT_NAMES):
                        try: f.unlink()
                        except: pass
        except: pass

    unpinRoblox()


class RobloxInstallerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if fnmatch.fnmatch(Path(event.src_path).name, "RobloxPlayerInstaller-*.exe"):
            try:
                Path(event.src_path).unlink()
            except: pass


def monFiles():
    DL_DIR.mkdir(parents=True, exist_ok=True)
    event_handler = RobloxInstallerHandler()
    observer = Observer()
    observer.schedule(event_handler, str(DL_DIR), recursive=False)
    observer.start()
    return observer


def monProcess():
    while True:
        roblox_found = False
        for proc in psutil.process_iter(['name']):
            if proc.info.get('name') in ROBLOX_PROCS:
                try:
                    proc.kill()
                    roblox_found = True
                except: pass

        if roblox_found:
            isRobloxOn()
            resetExplor()

        time.sleep(5)


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
    delRoblox()
    isRobloxOn()
    observer = monFiles()
    threading.Thread(target=monProcess, daemon=True).start()

    try: observer.join()
    except KeyboardInterrupt:
        observer.stop()


if __name__ == "__main__": main()