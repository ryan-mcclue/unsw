// SPDX-License-Identifier: zlib-acknowledgement
#pragma once

#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#error "This program is structured to only work on little-endian devices!"
#endif

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

typedef uint8_t u8;
typedef uint32_t u32;
typedef uint64_t u64;
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
