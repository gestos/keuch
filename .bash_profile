#if 		[ "$(tty)" = "/dev/tty1" ]; then
#			echo "start X"
#			startx
#			logout
#   
#elif 
#		[ "$(tty)" = "/dev/tty2" ]; then
#			screen
#			logout
#fi
setxkbmap de
echo "$HOME/.bash_prfile"


[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
export PS1='\[\033k\033\\\]\[\e[0;34m\]\u\[\e[0m\]@\[\e[1;30m\]\h:\[\e[0m\]\w\$ '
if [ "$TERM" == "xterm" ]; then
	# No it isn't, it's gnome-terminal
	export TERM=xterm-256color
fi
# if [ "$TERM" == "screen" ]; then
# 	# No it isn't, it's gnome-terminal
# 	export TERM=screen-256color
# fi
