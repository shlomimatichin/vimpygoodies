import vim
import vimrange
import json
import yaml


def JSONToYAML(*args):
    range = vimrange.VimRange(*args)
    content = range.content()
    data = json.loads(content)
    indent = '    '
    newContent = yaml.dump(data, default_flow_style=False)
    range.replace(newContent)


def YAMLToJSON(*args):
    range = vimrange.VimRange(*args)
    content = range.content()
    data = yaml.load(content)
    indent = '    '
    newContent = json.dumps(data, indent=indent)
    range.replace(newContent)


aliases = dict(
    json2yaml=JSONToYAML,
    JSON2YAML=JSONToYAML,
    j2y=JSONToYAML,
    J2Y=JSONToYAML,

    yaml2json=YAMLToJSON,
    YAML2JSON=YAMLToJSON,
    y2j=YAMLToJSON,
    Y2J=YAMLToJSON,
)
