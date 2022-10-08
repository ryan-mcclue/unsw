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

#include "common.h"
#include "io.c"
#include "messages.h"

#define DEVICE_BLOCK_TIME_SEC 10

typedef struct
{
  char device_name[64];
} ConnectedClient;

typedef struct
{
  ConnectedClient clients[32];
  u32 num_clients;
} ConnectedClients;

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
        ConnectedClients connected_clients = {0};

        // IMPORTANT(Ryan): This is the TCP welcoming socket. It will perform TCP handshake
        int server_sock = socket(AF_INET, SOCK_STREAM, 0);
        if (server_sock != -1)
        {
          int opt_val = 1;
          if (setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, (void *)&opt_val, 
                sizeof(opt_val)) == -1)
          {
            FPRINTF(stderr, "Warning: unable to set resuable socket (%s)\n", strerror(errno));
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
                    FPRINTF(stderr, "Error: failed to fork client (%s)\n", strerror(errno));
                  }
                  else
                  {
                    if (fork_res == FORK_CHILD_PID)
                    {
                      int exit_on_parent_close = prctl(PR_SET_PDEATHSIG, SIGTERM); 
                      if (exit_on_parent_close == -1)
                      {
                        FPRINTF(stderr, "Warning: failed to set exit child on parent exit (%s)\n", strerror(errno));
                      }

                      while (true)
                      {
                        Message msg_request = {0}; 
                        readx(client_fd, &msg_request, sizeof(msg_request)); 

                        Message msg_response = {0};

                        switch (msg_request.type)
                        {
                          case AUTHENTICATION_REQUEST:
                          {
                            char *device_name = msg_request.device_name;
                            char *password = msg_request.password;

                            // check_if_device_blocked()

                            msg_response.type = AUTHENTICATION_RESPONSE;

                            if (verify_credentials(&client_credentials, device_name, password))
                            {
                              msg_response.authentication_status = AUTHENTICATION_REQUEST_SUCCESS;
                              strncpy(msg_response.response_message, "Welcome!", sizeof(msg_response.response_message));
                              
                              ConnectedClient *cur_client = &connected_clients.clients[connected_clients.num_clients];
                              strncpy(cur_client->device_name, device_name, sizeof(cur_client->device_name));

                              connected_clients.num_clients++;
                              // recieve_UDP_port_number()
                              //
                              // Active edge device sequence number; timestamp; edge device name; edge
                              // device IP address; edge device UDP server port number
                              // 1; 30 September 2022 10:31:13; supersmartwatch; 129.64.31.13; 5432
                              // write_to_device_log("cse_edge_device_log.txt")
                            }
                            else
                            {
                              msg_response.authentication_status = AUTHENTICATION_REQUEST_FAILED;
                            }
                          } break;

                          ASSERT_DEFAULT_CASE()
                        }
                        
                        writex(client_fd, &msg_response, sizeof(msg_response));
                      }
                    }
                    else
                    {
                      #if 0
                        // IMPORTANT(Ryan): This will close on child exit. 
                        // Necessary, as GDB is only controlling the child process
                        // Otherwise will may get a zombie/defunct (process isn't running, just exists in process table) process as
                        // 'parent' process will not close this 'child' properly
                        
                        int child_status = 0;
                        pid_t wait_ret = wait(&child_status);
                        if (wait_ret == -1)
                        {
                          FPRINTF(stderr, "Error: wait failed\n");
                        }
                        exit(1);
                      #endif
                    }
                  }
                }
                else
                {
                  FPRINTF(stderr, "Error: unable to accept connection\n");
                }
              }
            }
            else
            {
              FPRINTF(stderr, "Error: unable to listen on socket\n");
            }
          }
          else
          {
            FPRINTF(stderr, "Error: unable to bind on socket\n");
          }
        }
        else
        {
          FPRINTF(stderr, "Error: unable to open socket\n");
        }
      }
      else
      {
        FPRINTF(stderr, "Error: invalid credentials file\n");
      }
    }
    else
    {
      FPRINTF(stderr, "Error: argument <number-of-consecutive-failed-attempts> must be between 1-5\n");
    }
  }
  else
  {
    FPRINTF(stderr, "Usage: ./server <port> <number-of-consecutive-failed-attempts>\n");
  }


  return 0;
}
