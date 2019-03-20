import vim
import re
import os


def dirtyTrace(*args):
    lineNumber = vim.current.range.start
    filename = vim.current.buffer.name
    fileType = os.path.splitext(filename)[1].lower()
    indent = re.match(r"(\s*)\S", vim.current.buffer[lineNumber]).group(1)
    if fileType in ['.py', '.pyx']:
        start = indent + "print('X'*100, "
        vim.current.buffer[lineNumber: lineNumber] = [
            "### DIRTY TRACE",
            start + ")",
            "### DIRTY TRACE END",
        ]
        vim.current.window.cursor = (lineNumber + 2, len(start))
    elif fileType in ['.h', '.hpp', '.hxx', '.c', '.cpp', '.cxx']:
        vim.current.buffer[lineNumber: lineNumber] = [
            "//// DIRTY TRACE",
            '''std::cerr << __FILE__ << ':' << __LINE__ << ": XXXX " << std::endl;''',
            "//// DIRTY TRACE END",
        ]
    else:
        raise Exception("Unknown file type: '%s' => '%s'" % (filename, fileType))


aliases = dict(
    dt=dirtyTrace,
    dirtyTrace=dirtyTrace,
    DirtyTrace=dirtyTrace,
    dirtytrace=dirtyTrace,
)
