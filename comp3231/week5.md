<!-- SPDX-License-Identifier: zlib-acknowledgement -->
will work with file descriptors. need to know mode (e.g. read-only), read/write pointer

for multiple processes, stdout might not be 1
dup means file descriptors share file pointers
global open file table, in which per process file descriptors point to this table

TODO: fs normally allows overriding of open files
TODO: how does fs buffering affect reliability of fs? 

fs buffer exists in kernel RAM as different speeds (ram and disk) and sizes (app and block size)
an app sends non-uniform block sizes which are then transfered from the kernel buffer in whole block sizes
a write can happen quickly, as don't have to wait for disk controller 
(explicitly flushing with `sync` probably onl required for larger writes, e.g. to USB)
inode and directory block writes are prioritised over data blocks, as more critical to system
also cache open disk blocks (may even do read-ahead preloading)
TODO: LRU cache eviction?

EXT2 inode:
* blocks 
* atime/ctime/mtime 
* uid/gid
* mode 
* reference count (account for hard links; soft links have distinct inode, but share data blocks)
* size (to account for sparse files, size is offset of highest byte written)
* direct blocks (to keep metadata size static, can store max. number of block numbers)
  - 4 byte block numbers
  - 12 direct blocks
  - single, double, triple indirect, i.e. block numbers to block containing block numbers

Harddrive format:
* boot block (os bootstrap code) 
* equally sized block groups
  - block group header information
  - inode table
  - data blocks
(there will be duplicated/redundant fields to aid recovery)

FS jounrnalling to aid reliability as operations non-atomic
e.g. deleting a file could crash at any stage of directory, inode, block etc.) 

SSDs still have seek time, albeit very small (so sequential still faster than random)
