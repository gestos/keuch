terminal colours for the 'ls' command (like e.g. the colour of directories or executables) can be customized.

Colours for 'ls' are defined in an environment variable called "$LS_COLORS". You can check its current contents with "echo $LS_COLORS".
Now if you like, you can change that variable yourself by exporting something like "export LS_COLORS=di=01;34:ln=01;36:ex=38;5;070". This would be just an example of how far I can grasp this myself: "di" for directories, "ex" for executables and so on.
However, the standard and much more convenient way is to evaluate the contents of /etc/DIR_COLORS where the colours for all possible kinds of file types are listed. Most of it is nicely explained here: http://unix.stackexchange.com/questions/94299/dircolors-modify-color-settings-globaly

Just the short way how I did mine:
1) cp /etc/DIR_COLORS ~/.config/my_dircolors   # of course you can choose this randomly
2) edit ~/.config/my_dircolors to your linking # 256 xterm-color chart is here http://upload.wikimedia.org/wikipedia/en/thumb/1/15/Xterm_256color_chart.svg/702px-Xterm_256color_chart.svg.png
3) eval "$(dircolors ~/.config/my_dircolors)" ; ls  # to see how they look
4) echo 'eval "$(dircolors ~/.config/my_dircolors)"' >> ~/.bashrc

and you're done

----

Sidenote: good vim syntax is "conf", as markdown uses ugly background colours for _thiskindofstuff_ and most of the more common syntaxes use the 'single quote for variable highlighting. conf is a very nice syntax!
