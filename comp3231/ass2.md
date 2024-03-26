<!-- SPDX-License-Identifier: zlib-acknowledgement -->

So in regard to concurrency, you can assume only a single process runs at a time

However, the design and implementation of your system calls should not assume only a single process will ever exist at a time. 
It should be possible to add a fork() implementation to your system call implementation, and then only synchronise your existing design to handle the concurrency.
- A lock to protect the access to this file descriptor. Since it's possible that two threads share the same copy of this bookkeeping data structure (e.g., after fork)
- fd space is process specific, i.e. different process may get the same file descriptor that represent different files 

Specifically, a viewer of your video should be able to determine the following:
  * What significant data structures have you added and what function do they perform?
  * What are any significant issues surrounding managing the data structures and the state they contain?
  * What data structures are per-process and what structures are shared between processes?
  * What are the main issues related to transferring data to and from applications?
FILE.H/PROC.H
A File represents a file for a process and its child processes.
Cursor represents each open file's unique read/write offset.
Ref_count indicates how many open references to this file from a dup or fork.
Fmi is a index into what memory slot this file is using.
For an advanced assignment, a synchronisation primitive would be added to account for child processes sharing the same file as their parent process. 
A FileMemoryID is a singly linked list of indexes into system wide file memory.
A FileDescriptor is a doubly linked list of indexes into process specific file pointers.
A FileTable contains system wide file memory. 
This is a instantiated as a global variable and so is shared between processes.
First_free_fmi is the first memory slot available for a new file to use.
A FileDescriptorTable contains process specific file pointers. 
This is added to the proc struct and so is per-process.
First_free_fd is the first file descriptor available for a new file to use.

MAIN.C/RUNPROGRAM.C/PROC.C:
The file memory id's are initialised after boot(), so they are available for all potential processes.
The file descriptors are initialised in runprogram(). 
All descriptors are marked as free except for 1 and 2, to account for stdout and stderr.
Next descriptors 1 and 2 are opened to the con: device and the process is launched.
To cleanup memory, on proc_destroy() all open files are closed.

FILE.C:
In sys_open(), must first copy file name from userspace to kernel memory.
This operation performed by copyinstr() ensures that we aren't passed a memory address that could potentially point to kernel structures and cause corruption.
In sys_close(), know to only free file memory if ref_count is 0, but to always free the file descriptor.
In sys_read(), transferring from kernel to userspace...
In sys_write(), transferring from userspace to kernel...

SYSCALL.C:
trapframe, 32bit etc.
