#!/usr/bin/python2.7

import xattr
import re
from pathlib import Path

PATH = Path('/Users/kp/Downloads')  # Replace as appropriate

files = [p for p in PATH.iterdir() if p.is_file()]
for p in files:

    print "\\" + "="*50 + "\\"
    print "\n* Listing extended attributes for: \n\t" + str(p) + "\n"

    x = str(xattr.listxattr(str(p)))
    x = re.sub('[() \']', '', x)

    list = x.split(",")
    for l in list:
        print l

    print "\n"

print "\\" + "="*50 + "\\"
