function! VimPyGoodies(...)
    python argv = []
    python import vim
    for anArg in a:000
        python argv.append(vim.eval("anArg"))
    endfor
    pyfile $HOME/.vim/bundle/vimpygoodies/py/main.py
endfunction

command -range -nargs=+ Goodies call VimPyGoodies(<f-args>)
