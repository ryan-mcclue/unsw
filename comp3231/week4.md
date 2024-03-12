<!-- SPDX-License-Identifier: zlib-acknowledgement -->
user<->filesystem:
* arbitrary-size:fixed-blocks
* contiguous:fragmented
* access-control, attributes
* hierarchical:flat

regular files, directories and device files (block, character)

a directory is mapping of file names
unique absolute path names from root directory of file system

file locks exist to prevent simultaneous access to a file
in linux, dentries (file names) are textual references to inode 
(a directory file is a mapping to dentries)
inode (indexed allocation) will be deleted when its reference counter is 0.
so, simultaneous read/write/deletion allowed on linux
on windows, mandatory file locks exist

SPI IC disk controller -> SPI driver -> filesystem (caching, write scheduling) -> VFS (inodes, open files)

a particular filesystem type may optimise itself for a particular medium, 
e.g. flash/cdrom/magnetic etc.
dynamic file blocks have internal but no external fragmentation

dynamic linked list bad for random access, e.g. coding in a file
so, keep a separate table for open files in memory (inodes) 
that provide a contiguous mapping to block numbers (large memory requirements for duplication)

sequential access->larger block size (fewer IO operations)
random access->smaller block size (less unrelated data)
