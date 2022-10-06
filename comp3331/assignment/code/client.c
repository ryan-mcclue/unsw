
// Commands:
// EDG (Edge Data Generation) which means the client side helps to generate data to simulate the data collection function in the real edge device, 
// UED (Upload Edge Data) it allows the edge device to upload a particular edge data file to the central server,
// SCS (Server Computation Service) the edge device can practice this command to request the server to
//do some basic computations on a particular data file, 
// DTE (Delete the data file (server side)), 
// AED (Active Edge Devices), request and display the active edge devices, OUT: exit this edge network, and
// UVF (Peer-to-peer Uploading Video Files) (will need to implement reliable ordered messages)

#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
#error "This server is structured to only work on little-endian devices!"
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

#include "messages.h"

INTERNAL Message
parse_command_buffer(char *command_buffer)
{
  Message result = {0};

  return result;
}

int
main(int argc, char *argv[])
{
  if (argc == 4)
  {
    char server_ip[64] = {0};
    strncpy(server_ip, argv[1], sizeof(server_ip));

    long int server_port = strtol(argv[2], NULL, 10);
    long int client_udp_port = strtol(argv[3], NULL, 10);

    int server_sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (server_sock != -1)
    {
      int opt_val = 1;
      if (setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, (void *)&opt_val, 
            sizeof(opt_val)) == -1)
      {
        fprintf(stderr, "Warning: unable to set resuable socket (%s)\n", strerror(errno));
      }

      struct sockaddr_in server_addr = {0};
      if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) == 1)
      {
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(server_port);

        bool have_authenticated = false;

        Message authentication_request = {0};
        authentication_request.type = AUTHENTICATION_REQUEST;

        while (!have_authenticated)
        {
          // TODO(Ryan): Should this be sent from the server? Don't think so
          char username[64] = {0};
          printf("Username: ");
          fgets(authentication_request.username, sizeof(authentication_request.username), stdin);

          char password[64] = {0};
          printf("Password: ");
          fgets(authentication_request.password, sizeof(authentication_request.password), stdin);

          int send_len = sendto(server_sock, &authentication_request, sizeof(authentication_request), 0, 
              (struct sockaddr *)&server_addr, sizeof(server_addr));
          if (send_len == -1)
          {
            fprintf(stderr, "Error: sendto failed (%s)\n", strerror(errno));
            exit(1);
          }

          Message authentication_response = {0};
          u32 recv_len = recv(server_sock, &authentication_response, sizeof(authentication_response), 0);
          if (recv_len == -1)
          {
            fprintf(stderr, "Error: recv failed (%s)\n", strerror(errno));
            exit(1);
          }

          printf("%s\n", authentication_response.response_message);

          if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_SUCCESS)
          {
            have_authenticated = true; 
          }
          else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_BLOCKED)
          {
            return -1;
          }
        }

#if 0
        bool part_of_network = true;
        while (part_of_network)
        {
          printf("Enter one of the following commands (EDG, UED, SCS, DTE, AED, UVF, OUT): ");
          char command_buffer[128] = {0};
          fgets(command_buffer, sizeof(command_buffer), stdin);

          Message request_message = parse_command_buffer(command_buffer);
        }
#endif

      }
      else
      {
        fprintf(stderr, "Error: invalid IP address provided (%s)\n", strerror(errno));
      }
    }
    else
    {
      fprintf(stderr, "Error: unable to create server socket (%s)\n", strerror(errno));
    }

    // prompt_credentials()
    // send_authentication()
    // parse_return()
    // if (success)
    // {
    //   send_udp_port_num()
    //   prompt_for_command()
    // }
    
    // running a udp server concurrently
    // furthermore, new thread for client upload
  }
  else
  {
    fprintf(stderr, "Usage: ./client <server-ip> <server-port> <client-udp_port>\n");
  }
  // request_connection()
  // send_name_and_password() 
  // --> recieve welcome message and command listing prompt
  // send_p2p_udp_port_num()

  return 0;
}
