<!-- SPDX-License-Identifier: zlib-acknowledgement -->
// git clone https://z5346008@nw-syd-gitlab.cseunsw.tech/COMP3231/24T1/grp201-asst2.git asst2-src
// #include <kern/errno.h>
// userland/testbin/asst2/asst2.c
// for testing with ass2.c cd ~/cs3231/asst2-src && bmake && bmake install 

// syscall()
switch (callno)
{
  i64 retval = 0;

  // return values: copyout(&local, userptr_arg);
  // input: copyin()
  case SYS_open:
  {
    // int open(const char *filename, int flags);
    // int open(const char *filename, int flags, mode_t mode);
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

}
// TODO(Ryan): may need to vop_fsync() to flush? 

#define ARRAY_COUNT(a) (sizeof(a)/sizeof(a[0]))
#define IS_POW2_ALIGNED(x, p) (((x) & ((p) - 1)) == 0)
#define IS_POW2(x) IS_POW2_ALIGNED(x, x) 

#define __DLL_PUSH_FRONT(first, last, node, next, prev) \
(\
  ((first) == NULL) ? \
  (\
    ((first) = (last) = (node)), \
    ((node)->next = (node)->prev = NULL) \
  )\
  : \
  (\
    ((node)->prev = NULL), \
    ((node)->next = (first)), \
    ((first)->prev = (node)), \
    ((first) = (node)) \
  )\
)
#define DLL_PUSH_FRONT(first, last, node) \
  __DLL_PUSH_FRONT(first, last, node, next, prev)

#define __DLL_REMOVE(first, last, node, next, prev) \
(\
  ((node) == (first)) ? \
  (\
    ((first) == (last)) ? \
    (\
      ((first) = (last) = NULL) \
    )\
    : \
    (\
      ((first) = (first)->next), \
      ((first)->prev = NULL) \
    )\
  )\
  : \
  (\
    ((node) == (last)) ? \
    (\
      ((last) = (last)->prev), \
      ((last)->next = NULL) \
    )\
    : \
    (\
      ((node)->next->prev = (node)->prev), \
      ((node)->prev->next = (node)->next) \
    )\
  )\
)
#define DLL_REMOVE(first, last, node) \
  __DLL_REMOVE(first, last, node, next, prev) 

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
  int fmi;
};

typedef struct FileMemoryID FileMemoryID;
struct FileMemoryID
{
  FileMemoryID *next;
  int fmi;
};

typedef struct FileDescriptor FileDescriptor;
struct FileDescriptor
{
  FileDescriptor *next, *prev;
  int fd;
};

typedef struct FileTable
struct FileTable
{
  File *files[MAX_PATH];
  File files_memory[MAX_PATH];

  FileMemoryID fmi_memory[MAX_PATH];
  FileMemoryID *first_free_fmi;

  FileDescriptor fd_memory[MAX_PATH];
  FileDescriptor *first_free_fd, *last_free_fd;
};

FileTable global_file_table;

#define PUSH_FD(fd) \
  DLL_PUSH_FRONT(global_file_table.first_free_fd, global_file_table.last_free_fd, fd)
#define REMOVE_FD(fd) \
  DLL_REMOVE(global_file_table.first_free_fd, global_file_table.last_free_fd, fd)
#define PUSH_FMI(fmi) \
  SLL_STACK_PUSH(global_file_table.first_free_fmi, fmi);
#define POP_FMI() \
  SLL_STACK_POP(global_file_table.first_free_fmi);


// boot()
for (int i = ARRAY_COUNT(global_file_table.fd_memory) - 1; i >= 0; i -= 1)
{
  // NOTE(Ryan): Reserved for stdout and stderr on startup
  if (i == 1 || i == 2) continue;

  FileDescriptor *fd = &global_file_table.fd_memory[i];
  fd->fd = i;
  PUSH_FD(fd);

  FileMemoryID *fmi = &global_file_table.fmi_memory[i];
  fmi->id = i;
  PUSH_FMI(fmi)
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
    file = global_file_table.files_memory[i];
    file->node = node;
    file->open_flags = O_RDWR;
    file->ref_count = 1;
    file->fmi = i;
  }

  return 0;
}
//

// kern/include/file.h, kern/syscall/file.c
int
sys_open(const char *filename, int flags, mode_t mode, uint64_t *retval)
{
  if (filename == NULL) return EFAULT;
  if ((flags & (O_RDONLY | O_WRONLY | O_RDWR)) == 0 || \\
       !IS_POW2(flags) || (flags > O_APPEND)) return EINVAL;
  if (global_file_table.first_free_fd == NULL) return EMFILE;
  
  char consumed_filename[MAX_PATH] = {0};
  strncpy(consumed_filename, filename, sizeof(consumed_filename));

  struct vnode *node = NULL;
  int res = vfs_open(consumed_filename, flags, mode, &node);
  if (res) return -res;

  FileDescriptor *fd = global_file_table.first_free_fd;
  REMOVE_FD(fd)

  FileMemoryID *fmi = global_file_table.first_free_fmi;
  POP_FMI()

  File *file = global_file_table.files[fd->fd];
  file = global_file_table.files_memory[fmi->fmi];
  file->node = node;
  file->open_flags = flags;
  file->ref_counter = 1;
  file->fmi = fmi->fmi;
  if (flags & O_APPEND)
  {
    struct stat stat_buf = {0};
    VOP_STAT(node, &stat_buf);
    file->cursor = stat_buf.st_size;
  }

  *retval = fd->fd;
  return 0;
}

int 
sys_close(int fd)
{
  if (!fd_is_open(fd)) return EBADF;

  File *file = global_file_table.files[fd];
  if (--file->ref_counter == 0) 
  {
    vfs_close(file->node);

    FileMemoryID *fmi = &global_file_table.fmi_memory[file->fmi];
    FMI_PUSH(fmi);

    file->node = NULL;
    file->cursor = 0;
    file->open_flags = 0;
    file->fmi = -1;
    file = NULL;
  }

  FileDescriptor *fd = &global_file_table.fd_memory[fd];
  PUSH_FD(fd)

  return 0;
}

ssize_t 
sys_read(int fd, userptr_t buf, size_t buflen, uint64_t *retval)
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

	ssize_t bytes_read = (ku.uio_offset - file->cursor);
	file->cursor = ku.uio_offset;

  *retval = bytes_read;
  return 0;
}

ssize_t
sys_write(int fd, userptr buf, size_t nbytes, uint64_t *retval)
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

	ssize_t bytes_written = (ku.uio_offset - file->cursor);
	file->cursor = ku.uio_offset;

  *retval = bytes_written;
  return 0;
}

off_t 
sys_lseek(int fd, off_t pos, int whence, uint64_t *retval)
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

  *retval = file->cursor;
  return 0; 
}

int 
sys_dup2(int oldfd, int newfd, uint64_t *retval)
{
  if (!fd_is_open(newfd) && global_file_table.first_free_fd == NULL)
  {
    return EMFILE; // or ENFILE?
  }

  FileDescriptor *matching_newfd = NULL;
  for (FileDescriptor *fd = global_file_table.first_free_fd; fd != NULL; fd = fd->next)
  {
    if (fd->fd == newfd) 
    {
      matching_newfd = fd;
      REMOVE_FD(fd);
      break;
    }
  }

  if ((!fd_is_open(newfd) && matching_newfd == NULL) || !fd_is_open(old)) return EBADF;

  if (fd_is_open(newfd)) 
  {
    sys_close(newfd);
    // NOTE(Ryan): Remove newfd from free list, as still in use
    FileDescriptor *fd = global_file_table.first_free_fd;
    REMOVE_FD(fd);
  }

  File *file = global_file_table.files[oldfd];
  global_file_table.files[newfd] = file;

  file->ref_counter += 1;
  
  *retval = newfd;
  return 0;
}

//struct vnode *cwd = curproc->p_cwd;

If too many files are open within a particular process, you should return EMFILE. 
If too many files are open systemwide, you should return ENFILE.
The per-process file descriptor table should be OPEN_MAX (128) in size. 

//
IMPORTANT: basic assignment has only one process at a time (advanced implements fork())
- per process file descriptor data structure?
- across processes, e.g. open file table (only if advanced)
