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
    uint64_t offset;
    int whence;
    join32to64(tf->tf_a2, tf->tf_a3, &offset);
    copyin((userptr_t)tf->tf_sp + 16, &whence, sizeof(int));

    off_t lseek(int fd, off_t pos, int whence);
    retval = sys_lseek(tf->a0, offset, whence);
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
      split64to32(retval64, &tf->tf_v0, &tf->tf_v1);
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


vfs_open()
vfs_close()
vfs_remove()

// TODO(Ryan): may need to vop_fsync() to flush? 
vop_write()
vop_read()
vop_stat()
vop_truncate()
VOP_TRUNCATE(vn, 0);
vop_mmap()

struct uio {
	struct iovec     *uio_iov;	/* Data blocks */
	unsigned          uio_iovcnt;	/* Number of iovecs */
	off_t             uio_offset;	/* Desired offset into object */
	size_t            uio_resid;	/* Remaining amt of data to xfer */
	enum uio_seg      uio_segflg;	/* What kind of pointer we have */
	enum uio_rw       uio_rw;	/* Whether op is a read or write */
	struct addrspace *uio_space;	/* Address space for user pointer */
};

struct iovec iov;
struct uio ku;

char numstr[8];
snprintf(numstr, sizeof(numstr), "%lu", num);
fstest_write(filesys, numstr, 1, 0)
fstest_write(const char *fs, const char *namesuffix,
	     int stridesize, int stridepos)

uio_kinit(&iov, &ku, buf, strlen(SLOGAN), pos, UIO_WRITE);
err = VOP_WRITE(vn, &ku);
		err = VOP_WRITE(vn, &ku);
		if (err) {
			kprintf("%s: Write error: %s\n", name, strerror(err));
			vfs_close(vn);
			vfs_remove(name);
			return -1;
		}

		if (ku.uio_resid > 0) {
			kprintf("%s: Short write: %lu bytes left over\n",
				name, (unsigned long) ku.uio_resid);
			vfs_close(vn);
			vfs_remove(name);
			return -1;
		}

		bytes += (ku.uio_offset - pos);
		shouldbytes += strlen(SLOGAN);
		pos = ku.uio_offset;
	}

if (bytes != shouldbytes) {
	kprintf("%s: %lu bytes written, should have been %lu!\n",
		name, (unsigned long) bytes,
		(unsigned long) (NCHUNKS*strlen(SLOGAN)));
	vfs_remove(name);
	return -1;
}
kprintf("%s: %lu bytes written\n", name, (unsigned long) bytes);


uio_kinit(&iov, &myuio, buf, sizeof(buf), 0, UIO_READ);
result = VOP_READ(vn, &myuio);

#define ARRAY_COUNT(a) (sizeof(a)/sizeof(a[0]))
#define IS_POW2_ALIGNED(x, p) (((x) & ((p) - 1)) == 0)
#define IS_POW2(x) IS_POW2_ALIGNED(x, x) 

#define __SLL_STACK_PUSH(first, node, next) \
(\
  ((node)->next = (first)), \
  ((first) = (node)) \
)
#define SLL_STACK_PUSH(first, node) \
  __SLL_STACK_PUSH(first, node, next)

#define __SLL_STACK_POP(first, next) \
(\
  ((first) != NULL) ? \
    (\
     ((first) = (first)->next) \
    )\
  : \
  (\
    (NULL) \
  )\
)
#define SLL_STACK_POP(first) \
  __SLL_STACK_POP(first, next)


// will work with file descriptors. need to know mode (e.g. read-only), read/write pointer
typedef struct File File;
struct File
{
  struct vnode *vnode;
  offset;
  mode_flags;
  open_flags;
  ref_count;
  pool_id;
};

typedef struct FileID FileID;
struct FileID
{
  FileID *next;
  int id;
};

typedef struct FileTable
struct FileTable
{
  File *files[MAX_PATH];
  File files_pool[MAX_PATH];

  FileID file_id_pool[MAX_PATH];
  FileID *first_free_file_id;
};

FileTable global_file_table;

// boot()
for (int i = 0; i < ARRAY_COUNT(global_file_table.file_id_pool); i += 1)
{
  FileID *f_id = &global_file_table.file_id_pool[i];
  f_id->id = i;
  // NOTE(Ryan): This won't add smallest first
  SLL_STACK_PUSH(global_file_table.first_free_file_id, f_id);
}

// Your implementation must allow programs to use dup2() to change stdin, stdout, stderr to point elsewhere.
// on startup->fd1 and fd2 "con:" device (i.e. identical source), however can be closed
// (modify runprogram() to acheive this)
// runprogram()
char con_device[5] = "con:";
r1 = vfs_open(conname,f1,m1,&v1);
strcpy(con_device, "con:"); 
r2 = vfs_open(conname,f2,m2,&v2); 

int std_out = sys_open("con:");
sys_dup2(std_out, something);

struct vnode *v;
result = vfs_open(progname, O_RDWR, 0, &v);
int vfs_open(char *path, int openflags, mode_t mode, struct vnode **ret);
//

// kern/include/file.h, kern/syscall/file.c
int
sys_open(const char *filename, int flags, mode_t mode)
{
  // NOTE: seems we just need to check if parameters are valid as vfs layer handles most errno codes.
  if (filename == NULL) return EFAULT;
  if ((flags & (O_RDONLY | O_WRONLY | O_RDWR)) == 0 || \\
       !IS_POW2(flags) || (flags > O_APPEND)) return EINVAL;
  if (global_state.first_free_file_id == NULL) return EMFILE;
  
  // the same file will have unique file table entry (e.g. own position; so one could overwrite the other)
  // only dup2 has separate fds point to same entry

  // NOTE(Ryan): Preserve filename
  char buf[MAX_PATH] = {0};
  strncpy(buf, filename, sizeof(buf));

  struct vnode *node = NULL;
  int res = vfs_open(buf, flags, mode, &node);
  if (res) return res;

  FileID *file_id = global_file_table.first_free_file_id;
  SLL_STACK_POP(global_file_table.first_free_file_id);
  int f_id = file_id->id;
  File *file = &global_file_table.files_pool[f_id];
  file->node = node;
  file->ref_counter = 1;
  file->pool_id = f_id;
  if (flags & O_APPEND)
  {
    struct stat stat_buf = {0};
    VOP_STAT(node, &stat_buf);
    file->cursor = stat_buf.st_size;
  }
  global_file_table.files[f_id] = file;
  
  return res;
}

int 
sys_close(int fd)
{
  File *file = global_file_table.files[fd];
  if (--file->ref_counter == 0) 
  {
    vfs_close(file->node);
    file->node = NULL;
    file->offset = 0
  }

  FileID *file_id = &global_file_table.file_id_pool[file->pool_id];
  file->pool_id = -1;
  SLL_STACK_PUSH(global_file_table.first_free_file_id, file_id);
}

//struct vnode *cwd = curproc->p_cwd;

  - use existing VFS and vnodes and track filesystem state
  - gracefully handle all possibly erroneous inputs
  - error codes as per os161 man pages (leniant to particular error code)
userland/include/unistd.h -> kern/include/syscall.h
put our code in kern/syscall/file.c
kernel facing, e.g. assumed syscall exception handler called us


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

