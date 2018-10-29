import vim


class Tab:
    def __init__(self):
        self._tabstop = int(vim.eval("&tabstop"))
        self._shiftwidth = int(vim.eval("&shiftwidth"))
        self._expandtab = int(vim.eval("&expandtab"))

    def roundUp(self, value):
        return ((int(value) + self._shiftwidth - 1) // self._shiftwidth) * self._shiftwidth

    def countChars(self, string):
        result = 0
        for c in string:
            if c == '\t':
                result = self.roundUp(result + 1)
            else:
                result += 1
        return result

    def produce(self, size, tab=False, roundUp=False):
        if tab:
            size *= self._shiftwidth
        if roundUp:
            size = self.roundUp(size)
        if self._expandtab:
            return ' ' * size
        else:
            return '\t' * (size / self._shiftwidth)
