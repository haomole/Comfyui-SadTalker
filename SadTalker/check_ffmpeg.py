import os
import sys
import subprocess
from pathlib import Path
import winreg

def check_ffmpeg_path():
    path_list = os.environ['Path'].split(';')
    ffmpeg_found = False

    for path in path_list:
        if 'ffmpeg' in path.lower() and 'bin' in path.lower():
            ffmpeg_found = True
            print("FFmpeg already installed, skipping...")
            break

    return ffmpeg_found

def add_ffmpeg_path_to_user_variable():
    ffmpeg_bin_path = Path('.\\ffmpeg\\bin')
    if ffmpeg_bin_path.is_dir():
        abs_path = str(ffmpeg_bin_path.resolve())
        
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )
            
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
                if abs_path not in current_path:
                    new_path = f"{current_path};{abs_path}"
                    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                    print(f"Added FFmpeg path to user variable 'Path': {abs_path}")
                else:
                    print("FFmpeg path already exists in the user variable 'Path'.")
            finally:
                winreg.CloseKey(key)
        except WindowsError:
            print("Error: Unable to modify user variable 'Path'.")
            sys.exit(1)

    else:
        print("Error: ffmpeg\\bin folder not found in the current path.")
        sys.exit(1)

def get_default_browser():
    browser = ""
    try:
        cmd = r'reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice /v ProgId'
        output = subprocess.check_output(cmd, shell=True).decode()
        browser = output.split()[-1].split('\\')[-1]
    except Exception as e:
        print(f"Error: {e}")
        browser = "Unknown"
    return browser

def main():
    if not check_ffmpeg_path():
        add_ffmpeg_path_to_user_variable()
    default_browser = get_default_browser()
    if not "chrome" in default_browser.lower() and not "edge" in default_browser.lower() and not "firefox" in default_browser.lower():
        print("默认浏览器不符合要求，可能会影响使用，请更换为Chrome或Edge浏览器")
            
if __name__ == "__main__":
    main()