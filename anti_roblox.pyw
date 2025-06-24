import os, time, subprocess, shutil, psutil, sys
from pathlib import Path
from win10toast import ToastNotifier

toast = ToastNotifier()

DOWNLOADS = Path.home() / "Downloads"
ROBLOX_PROCESSES = ["RobloxPlayerBeta.exe", "RobloxStudioBeta.exe"]
ROBLOX_DIR = Path(os.getenv("LOCALAPPDATA", "")) / "Roblox" / "Versions"
STARTUP_BAT = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "anti_roblox.bat"

def delete_installer():
    for file in DOWNLOADS.glob("RobloxPlayerInstaller-*.exe"):
        try:
            file.unlink()
            toast.show_toast("Anti-Roblox", f"{file.name} deleted", duration=3)
        except: pass

def kill_roblox():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in ROBLOX_PROCESSES:
            try:
                proc.kill()
                toast.show_toast("Anti-Roblox", f"{proc.info['name']} closed", duration=3)
            except: pass

def uninstall_roblox():
    if ROBLOX_DIR.exists():
        try:
            for proc in ROBLOX_PROCESSES:
                subprocess.call(['taskkill', '/f', '/im', proc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            shutil.rmtree(ROBLOX_DIR, ignore_errors=True)
            toast.show_toast("Anti-Roblox", "Player + Studio uninstalled", duration=3)
        except: pass

def set_autostart():
    exe_path = sys.executable
    if not STARTUP_BAT.exists():
        try:
            with open(STARTUP_BAT, 'w', encoding='utf-8') as f:
                f.write(f'start \"\" \"{exe_path}\"\n')
        except: pass

def anti_loop():
    set_autostart()
    while True:
        delete_installer()
        kill_roblox()
        uninstall_roblox()
        time.sleep(8)

if __name__ == "__main__": anti_loop()