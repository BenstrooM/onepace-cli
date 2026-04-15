import sys
import argparse

import questionary
from rich.console import Console

import config
import scraper
import player

console = Console()

STYLE = questionary.Style([
    ("selected", "fg:cyan bold"),
    ("pointer", "fg:cyan bold"),
    ("highlighted", "fg:cyan"),
    ("answer", "fg:cyan bold"),
])


def _arc_label(arc):
    parts = [arc["title"]]
    if arc.get("language"):
        parts.append(f"[{arc['language']}]")
    if arc.get("anime_range"):
        parts.append(f"({arc['anime_range']})")
    return "  ".join(parts)


def _ep_label(ep):
    if ep.get("anime_eps"):
        return f"{ep['title']}  (original {ep['anime_eps']})"
    return ep["title"]


def main():
    parser = argparse.ArgumentParser(prog="onepace-cli")
    parser.add_argument("--refresh", action="store_true", help="Ignore cache and re-fetch episode list")
    args = parser.parse_args()

    console.print("\n[bold cyan]One Pace[/bold cyan]\n")

    cfg = config.load_config()

    console.print("[dim]Loading episodes...[/dim]", end="\r")
    try:
        arcs = scraper.fetch_arcs(
            cache_hours=cfg["cache_hours"],
            force_refresh=args.refresh,
        )
    except Exception as e:
        console.print(f"[red]Could not fetch episode list: {e}[/red]")
        sys.exit(1)
    console.print(" " * 30, end="\r")

    history = config.load_history()
    if history:
        label = f"{history['arc_title']} – {history['ep_title']}"
        resume = questionary.confirm(f"Resume from {label}?", style=STYLE).ask()
        if resume is None:
            sys.exit(0)
        if resume:
            _launch(arcs, history["arc_index"], history["ep_index"], cfg)
            return

    arc_i = questionary.select(
        "Select arc:",
        choices=[
            questionary.Choice(
                title=_arc_label(arc),
                value=i,
            )
            for i, arc in enumerate(arcs)
        ],
        style=STYLE,
    ).ask()

    if arc_i is None:
        sys.exit(0)

    ep_i = questionary.select(
        f"Select episode  (manga chapters not available in this dataset):",
        choices=[
            questionary.Choice(title=_ep_label(ep), value=j)
            for j, ep in enumerate(arcs[arc_i]["episodes"])
        ],
        style=STYLE,
    ).ask()

    if ep_i is None:
        sys.exit(0)

    _launch(arcs, arc_i, ep_i, cfg)


def _launch(arcs, arc_i, ep_i, cfg):
    arc = arcs[arc_i]
    ep = arc["episodes"][ep_i]

    console.print(f"\n[bold]{arc['title']}[/bold] – [bold]{ep['title']}[/bold]\n")
    config.save_history(arc_i, arc["title"], ep_i, ep["title"])
    player.play(ep["stream_url"], cfg.get("mpv_args", []))


if __name__ == "__main__":
    main()
