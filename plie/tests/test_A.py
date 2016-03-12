"""

Set up the path for the other modules

"""

import os
import sys
import pathlib

p = pathlib.Path(os.getcwd())                           # Who
if p.parts[-1] == 'tests':                              # doesn't
    sys.path.insert(0, os.path.abspath('../../'))       # love
elif p.parts[-1] == 'plie' and p.parts[-2] == 'Plie':   # path
    sys.path.insert(0, os.path.abspath('../'))          # hacking?

