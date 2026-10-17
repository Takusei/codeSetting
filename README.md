# codeSetting

This repo contains settings for VS Code, oh-my-zsh, Ghostty, and Neovim (LazyVim) to keep them consistent across devices.

Some of the .zshrc refer to this doc:
https://vicfree.com/2023/02/install-zsh-in-git-bash-for-windows/

## Neovim / LazyVim

`nvim/` is a backup of `~/.config/nvim`, including custom Lua settings and
`lazy-lock.json` (the recorded plugin versions). Installed plugins and caches
are not included.

Custom settings include the Dracula theme, mouse support, the system clipboard,
absolute line numbers, and two-space indentation.

To restore, run these commands from this repository's root. Any existing config
is moved to a timestamped backup first:

```sh
mkdir -p ~/.config
if [ -e ~/.config/nvim ] || [ -L ~/.config/nvim ]; then
  mv ~/.config/nvim ~/.config/nvim.backup-$(date +%Y%m%d-%H%M%S)
fi
cp -R nvim ~/.config/nvim
nvim
```

Neovim and Git must be installed. The first launch downloads missing plugins;
run `:Lazy restore` to restore the versions recorded in the lockfile.

To refresh this backup after changing your local settings, run from the repo root:

```sh
rsync -av --delete --exclude='.git/' ~/.config/nvim/ nvim/
```

This replaces the repository's `nvim/` contents with your current local config.
Review `git diff` and `git status` before committing.
