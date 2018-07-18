import os
import sys
sys.path.append(os.path.join(os.environ['HOME'], ".vim", "bundle", "vimpygoodies", "py"))
import vim
import goodiesentrypoints

line1 = int(argv.pop(0)) - 1
line2 = int(argv.pop(0)) - 1
command = argv.pop(0)
goodiesentrypoints.reloadWhatChanged()
goodiesentrypoints.invoke(command, [line1, line2] + argv)
