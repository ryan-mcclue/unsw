<!-- SPDX-License-Identifier: zlib-acknowledgement -->
git clone https://z5346008@nw-syd-gitlab.cseunsw.tech/COMP3231/24T1/grp201-asst2.git asst2-src
#include <kern/errno.h>

TODO: check uninitialised git log

We give you two system call implementations: sys_reboot() in main/main.c and sys___time() in syscall/time_syscalls.c. In GDB, if you put a breakpoint on sys_reboot() and run the "reboot" program, you can use "backtrace" (or "where") to see how it got there.

* existing syscall template
* existing user space binary makefile template
* test: sys161 kernel "p /testbin/asst2".

* open, read, write, lseek, close, dup2
  - use existing VFS and vnodes and track filesystem state
  - gracefully handle all possibly erroneous inputs
  - error codes as per os161 man pages (leniant to particular error code)
userland/include/unistd.h -> kern/include/syscall.h
put our code in kern/syscall/file.c

IMPORTANT: basic assignment has only one process at a time (advanced implements fork())
IMPORTANT: so, no synchronisation across data structures?
TODO: can two threads call a system call at the same time?
- per process file descriptor data structure?
- across processes, e.g. open file table (only if advanced)
- keep track of open files and transfer data from kernel to userspace

For this basic assignment, the file descriptors 1 (stdout) and 2 (stderr) must start out attached to the console device ("con:"), 0 (stdin) can be left unattached. You will probably modify runprogram() to achieve this. Your implementation must allow programs to use dup2() to change stdin, stdout, stderr to point elsewhere.


