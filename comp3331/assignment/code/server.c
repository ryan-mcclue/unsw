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

#include "io.c"
#include "messages.h"

typedef struct
{
  u32 socket_handle;
  char device_name[32];
  char ip[32];
  u32 port;
  u32 p2p_port;
  char date_active[32];
} ConnectedClient;

#define MAX_CONNECTED_CLIENTS 32
GLOBAL ConnectedClient global_connected_clients[MAX_CONNECTED_CLIENTS];

#define FORK_CHILD_PID 0

int
main(int argc, char *argv[])
{
  if (argc == 3)
  {
    long int server_port = strtol(argv[1], NULL, 10);
    long int number_of_consecutive_failed_attempts = strtol(argv[2], NULL, 10);
    if (number_of_consecutive_failed_attempts > 0 && number_of_consecutive_failed_attempts < 6)
    {
      ClientCredentials client_credentials = parse_credentials("credentials.txt");
      if (client_credentials.num_credentials != 0)
      {
        // IMPORTANT(Ryan): This is the TCP welcoming socket. It will perform TCP handshake
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
                    if (fork_res == FORK_CHILD_PID)
                    {
                    }
                  }
                }
                else
                {
                  fprintf(stderr, "Error: unable to accept connection\n");
                }
              }
            }
            else
            {
              fprintf(stderr, "Error: unable to listen on socket\n");
            }
          }
          else
          {
            fprintf(stderr, "Error: unable to bind on socket\n");
          }
        }
        else
        {
          fprintf(stderr, "Error: unable to open socket\n");
        }
      }
      else
      {
        fprintf(stderr, "Error: invalid credentials file\n");
      }
    }
    else
    {
      fprintf(stderr, "Error: argument <number-of-consecutive-failed-attempts> must be between 1-5\n");
    }
  }
  else
  {
    fprintf(stderr, "Usage: ./server <port> <number-of-consecutive-failed-attempts>\n");
  }


  return 0;
}
