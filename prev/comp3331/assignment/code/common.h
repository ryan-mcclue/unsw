// SPDX-License-Identifier: zlib-acknowledgement
#pragma once

#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#error "This program is structured to only work on little-endian devices!"
#endif

#define _XOPEN_SOURCE 500
#define _GNU_SOURCE

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <assert.h>
#include <signal.h>
#include <stdarg.h>

#include <ftw.h>

#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/prctl.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>

#define INTERNAL static
#define GLOBAL static

#define ASSERT_DEFAULT_CASE() default: { assert(!"UNREACHABLE DEFAULT CASE"); }

#define ARRAY_LEN(arr) \
  (sizeof(arr) / sizeof(arr[0]))

typedef uint8_t u8;
typedef uint32_t u32;
typedef int32_t s32;
typedef uint64_t u64;
typedef int64_t s64;
typedef float r32;

INTERNAL u64
get_ms_epoch(void)
{
  u64 result = 0;

  struct timespec time_spec = {0};
  clock_gettime(CLOCK_MONOTONIC_RAW, &time_spec);

  result = (time_spec.tv_sec * 1000LL) + (time_spec.tv_nsec / 1000000.0f);

  return result;
}

INTERNAL void
FPRINTF(FILE *stream, char *format, ...)
{
  va_list args = {0};
  va_start(args, format);

  vfprintf(stderr, format, args);

  va_end(args);
}

INTERNAL void
writex(int fd, void *buf, size_t count)
{
  int bytes_written = write(fd, buf, count);
  if (bytes_written == -1)
  {
    FPRINTF(stderr, "Error: write failed (%s)\n", strerror(errno));
    exit(1);
  }
  if (bytes_written != count)
  {
    FPRINTF(stderr, "Warning: write failed to write all bytes (%s)\n", strerror(errno));
  }
}

INTERNAL void
sendtox(int sockfd, void *buf, u32 len, int flags, struct sockaddr *dest_addr, socklen_t addrlen)
{
  int bytes_written = sendto(sockfd, buf, len, flags, dest_addr, addrlen);
  if (bytes_written == -1)
  {
    FPRINTF(stderr, "Error: sendto failed (%s)\n", strerror(errno));
    exit(1);
  }
}

INTERNAL void
readx(int fd, void *buf, size_t count)
{
  int bytes_read = read(fd, buf, count);
  if (bytes_read == -1)
  {
    FPRINTF(stderr, "Error: read failed (%s)\n", strerror(errno));
    exit(1);
  }
}

INTERNAL void *
mallocx(size_t size)
{
  void *result = NULL;

  result = malloc(size);
  if (result == NULL)
  {
    FPRINTF(stderr, "Error: malloc failed (%s)\n", strerror(errno));
    exit(1);
  }

  return result;
}
