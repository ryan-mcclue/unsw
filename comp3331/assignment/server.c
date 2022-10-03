// SPDX-License-Identifier: zlib-acknowledgement
//
// authentication
//
// fork() copies memory (however, optimisation is copy-on-write making vfork() obsolete)
// clone() is actual syscall allowing for sharing memory and execution space (file desriptors etc.)
//
// message logging
//
// authenticate() 'credentials.txt'

// record_connection() 'edge-device-log.txt'
// Active edge device sequence number; timestamp; edge device name; edge
// device IP address; edge device UDP server port number
// 1; 30 September 2022 10:31:13; supersmartwatch; 129.64.31.13; 5432

#define DEVICE_BLOCK_TIME_SEC 10

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

typedef struct
{
  u32 socket_handle;
  char device_name[32];
  char ip[32];
  u32 port;
  char date_active[32];
} ConnectedClient;

#define MAX_CONNECTED_CLIENTS 32
GLOBAL ConnectedClient global_connected_clients[MAX_CONNECTED_CLIENTS];

typedef struct
{
  char name[64];
  char password[64];
} ClientCredential;
typedef struct
{
  ClientCredential credentials[64];
  u32 num_credentials;
} ClientCredentials;


typedef struct 
{
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

INTERNAL ClientCredentials
parse_credentials(void)
{
  ClientCredentials result = {0};

  ReadFileResult credentials_read = read_entire_file("credentials.txt");
  if (credentials_read.contents != NULL)
  {
    char *credentials_at = (char *)credentials_read.contents;     

    while (credentials_at[0] != '\0')
    {
      consume_whitespace(&credentials_at);
      char *name_start = credentials_at;
      consume_alpha(&credentials_at);
      char *name_end = credentials_at - 1;
      // strcpy

      consume_whitespace(&credentials_at);
      char *password_start = credentials_at;
      consume_alpha(&credentials_at);
      char *password_end = credentials_at - 1;
    }

    free(credentials_read.contents);
  }

  return result;
}

int
main(int argc, char *argv[])
{
  if (argc == 3)
  {
    long int server_port = strtol(argv[1], NULL, 10);
    long int number_of_consecutive_failed_attempts = strtol(argv[2], NULL, 10);

    ClientCredentials client_credentials = parse_credentials();
    if (client_credentials.num_credentials != 0)
    {

    }
    else
    {
      fprintf(stderr, "Error: invalid credentials.txt\n");
    }
#if 0
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
        u32 max_num_connections = 100;
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
#if 0
                  child
                  if (client_is_authenticated())
                  {
                    send_command_menu()
                    wait_for_command()
                    parse_command()
                  }
                  else
                  {
                    parse_authentication()
                  }
#endif
                }
              }

              char tmp_buf[4096] = {0};
              char method[8] = {0};
              char uri[128] = {0};
              int bytes_read = read(client_fd, tmp_buf, sizeof(tmp_buf));
              if (bytes_read != -1)
              { 
                tmp_buf[bytes_read] = '\0';
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
#endif
  }
  else
  {
    fprintf(stderr, "Usage: ./server <port> <number-of-consecutive-failed-attempts>\n");
  }


  return 0;
}




#if 0
int
main(int argc, char *argv[])
{
  if (argc == 2)
  {
    int port = argv[1]; 
    int failed_authentication_attempts_lim = argv[2]; // 1-5

"Invalid number of allowed failed consecutive attempts: number. The valid value of argument number is an integer between 1 and 5"
  }
  else
  {
  }

  return 0;
}
#endif
