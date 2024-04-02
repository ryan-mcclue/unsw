<!-- SPDX-License-Identifier: zlib-acknowledgement -->
FILE.H/PROC.H
A File represents a file for a process and its child processes.
A FileMemoryID is a list of indexes into file memory.
A FileDescriptor is a list of indexes into file pointers.
A FileTable contains system wide file memory. 
A FileDescriptorTable contains process specific file pointers. 
An issue to address is multiple processes opening the same file.
To handle this, FileTable is instantiated as a global variable and is shared between processes.
FileDescriptor table is added to the proc struct and so is per-process. 
This gives multiple processes unique file cursors to the same file memory.

MAIN.C/RUNPROGRAM.C/PROC.C:
The file memory id's are initialised after boot(), 
so they are available for all potential processes.

The file descriptors are initialised in runprogram(). 
All descriptors are marked as free except for 1 and 2, to account for stdout and stderr.
Next descriptors 1 and 2 are opened to the con: device and the process is launched.

To cleanup memory, on proc_destroy() all open files are closed.

SYSCALL.C/FILE.C:
As dealing with syscall ABI, the arguments must be explicitly obtained from registers
or the stack.
The syscall must return errno and the actual result placed in an argument pointer.

For open(), the first free file descriptor is assigned to the first free file memory id.
For close(), the file memory is only freed if ref_count is 0, 
but the file descriptor is always freed.
For read() and write(), memory is acessed from file cursor. 
The destination and source addresses must be checked to ensure not copying to an invalid location 
like an unrelated kernel structure, device or NULL that could cause corruption or a system crash.
Furthermore, the size of the buffer must be verified to prevent buffer overflows.
These details are handled by uio_uinit(). 
For lseek(), the file cursor is adjusted.
For dup2(), newfd is pointed to oldfd's file pointer.



IMPORTANT: ffmpeg -i asst1-video.mkv -c copy asst1-video.mp4
