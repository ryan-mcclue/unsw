<!-- SPDX-License-Identifier: zlib-acknowledgement -->
// git clone https://z5346008@nw-syd-gitlab.cseunsw.tech/COMP3231/24T1/grp201-asst2.git asst2-src
// #include <kern/errno.h>
// userland/testbin/asst2/asst2.c

// syscall()
switch (callno)
{
  i64 retval = 0;

  // return values: copyout(&local, userptr_arg);
  // input: copyin()
  case SYS_open:
  {
    int open(const char *filename, int flags);
    int open(const char *filename, int flags, mode_t mode);
    retval = sys_open((userptr)tf->a0, tf->a1, tf->a2);
  } break;
  case SYS_close:
  {
    int close(int fd);
    retval = sys_close(tf->a0);
  } break;
  case SYS_read:
  {
    still 32bit return
    ssize_t read(int fd, void *buf, size_t buflen);
    retval = sys_read(tf->a0, (userptr)tf->a1, tf->a2);
  } break;
  case SYS_write:
  {
    ssize_t write(int fd, const void *buf, size_t nbytes);
    retval = sys_write(tf->a0, (userptr)tf->a1, tf->a2);
  } break;
  case SYS_lseek:
  {
    off_t 64bit
    off_t lseek(int fd, off_t pos, int whence);
    retval = sys_lseek(tf->a0, tf->a2, tf->a3, tf->a4);
  } break;
  case SYS_dup2:
  {
    int dup2(int oldfd, int newfd);
    retval = sys_dup2(tf->a0, tf->a1);
  } break;

  if (retval < 0)
  {
    int errno = (int)retval;
    tf->tf_v0 = errno;
    tf->tf_a3 = 1; // signal error
  }
  else
  {
    if (callno == SYS_lseek)
    {
		  tf->tf_v0 = (u32)((u64)retval >> 32);
      tf->tf_v1 = (u32)retval;
    }
    else
    {
		  tf->tf_v0 = retval;
    }
		tf->tf_a3 = 0;      // signal no error
  }

open/close (vfs_open/close), read/write (vop_read/write), lseek, dup2
}
//

// boot()
u32 open_fds[OPEN_MAX];

// 

// Your implementation must allow programs to use dup2() to change stdin, stdout, stderr to point elsewhere.
// on startup->fd1 and fd2 "con:" device (i.e. identical source), however can be closed
// (modify runprogram() to acheive this)
// runprogram()
char con_device[5] = "con:";
r1 = vfs_open(conname,f1,m1,&v1);
strcpy(con_device, "con:"); 
r2 = vfs_open(conname,f2,m2,&v2); 

struct vnode *v;
result = vfs_open(progname, O_RDWR, 0, &v);
int vfs_open(char *path, int openflags, mode_t mode, struct vnode **ret);
//

// kern/include/file.h, kern/syscall/file.c


  - use existing VFS and vnodes and track filesystem state
  - gracefully handle all possibly erroneous inputs
  - error codes as per os161 man pages (leniant to particular error code)
userland/include/unistd.h -> kern/include/syscall.h
put our code in kern/syscall/file.c
kernel facing, e.g. assumed syscall exception handler called us

get cwd from curpoc() proc struct

will be getting args from struct trapframe? (so consult, syscall procedure)
copyin((userptr_t)tf->tf_sp + 16, &whence, sizeof(int));

If too many files are open within a particular process, you should return EMFILE. 
If too many files are open systemwide, you should return ENFILE.
The per-process file descriptor table should be OPEN_MAX (128) in size. 

maintain a reference count; so also have a bitmap?
//


We give you two system call implementations: sys_reboot() in main/main.c 
and sys___time() in syscall/time_syscalls.c. 
In GDB, if you put a breakpoint on sys_reboot() and run the "reboot" program,
you can use "backtrace" (or "where") to see how it got there.

* existing syscall template
* existing user space binary makefile template

copyout(const void *src, userptr_t userdest, size_t len)
uio.h

vfs_close() to avoid memory leak?


IMPORTANT: basic assignment has only one process at a time (advanced implements fork())
IMPORTANT: so, no synchronisation across data structures?
TODO: can two threads call a system call at the same time?
- per process file descriptor data structure?
- across processes, e.g. open file table (only if advanced)
- keep track of open files and transfer data from kernel to userspace

