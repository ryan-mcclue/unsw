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
* Indexed (file points to data structure which has pointers to all blocks)
  - Access: Fast sequential, fast random
  (ext fs uses inodes, FAT has file allocation table, index block, file control block etc.)
  (there is memory overhead of maintaining )
  (updating/deleting are only 1 write)

Storing free blocks:
* Linked list: fast search, not contiguous
* Bitmap: slow search, high memory, contiguous

A sparse file has logical size different to physical, i.e. stores 0s in metadata rather than storing 

regular files, directories and device files (block, character)

a directory is mapping of file names
unique absolute path names from root directory of file system

file locks exist to prevent simultaneous access to a file
in linux, dentries (file names) are textual references to inode 
(a directory file is a mapping to dentries)
inode (indexed allocation) will be deleted when its reference counter is 0.
so, simultaneous read/write/deletion allowed on linux
on windows, mandatory file locks exist

SPI IC disk controller -> SPI driver -> filesystem (caching, write scheduling) -> VFS (vnode) -> FS (write/read/mount, allocation strategies, inodes, etc.)
VFS abstracts different filesystems, file types (device /dev, network, kernel data structure /proc files etc.), allocation strategies? etc.

EXT3:
inode (blocks, atime/ctime/mtime, uid/gid, mode, size etc.)
IMPORTANT: to account for sparse files, size is offset of highest byte written
IMPORTANT: to keep metadata size static, can store max. number of block numbers:
  - 4 byte block numbers
  - 12 direct blocks
  - single, double, triple indirect, i.e. block number to block containing block numbers

a particular filesystem type may optimise itself for a particular medium, 
e.g. flash/cdrom/magnetic etc.
