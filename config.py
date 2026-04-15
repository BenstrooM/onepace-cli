import json
import time
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "onepace"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
CACHE_FILE = CONFIG_DIR / "cache.json"

DEFAULT_CONFIG = {
    "mpv_args": [],
    "cache_hours": 24,
}


def _ensure():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    _ensure()
    if not CONFIG_FILE.exists():
        _write(CONFIG_FILE, DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    return {**DEFAULT_CONFIG, **_read(CONFIG_FILE)}


def load_history():
    _ensure()
    if not HISTORY_FILE.exists():
        return None
    return _read(HISTORY_FILE)


def save_history(arc_index, arc_title, ep_index, ep_title):
    _ensure()
    _write(HISTORY_FILE, {
        "arc_index": arc_index,
        "arc_title": arc_title,
        "ep_index": ep_index,
        "ep_title": ep_title,
    })


def load_cache():
    _ensure()
    if not CACHE_FILE.exists():
        return None
    return _read(CACHE_FILE)


def save_cache(arcs):
    _ensure()
    _write(CACHE_FILE, {"timestamp": time.time(), "arcs": arcs})


def _read(path):
    with open(path) as f:
        return json.load(f)


def _write(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
