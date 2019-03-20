import vim
import vimrange
import json


def formatJSON(*args):
    range = vimrange.VimRange(*args)
    content = range.content()
    data = json.loads(content)
    indent = '    '
    newContent = json.dumps(data, indent=indent)
    range.replace(newContent)


aliases = dict(
    formatJSON=formatJSON,
    fj=formatJSON,
)
