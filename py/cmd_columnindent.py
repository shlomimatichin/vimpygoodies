import vim
import re
import os
from codetools import columnindentcpp
from codetools import columnindentpy
import vimrange


def columnIndent(*args):
    range = vimrange.VimRange(*args)
    filename = vim.current.buffer.name
    fileType = os.path.splitext(filename)[1].lower()
    if fileType in ['.h', '.hpp', '.hxx', '.c', '.cpp', '.cxx']:
        instance = columnindentcpp.ColumnIndentCPP(range.content())
        range.replace(instance.format())
    elif fileType in ['.py']:
        instance = columnindentpy.ColumnIndentPy(range.content())
        range.replace(instance.format())
    else:
        raise Exception("Unknown file type: '%s' => '%s'" % (filename, fileType))


aliases = dict(
    columnIndent=columnIndent,
    ci=columnIndent,
)
