// SPDX-License-Identifier: zlib-acknowledgement
#include "io.h"

INTERNAL void
clear_file(const char *file_name)
{
  int file_fd = open(file_name, O_CREAT | O_TRUNC | O_WRONLY, 0666); 
  if (file_fd != -1) 
  {
    close(file_fd);
  }
  else
  {
    FPRINTF(stderr, "Error: unable to open file %s (%s)\n", file_name, strerror(errno));
  }
}

INTERNAL int 
__unlink_cb(const char *fpath, const struct stat *sb, int typeflag, struct FTW *ftwbuf)
{
  int rv = remove(fpath);

  if (rv == -1)
  {
    FPRINTF(stderr, "Error: Unable to remove path %s (%s)\n", fpath, strerror(errno));
  }

  return rv;
}

INTERNAL int 
rm_rf(char *path)
{
  return nftw(path, __unlink_cb, 64, FTW_DEPTH | FTW_PHYS);
}

INTERNAL void
clear_folder(char *path)
{
  if (access(path, F_OK) == 0)
  {
    rm_rf(path);
  }

  // IMPORTANT(Ryan): Executable important to enter
  mkdir(path, 0777);
}


INTERNAL void
write_entire_file(char *file_name, void *buf, u64 buf_size)
{
  int file_fd = open(file_name, O_CREAT | O_TRUNC | O_WRONLY, 0666); 
  if (file_fd != -1) 
  {
    u8 *byte_location = (u8 *)buf;
    u32 bytes_to_write = buf_size;

    while (bytes_to_write > 0) 
    {
      int write_res = write(file_fd, byte_location, bytes_to_write); 
      if (write_res != -1) 
      {
        bytes_to_write -= write_res;
        byte_location += write_res;
      }
      else
      {
        FPRINTF(stderr, "Error: unable to write file %s (%s)\n", file_name, strerror(errno));
        break;
      }
    }

    close(file_fd);
  }
  else
  {
    FPRINTF(stderr, "Error: unable to open file %s (%s)\n", file_name, strerror(errno));
  }
}

INTERNAL ReadFileResult
read_entire_file(char *file_name)
{
  ReadFileResult result = {0};

  int file_fd = open(file_name, O_RDONLY); 
  if (file_fd != -1) 
  {
    struct stat file_stat = {0};
    int fstat_res = fstat(file_fd, &file_stat);
    if (fstat_res != -1) 
    {
      result.contents = malloc(file_stat.st_size);
      if (result.contents != NULL)
      {
        result.size = file_stat.st_size;
        size_t bytes_to_read = file_stat.st_size;
        u8 *byte_location = (u8 *)result.contents;
        while (bytes_to_read > 0) 
        {
          int read_res = read(file_fd, byte_location, bytes_to_read); 
          if (read_res != -1) 
          {
            bytes_to_read -= read_res;
            byte_location += read_res;
          }
          else
          {
            FPRINTF(stderr, "Error: unable to read file %s (%s)\n", file_name, strerror(errno));
            free(result.contents);
            break;
          }
        }
      }
      else
      {
        FPRINTF(stderr, "Error: unable to malloc memory for file %s (%s)\n", file_name, strerror(errno));
      }
    }
    else
    {
      FPRINTF(stderr, "Error: unable to fstat file %s (%s)\n", file_name, strerror(errno));
    }
  }
  else
  {
    FPRINTF(stderr, "Error: unable to open file %s (%s)\n", file_name, strerror(errno));
  }
    
  return result;
}

INTERNAL void
append_to_file_buf(char *file_name, char *buf, u32 buf_len)
{
  int file_fd = open(file_name, O_CREAT | O_RDWR, 0666); 
  if (file_fd != -1) 
  {
    if (lseek(file_fd, 0, SEEK_END) != -1)
    {
      if (write(file_fd, buf, buf_len) != -1)
      {
        close(file_fd);
      }
      else
      {
        FPRINTF(stderr, "Error: unable to write to end of file %s (%s)\n", file_name, strerror(errno));
      }
    }
    else
    {
      FPRINTF(stderr, "Error: unable to lseek to end of file %s (%s)\n", file_name, strerror(errno));
    }
  }
  else
  {
    FPRINTF(stderr, "Error: unable to open/read file %s (%s)\n", file_name, strerror(errno));
  }
}

INTERNAL void
append_to_file(char *file_name, char *format, ...)
{
  int file_fd = open(file_name, O_CREAT | O_RDWR, 0666); 
  if (file_fd != -1) 
  {
    if (lseek(file_fd, 0, SEEK_END) != -1)
    {
      va_list args = {0};
      va_start(args, format);

      char append_buf[128] = {0};
      vsnprintf(append_buf, sizeof(append_buf), format, args); 

      if (write(file_fd, append_buf, strlen(append_buf)) != -1)
      {
        close(file_fd);
      }
      else
      {
        FPRINTF(stderr, "Error: unable to write to end of file %s (%s)\n", file_name, strerror(errno));
      }

      va_end(args);
    }
    else
    {
      FPRINTF(stderr, "Error: unable to lseek to end of file %s (%s)\n", file_name, strerror(errno));
    }
  }
  else
  {
    FPRINTF(stderr, "Error: unable to open/read file %s (%s)\n", file_name, strerror(errno));
  }
}

INTERNAL void
consume_whitespace(char **at)
{
  while (isspace((*at)[0]))
  {
    (*at)++;
  }
}

INTERNAL u32
consume_identifier(char **at)
{
  u32 result = 0;

  while (!isspace((*at)[0]) && (*at[0]) != '\0')
  {
    (*at)++;
    result++;
  }

  return result;
}

#define VERIFICATION_INVALID_CREDENTIALS 0
#define VERIFICATION_VALID_CREDENTIALS 1
#define VERIFICATION_INVALID_DEVICE_NAME 2

INTERNAL int
verify_credentials(ClientCredentials *credentials, char *device_name, char *password)
{
  int result = VERIFICATION_INVALID_CREDENTIALS;

  bool device_present = false;
  bool credentials_valid = false;

  for (u32 credential_i = 0; credential_i < credentials->num_credentials; ++credential_i)
  {
    ClientCredential credential = credentials->credentials[credential_i];
    if (strcmp(credential.name, device_name) == 0)
    {
      device_present = true;
      if (strcmp(credential.password, password) == 0)
      {
        credentials_valid = true;
        break;
      }
    }
  }
  
  if (device_present && credentials_valid)
  {
    result = VERIFICATION_VALID_CREDENTIALS;
  }
  else if (!device_present)
  {
    result = VERIFICATION_INVALID_DEVICE_NAME;
  }

  return result;
}

INTERNAL ClientCredentials
parse_credentials(char *credentials)
{
  ClientCredentials result = {0};

  ReadFileResult credentials_read = read_entire_file(credentials);
  if (credentials_read.contents != NULL)
  {
    char *credentials_at = (char *)credentials_read.contents;     

    while (credentials_at[0] != '\0')
    {
      ClientCredential *credential = &result.credentials[result.num_credentials];

      consume_whitespace(&credentials_at);
      char *name_start = credentials_at;
      u32 name_len = consume_identifier(&credentials_at);
      if (name_len != 0)
      {
        memcpy(credential->name, name_start, name_len);
        credential->name[name_len] = '\0';

        consume_whitespace(&credentials_at);
        char *password_start = credentials_at;
        u32 password_len = consume_identifier(&credentials_at);

        if (password_len != 0)
        {
          memcpy(credential->password, password_start, password_len);
          credential->password[password_len] = '\0';

          result.num_credentials++;
        }
        else
        {
          FPRINTF(stderr, "Error: expected password to follow device name in credentials.txt\n");
        }

        consume_whitespace(&credentials_at);
      }
      else
      {
        FPRINTF(stderr, "Error: expected device name to appear in credentials.txt\n");
      }
    }

    free(credentials_read.contents);
  }

  return result;
}


