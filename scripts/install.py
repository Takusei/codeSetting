#!/usr/bin/env python3
"""Preview or install selected configurations using backed-up symlinks."""

import argparse
from datetime import datetime
import os
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[1]


def destinations(home, config, platform):
    vscode = (
        home / "Library/Application Support/Code/User/settings.json"
        if platform == "darwin"
        else config / "Code/User/settings.json"
    )
    return {
        "shell": (REPO / "shell/zshrc", home / ".zshrc"),
        "nvim": (REPO / "nvim", config / "nvim"),
        "ghostty": (REPO / "ghostty/config", config / "ghostty/config"),
        "vscode": (REPO / "vscode/settings.json", vscode),
    }


def install_link(source, target, apply=False):
    if target.is_symlink() and target.resolve() == source.resolve():
        print(f"Already linked: {target}")
        return
    if not source.exists():
        raise FileNotFoundError(f"Missing source: {source}")
    # Do not move a directory containing the checkout itself.
    if target.is_dir() and not target.is_symlink() and source.resolve().is_relative_to(target.resolve()):
        raise ValueError(f"Destination contains the source checkout: {target}")
    backup = None
    if os.path.lexists(target):
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = target.with_name(f"{target.name}.backup-{stamp}")
        while os.path.lexists(backup):
            backup = backup.with_name(backup.name + "-1")
        print(f"Backup: {target} -> {backup}")
    print(f"Link: {target} -> {source}")
    if not apply:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if backup is not None:
        target.rename(backup)
    try:
        target.symlink_to(source, target_is_directory=source.is_dir())
    except OSError:
        if backup is not None:
            backup.rename(target)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("components", nargs="*", help="shell, nvim, ghostty, vscode (default: shell nvim ghostty)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Apply changes; existing destinations are backed up")
    mode.add_argument("--dry-run", action="store_true", help="Preview only (the default)")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Alternate home for testing or staging")
    args = parser.parse_args()
    if sys.platform not in ("darwin", "linux"):
        parser.error("This installer supports macOS and Linux (including WSL). See README for Windows.")
    home = args.home.expanduser().absolute()
    # An alternate home must not accidentally use the real user's XDG directory.
    config = home / ".config"
    if home == Path.home() and os.environ.get("XDG_CONFIG_HOME"):
        config = Path(os.environ["XDG_CONFIG_HOME"])
        if not config.is_absolute():
            parser.error("XDG_CONFIG_HOME must be absolute")
    mapping = destinations(home, config, sys.platform)
    components = args.components or ["shell", "nvim", "ghostty"]
    unknown = set(components) - mapping.keys()
    if unknown:
        parser.error(f"Unknown components: {', '.join(sorted(unknown))}")
    if not args.apply:
        print("Preview only. Run with --apply to make these changes.")
    for component in dict.fromkeys(components):
        install_link(*mapping[component], apply=args.apply)


if __name__ == "__main__":
    main()
