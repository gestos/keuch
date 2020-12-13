execute pathogen#infect()
set term=xterm-256color		" we're on a color terminal
syntax on			" we want syntax_highlighting
set nu				" show lines (column to the left)
set t_ut=			" clear the terminalbackground on start - see http://sunaku.github.io/vim-256color-bce.html
filetype plugin indent on	" use plugins, or so i guess
set omnifunc=syntaxcomplete#Complete
set tabstop=2		" while in edit mode, tab is 2 chars wide
set shiftwidth=2		" same is true for identation of lines and blocks
set mouse=a			" mousescrolling and copying without linenumbers
set nowrap			" no linewrapping as starting default mode
set nofixendofline
set noeol
set binary

au BufNewFile,BufRead * if &ft == '' | set ft=sh | endif  " unknown filetypes will be recognized and highlighted as "sh" files
let mapleader=" "
nmap <leader><Right> :bnext<CR>
nmap <leader><Left> :bprevious<CR>
nmap <leader>t :NERDTreeToggle<CR>
nmap <leader>e :Explore<CR>
set hidden
autocmd BufWinLeave ?* mkview 1	" save the folds when leaving vim
autocmd BufWinEnter ?* silent loadview 1 " load folds on start

command Trailclean %s:\s\+$::
command! -nargs=* -complete=shellcmd Pexec execute "below new | 0read ! python # <args>"
command! -nargs=* -complete=shellcmd Rsplit execute "new | setlocal buftype=nofile bufhidden=hide noswapfile | r! <args>"

" air-line
let g:airline_powerline_fonts = 1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#fnamemod = ':t'
if !exists('g:airline_symbols')
	let g:airline_symbols = {}
endif

"unicode symbols
let g:airline_left_sep = '»'
let g:airline_right_sep = '«'
let g:airline_symbols.linenr = '|'
let g:airline_symbols.branch = '<'
let g:airline_symbols.paste = 'ρ'
let g:airline_symbols.paste = 'Þ'
let g:airline_symbols.paste = '>'
let g:airline_symbols.whitespace = 'Ξ'
let g:airline_symbols.maxlinenr = '|'
" airline symbols
"let g:airline_left_sep = ''
"let g:airline_left_alt_sep = ''
"let g:airline_right_sep = ''
"let g:airline_right_alt_sep = ''
"let g:airline_symbols.branch = ''
"let g:airline_symbols.readonly = ''
"let g:airline_symbols.linenr = '
"set laststatus=2		" always show the statusline ; not needed cause of airline

set guifont=DejaVu\ Sans:s10

set foldcolumn=3
set foldmethod=manual
colo gesterich
