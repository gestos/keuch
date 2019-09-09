echo "$BASH_SOURCE (no login shell?)"

echo "setting up aliases"
alias calcurse='LC_ALL=de_DE.ISO8859-1 calcurse'
alias ls='ls -l --color=auto --group-directories -h'
alias ppstree='pstree -p'
alias evime='vim -u ~/.vimcryp -x'
alias cal='cal -Nwy'

echo "set xkb map to de for umlauts"
setxkbmap de

echo "set up terminal prompt colors"
export PS1='\[\033k\033\\\]\[\e[0;34m\]\u\[\e[0m\]@\[\e[1;30m\]\h:\[\e[0m\]\w\$ '
if [ "$TERM" == "xterm" ]; then
	export TERM=xterm-256color
fi

echo "read dircolors for ls colors from $HOME/.dir_colors"
eval "$(dircolors -b ~/.dir_colors)"
