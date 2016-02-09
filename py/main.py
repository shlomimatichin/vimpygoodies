import os
import sys
sys.path.append(os.path.join(os.environ['HOME'], ".vim", "bundle", "vimpygoodies", "py"))
import vim
import entrypoints

command = argv.pop(0)
entrypoints.reloadWhatChanged()
entrypoints.invoke(command, argv)
