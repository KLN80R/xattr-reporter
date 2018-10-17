# xattr-reporter

### Overview:

This project produces a time-lined report of the extended attributes of files within a given directory, including their associated metadata. 

**Note:** This tool is currently only compatible with macOS and Linux systems. Please refer to [ads-reporter](https://github.com/KLN80R/xattr-reporter/blob/master/README.md#ads-reporter) for an equivalent tool for Windows systems.

### Usage:

```
usage: xattr-reporter.py [-h] [-r] [-o OUTPUT] [-a] path`
```

```
positional arguments:
  path                  path to directory to be scanned for extended
                        attributes

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       recursively scan for extended attributes
  -o OUTPUT, --output OUTPUT
                        name of file to output to
  -a, --ascending       sort by time ascending (default is descending)
 ```

### Requirements:
This tool uses Python 2.7 and requires the following libraries:

- xattr 0.9.6  
- pathlib 1.0.1  
- Markdown 3.0.1  
- pdfkit 0.6.1  
- wkhtmltopdf 0.2  
- hexdump 3.3

All requirements can be installed with the command

`pip install -r requirements.txt`

# ads-reporter

### Overview:

This tool produces a time-lined report of the alternate data streams of files within a given directory, including their associated metadata.

**Note:** This tool is currently only compatible with Windows systems. Please refer to [xattr-reporter](https://github.com/KLN80R/xattr-reporter/blob/master/README.md#xattr-reporter) for an equivalent tool for Windows systems.


