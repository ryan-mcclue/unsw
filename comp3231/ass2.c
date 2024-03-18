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
  off_t cursor;
  int open_flags;
  int ref_count;
  int memory_id;
};

typedef struct FileID FileID;
struct FileID
{
  FileID *next;
  int id;
};

typedef struct FileDescriptor FileDescriptor;
struct FileDescriptor
{
  FileDescriptor *next;
  int fd;
};

typedef struct FileTable
struct FileTable
{
  File *files[MAX_PATH];
  File files_memory[MAX_PATH];

  FileMemoryID file_memory_id_memory[MAX_PATH];
  FileMemoryID *first_free_file_memory_id;

  FileDescriptor file_descriptor_memory[MAX_PATH];
  FileDescriptor *first_free_file_descriptor;
};

FileTable global_file_table;

// boot()
for (int i = ARRAY_COUNT(global_file_table.file_descriptor_memory) - 1; 
     i >= 0; 
     i -= 1)
{
  // NOTE(Ryan): Reserved for stdout and stderr on startup
  if (i == 1 || i == 2) continue;

  FileDescriptor *fd = &global_file_table.file_descriptor_memory[i];
  fd->fd = i;
  SLL_STACK_PUSH(global_file_table.first_free_file_descriptor, fd);

  FileMemoryID *file_memory_id = &global_file_table.file_memory_id_memory[i];
  file_memory_id->id = i;
  SLL_STACK_PUSH(global_file_table.first_free_file_memory_id, file_memory_id);
}

bool
fd_is_open(int fd)
{
  return (fd >= 0 && fd < ARRAY_COUNT(global_file_table.files) && \
          global_file_table.files[fd] != NULL);
}

// runprogram()
int
attach_stdout_and_stderr(void)
{
  for (int i = 1; i < 3; i += 1)
  {
    char con_device[5] = "con:";
    struct vnode *node = NULL;
    int res = vfs_open(con_device, O_RDWR, 0, &node);
    if (res) return res;
    File *file = global_file_table.files[i];
    file = global_file_table.files_pool[i];
    file->node = node;
    file->open_flags = O_RDWR;
    file->ref_count = 1;
    file->memory_id = i;
  }

  return 0;
}
//

// kern/include/file.h, kern/syscall/file.c
int
sys_open(const char *filename, int flags, mode_t mode)
{
  if (filename == NULL) return EFAULT;
  if ((flags & (O_RDONLY | O_WRONLY | O_RDWR)) == 0 || \\
       !IS_POW2(flags) || (flags > O_APPEND)) return EINVAL;
  if (global_state.first_free_fd == NULL) return EMFILE;
  
  char consumed_filename[MAX_PATH] = {0};
  strncpy(consumed_filename, filename, sizeof(consumed_filename));

  struct vnode *node = NULL;
  int res = vfs_open(consumed_filename, flags, mode, &node);
  if (res) return res;

  FileDescriptor *file_descriptor = global_file_table.first_free_file_descriptor;
  SLL_STACK_POP(global_file_table.first_free_file_descriptor);

  FileMemoryID *file_memory_id = global_file_table.first_free_file_memory_id;
  SLL_STACK_POP(global_file_table.first_free_file_memory_id);

  File *file = global_file_table.files[file_descriptor->fd];
  file = global_file_table.files_memory[file_memory_id->id];
  file->node = node;
  file->open_flags = flags;
  file->ref_counter = 1;
  file->memory_id = file_memory_id->id;
  if (flags & O_APPEND)
  {
    struct stat stat_buf = {0};
    VOP_STAT(node, &stat_buf);
    file->cursor = stat_buf.st_size;
  }
  
  return res;
}

int 
sys_close(int fd)
{
  if (!fd_is_open(fd)) return EBADF;

  File *file = global_file_table.files[fd];
  if (--file->ref_counter == 0) 
  {
    vfs_close(file->node);

    FileMemoryID *file_memory_id = &global_file_table.file_memory_id_memory[file->memory_id];
    SLL_STACK_PUSH(global_file_table.first_free_file_memory_id, file_memory_id);

    file->node = NULL;
    file->cursor = 0;
    file->open_flags = 0;
    file->memory_id = -1;
    file = NULL;
  }

  FileDescriptor *file_descriptor = &global_file_table.file_descriptor_memory[fd];
  SLL_STACK_PUSH(global_file_table.first_free_file_descriptor, file_descriptor);
}

ssize_t 
sys_read(int fd, userptr_t buf, size_t buflen)
{
  if (!fd_is_open(fd)) return EBADF;

  File *file = global_file_table.files[fd];
  if (file->open_flags & O_RDONLY == 0) return EBADF;

  struct iovec iov = {0};
  struct uio ku = {0};
  uio_uinit(&iov, &ku, buf, buflen, file->cursor, UIO_READ);
  int res = VOP_READ(file->node, &ku);
  if (res) return res;

  // TODO: should ku.uio_resid != 0 give EIO?
  // read = (buflen - ku.uio_resid)

	ssize_t bytes = (ku.uio_offset - file->cursor);
	file->cursor = ku.uio_offset;

  return bytes;
}

ssize_t
sys_write(int fd, userptr buf, size_t nbytes)
{
  if (!fd_is_open(fd)) return EBADF;

  File *file = global_file_table.files[fd];
  if (file->open_flags & O_WRONLY == 0) return EBADF;

  struct iovec iov = {0};
  struct uio ku = {0};
  uio_uinit(&iov, &ku, buf, nbytes, file->cursor, UIO_WRITE);
  int res = VOP_WRITE(file->node, &ku);
  if (res) return res;

  // TODO: should ku.uio_resid != 0 give EIO?

	ssize_t bytes = (ku.uio_offset - file->cursor);
	file->cursor = ku.uio_offset;

  return bytes;
}

off_t 
sys_lseek(int fd, off_t pos, int whence)
{
  if (!fd_is_open(fd)) return EBADF;
  File *file = global_file_table.files[fd];

  if (!VOP_ISSEEKABLE(file->node)) return ESPIPE;

  off_t seek_pos = 0;
  switch (whence)
  {
    case SEEK_SET:
    {
      seek_pos = pos;
    } break;
    case SEEK_CUR:
    {
      seek_pos = file->cursor + pos;
    } break;
    case SEEK_END:
    {
      struct stat stat_buf = {0};
      VOP_STAT(file->node, &stat_buf);
      seek_pos = stat_buf.st_size + pos;
    } break;
    default:
    {
      return EINVAL;
    };
  }

  if (seek_pos < 0) return EINVAL;

  file->cursor = seek_pos;
  return file->cursor;
}

int 
sys_dup2(int oldfd, int newfd)
{
  if (!fd_is_open(newfd) && global_file_table.first_free_file_descriptor == NULL)
  {
    return EMFILE;
  }

  bool valid_newfd = fd_is_open(newfd);
  for (FileDescriptor *fd = global_file_table.first_free_file_descriptor;
      fd != NULL;
      fd = fd->next)
  {
    if (fd->fd == newfd) 
    {
      // TODO: remove this entry from free list (DLL queue required)
      valid_newfd = true;
      break;
    }
  }

  if (!valid_newfd || !fd_is_open(old)) return EBADF;

  if (fd_is_open(newfd)) 
  {
    sys_close(newfd);
    // NOTE(Ryan): Remove newfd from free list, as are going to use
    SLL_STACK_POP(global_file_table.first_free_file_descriptor);
  }

  File *file = global_file_table.files[oldfd];
  global_file_table.files[newfd] = file;

  file->ref_counter += 1;

  return newfd;
}

//struct vnode *cwd = curproc->p_cwd;

If too many files are open within a particular process, you should return EMFILE. 
If too many files are open systemwide, you should return ENFILE.
The per-process file descriptor table should be OPEN_MAX (128) in size. 

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

