# LazyVim Setup Guide (macOS + Ghostty)

For the complete restore workflow, start with the [repository README](../README.md).
The settings examples below explain customization; restoring the repo already
provides its saved options. The Ghostty snippet is minimal; `ghostty/config` is
the authoritative configuration.

## 1. Install Homebrew

Check whether Homebrew is installed:

```bash
brew --version
```

If it isn't installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the instructions printed by Homebrew to add it to your `PATH`.

## 2. Install Ghostty and Nerd Font

```bash
brew install --cask ghostty
brew install --cask font-jetbrains-mono-nerd-font
```

In Ghostty, open `~/.config/ghostty/config` and add:

```ini
# === 字体 ===
font-family = JetBrainsMono Nerd Font Mono
font-size = 14

# === 主题 ===
theme = Dracula

# === 启动目录 ===
working-directory = ~/workspace
```

Create the workspace:

```bash
mkdir -p ~/workspace
```

## 3. Install Neovim and dependencies

```bash
brew install neovim git ripgrep fd fzf lazygit tree-sitter-cli
```

Install Xcode Command Line Tools if necessary:

```bash
xcode-select --install
```

Check the installation:

```bash
nvim --version
rg --version
fd --version
lazygit --version
```

## 4. Restore this repository's LazyVim configuration

From the repository root, preview and apply:

```sh
python3 scripts/install.py nvim --dry-run
python3 scripts/install.py nvim --apply
```

Existing configuration is backed up automatically. This links the saved config,
including your custom options, theme and plugin lockfile. Do not clone a fresh
starter over this destination.

## 5. Launch LazyVim

```bash
cd ~/workspace
nvim .
```

On the first launch, wait for the plugins to finish installing. Run `:Lazy restore`
to restore the versions recorded in the saved lockfile.

Run the health checks inside Neovim:

```vim
:checkhealth
:LazyHealth
```

## 6. Basic Vim commands

| Shortcut | Action |
|---|---|
| `i` | Enter Insert mode |
| `Esc` | Return to Normal mode |
| `h/j/k/l` | Move left/down/up/right |
| `dd` | Delete a line |
| `yy` | Copy a line |
| `p` | Paste |
| `u` | Undo |
| `Ctrl+r` | Redo |
| `gg` | Jump to first line |
| `G` | Jump to last line |
| `:w` | Save |
| `:q` | Quit current window |
| `:qa` | Quit Neovim |
| `:qa!` | Quit without saving changes |
| `:wqa` | Save all and quit |

To cancel the most recent insert operation, press `Esc`, then `u`.

## 7. LazyVim shortcuts

The default leader key is `Space`.

| Shortcut | Action |
|---|---|
| `Space Space` | Find files |
| `Space e` | Toggle file explorer |
| `Space /` | Search text in project |
| `Space ,` | Switch buffers |
| `Space g g` | Open LazyGit |
| `Space c f` | Format code |
| `Space c r` | Rename symbol |
| `gd` | Go to definition |
| `Space q q` | Quit LazyVim |

Some actions require an active language server or the relevant plugin.

## 8. Mouse support (already configured)

Edit:

```bash
nvim ~/.config/nvim/lua/config/options.lua
```

Add:

```lua
-- === 鼠标支持 ===
vim.opt.mouse = "a"

-- === 系统剪贴板 ===
vim.opt.clipboard = "unnamedplus"

-- === 行号 ===
vim.opt.number = true
vim.opt.relativenumber = false
```

Save and restart Neovim.

## 9. Dracula theme reference

The saved config already includes Dracula. The following is an alternative
configuration example, not a required restore step:

```bash
mkdir -p ~/.config/nvim/lua/plugins
nvim ~/.config/nvim/lua/plugins/dracula.lua
```

Add:

```lua
return {
  {
    "Mofiqul/dracula.nvim",
    lazy = false,
    priority = 1000,
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "dracula",
    },
  },
}
```

Restart Neovim and allow the plugin manager to install the theme.

## 10. Test with a project

```bash
mkdir -p ~/workspace/lazyvim-test
cd ~/workspace/lazyvim-test

echo 'print("Hello LazyVim")' > main.py

nvim .
```

Open `main.py`, press `i` to edit, `Esc` to exit Insert mode, and `:w` to save.

## 11. Optional: Create a Zsh alias

Add to `~/.zshrc`:

```zsh
alias v="nvim"
```

Reload:

```bash
source ~/.zshrc
```

Now you can open a project with:

```bash
cd ~/workspace/my-project
v .
```

## 12. Troubleshooting

**Font icons appear broken**

Check the installed font name:

```bash
fc-list | grep -i JetBrains
```

On macOS, if `fc-list` is unavailable, use:

```bash
ghostty +list-fonts | grep -i JetBrains
```

**File search doesn't work**

Verify ripgrep and fd:

```bash
which rg
which fd
```

**Plugins fail to install**

Inside Neovim:

```vim
:Lazy
```

Use `:Lazy restore` to retry installation at the recorded versions.
Use sync only when you intentionally want to update plugins and the lockfile.

**File explorer disappeared**

Press `Space e` to reopen it.

**Need to learn Vim basics**

Run:

```bash
nvim +Tutor
```

## Official resources

- [Neovim](https://neovim.io/)
- [LazyVim Installation](https://www.lazyvim.org/installation)
- [LazyVim Keymaps](https://www.lazyvim.org/keymaps)
- [Ghostty](https://ghostty.org/)
- [Dracula Neovim](https://github.com/Mofiqul/dracula.nvim)
