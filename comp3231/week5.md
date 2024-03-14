<!-- SPDX-License-Identifier: zlib-acknowledgement -->
fs -> vnode -> vnode_ops:
 - vop_creat etc. operate on vnodes
work with filenames with vfs_mkdir()  
will work with file descriptors. need to know mode (e.g. read-only), read/write pointer

for multiple processes, stdout might not be 1
per process open file descriptor array
dup means file descriptors share file pointers
so global open file table, in which per process file descriptors point to this table

TODO: fs normally allows overriding of open files
TODO: how does fs buffering affect reliability of fs? 

fs buffer exists in kernel RAM as different speeds (ram and disk) and sizes (app and block size)
an app sends non-uniform block sizes which are then transfered from the kernel buffer in whole block sizes
a write can happen quickly, as don't have to wait for disk controller 
inode and directory block writes are prioritised over data blocks, as more critical to system
also cache open disk blocks (may even do read-ahead preloading)
TODO: LRU cache eviction?
https://elgar.cse.unsw.edu.au/~cs3231/23T1/lectures/lect11.pdf
