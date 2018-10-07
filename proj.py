import sys
import re
import xattr
from pathlib import Path


if __name__ == "__main__":

	if len(sys.argv) != 2:
		print "Usage: python proj.py <downloads folder>"
		exit(1)

	PATH = Path(sys.argv[1])
	
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
