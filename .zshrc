# This is the zsh configuration without oh-my-zsh, using zsh plugins and custom settings.
# History configurations
# https://manpages.debian.org/bullseye/zsh-common/zshparam.1.en.html
HISTFILE=~/.zsh-history
HISTSIZE=1000
SAVEHIST=2000
HISTORY_IGNORE='(history*|h|ls|ll|la|l|cd|pwd|exit|cd ..)'
# configure key keybindings
# https://manpages.debian.org/bullseye/zsh-common/zshzle.1.en.html
bindkey -e                                        # emacs key bindings
bindkey ' ' magic-space                           # do history expansion on space
bindkey '^U' backward-kill-line                   # ctrl + U
bindkey '^[[3;5~' kill-word                       # ctrl + Supr
bindkey '^[[3~' delete-char                       # delete
bindkey '^[[1;5C' forward-word                    # ctrl + ->
bindkey '^[[1;5D' backward-word                   # ctrl + <-
bindkey '^[[5~' beginning-of-buffer-or-history    # page up
bindkey '^[[6~' end-of-buffer-or-history          # page down
bindkey '^[[H' beginning-of-line                  # home
bindkey '^[[F' end-of-line                        # end
bindkey '^[[Z' undo                               # shift + tab undo last action

# zsh options, case insensitive and underscores are ignored
# https://zsh.sourceforge.io/Doc/Release/Options.html
#setopt APPEND_HISTORY      # append their history list to the history file, rather than replace it.
setopt INC_APPEND_HISTORY   # history lines are added to the $HISTFILE incrementally
setopt HIST_FCNTL_LOCK      # add zsh history file lock avoid corruption
setopt HIST_IGNORE_ALL_DUPS # history list duplicates an older one, the older command is removed from the list
# setopt hist_ignore_dups   # ignore duplicated commands history list
setopt HIST_IGNORE_SPACE    # ignore commands that start with space
setopt HIST_VERIFY          # show command with history expansion to user before running it
setopt AUTO_CD              # change directory just by typing its name
setopt INTERACTIVE_COMMENTS # allow comments in interactive mode
setopt NUMERIC_GLOB_SORT    # sort filenames numerically when it makes sense
setopt PROMPT_SUBST         # prompt extend function, for git branch display

# xterm set the title
# \033=\e, \007=\a, \012=\n, \015=\r, https://manpages.debian.org/bullseye/manpages/ascii.7.en.html
# https://manpages.debian.org/bullseye/xterm/xterm.1.en.html
# https://web.archive.org/web/20221206072000/https://tldp.org/HOWTO/Xterm-Title-4.html
case $TERM in xterm*)
    precmd () {print -Pn "\e]0;%~\a"}
    ;;
esac

# --- Git branch display function ---
function git_prompt_info {
  if git rev-parse --is-inside-work-tree &>/dev/null; then
    local branch=$(git symbolic-ref --short HEAD 2>/dev/null)
    local dirty=$(git status --porcelain 2>/dev/null)
    [[ -n $dirty ]] && echo "%F{yellow}$branch*%f " || echo "%F{green}$branch%f "
  fi
}

# --- Right prompt: Time (HH:MM:SS) ---
RPROMPT='%F{magenta}%*%f'

# --- Left prompt: Path + Git + Fancy Arrow ---
PROMPT='%F{cyan}%~%f $(git_prompt_info) %F{green}❯%f '


# enable color support of ls, less and man, and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    export LS_COLORS="$LS_COLORS:ow=30;44:" # fix ls color for folders with 777 permissions

    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
    alias diff='diff --color=auto'
    alias ip='ip --color=auto'

    export LESS_TERMCAP_mb=$'\E[1;31m'     # begin blink
    export LESS_TERMCAP_md=$'\E[1;36m'     # begin bold
    export LESS_TERMCAP_me=$'\E[0m'        # reset bold/blink
    export LESS_TERMCAP_so=$'\E[01;33m'    # begin reverse video
    export LESS_TERMCAP_se=$'\E[0m'        # reset reverse video
    export LESS_TERMCAP_us=$'\E[1;32m'     # begin underline
    export LESS_TERMCAP_ue=$'\E[0m'        # reset underline

    # Take advantage of $LS_COLORS for completion as well
    zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
    zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
fi

# some useful aliases
alias ll='ls -laFh'
alias la='ls -A'
alias l='ls -AF1'
alias pwd='pwd -W'

# be paranoid
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

function extract () {
   if [ -f $1 ] ; then
       case $1 in
           *.tar.bz2)   tar xvjf $1    ;;
           *.tar.gz)    tar xvzf $1    ;;
           *.bz2)       bunzip2 $1     ;;
           *.rar)       unrar x $1     ;;
           *.gz)        gunzip $1      ;;
           *.tar)       tar xvf $1     ;;
           *.tbz2)      tar xvjf $1    ;;
           *.tgz)       tar xvzf $1    ;;
           *.zip)       unzip $1       ;;
           *.Z)         uncompress $1  ;;
           *.7z)        7z x $1        ;;
           *)           echo "don't know how to extract '$1'..." ;;
       esac
   else
       echo "'$1' is not a valid file!"
   fi
 }


# enable syntax-highlighting
# if [ -f ~/workspace/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
#     . ~//workspace/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
#     ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern)
#     ZSH_HIGHLIGHT_STYLES[default]=none
#     ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=white,underline
#     ZSH_HIGHLIGHT_STYLES[reserved-word]=fg=cyan,bold
#     ZSH_HIGHLIGHT_STYLES[suffix-alias]=fg=green,underline
#     ZSH_HIGHLIGHT_STYLES[global-alias]=fg=green,bold
#     ZSH_HIGHLIGHT_STYLES[precommand]=fg=green,underline
#     ZSH_HIGHLIGHT_STYLES[commandseparator]=fg=blue,bold
#     ZSH_HIGHLIGHT_STYLES[autodirectory]=fg=green,underline
#     ZSH_HIGHLIGHT_STYLES[path]=bold
#     ZSH_HIGHLIGHT_STYLES[path_pathseparator]=
#     ZSH_HIGHLIGHT_STYLES[path_prefix_pathseparator]=
#     ZSH_HIGHLIGHT_STYLES[globbing]=fg=blue,bold
#     ZSH_HIGHLIGHT_STYLES[history-expansion]=fg=blue,bold
#     ZSH_HIGHLIGHT_STYLES[command-substitution]=none
#     ZSH_HIGHLIGHT_STYLES[command-substitution-delimiter]=fg=magenta,bold
#     ZSH_HIGHLIGHT_STYLES[process-substitution]=none
#     ZSH_HIGHLIGHT_STYLES[process-substitution-delimiter]=fg=magenta,bold
#     ZSH_HIGHLIGHT_STYLES[single-hyphen-option]=fg=green
#     ZSH_HIGHLIGHT_STYLES[double-hyphen-option]=fg=green
#     ZSH_HIGHLIGHT_STYLES[back-quoted-argument]=none
#     ZSH_HIGHLIGHT_STYLES[back-quoted-argument-delimiter]=fg=blue,bold
#     ZSH_HIGHLIGHT_STYLES[single-quoted-argument]=fg=yellow
#     ZSH_HIGHLIGHT_STYLES[double-quoted-argument]=fg=yellow
#     ZSH_HIGHLIGHT_STYLES[dollar-quoted-argument]=fg=yellow
#     ZSH_HIGHLIGHT_STYLES[rc-quote]=fg=magenta
#     ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]=fg=magenta,bold
#     ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]=fg=magenta,bold
#     ZSH_HIGHLIGHT_STYLES[back-dollar-quoted-argument]=fg=magenta,bold
#     ZSH_HIGHLIGHT_STYLES[assign]=none
#     ZSH_HIGHLIGHT_STYLES[redirection]=fg=blue,bold
#     ZSH_HIGHLIGHT_STYLES[comment]=fg=black,bold
#     ZSH_HIGHLIGHT_STYLES[named-fd]=none
#     ZSH_HIGHLIGHT_STYLES[numeric-fd]=none
#     ZSH_HIGHLIGHT_STYLES[arg0]=fg=cyan
#     ZSH_HIGHLIGHT_STYLES[bracket-error]=fg=red,bold
#     ZSH_HIGHLIGHT_STYLES[bracket-level-1]=fg=blue,bold
#     ZSH_HIGHLIGHT_STYLES[bracket-level-2]=fg=green,bold
#     ZSH_HIGHLIGHT_STYLES[bracket-level-3]=fg=magenta,bold
#     ZSH_HIGHLIGHT_STYLES[bracket-level-4]=fg=yellow,bold
#     ZSH_HIGHLIGHT_STYLES[bracket-level-5]=fg=cyan,bold
#     ZSH_HIGHLIGHT_STYLES[cursor-matchingbracket]=standout
# fi

# enable auto-suggestions based on the history
if [ -f ~/workspace/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
    . ~/workspace/zsh-autosuggestions/zsh-autosuggestions.zsh
    # change suggestion color
    ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#9e9e9e'
fi
# enable extend completion
fpath=(~/workspace/zsh-completions/src $fpath)

# old way add funtion
#source ~/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/workspace/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
#source ~/zsh-completions/zsh-completions.plugin.zsh

# compinit https://manpages.debian.org/bullseye/zsh-common/zshcompsys.1.en.html
# zstyle https://manpages.debian.org/bullseye/zsh-common/zshmodules.1.en.html
zstyle :compinstall filename '~/.zshrc'
autoload -Uz compinit
compinit -d ~/.zcompdump

zstyle ':completion:*:*:*:*:*' menu select
zstyle ':completion:*' auto-description 'specify: %d'
zstyle ':completion:*' completer _expand _complete
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
zstyle ':completion:*' rehash true
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'