<!-- SPDX-License-Identifier: zlib-acknowledgement -->
user<->filesystem:
* arbitrary-size:fixed-blocks
* contiguous:fragmented
* access-control, attributes
* hierarchical:flat

Generally have fixed block sizes:
* Large: fewer IO; good for sequential access
* Small: less unrelated data; good for random access

Block allocation strategies: (all have internal fragmentation)
(So, when create a file, will allocate as many blocks as needed and update as go)
* Contiguous
  - Access: Fast sequential, fast random
  - External Fragmentation (only really applicable for read-only)
* Linked
  - Access: Fast sequential, slow random
* Indexed (a data structure which has pointers to all blocks)
  (considered 1write as the shifting of block numbers occurs in inode that is in ram, not disk)
  - Access: Fast sequential, fast random
  (ext fs uses inodes with pointers for each file;
  (FAT has a single file allocation table for all files, index block, file control block etc.)
  IMPORTANT: FAT is indexed, i.e. in RAM, however stores with linked list allocation
  (there is memory overhead of maintaining )
  (updating/deleting are only 1 write)

Storing free blocks:
* Linked list: no extra space, slower as more disk accesses (storage free, as store free blocks in blocks themselves)
* Bitmap: faster search, contiguous (used by linux as contiguous faster for hardware and caching)
  (if deleted, actually only mark as free on bitmap, block is not physically cleared)

A sparse file has logical size different to physical, i.e. stores 0s in metadata rather than storing 

regular files, directories and device files (block, character)

a directory is mapping of file names to inode numbers (a hard link has same number, different name)
unique absolute path names from root directory of file system

file locks exist to prevent simultaneous access to a file
in linux, dentries (file names) are textual references to inode 
(a directory file is a mapping to dentries)
inode (indexed allocation) will be deleted when its reference counter is 0.
so, simultaneous read/write/deletion allowed on linux
on windows, mandatory file locks exist

SPI IC disk controller -> SPI driver -> filesystem (caching, write scheduling) -> VFS (vnode) -> FS (write/read/mount, allocation strategies, inodes, etc.)
VFS abstracts different filesystems, file types (device /dev, network, kernel data structure /proc files etc.), handles concurrency issues 

a particular filesystem type may optimise itself for a particular medium, 
e.g. flash/cdrom/magnetic etc.
