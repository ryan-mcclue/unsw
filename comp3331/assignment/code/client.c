
// Commands:
// EDG (Edge Data Generation) which means the client side helps to generate data to simulate the data collection function in the real edge device, 
// UED (Upload Edge Data) it allows the edge device to upload a particular edge data file to the central server,
// SCS (Server Computation Service) the edge device can practice this command to request the server to
//do some basic computations on a particular data file, 
// DTE (Delete the data file (server side)), 
// AED (Active Edge Devices), request and display the active edge devices, OUT: exit this edge network, and
// UVF (Peer-to-peer Uploading Video Files) (will need to implement reliable ordered messages)

#include "common.h"
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
      if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) == 1)
      {
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(server_port);

        if (connect(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) != -1)
        {
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

            int bytes_sent = write(server_sock, &authentication_request, sizeof(authentication_request));
            if (bytes_sent == -1)
            {
              FPRINTF(stderr, "Error: write failed (%s)\n", strerror(errno));
              exit(1);
            }
          }
        }
        else
        {
          FPRINTF(stderr, "Error: failed to connect (%s)\n", strerror(errno));
        }


#if 0
          Message authentication_response = {0};
          int bytes_read = read(server_sock, &authentication_response, sizeof(authentication_response));
          if (bytes_read == -1)
          {
            FPRINTF(stderr, "Error: read failed (%s)\n", strerror(errno));
            exit(1);
          }

          printf("%s\n", authentication_response.response_message);

          if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_SUCCESS)
          {
            have_authenticated = true; 
          }
          else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_FAILED)
          {

          }
          else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_BLOCKED)
          {

          }
#endif

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
        FPRINTF(stderr, "Error: invalid IP address provided (%s)\n", strerror(errno));
      }
    }
    else
    {
      FPRINTF(stderr, "Error: unable to create server socket (%s)\n", strerror(errno));
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
    FPRINTF(stderr, "Usage: ./client <server-ip> <server-port> <client-udp_port>\n");
  }
  // request_connection()
  // send_name_and_password() 
  // --> recieve welcome message and command listing prompt
  // send_p2p_udp_port_num()

  return 0;
}
