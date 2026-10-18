# Personal settings

Shared settings for Zsh, Ghostty, Neovim (LazyVim), and VS Code across machines.
The checkout is the source of truth: the installer links supported configs to it.
Changes to linked files appear in `git diff`; review and commit them before pulling
on another machine. Keep this checkout in a stable location.

## Restore on macOS or Linux

Install Python 3.9+ and the applications you want to configure first. This installer
only manages config files. The separate shell dependency installer below installs
Oh My Zsh, its theme and plugins; other apps, fonts, and extensions need separate setup.
Native Windows / Git Bash installation is manual; WSL can use the Linux workflow.

From the repository root, preview the default components:

```sh
python3 scripts/install.py
```

Apply after reviewing the printed destinations:

```sh
python3 scripts/install.py --apply
```

The defaults are `shell nvim ghostty`. Select individual components if desired:

```sh
python3 scripts/install.py shell nvim --dry-run
python3 scripts/install.py shell nvim --apply
python3 scripts/install.py vscode --dry-run
python3 scripts/install.py vscode --apply
```

VS Code is opt-in because this replaces its entire user settings file, rather than
merging it. Close the relevant app before applying settings. On macOS, if Ghostty
already has a config under `~/Library/Application Support/com.mitchellh.ghostty/`,
review that file too so it does not conflict with the linked XDG config.

Existing files, directories, and even broken symlinks are moved to unique
`<name>.backup-<timestamp>` siblings. Already-correct links are skipped. A failed
link creation restores that component's backup; completed earlier components are
not rolled back. To undo, remove only the installed symlink and move its backup
back to the original name. If no backup existed, simply remove the symlink.

| Component | Source | Destination |
|---|---|---|
| Shell | `shell/zshrc` | `~/.zshrc` |
| Neovim | `nvim/` | `~/.config/nvim` |
| Ghostty | `ghostty/config` | `~/.config/ghostty/config` |
| VS Code, macOS | `vscode/settings.json` | `~/Library/Application Support/Code/User/settings.json` |
| VS Code, Linux | `vscode/settings.json` | `~/.config/Code/User/settings.json` |

The installer honors an absolute `XDG_CONFIG_HOME` for XDG destinations.
VS Code Insiders, named profiles, and portable installations require manual setup.

## Shell choices and local settings

`shell/zshrc` is the latest local macOS configuration, using Oh My Zsh and
Powerlevel10k. A commented-out literal API key was omitted, and optional
`~/.zshrc.local` loading was added for machine-only settings and credentials.

Install the shell dependencies before linking the config on a fresh machine:

```sh
# Preview (no downloads or changes)
python3 scripts/install_shell.py
# Install Oh My Zsh, Powerlevel10k, and all four external plugins
python3 scripts/install_shell.py --apply
# Or also install missing bat and eza through an existing Homebrew
python3 scripts/install_shell.py --apply --brew-tools
# Link the configuration, backing up any existing ~/.zshrc
python3 scripts/install.py shell --apply
```

Requires Python 3.9+, Git, Zsh, and network access to GitHub when applying.
The dependencies are [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh),
[Powerlevel10k](https://github.com/romkatv/powerlevel10k),
[zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions),
[zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting),
[you-should-use](https://github.com/MichaelAquilina/zsh-you-should-use), and
[zsh-bat](https://github.com/fdellwing/zsh-bat). The `git` plugin comes with Oh My Zsh.
The script uses `~/.oh-my-zsh/custom`, matching this repo's zshrc; custom `ZSH` or
`ZSH_CUSTOM` environment values are not used.

Existing installations are skipped without updating or replacing them. Conflicting
paths stop installation for manual review. Downloads are staged before being moved
into place; completed dependencies remain installed if a later download fails.
Rerun to finish. New clones use the current upstream default branch, not pinned
versions. The script does not change your login shell or replace `.zshrc`/`.p10k.zsh`.
`--home /path/to/temporary-home` stages dependencies elsewhere; `--brew-tools` still
installs tools through your system's Homebrew, so omit that flag for isolated staging.

Without Homebrew, install `bat` and `eza` through your OS package manager. Some Linux
packages name the executable `batcat`; zsh-bat needs `bat` on PATH. Optional Bun,
Docker, OpenClaw, and local environment initialization is skipped when absent;
these applications and asdf Java are not installed by this script.

Open a new Zsh session and run `p10k configure` to create `~/.p10k.zsh` (an existing
file is retained). For prompt icons, install and select a Nerd Font in your terminal;
see the [Powerlevel10k font instructions](https://github.com/romkatv/powerlevel10k#fonts).
`shell/legacy/p10k.zsh` remains an older reference, not an automatically installed preset.

Copy `shell/local.zsh.example` to `~/.zshrc.local` for machine-specific PATH entries
and credentials. Do not overwrite an existing local file.

`shell/macos.zsh` and `shell/linux.zsh` are retained helpers from the previous
portable setup; the current local snapshot does not load them. `shell/legacy/`
preserves the older Linux Oh My Zsh setup and Powerlevel10k settings as references.

## Application notes

- **Neovim:** install Neovim, Git, and the dependencies described in
  [the LazyVim guide](docs/lazyvim.md). First launch downloads plugins. Use
  `:Lazy restore` for recorded versions from `nvim/lazy-lock.json`, then
  `:checkhealth`. Keep the lockfile tracked. The unused starter example lives in
  `docs/reference/lazyvim-example.lua` and is not loaded.
- **Ghostty:** the saved config uses JetBrainsMono Nerd Font Mono and starts in
  `~/workspace`; install that font and create the directory. The current config
  contains macOS-specific appearance and keyboard preferences; review them before
  enabling Ghostty on Linux.
- **VS Code:** see [import and extension notes](vscode/README.md).
- **iTerm2:** see [legacy export notes](iterm2/README.md). Full session-state
  exports are not part of the automatic installation.

## Day-to-day workflow

Edit configs through their installed paths or directly in this checkout. Before
switching machines, review `git diff` and commit the settings you want to share.
On another machine, review its local changes before pulling. Do not run the old
`rsync --delete` backup command against a linked directory.

Do not commit `.env` files, tokens, private keys, local overrides, or new full-state
exports. `.gitignore` helps with accidental additions; it does not remove already
tracked files or content from Git history.

## Validate without touching your settings

```sh
zsh -n shell/zshrc
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/install.py --dry-run
python3 scripts/install_shell.py --dry-run
```

For an isolated installation, pass `--home /path/to/temporary-home`. This also
isolates XDG destinations from the real user's environment.
