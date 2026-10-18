# macOS-specific defaults.
if [[ ! -x /usr/bin/dircolors ]]; then
  alias ls='ls -G'
fi
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,time,command'
