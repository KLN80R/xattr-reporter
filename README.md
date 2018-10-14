# ADS-Reporter

### Overview:

This project produces a time-lined report of the alternate data stream/extended attributes of files within a given directory, including their associated metadata.

[Usage](#usage:)  
[Requirements](#requirements:)  
[Extended Attributes macOS](#extended-attributes-macos:)  
[Extended Attributes Linux](#extended-attributes-linux:)  
[Reference List](#reference-list:)  

NB: Extended attributes are currently only available on Mac OS and Linux systems.

### Usage:

`python proj.py [directory-path]`

### Requirements:

- xattr 0.9.6  
`pip install xattr`  

- pathlib 1.0.1  
`pip install pathlib`  

### Extended Attributes macOS:

Below is an outline of extended attributes typically found on macOS, with a particular focus on macOS High Sierra and Mojave. This is not an exhaustive list and only represents those extended attributes that were created by Apple and are frequently found within the file system. It is worth bearing in mind that any user is also able to create their own extended attributes to attach to files, and that these have not been included in our research.

- **com.apple.quarantine**    

    All files which have been downloaded from the internet, either via web browser or mail client, feature this extended attribute. The contents of this attribute (the gatekeeper score in particular) are used to determine if the file needs its signature checked before use by applications.  

    `[gatekeeper score];[clock time];[downloaded from];[UUID]`

- **com.apple.FinderInfo**

    Used to store some minimal Finder information in binary format. This attribute allows backwards compatibility with pre macOS Mavericks HFS+ metadata. A typical use involves certain bits set within the attribute represent the current tags/label colour finder. It may also contain old file formats if the file type was changed.

- **com.apple.ResourceFork**  

    The resource fork of a file. Often used to store information such as preview or thumbnail images, dialogue definitions or text collections. This attribute is also proxy for legacy HFS+ metadata.

- **com.apple.lastuseddate#PS**  

    Simply the last time a file was accessed in binary data (non-human readable) format.

- **com.apple.diskimages.fsck**

    This attribute records binary data information about the most recent file system consistency check `fsck` of the disk image file it is associated with. This check occurs during an attempt to mount the image.

- **com.apple.diskimages.recentcksum**

    This attribute is tied to disk image files that have been successfully mounted and contains a record the most recent checksum verification using `hdiutil`.  

    `i:[integer] on [Event UUID] @ [system time] - CRC32: $[checksum]`

- **com.apple.metadata:kMDItemWhereFroms**

    Contains information regarding the origin URL of the downloaded file. This data appears in the 'Get Info' Finder dialogue box. The URL is stored in a *binary property list* `(bplist)`.

- **com.apple.metadata:_kMDItemUserTags**  

    Similar to com.apple.FinderInfo but solely for finder tag information, particularly for macOS post-Mavericks. It does, however store this in a *binary property list* `(bplist)` and can represent multiple tag colours in the order they were added.

- **com.apple.metadata:kMDLabel_**

    Contains a string of characters written when the OS discovers a checksum verification failed.

- **com.apple.metadata:_kTimeMachine[Newest|Oldest]Snapshot**

    Contains the timestamp for the newest or oldest time machine backup of the given folder.

- **com.apple.metadata:kMDItemDownloadedDate**  

    Timestamp of when the file was downloaded.

- **com.apple.metadata:kMDItemIsScreenCapture:**

    Flag designating whether the file is a screenshot.

- **com.apple.metadata:kMDItemScreenCaptureGlobalRect:**

    Contains values designating the positioning of the screenshot, as well as its dimensions. These are half of the screenshots pixel width and height.

- **com.apple.metadata:kMDItemScreenCaptureType:**

    Designates whether the screenshot is a manual selection, full screen or a specific window.


### Reference List

https://eclecticlight.co/2017/08/14/show-me-your-metadata-extended-attributes-in-macos-sierra/
https://eclecticlight.co/2018/02/08/xattr-com-apple-diskimages-recentcksum-disk-image-checksum/
https://eclecticlight.co/2018/02/08/xattr-com-apple-diskimages-fsck-record-of-disk-image-integrity-check/  
https://eclecticlight.co/2017/12/21/xattr-com-apple-metadatakmditemwherefroms-origin-of-downloaded-file/
http://rixstep.com/2/20180729,00.shtml
http://krypted.com/tag/com-apple-finderinfo/
https://arstechnica.com/gadgets/2013/10/os-x-10-9/9/
https://www.pressreader.com/australia/mac-life/20180529/283034055211985
https://blog.padil.la/2016/06/30/using-file-attributes-to-fill-volumes-and-bypass-os-x-server-limits/
