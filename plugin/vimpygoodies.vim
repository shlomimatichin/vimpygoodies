function! VimPyGoodies(...)
    python3 argv = []
    python3 import vim
    for anArg in a:000
        python3 argv.append(vim.eval("anArg"))
    endfor
    py3file $HOME/.vim/bundle/vimpygoodies/py/main.py
endfunction

command -range -nargs=+ Goodies call VimPyGoodies(<line1>,<line2>,<f-args>)
