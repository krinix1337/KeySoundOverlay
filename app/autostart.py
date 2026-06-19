import sys
import os
import winreg

REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "KeySoundOverlay"

def get_run_command():
    """Generates the absolute command line path to start the application."""
    exe_path = os.path.abspath(sys.executable)
    # If running directly under Python interpreter
    if "python" in os.path.basename(exe_path).lower():
        # In python execution, sys.argv[0] is the entry main.py script
        # Locate main.py relative to the working directory or script path
        main_script = os.path.abspath(sys.argv[0])
        # Use pythonw if possible to avoid opening command prompts
        pythonw_path = exe_path.lower().replace("python.exe", "pythonw.exe")
        target_exe = pythonw_path if os.path.exists(pythonw_path) else exe_path
        return f'"{target_exe}" "{main_script}"'
    else:
        # Packaged executable run
        return f'"{exe_path}"'

def set_autostart(enable):
    """Enables or disables the Windows HKCU Run registry value."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_SET_VALUE)
        if enable:
            cmd = get_run_command()
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error modifying autostart registry key: {e}")
        return False

def is_autostart_enabled():
    """Checks if the application autostart registry entry exists."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        # Check if the registry value commands match
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error querying autostart registry: {e}")
        return False
