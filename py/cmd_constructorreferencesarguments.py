import vim
import re
import os
from codetools import constructorreferenceargumentscpp


def constructorReferencesArguments(*args):
    filename = vim.current.buffer.name
    fileType = os.path.splitext(filename)[1].lower()
    content = "\n".join(vim.current.range)
    if fileType in ['.h', '.hpp', '.hxx', '.c', '.cpp', '.cxx']:
        instance = constructorreferenceargumentscpp.ConstructorReferenceArgumentsCPP(content)
        vim.current.range.append(instance.format().rstrip().split("\n"))
    else:
        raise Exception("Unknown file type: '%s' => '%s'" % (filename, fileType))


aliases = dict(
    constructorReferencesArguments=constructorReferencesArguments,
    cra=constructorReferencesArguments,
)
