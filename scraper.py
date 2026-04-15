import re
import time

import requests

EPISODES_URL = "https://raw.githubusercontent.com/DendyLusus/one-pace-map/main/data/episodes.json"


def fetch_arcs(cache_hours=24, force_refresh=False):
    from config import load_cache, save_cache

    if not force_refresh:
        cached = load_cache()
        if cached:
            age_hours = (time.time() - cached["timestamp"]) / 3600
            if age_hours < cache_hours:
                return cached["arcs"]

    response = requests.get(EPISODES_URL, timeout=15)
    response.raise_for_status()

    arcs = _parse(response.json())
    save_cache(arcs)
    return arcs


def _parse(data):
    arcs = []

    for entry in data:
        episodes = entry.get("episodes", [])
        if not episodes:
            continue

        parsed_eps = [_parse_episode(ep) for ep in episodes]

        arcs.append({
            "title": entry["title"],
            "language": _language_label(entry.get("sub", ""), entry.get("dub", "")),
            "anime_range": _arc_anime_range(parsed_eps),
            "episodes": parsed_eps,
        })

    return arcs


def _parse_episode(ep):
    anime_eps = _extract_anime_eps(ep["file_name"])
    if anime_eps:
        label = f"ep {anime_eps}"
    else:
        label = ""

    return {
        "title": f"Episode {ep['episode_num']}",
        "anime_eps": label,
        "stream_url": ep["url"],
    }


def _extract_anime_eps(file_name):
    match = re.search(r"\[One Pace\]\[([0-9]+(?:-[0-9]+)?)\]", file_name)
    if match:
        return match.group(1)
    return ""


def _arc_anime_range(episodes):
    nums = []
    for ep in episodes:
        for n in re.findall(r"\d+", ep.get("anime_eps", "")):
            nums.append(int(n))
    if not nums:
        return ""
    lo, hi = min(nums), max(nums)
    return f"anime {lo}" if lo == hi else f"anime {lo}-{hi}"


def _language_label(sub, dub):
    if dub == "en":
        return "Dubbed"
    if dub == "ja" and sub == "en":
        return "Subbed"
    if sub == "en":
        return "Subbed"
    return ""
