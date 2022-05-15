#!/usr/bin/env python
from __future__ import print_function

import sys
import platform


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


OSCaseSensitive = True
if platform.system() == "Windows":
    OSCaseSensitive = False
elif platform.system() == "Darwin":
    # This OS is not case sensitive by default.
    OSCaseSensitive = False
