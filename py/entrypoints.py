import glob
import os
import traceback
import sys
try:
    try:
        from importlib import reload
    except:
        from imp import reload
except:
    pass

_all = {}
_aliases = {}


def reloadWhatChanged():
    for moduleName in ['codetools']:
        for subModuleName in sys.modules:
            if not subModuleName.startswith(moduleName + "."):
                continue
            if sys.modules[subModuleName] is None:
                continue
            reload(sys.modules[subModuleName])
    for filename in glob.glob("%s/.vim/bundle/vimpygoodies/py/cmd_*.py" % os.environ['HOME']):
        try:
            if filename in _all:
                if os.stat(filename).st_mtime == _all[filename].mtime:
                    continue
                for alias in _all[filename].aliases:
                    if alias in _aliases:
                        del _aliases[alias]
            moduleName = os.path.basename(filename)[:-len(".py")]
            module = __import__(moduleName)
            reload(module)
            for alias, method in module.aliases.items():
                if alias in _aliases:
                    raise Exception("VimPyGoodies: Alias '%s' already exists" % alias)
                _aliases[alias] = method
            _all[filename] = module
            module.mtime = os.stat(filename).st_mtime
        except:
            print("Unable to load '%s'" % filename)
            traceback.print_exc()


def invoke(command, argv):
    if command not in _aliases:
        raise Exception("No such alias '%s'" % command)
    _aliases[command](*argv)
