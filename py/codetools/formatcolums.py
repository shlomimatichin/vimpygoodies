import re
from . import tab


class FormatColums:
    def __init__(self, parse, maximumLineLength=109,
                 alwaysNewLineForFirstParameter=False, minimumSpaceBetweenColumns=2):
        self._parse = parse
        self._maximumLineLength = maximumLineLength
        self._alwaysNewLineForFirstParameter = alwaysNewLineForFirstParameter
        self._minimumSpaceBetweenColumns = minimumSpaceBetweenColumns
        self._tab = tab.Tab()
        self._lines = self._toLines(parse.rows())
        self._lead = parse.lead()
        self._indentationCharacters = self._tab.countChars(self._lead)
        if not self._lead.isspace():
            mustAddNewLine = self._alwaysNewLineForFirstParameter
            if self._indentationCharacters + self._longestLine() > self._maximumLineLength:
                mustAddNewLine = True
                self._indentationCharacters = self._maximumLineLength - self._tab.roundUp(self._longestLine)
                if self._indentationCharacters < self._minimumIndentation():
                    self._indentationCharacters = self._minimumIndentation()
            if mustAddNewLine:
                self._lead + '\n' + self._indentation()
            else:
                assert self._indentationCharacters >= self._tab.countChars(self._lead)
                self._lead += ' ' * (self._indentationCharacters - self._tab.countChars(self._lead))

    def format(self):
        return self._lead + ('\n' + self._indentation()).join(self._lines) + self._parse.tail()

    def _minimumIndentation(self):
        assert not self._lead.isspace()
        spacePrefix = re.match(r'(\s*)', self._lead).group(0)
        return self._tab.countChars(spacePrefix + '\t')

    def _indentation(self):
        return self._tab.produce(self._indentationCharacters)

    def _longestLine(self):
        return max(len(l) for l in self._lines)

    def _toLines(self, rows):
        if len(rows[0]) == 1:
            return [r[0] for r in rows]
        else:
            return self._twoColumnsToLines(rows)

    def _twoColumnsToLines(self, rows):
        assert len(rows[0]) == 2
        maxLengthFirstColumn = max(len(r[0]) for r in rows)
        firstColumSize = maxLengthFirstColumn + self._minimumSpaceBetweenColumns
        return [r[0] + ' ' * (firstColumSize - len(r[0])) + r[1] for r in rows]
