# onepace-cli

A terminal interface for watching [One Pace](https://onepace.net) — the fan-edited One Piece version that cuts filler and matches the manga pacing.

Streams episodes directly in mpv from the terminal. Remembers where you left off.

## Requirements

- Python 3.8+
- [mpv](https://mpv.io/installation/)

## Installation

```sh
git clone https://github.com/benjemiin/onepace-cli.git
cd onepace-cli
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```sh
python .
```

```sh
python . --refresh   # force re-fetch episode list (bypasses 24h cache)
```

On first launch you'll pick an arc and episode. Next time you open it, you'll be asked if you want to resume from where you left off.

## Configuration

Config is stored at `~/.config/onepace/config.json` and is created automatically on first run.

| Key | Default | Description |
|-----|---------|-------------|
| `cache_hours` | `24` | How long to cache the episode list before re-fetching |
| `mpv_args` | `[]` | Extra arguments passed to mpv (e.g. `["--fullscreen"]`) |

## Data source

Episode data comes from [DendyLusus/one-pace-map](https://github.com/DendyLusus/one-pace-map) — a community-maintained JSON updated daily. Streams are hosted on pixeldrain.
