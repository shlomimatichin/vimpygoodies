vimpygoodies - shlomps code transformations as a vim plugin
===========================================================

Features include:
-----------------
* ci - column indent - for table formatting of function calls (c++/py)
* cra - constructor reference arguments - copy parameters passed to __init__ to self._ or c++ constructor to private
* nf - new file - template for new header file in c++.
* pj - format json
* py - format yaml

Usage:
------
:<range>Goodies ci

Setting your work environment:
------------------------------

install vim's buffer explorer, vimgo
~~~ sh
sudo apt-get install -y vim-gnome vim-pathogen git python-yaml python-simplejson pep8 exuberant-ctags 

cd /tmp
git clone https://github.com/tpope/vim-pathogen
mkdir -p ~/.vim/bundle
mkdir -p ~/.vim/plugin
mv vim-pathogen/autoload ~/.vim
cat > ~/.vimrc << 'EOF'
execute pathogen#infect()
syntax on
filetype plugin indent on

set tabstop=4
set shiftwidth=4
set autoindent
set incsearch
set expandtab
set hlsearch
set encoding=utf-8

map <C-j> :cn<CR>
map <C-k> :cp<CR>

map <C-h> :bp<CR>
map <C-l> :bn<CR>
map <M-Right> :bn
map <M-Left> :bp

map #8 :tp
map #9 :tn

if has("gui_running")
	colorscheme darkblue
	set guifont=Monospace\ 18
endif
command TinyFont :set guifont=Monospace\ 12
command SmallFont :set guifont=Monospace\ 14
command LargeFont :set guifont=Monospace\ 18

if !empty($VIMMAKEPRG)
    set makeprg=$VIMMAKEPRG
endif
EOF
## MAC: change Monospace\ 18 to Menlo:h24
cat > ~/.vim/plugin/togglecomment.vim << 'EOF'
function ToggleComment()
        let bufferName = bufname( "%" )
        if bufferName =~ "[.]h$" || bufferName =~ "[.]cpp$" || bufferName =~ "[.]c$" || bufferName =~ "[.]js$" || bufferName =~ "[.]html$" || bufferName =~ "[.]go$"
                let commentSign = "//"
                let uncommentAction = "0xx"
        else
                let commentSign = "#"
                let uncommentAction = "0x"
        endif
        let line = getline( "." )
        if line[ 0 ] == commentSign || line[ 0 : 1 ] == commentSign
                execute "normal " . uncommentAction
        else
                execute "normal " . "0i" . commentSign
        endif
endfunction

map co :call ToggleComment() <CR>
EOF
cd ~/.vim/bundle
git clone https://github.com/scrooloose/syntastic.git
git clone https://github.com/godlygeek/tabular.git
git clone https://github.com/fatih/vim-go.git
git clone https://github.com/shlomimatichin/vimpygoodies.git
git clone https://github.com/tpope/vim-vinegar.git
#git clone https://github.com/corntrace/bufexplorer
git clone https://github.com/jlanzarotta/bufexplorer.git
git clone https://github.com/junegunn/fzf
~~~

MAC setup:
----------
Turn on filevault (security)
Turn on ssh (sharing)
Increase keyboard key repeat rate to maximum
install MacVim http://macvim-dev.github.io/macvim/
~~~ sh
cat > ~/vim.sh << 'EOF'
#!/bin/sh
/Applications/MacVim.app/Contents/MacOS/MacVim $@ &
EOF
chmod 755 ~/vim.sh
~~~
