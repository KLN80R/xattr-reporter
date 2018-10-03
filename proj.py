#!/usr/bin/python2.7

import xattr
from pathlib import Path

PATH = Path('/Users/kp/Downloads')  # Replace as appropriate

files = [p for p in PATH.iterdir() if p.is_file()]
for p in files:
    print "\\" + "="*50 + "\\"
    print "\n* Listing extended attributes for: " + str(p) + "\n"
    x = xattr.listxattr(str(p))
    print str(x)
    print "\n*"
