export PS1='\[\033k\033\\\]\[\e[0;34m\]\u\[\e[0m\]@\[\e[1;30m\]\h:\[\e[0m\]\w\$ '
alias calcurse='LC_ALL=de_DE.ISO8859-1 calcurse'
alias ls='ls -l --color=auto --group-directories -h'
alias ppstree='pstree -p'
alias evime='vim -u ~/.vimcryp -x'
# alias urxvt='urxvt -pe tabbed'
########## funktion
#function settitle() {
#	if [ -n "$STY" ]; then
#	echo "Setting screen titles to $@"
#	printf "\033k%s\033\\" "$@"
#	screen -X eval "at\\# title $@" "shelltitle $@"
#	else
#	printf "\033]0;%s\007" "$@"
#	fi
#	}
alias cal='cal -Nwy'
echo $(pwd)/"$BASH_SOURCE"
#env > /home/keuch/env_bashrc

export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting
export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*

if [ "$TERM" == "xterm" ]; then
	# No it isn't, it's gnome-terminal
	export TERM=xterm-256color
fi
if [ "$TERM" == "screen" ]; then
	# No it isn't, it's gnome-terminal
	export TERM=screen-256color
fi
