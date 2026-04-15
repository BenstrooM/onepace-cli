import subprocess
import sys
import platform


def play(stream_url, extra_args=None):
    cmd = ["mpv", stream_url]
    if extra_args:
        cmd.extend(extra_args)

    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        _mpv_not_found()
        sys.exit(1)


def _mpv_not_found():
    os_name = platform.system()
    if os_name == "Darwin":
        hint = "brew install mpv"
    elif os_name == "Windows":
        hint = "winget install mpv  (or download from https://mpv.io/installation/)"
    else:
        hint = "sudo apt install mpv  /  sudo pacman -S mpv  /  see https://mpv.io/installation/"
    print(f"mpv is not installed. Install it with: {hint}")
