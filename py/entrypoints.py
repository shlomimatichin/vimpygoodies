import glob
import os
import traceback

_all = {}
_aliases = {}


def reloadWhatChanged():
    for filename in glob.glob("%s/.vim/bundle/vimpygoodies/py/cmd_*.py" % os.environ['HOME']):
        try:
            if filename in _all:
                if os.stat(filename).st_mtime == _all[filename].mtime:
                    continue
                for alias in _all[filename].aliases:
                    del _aliases[alias]
            moduleName = os.path.basename(filename)[:-len(".py")]
            module = __import__(moduleName)
            reload(module)
            for alias, method in module.aliases.iteritems():
                if alias in _aliases:
                    raise Exception("VimPyGoodies: Alias '%s' already exists" % alias)
                _aliases[alias] = method
            _all[filename] = module
            module.mtime = os.stat(filename).st_mtime
        except:
            print "Unable to load '%s'" % filename
            traceback.print_exc()


def invoke(command, argv):
    if command not in _aliases:
        raise Exception("No such alias '%s'" % command)
    _aliases[command](*argv)
