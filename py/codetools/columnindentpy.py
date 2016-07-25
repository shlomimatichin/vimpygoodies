from . import parsesimplecall
import re
from . import tab


class ColumnIndentPy:
    def __init__(self, input, maximumLineLength=109):
        self._input = input
        self._maximumLineLength = maximumLineLength
        self._tab = tab.Tab()
        self._parse = parsesimplecall.ParseSimpleCall(input)
        longestArg = max([r[0] for r in self._parse.rows()])
        self._firstArgOnSameLine = self._tab.countChars(self._parse.lead() + longestArg) <= self._maximumLineLength

    def format(self):
        if self._firstArgOnSameLine:
            return self._parse.lead() + \
                ("\n" + self._indentation()).join([r[0] for r in self._parse.rows()]) + \
                self._parse.tail()
        else:
            return self._parse.lead() + "\n" + self._indentation() + \
                ("\n" + self._indentation()).join([r[0] for r in self._parse.rows()]) + \
                self._parse.tail()

    def _indentation(self):
        if self._firstArgOnSameLine:
            size = self._tab.countChars(self._parse.lead())
        else:
            spacePrefix = re.match(r"\s*", self._input).group(0)
            size = self._tab.roundUp(self._tab.countChars(spacePrefix + '\t'))
        return self._tab.produce(size)
