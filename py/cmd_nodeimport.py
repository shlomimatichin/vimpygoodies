import vim
import re
import os
import glob
import vimrange

JS_EXTENSIONS = [".js", ".jsx", ".ts", ".tsx"]


def nodeImport(*args):
    range = vimrange.VimRange(*args)
    currentWord = range.currentWord()
    lineNumber = vim.current.range.start
    vimFilename = vim.current.buffer.name
    fileType = os.path.splitext(vimFilename)[1].lower()
    assert fileType in JS_EXTENSIONS, "this command only works on JS/TS file types"
    javascriptRoot = _findJavascriptProjectRoot(os.path.dirname(vimFilename))

    toAdd = None
    for fullpath in _allJavascriptCodeUnderDirectory(javascriptRoot):
        with open(fullpath) as f:
            contents = f.read()
        contents = "\n" + contents
        match = re.search(r"\nimport\s+%s\s+from\s+(.*)\n" % currentWord, contents)
        if match is not None:
            toAdd = "import %s from '%s';\n" % (currentWord, _calculatePath(fullpath, match.group(1).strip("\"';"), vimFilename))
            break
        match = re.search(r"\nimport\s+\*\s+as\s+%s\s+from\s+(.*)\n" % currentWord, contents)
        if match is not None:
            toAdd = "import * as %s from '%s';\n" % (currentWord, _calculatePath(fullpath, match.group(1).strip("\"';"), vimFilename))
            break
    if toAdd is None:
        raise Exception("Import not found")
    firstNonImportLineIndex = _firstNonImportLineIndex()
    vim.current.buffer[firstNonImportLineIndex: firstNonImportLineIndex] = [toAdd]


def _calculatePath(importingFile, importPath, relativeTo):
    importingFile = os.path.abspath(importingFile)
    relativeTo = os.path.abspath(relativeTo)
    imported = os.path.abspath(os.path.join(os.path.dirname(importingFile), importPath))
    result = os.path.relpath(imported, os.path.dirname(relativeTo))
    if result[0] != '.':
        result = './' + result
    return result


def _firstNonImportLineIndex():
    result = 0
    for index, line in enumerate(vim.current.buffer):
        if len(line.strip()) == 0 and index + 1 < len(vim.current.buffer) and \
                vim.current.buffer[index + 1].startswith("import"):
            continue
        if line.startswith("import"):
            result = index + 1
    return result


def _allJavascriptCodeUnderDirectory(directory):
    for root, dirs, filenames in os.walk(directory):
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        for filename in filenames:
            fileType = os.path.splitext(filename)[1].lower()
            fullpath = os.path.join(root, filename)
            if fileType not in JS_EXTENSIONS:
                continue
            if os.stat(fullpath).st_size > 100 * 1024: # skip generate files
                continue
            yield fullpath


def _findJavascriptProjectRoot(directory):
    #stop when node_modules found, .git found, or no more javascript files in directory
    directory = os.path.abspath(directory)
    parts = directory.split(os.path.sep)
    lastPart = None
    while len(parts) > 1:
        candidate = os.path.sep.join(parts)
        containsJavascriptFiles = False
        for filename in glob.glob(os.path.join(candidate, "*")):
            if os.path.splitext(filename)[1].lower() in JS_EXTENSIONS:
                containsJavascriptFiles = True
                break
        if not containsJavascriptFiles:
            assert lastPart is not None
            return os.path.join(candidate, lastPart)
        if os.path.exists(os.path.join(candidate, "node_modules")):
            return candidate
        if os.path.exists(os.path.join(candidate, ".git")):
            return candidate
        lastPart = parts.pop()



aliases = dict(
    nodeImport=nodeImport,
    NodeImport=nodeImport,
    ni=nodeImport,
)
