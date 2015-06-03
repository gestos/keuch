execute pathogen#infect()
set term=xterm-256color		" we're on a color terminal
colo getafe			" we like this colorscheme_
syntax on			" we want syntax_highlighting
set nu				" show lines (column to the left)
set t_ut=			" clear the terminalbackground on start - see http://sunaku.github.io/vim-256color-bce.html
filetype plugin indent on	" use plugins, or so i guess
set omnifunc=syntaxcomplete#Complete
set softtabstop=2		" while in edit mode, tab is 2 chars wide
set shiftwidth=2		" same is true for identation of lines and blocks

au BufNewFile,BufRead * if &ft == '' | set ft=sh | endif  " unknown filetypes will be recognized and highlighted as "sh" files
let mapleader = " "
nmap <leader><space> :bnext<CR>
set hidden



let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#fnamemod = ':t'
set laststatus=2		" always show the statusline ; not needed cause of airline





" set statusline=%F%=%l,%c	; show filename, line numbers and character position ; not needed cause of airline
