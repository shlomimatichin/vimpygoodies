from . import parsecppfunctionsignature
import re
from . import tab
from . import formatcolums
from . import parsecppmemberlist


class ConstructorReferenceArgumentsCPP:
    def __init__(self, input):
        self._input = input
        self._tab = tab.Tab()
        self._parse = parsecppfunctionsignature.ParseCPPFunctionSignature(input)

    def format(self):
        return self._formatInitializationList() + \
                self._indentation() + '{}\n\n' + \
                "private:\n" + \
                self._formatMembers()

    def _formatMembers(self):
        membersRaw = self._tab.produce(1, tab=True) + ";\n".join(r[0] + ' _' + r[1] for r in self._parse.argumentsTwoColumTable()) + ";\n"
        parse = parsecppmemberlist.ParseCPPMemberList(membersRaw);
        return formatcolums.FormatColums(parse).format()

    def _indentation(self, add = ""):
        spacePrefix = re.match(r"\s*", self._input).group(0)
        return self._tab.produce(self._tab.countChars(spacePrefix + add), roundUp=True)

    def _formatInitializationList(self):
        return ",\n".join(self._indentation('\t') + "_%s(%s)" % (p, p) for p in self._parameters()) + '\n'

    def _parameters(self):
        return [re.search(r"\w+", r[1]).group(0) for r in self._parse.rows()]
