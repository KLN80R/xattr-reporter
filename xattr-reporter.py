import os
import sys
import time
import json
import xattr
import pdfkit
import argparse
from pathlib import Path
from markdown import markdown

# Generate a markdown report of ADS data per file
def genReport(xattrs, path, file_name):

	#TODO Make this write out to a file

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


# get extended attributes for each file in a given directory and return dict
def get_xattrs(path):
	
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

	return xattrs


# Main
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="path to directory to be scanned for extended attributes", type=str)
	parser.add_argument("-r", "--recursive", action="store_true", help="recursively scan for extended attributes")
	parser.add_argument("-o", "--output", type=str, help="name of output file")
	args = parser.parse_args()

	path = Path(args.path)
	xattrs = get_xattrs(path)
	
	if args.output:
		genReport(xattrs, path, args.output)
		toPDF(args.output)
	else:
		print(json.dumps(xattrs, indent=4))

