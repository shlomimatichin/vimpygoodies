import vim
import re
import os
from codetools import constructorreferenceargumentscpp
from codetools import constructorreferenceargumentspy
import vimrange


def constructorReferencesArguments(*args):
    range = vimrange.VimRange(*args)
    filename = vim.current.buffer.name
    fileType = os.path.splitext(filename)[1].lower()
    if fileType in ['.h', '.hpp', '.hxx', '.c', '.cpp', '.cxx']:
        instance = constructorreferenceargumentscpp.ConstructorReferenceArgumentsCPP(range.content())
        range.append(instance.format().rstrip())
    if fileType in ['.py']:
        instance = constructorreferenceargumentspy.ConstructorReferenceArgumentsPy(range.content())
        range.append(instance.format().rstrip())
    else:
        raise Exception("Unknown file type: '%s' => '%s'" % (filename, fileType))


aliases = dict(
    constructorReferencesArguments=constructorReferencesArguments,
    cra=constructorReferencesArguments,
)
