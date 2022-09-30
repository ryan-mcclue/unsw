// SPDX-License-Identifier: zlib-acknowledgement

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <stdbool.h>

#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <fcntl.h>

#define INTERNAL static
#define GLOBAL static

typedef uint32_t u32;
typedef uint64_t u64;
typedef float r32;

typedef struct
{
  
} ReadFileResult;

INTERNAL ReadFileResult
read_entire_file(char *file_name)
{
  ReadFileResult result = {0};

  FILE *fp = fopen(file_name, "rb");
  if (fp != NULL)
  {
    int file_size = fseek(fp, 0, SEEK_END);
    result.memory = malloc();
  }

  return result;
}

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
                assert(strcmp(method, "GET") == 0);

                consume_whitespace(&at);
                char *uri = at; 
                u32 uri_len = consume_identifier(&at);
                memcpy(uri, uri_start, uri_len + 1);
                uri[uri_len] = '\0';

                ReadFileResult read_file = read_entire_file(uri);
                if (read_file.mem != NULL)
                {
                  char header[] = {
                    "HTTP/1.1 200 OK\r\n"
                    // "Content-Type: image/jpeg\r\n
                    // "Content-Length\r\n\r\n"
                    // TODO(Ryan): Can we get away with not sending Content-Type
                  };

                  write(client_fd, header, sizeof(header);
                  write(client_fd, read_file.mem, read_file.file_size);
                }
                else
                {
                  char html_404[64] = "HTTP/1.1 404 Not Found\r\n\r\n";
                  write(client_fd, html_404, sizeof(html_404));
                }
              }
              else
              {
                fprintf(stderr, "Error: failed to read bytes from client socket (%s)\n", strerror(errno));
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
