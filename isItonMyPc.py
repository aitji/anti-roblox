import os
import json
import urllib.request
from pathlib import Path
from packaging import version

APPDIR = Path(os.getenv("LOCALAPPDATA", "")) / "anti-roblox"
EXE_PATH = APPDIR / "anti_roblox.exe"
VERSION_FILE = APPDIR / "version.json"
STARTUP_BAT = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Start Menu/Programs/Startup/anti_roblox.bat"
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/aitji/anti-roblox/main/version.json"

def getLocalVer():
    if VERSION_FILE.exists():
        try:
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("version", "unknown")
        except: return "unknown"
    return None

def getVersion():
    try:
        with urllib.request.urlopen(REMOTE_VERSION_URL, timeout=5) as res:
            data = json.loads(res.read().decode())
            return data.get("version", "unknown")
    except: return None

def isBatOn(): return STARTUP_BAT.exists()
def isExeOn(): return EXE_PATH.exists()

def delAntiRoblox():
    removed_any = False
    for path in [EXE_PATH, VERSION_FILE, STARTUP_BAT]:
        if path.exists():
            try:
                path.unlink()
                print(f"Removed: {path}")
                removed_any = True
            except Exception as e: print(f"Failed to remove {path}: {e}")
    if APPDIR.exists() and not any(APPDIR.iterdir()):
        try:
            APPDIR.rmdir()
            print(f"Removed empty folder: {APPDIR}")
        except Exception as e:
            print(f"Failed to remove folder {APPDIR}: {e}")
    if not removed_any: print("No anti-roblox files found to remove.")

def main():
    print("* Checking Anti-Roblox presence on this PC\n")

    isExe = isExeOn()
    isBat = isBatOn()
    ver = getLocalVer()
    rVer = getVersion()

    print(f"Anti-Roblox EXE found: {'Yes' if isExe else 'No'}")
    if isExe: print(f"Local version: {ver}")
    else: print("Local version: N/A")

    print(f"Startup .bat found: {'Yes' if isBat else 'No'}")

    if rVer:
        print(f"Latest remote version: {rVer}")
        if ver and ver != "unknown":
            try:
                if version.parse(ver) < version.parse(rVer): print("Update available!")
                else: print("You have the latest version.")
            except: print("Version comparison failed.")
        else: print("Local version unknown or missing.")
    else: print("Could not fetch latest version info.")

    print("\nDo you want to REMOVE anti-roblox files from this PC? (y/N): ", end='')
    choice = input().strip().lower()
    if choice == 'y': delAntiRoblox()
    else: print("No files were removed.")

if __name__ == "__main__": main()