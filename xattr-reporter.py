import os
import sys
import time
import json
import xattr
import pdfkit
import struct
import hexdump
import argparse
from pathlib import Path
from markdown import markdown

reload(sys)
sys.setdefaultencoding('utf8')

def sanitize(s):
	return "".join(i for i in s if ord(i)<128)

# Generate a markdown report of extended attribute data per file
def genReport(xattrs, path, file_name):

	r = open(file_name + '.md', 'w')

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

# Convert report markdown file to a pdf
def toPDF(file_name):

	inputFile = file_name + '.md'
	outputFile = file_name + '.pdf'

	with open(inputFile, 'r') as f:
		html = markdown(f.read(), output_format='html4')

	pdfkit.from_string(html, outputFile)

# Output attributes according to their data/display type
def handleAttr(attr_name, attr_val):

	if ("com.apple.lastuseddate#PS" in attr_name):

		# Convert hexdump to timestamp
		ret = hexdump.dump(attr_val)
		ret = ret.replace(" ", "")
		ret = ret[:8]
		ret = "".join(reversed([ret[i:i+2] for i in range(0, len(ret), 2)]))
		ret = float.fromhex(ret)
		ret = time.localtime(ret)
		ret = time.strftime('%Y-%m-%d %H:%M:%S', ret)
		return ret

	elif ("com.apple.quarantine" in attr_name):
		t = attr_val[5:13]
		t = float.fromhex(t)
		t = time.localtime(t)

		ret = attr_val[:5] + time.strftime("%Y-%m-%d %H:%M:%S", t) + attr_val[13:]
		return ret


	elif ("com.apple.diskimages.fsck" in attr_name):
		ret = hexdump.dump(attr_val)

	elif ("com.apple.metadata:com_apple_mail_dateReceived" in attr_name):
		ret = hexdump.dump(attr_val)

	elif ("com.apple.metadata:com_apple_mail_dateSent" in attr_name):
		ret = hexdump.dump(attr_val)

	elif ("com.apple.metadata:com_apple_mail_isRemoteAttachment" in attr_name):
		ret = hexdump.dump(attr_val)

	elif ("metadata" in attr_name):
		ret = sanitize(attr_val)

	else:
		ret = sanitize(attr_val)

	return ret

# Get extended attributes for each file in a given directory and return dict
def get_xattrs(path, asc=False, recurse=False):

	files = [p for p in path.iterdir() if p.is_file()]
	dirs = []
	if recurse:
		dirs = [sd for sd in path.iterdir() if sd.is_dir()]
		for sd in dirs:
			files += [p for p in sd.iterdir() if p.is_file()]
			dirs += [new_dir for new_dir in sd.iterdir() if new_dir.is_dir()]

	xattrs = []
	for p in files:
		file_xattrs = {}
		file_xattrs['file_path'] = str(p)
		file_xattrs['create_time'] = time.ctime(os.path.getctime(str(p)))
		file_xattrs['extended_attributes'] = []

		x = xattr.listxattr(str(p))
		for attr in x:
			attr_name = str(attr)
			attr_val = xattr.getxattr(str(p), attr_name)
			attr_val = handleAttr(attr_name, attr_val)
			file_xattrs['extended_attributes'].append({ attr_name : attr_val })

		xattrs.append(file_xattrs)

	if asc:
		# Sort by create time ascending
		xattrs.sort(key=lambda x:x['create_time'])
	else:
		# Sort by create time descending
		xattrs.sort(key=lambda x:x['create_time'], reverse=True)

	return xattrs


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="path to directory to be scanned for extended attributes", type=str)
	parser.add_argument("-r", "--recursive", action="store_true", help="recursively scan for extended attributes")
	parser.add_argument("-o", "--output", type=str, help="name of file to output to")
	parser.add_argument("-a", "--ascending", action="store_true", help="sort by time ascending (default is descending)")
	args = parser.parse_args()

	path = Path(args.path)
	xattrs = get_xattrs(path, args.ascending, args.recursive)

	if args.output:
		genReport(xattrs, path, args.output)
		toPDF(args.output)
	else:
		print(json.dumps(xattrs, indent=4))
