#!/usr/bin/env python3
"""Install the Oh My Zsh dependencies used by shell/zshrc (preview by default)."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


# Paths match shell/zshrc. The git plugin is bundled with Oh My Zsh.
REPOSITORIES = (
    ("ohmyzsh/ohmyzsh", "", "oh-my-zsh.sh"),
    ("romkatv/powerlevel10k", "custom/themes/powerlevel10k", "powerlevel10k.zsh-theme"),
    ("zsh-users/zsh-autosuggestions", "custom/plugins/zsh-autosuggestions", "zsh-autosuggestions.plugin.zsh"),
    ("zsh-users/zsh-syntax-highlighting", "custom/plugins/zsh-syntax-highlighting", "zsh-syntax-highlighting.plugin.zsh"),
    ("MichaelAquilina/zsh-you-should-use", "custom/plugins/you-should-use", "you-should-use.plugin.zsh"),
    ("fdellwing/zsh-bat", "custom/plugins/zsh-bat", "zsh-bat.plugin.zsh"),
)


def needs_install(target, marker):
    if not os.path.lexists(target):
        return True
    if not (target / marker).is_file():
        raise ValueError(f"Existing destination lacks {marker}: {target}. Inspect it manually; nothing was overwritten.")
    return False


def install_repository(repository, target, marker, apply=False):
    if not needs_install(target, marker):
        print(f"Already installed (kept unchanged): {target}")
        return
    url = f"https://github.com/{repository}.git"
    print(f"Clone: {url} -> {target}", flush=True)
    if not apply:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    # Failed downloads leave no incomplete installation at the destination.
    with tempfile.TemporaryDirectory(prefix=".shell-install-", dir=target.parent) as temporary:
        staging = Path(temporary) / "checkout"
        subprocess.run(["git", "clone", "--depth=1", "--", url, str(staging)], check=True)
        if not (staging / marker).is_file():
            raise ValueError(f"Downloaded {repository} is missing {marker}")
        if os.path.lexists(target):
            raise ValueError(f"Destination appeared during download: {target}")
        staging.rename(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Download missing dependencies")
    mode.add_argument("--dry-run", action="store_true", help="Preview only (default)")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Alternate home for staging")
    parser.add_argument("--brew-tools", action="store_true", help="Also install missing bat/eza using an existing Homebrew")
    args = parser.parse_args()
    if sys.platform not in ("darwin", "linux"):
        parser.error("Supports macOS and Linux (including WSL).")
    if args.apply and not shutil.which("git"):
        parser.error("Install Git first, then rerun this script.")
    missing_tools = [name for name in ("bat", "eza") if not shutil.which(name)]
    if args.brew_tools and args.apply and missing_tools and not shutil.which("brew"):
        parser.error("--brew-tools requires Homebrew on PATH.")
    root = args.home.expanduser().absolute() / ".oh-my-zsh"
    if not args.apply:
        print("Preview only. Run with --apply to install.")
    try:
        # Detect conflicting existing paths before downloading anything.
        for _, relative, marker in REPOSITORIES:
            needs_install(root / relative, marker)
        if missing_tools:
            if args.brew_tools:
                print(f"Run: brew install {' '.join(missing_tools)}", flush=True)
                if args.apply:
                    subprocess.run(["brew", "install", *missing_tools], check=True)
            else:
                print(f"Install with your package manager: {', '.join(missing_tools)} (or use --brew-tools).")
        for repository, relative, marker in REPOSITORIES:
            install_repository(repository, root / relative, marker, args.apply)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1
    print("Next: link shell/zshrc with python3 scripts/install.py shell --apply.")
    print("Then open Zsh and run p10k configure. Select a Nerd Font in your terminal.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
