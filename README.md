# ADS-Reporter

### Overview:

This project produces a time-lined report of the alternate data stream/extended attributes of files within a given directory, including their associated metadata.

NB: Extended attributes are currently only available on Mac OS and Linux systems.

### Usage:

`python proj.py [directory-path]`

### Requirements:

- xattr 0.9.6  
`pip install xattr`  

- pathlib 1.0.1  
`pip install pathlib`  

### Extended Attributes macOS

Below is an outline of extended attributes typically found on macOS. This is not an exhaustive list. It is worth bearing in mind that any user is able to create their own attributes to attach to files.

- **com.apple.quarantine**    

    All files which have been downloaded from the internet, either via web browser or mail client, feature this extended attribute. The contents of this attribute (the gatekeeper score in particular) is used to determine if the file needs its signature checked before use by applications.  

    `[gatekeeper score];[clock time];[downloaded from];[UUID]`

- **com.apple.ResourceFork**  

    The resource fork of a file, often used to store information such as preview or thumbnail images, dialogue definitions or text collections.
