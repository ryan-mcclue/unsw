<!-- SPDX-License-Identifier: zlib-acknowledgement -->
git clone https://z5346008@nw-syd-gitlab.cseunsw.tech/COMP3231/24T1/grp201-asst2.git asst2-src
#include <kern/errno.h>

userland/testbin/asst2/asst2.c

kernel facing, e.g. assumed syscall exception handler called us

on startup->fd1 and fd2 "con:" device (i.e. identical source), however can be closed
(modify runprogram() to acheive this)
```
char con_device[5] = "con:";
r1 = vfs_open(conname,f1,m1,&v1);
strcpy(con_device, "con:"); 
r2 = vfs_open(conname,f2,m2,&v2); 

struct vnode *v;
result = vfs_open(progname, O_RDWR, 0, &v);
int vfs_open(char *path, int openflags, mode_t mode, struct vnode **ret);
```
u32 open_fds[OPEN_MAX];

get cwd from curpoc() proc struct

will be getting args from struct trapframe? (so consult, syscall procedure)
copyin((userptr_t)tf->tf_sp + 16, &whence, sizeof(int));

If too many files are open within a particular process, you should return EMFILE. 
If too many files are open systemwide, you should return ENFILE.
The per-process file descriptor table should be OPEN_MAX (128) in size. 

maintain a reference count; so also have a bitmap?

work with:
kern/include/syscall.h, kern/include/file.[ch]
Boot time initilisation code can be called from the end of boot() in kern/main/main.c .

prefix with sys_

We give you two system call implementations: sys_reboot() in main/main.c 
and sys___time() in syscall/time_syscalls.c. 
In GDB, if you put a breakpoint on sys_reboot() and run the "reboot" program,
you can use "backtrace" (or "where") to see how it got there.

* existing syscall template
* existing user space binary makefile template
* test: sys161 kernel "p /testbin/asst2".

copyout(const void *src, userptr_t userdest, size_t len)
uio.h

vfs_close() to avoid memory leak?

* open/close (vfs_open/clos), read/write (vop_read/write), lseek, dup2
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



