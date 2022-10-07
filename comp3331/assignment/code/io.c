// SPDX-License-Identifier: zlib-acknowledgement
#include "io.h"

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
    
  return result;
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

INTERNAL bool
verify_credentials(ClientCredentials *credentials, char *username, char *password)
{
  bool result = false;

  for (u32 credential_i = 0; credential_i < credentials->num_credentials; ++credential_i)
  {
    ClientCredential credential = credentials->credentials[credential_i];
    if (strcmp(credential.name, username) == 0 && strcmp(credential.password, password) == 0)
    {
      result = true;
      break;
    }
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
