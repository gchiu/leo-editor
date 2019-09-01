"""
This is a bit awkward, but yoton is a package that is designed to work from
Python 2.4 to Python 3.x. As such, it does not have relative imports and
must be imported as an absolute package. That is what this module does...
"""
import os
import sys

try:
    import leo.core.leoGlobals as leo_g
    # leo_g.pr('pyzo/yotonloader.py')
except Exception:
    leo_g = None

# Import yoton
sys.path.insert(0, os.path.dirname(__file__))
import yoton  # noqa
assert yoton

# Reset
sys.path.pop(0)
