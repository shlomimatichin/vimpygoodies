import vim
import re
import os


def newFile(*args):
    currentContent = "".join(vim.current.buffer).strip()
    if currentContent != "":
        print "Buffer not empty, will not generate"
        return
    fileType = os.path.splitext(vim.current.buffer.name)[1]
    relative = vim.current.buffer.name[len(os.getcwd()) + len(os.path.sep):]
    relative = os.path.splitext(relative)[0]
    relativeParts = relative.split(os.path.sep)
    if relativeParts[0] in ["cpp", "py", "src", "js"]:
        relativeParts.pop(0)
    basename = relativeParts[-1]
    if fileType == ".h":
        vim.current.buffer[:] = _newHeaderFile(relativeParts)
    else:
        raise Exception("Unknown file type: '%s' => '%s'" % (vim.current.buffer.name, fileType))


aliases = dict(
    nf=newFile,
    newFile=newFile,
    NewFile=newFile,
    newfile=newFile,
)


def _makeWords(parts):
    result = []
    for part in parts:
        result += re.findall(r"[A-Z]+[^A-Z]*", part)
    return result

def _newHeaderFile(relativeParts):
    protectMacro = "__" + "_".join([w.upper() for w in _makeWords(relativeParts)]) + "_H__"
    className = relativeParts[-1]
    result = [
        "#ifndef %s" % protectMacro,
        "#define %s" % protectMacro,
        "",
    ]
    for namespace in relativeParts[:-2]:
        result.append('namespace %s {' % namespace)
    if len(relativeParts) > 1:
        result += [
            'namespace %s' % relativeParts[-2],
            '{',
            "",
        ]
    result += [
        "class %s" % className,
        "{",
        "public:",
        "private:",
        "",
        "    %s(const %s & rhs) = delete;" % (className, className),
        "    %s & operator=(const %s & rhs) = delete;" % (className, className),
        "};",
    ]
    if len(relativeParts) > 1:
        result.append("")
    for namespace in reversed(relativeParts[:-1]):
        result.append("} // namespace %s" % namespace)
    result += [
        "",
        "#endif // %s" % protectMacro,
    ]
    return result
