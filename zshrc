export ZSH=~/.oh-my-zsh

plugins=(colored-man-pages colorize compleat git github
         history history-substring-search screen)

REPORTTIME=10

setopt notify
setopt completeinword
setopt prompt_subst

autoload -U compinit #promptinit bashcompinit
compinit
#promptinit
#bashcompinit

zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion::complete:*' use-cache 1

PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/X11/bin:/usr/local/git/bin:/usr/texbin:$PATH

source $ZSH/oh-my-zsh.sh

# Load dot files
source ~/.zsh_aliases
source ~/.zsh_prompt

# OPAM configuration
export PATH=/home/trustinsoft/prefix/opam/bin:$PATH
export OPAMROOT=/home/trustinsoft/prefix/opam/root
. /home/trustinsoft/prefix/opam/root/opam-init/init.sh > /dev/null 2> /dev/null || true
export LANG=en_US
