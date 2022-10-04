// SPDX-License-Identifier: zlib-acknowledgement

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <stdbool.h>
#include <ctype.h>
#include <assert.h>

#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#define INTERNAL static
#define GLOBAL static

typedef uint8_t u8;
typedef uint32_t u32;
typedef uint64_t u64;
typedef float r32;

typedef struct {
  void *contents;
  u32 size;
} ReadFileResult;

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
            fprintf(stderr, "Error: unable to read file %s (%s)\n", file_name, strerror(errno));
            free(result.contents);
            break;
          }
        }
      }
      else
      {
        fprintf(stderr, "Error: unable to malloc memory for file %s (%s)\n", file_name, strerror(errno));
      }
    }
    else
    {
      fprintf(stderr, "Error: unable to fstat file %s (%s)\n", file_name, strerror(errno));
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

  while (isalnum((*at)[0]) || (*at)[0] == ':' || (*at)[0] == '-' || (*at)[0] == '/' ||
         (*at)[0] == '.')
  {
    (*at)++;
    result++;
  }

  return result;
}

// TODO(Ryan): Gracefully shut-down inactive: 
// SO_RCVTIMEOUT on the socket and when you get read() returning -1 with errno == EAGAIN/EWOULDBLOCK, timeout hit

int
main(int argc, char *argv[])
{
  if (argc == 2)
  {
    long int server_port = strtol(argv[1], NULL, 10);

    int server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock != -1)
    {
      int opt_val = 1;
      if (setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, (void *)&opt_val, 
            sizeof(opt_val)) == -1)
      {
        fprintf(stderr, "Warning: unable to set resuable socket (%s)\n", strerror(errno));
      }

      struct sockaddr_in server_addr = {0};
      server_addr.sin_family = AF_INET;
      server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
      server_addr.sin_port = htons(server_port);

      if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) != -1)
      {
        u32 max_num_connections = 1;
        if (listen(server_sock, max_num_connections) != -1)
        {
          while (true)
          {
            struct sockaddr_in client_addr = {0}; 
            u32 client_size = sizeof(client_addr);
            int client_fd = accept(server_sock, (struct sockaddr *)&client_addr, &client_size);
            if (client_fd != -1)
            {
              pid_t fork_res = fork();
              if (fork_res == -1)
              {
                fprintf(stderr, "Error: failed to fork client (%s)\n", strerror(errno));
              }
              else
              {
                if (fork_res == 0)
                {
                  while (true)
                  {
                    char tmp_buf[4096] = {0};
                    char method[8] = {0};
                    char uri[128] = {0};
                    int bytes_read = read(client_fd, tmp_buf, sizeof(tmp_buf));
                    if (bytes_read != -1)
                    { 
                      tmp_buf[bytes_read] = '\0';

                      char *at = tmp_buf;
                      consume_whitespace(&at);

                      char *method_start = at; 
                      u32 method_len = consume_identifier(&at);
                      memcpy(method, method_start, method_len + 1);
                      method[method_len] = '\0';
                      printf("method: %s\n", method);
                      assert(strcmp(method, "GET") == 0);

                      consume_whitespace(&at);
                      char *uri_start = at; 
                      u32 uri_len = consume_identifier(&at);
                      memcpy(uri, uri_start, uri_len + 1);
                      uri[uri_len] = '\0';

                      printf("uri: %s\n", uri);

                      char resource_type[16] = {0};

                      char *resource_ptr = uri;
                      if (strcmp(uri, "/") == 0)
                      {
                        resource_ptr = "index.html";
                        strncpy(resource_type, "text/html", sizeof(resource_type));
                      }
                      else
                      {
                        char file_extension[8] = {0};

                        char *file_extension_at = uri;
                        while (file_extension_at[0] != '.' && file_extension_at[0] != '\0')
                        {
                          file_extension_at++;
                        }
                        if (file_extension_at[0] != '\0')
                        {
                          u32 file_extension_len = 0;
                          while (file_extension_at[0] != '\0')
                          {
                            file_extension_at++;
                            file_extension_len++;
                          }

                          memcpy(file_extension, file_extension_at - file_extension_len + 1, file_extension_len + 1);
                          file_extension[file_extension_len] = '\0';

                          printf("file extension: %s\n", file_extension);

                          if (strcmp(file_extension, "html") == 0)
                          {
                            strncpy(resource_type, "text/html", sizeof(resource_type));
                          }
                          if (strcmp(file_extension, "png") == 0)
                          {
                            strncpy(resource_type, "image/png", sizeof(resource_type));
                          }
                          if (strcmp(file_extension, "jpg") == 0 || strcmp(file_extension, "jpeg") == 0)
                          {
                            strncpy(resource_type, "image/jpeg", sizeof(resource_type));
                          }

                        }
                        resource_ptr++;
                      }

                      ReadFileResult read_file = read_entire_file(resource_ptr);
                      if (read_file.contents != NULL)
                      {
                        char header[256] = {0};
                        int header_size = snprintf(header, sizeof(header), "HTTP/1.1 200 OK\r\nContent-Type: %s\r\nContent-Length: %d\r\n\r\n", resource_type, read_file.size);

                        write(client_fd, header, header_size);
                        write(client_fd, read_file.contents, read_file.size);

                        free(read_file.contents);
                      }
                      else
                      {
                        char html_404[128] = {0};
                        // NOTE(Ryan): Choose not to pass Connection: Close for persistence
                        int html_404_size = snprintf(html_404, sizeof(html_404), "HTTP/1.1 404 Not Found\r\nContent-Length: 9\r\n\r\nNot Found");
                        write(client_fd, html_404, html_404_size);
                      }
                    }
                    else
                    {
                      fprintf(stderr, "Error: failed to read bytes from client socket (%s)\n", strerror(errno));
                    }
                  }
                }
              }
            }
            else
            {
              fprintf(stderr, "Error: failed to accept connection (%s)\n", strerror(errno));
            }
          }
        }
        else
        {
          fprintf(stderr, "Error: unable to listen for connections (%s)\n", strerror(errno));
        }
      }
      else
      {
        fprintf(stderr, "Error: unable to bind socket (%s)\n", strerror(errno));
      }
    }
    else
    {
      fprintf(stderr, "Error: unable to open socket (%s)\n", strerror(errno));
    }
  }
  else
  {
    fprintf(stderr, "Usage: ./WebServer <port>\n");
  }


  return 0;
}
