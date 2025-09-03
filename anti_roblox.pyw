import os
import sys
import time
import json
import shutil
import threading
import psutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ctypes
import datetime
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import win32com.client

# ---------------- CONFIG ---------------- #

APPDIR = Path(os.getenv("LOCALAPPDATA", "")) / "anti-roblox"
LOG_DIR = APPDIR / "logs"
EXE_PATH = APPDIR / "anti_roblox.exe"
VERSION_FILE = APPDIR / "version.json"
STARTUP_DIR = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Start Menu/Programs/Startup"
DL_DIR = Path.home() / "Downloads"
INTERVAL_SLEEP = 30

BLOCK_EXES = {
    "RobloxPlayerBeta.exe": None,
    "RobloxStudioBeta.exe": None
}

found_links = set()
lock = threading.Lock()

REMOTE_VERSION = "https://raw.githubusercontent.com/aitji/anti-roblox/main/version.json"
REMOTE_EXE = "https://github.com/aitji/anti-roblox/raw/main/dist/anti_roblox.exe"

# ---------------- LOGGING ---------------- #

LOG_DIR.mkdir(parents=True, exist_ok=True)
def log(message, level="INFO", fromWhere=""):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"{today}.log"
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{level or 'INFO'}] {message}{f'- {fromWhere}' if fromWhere else ''}\n")

# ---------------- SINGLE INSTANCE ---------------- #

mutex = ctypes.windll.kernel32.CreateMutexW(None, True, "AntiRobloxUniqueMutex")
if ctypes.GetLastError() == 183:
    log(f'Another instance is running', '', "SINGLE INSTANCE")
    sys.exit("Another instance is running")

# ---------------- UTILITIES ---------------- #

def refresh_desktop():
    try:
        ctypes.windll.shell32.SHChangeNotify(0x8000000, 0x1000, None, None)
        log("Desktop refreshed", '', "refresh_desktop")
    except Exception as e:
        log(f"Desktop refresh failed: {e}", "ERROR", "refresh_desktop")

def delete_file_safe(f):
    try:
        Path(f).unlink()
        log(f"Deleted file: {f}", '', "delete_file_safe")
    except Exception as e:
        log(f"Failed deleting {f}: {e}", "ERROR", "delete_file_safe")

def delete_folder_safe(p):
    try:
        shutil.rmtree(p, ignore_errors=True)
        log(f"Removed folder: {p}", '', "delete_folder_safe")
    except Exception as e:
        log(f"Failed removing folder {p}: {e}", "ERROR", "delete_folder_safe")

# ---------------- SCAN & DELETE ---------------- #

def scan_lnk_for_exes(path, exe_names):
    try:
        with open(path, "rb") as f:
            data = f.read(1024).lower()
            for exe in exe_names:
                if exe.lower().encode() in data:
                    return True
    except Exception as e:
        log(f"Failed reading {path}: {e}", "ERROR", "scan_lnk_for_exes")
    return False

def scan_folder_for_exe_links(folder):
    batch = []
    try:
        for dirpath, dirnames, filenames in os.walk(folder):
            dirnames[:] = [d for d in dirnames if os.access(os.path.join(dirpath, d), os.R_OK)]
            for f in filenames:
                if f.lower().endswith(".lnk"):
                    full_path = os.path.join(dirpath, f)
                    batch.append(full_path)
                    if len(batch) >= 256:
                        with lock:
                            for p in batch:
                                if scan_lnk_for_exes(p, list(BLOCK_EXES.keys())):
                                    found_links.add(p)
                        batch.clear()
        if batch:
            with lock:
                for p in batch:
                    if scan_lnk_for_exes(p, list(BLOCK_EXES.keys())):
                        found_links.add(p)
    except Exception as e:
        log(f"Scan folder error {folder}: {e}", "ERROR", "scan_folder_for_exe_links")

def delete_found_links():
    with lock:
        for f in list(found_links): delete_file_safe(f)
        found_links.clear()
    refresh_desktop()

def del_blocked_processes():
    for proc in psutil.process_iter(['pid','name']):
        if proc.info.get('name') in BLOCK_EXES:
            try:
                proc.kill()
                log(f"Killed process: {proc.info.get('name')}", "", "del_blocked_processes")
            except Exception as e:
                log(f"Failed to kill {proc.info.get('name')}: {e}", "ERROR", "del_blocked_processes")

# ---------------- FILE MONITOR ---------------- #

class InstallerHandler(FileSystemEventHandler):
    def on_created(self, event):
        path = Path(event.src_path)
        if path.suffix.lower() == ".exe" and path.name in BLOCK_EXES:
            delete_file_safe(path)

def monitor_downloads():
    DL_DIR.mkdir(parents=True, exist_ok=True)
    observer = Observer()
    observer.schedule(InstallerHandler(), str(DL_DIR), recursive=False)
    observer.start()
    return observer

# ---------------- PROCESS MONITOR ---------------- #

def monitor_processes():
    while True:
        del_blocked_processes()
        desktop_paths = [Path.home() / "Desktop", Path(os.getenv("PUBLIC","")) / "Desktop"]
        with ThreadPoolExecutor(max_workers=os.cpu_count()*2) as ex:
            ex.map(scan_folder_for_exe_links, desktop_paths)
        delete_found_links()
        time.sleep(INTERVAL_SLEEP)

# ---------------- STARTUP & UPDATE ---------------- #

def create_startup_shortcut():
    STARTUP_DIR.mkdir(parents=True, exist_ok=True)
    shortcut_path = STARTUP_DIR / "AntiRoblox.lnk"
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.Targetpath = str(EXE_PATH)
        shortcut.WorkingDirectory = str(EXE_PATH.parent)
        shortcut.WindowStyle = 7
        shortcut.IconLocation = str(EXE_PATH)
        shortcut.save()
        log(f"Created startup shortcut: {shortcut_path}", '', "create_startup_shortcut")
    except Exception as e:
        log(f"Failed creating startup shortcut: {e}", "ERROR", "create_startup_shortcut")

def setup_startup():
    APPDIR.mkdir(exist_ok=True)
    if not EXE_PATH.exists(): shutil.copy2(sys.executable, EXE_PATH)
    create_startup_shortcut()
    if not VERSION_FILE.exists():
        with open(VERSION_FILE, "w") as f: json.dump({"version":"1.0"}, f)
    log("Setup completed", '', "setup_startup")

def check_update():
    try:
        with urllib.request.urlopen(REMOTE_VERSION, timeout=5) as res:
            remote = json.load(res)
        local = {"version":"0.0"}
        if VERSION_FILE.exists():
            with open(VERSION_FILE, "r") as f: local = json.load(f)
        if remote["version"] > local.get("version","0.0"):
            tmp = APPDIR / "update.exe"
            urllib.request.urlretrieve(REMOTE_EXE, tmp)
            shutil.move(str(tmp), EXE_PATH)
            with open(VERSION_FILE, "w") as f: json.dump(remote,f)
            log(f"Updated to version {remote['version']}", "", "check_update")
            os.startfile(EXE_PATH)
            sys.exit()
    except Exception as e:
        log(f"Update check failed: {e}", "ERROR", "check_update")

# ---------------- MAIN ---------------- #

def main():
    setup_startup()
    check_update()
    del_blocked_processes()
    desktop_paths = [Path.home() / "Desktop", Path(os.getenv("PUBLIC","")) / "Desktop"]
    with ThreadPoolExecutor(max_workers=os.cpu_count()*2) as ex:
        ex.map(scan_folder_for_exe_links, desktop_paths)
    delete_found_links()
    observer = monitor_downloads()
    threading.Thread(target=monitor_processes, daemon=True).start()
    log("Anti-Roblox started successfully", "", "main")

    try: observer.join()
    except KeyboardInterrupt:
        observer.stop()
        log("Anti-Roblox stopped by user", "STOP", "main")

if __name__ == "__main__": main()