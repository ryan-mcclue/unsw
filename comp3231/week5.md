<!-- SPDX-License-Identifier: zlib-acknowledgement -->
will work with file descriptors. need to know mode (e.g. read-only), read/write pointer

directory is just another inode, 
stores name, rec length, file names

for multiple processes, stdout might not be 1
dup means file descriptors share file pointers
global open file table, in which per process file descriptors point to this table

fs buffer exists in kernel RAM as different speeds (ram and disk) and sizes (app and block size)
an app sends non-uniform block sizes which are then transfered from the kernel buffer in whole block sizes
a write can happen quickly, as don't have to wait for disk controller 
(explicitly flushing with `sync` probably only required for larger writes, e.g. to USB)

(linux has 'raw' devices with no buffering)

inode and directory block writes are prioritised over data blocks, as more critical to system
cache also open disk blocks (may even do read-ahead preloading; LRU cache eviction)

EXT2 inode:
* blocks 
* atime/ctime/mtime 
* uid/gid
* mode 
* reference count (account for hard links; soft links have distinct inode, but share data blocks)
* size (to account for sparse files, size is offset of highest byte written)
       (also, the files blocks may store an indirect block)
* direct blocks (to keep metadata size static, can store max. number of block numbers)
  - 12 direct blocks
  - single (n), double (n^2), triple indirect (n^3), i.e. block numbers to block containing block numbers
  - 4 byte block numbers (so block_size / 4 would give number of block numbers single indirect can store)

Harddrive format:
* boot block (os bootstrap code) 
* equally sized block groups
  - redundant superblock (aid recovery)
  - block group header information, e.g. inode and data bitmaps
  - inode table
  - data blocks
(inodes stored in same location as block groups as often have to interact with both)

File operations occur in stages and are non-atomic
e.g. deleting a file could crash at any stage:
  1. removing directory entry 
  2. marking inode as free
  3. mark disk blocks as free
  IMPORTANT: files still persist, only actually deleted when overwritten with something else 
FS journalling aims to introduce a degree of atomicity. 
First write to change to journal, then perform actual operation and remove journal entries. (write each steps to journal)

On startup, can then look at journal to see if operation completed.
on startup look at journal entry; journal says directory removed; check if it is; if not do; continue and then remove journal entry
(so journal only keeps track of uncommited changes)

SSDs still have seek time, albeit very small (so sequential still faster than random)
