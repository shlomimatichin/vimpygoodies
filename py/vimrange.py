import vim
import re


class VimRange:
    def __init__(self, line1, line2, *args):
        self._line1 = line1
        self._line2 = line2
        self._vimRange = line1 == line2

    def content(self):
        if self._vimRange:
            return "\n".join(vim.current.range)
        else:
            return "\n".join(vim.current.buffer[self._line1: self._line2 + 1])

    def append(self, content):
        asLines = content.rstrip().split("\n")
        if self._vimRange:
            newLines = vim.current.range[:] + asLines
            vim.current.range[:] = newLines
        else:
            vim.current.buffer[self._line2 + 1: self._line2 + 1] = asLines

    def replace(self, content):
        asLines = content.rstrip().split("\n")
        if self._vimRange:
            vim.current.range[:] = asLines
        else:
            vim.current.buffer[self._line1: self._line2 + 1] = asLines

    def currentWord(self):
        row, col = vim.current.window.cursor
        line = vim.current.buffer[row-1]
        right = re.match(r"\w+", line[col:]).group(0)
        left = re.search(r"\w*$", line[:col]).group(0)
        return left + right
