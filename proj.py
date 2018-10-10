import os
import sys
import time
import json
import xattr
from pathlib import Path

def genReport(xattrs, path):

	#TODO Make this write out to a file

	r = open('report.md', 'w')

	r.write("## Extended Attributes Report for " + str(path) + "\n\n")
	for f in xattrs:

		r.write("#### File Path:\n\n")
		r.write(f['file_path'] + "\n\n")

		r.write("#### Extended Attributes:\n\n")
		for x in f['extended_attributes']:
			r.write("- **" + x.keys()[0] + ":**\n\n")
			r.write("    " + x[x.keys()[0]] + "\n\n")

		r.write("\n\n---\n\n")

	r.close()

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print "Usage: python proj.py <downloads folder>"
		exit(1)

	path = Path(sys.argv[1])

	#TODO add flag for whether to sort descending or ascending

	# get extended attributes for each file in given directory
	files = [p for p in path.iterdir() if p.is_file()]
	xattrs = []
	for p in files:
		file_xattrs = {}

		file_xattrs['file_path'] = str(p)
		file_xattrs['create_time'] = time.ctime(os.path.getctime(str(p)))
		file_xattrs['extended_attributes'] = []

		x = xattr.listxattr(str(p))
		for attr_name in x:
			file_xattrs['extended_attributes'].append({str(attr_name):xattr.getxattr(str(p), str(attr_name))})

		xattrs.append(file_xattrs)

	# sort list by time descending
	xattrs.sort(key=lambda x:x['create_time'], reverse=True)

	# print(json.dumps(xattrs, indent=4))
	genReport(xattrs, path)
