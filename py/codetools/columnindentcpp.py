from . import parsecpp
from . import parsecppmemberlist
from . import parsesimplecall
from . import parsecppfunctionsignature
from . import formatcolums


class ColumnIndentCPP:
    def __init__(self, content):
        classify = parsecpp.Classification(content)
        if classify.memberList():
            self._parse = parsecppmemberlist.ParseCPPMemberList(content)
        elif content.rstrip().endswith(';'):
            #guess: ends with ; is a call, not a declaration
            self._parse = parsesimplecall.ParseSimpleCall(content)
        else:
            self._parse = parsecppfunctionsignature.ParseCPPFunctionSignature(content)

    def format(self):
        return formatcolums.FormatColums(self._parse).format()
