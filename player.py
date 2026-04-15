import subprocess
import sys


def play(stream_url, extra_args=None):
    cmd = ["mpv", stream_url]
    if extra_args:
        cmd.extend(extra_args)

    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print("mpv is not installed. Install it with: sudo pacman -S mpv")
        sys.exit(1)
