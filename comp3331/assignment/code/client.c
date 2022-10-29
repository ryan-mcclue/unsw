
// TODO(Ryan):
// Both the client and server MUST print meaningful messages at the
// command prompt that capture the specific interactions taking place. You are free to choose the precise
// text that is displayed.

// TODO(Ryan): Are going to test automated? i.e. will have to use locks()?

// Commands:
// EDG (Edge Data Generation) which means the client side helps to generate data to simulate the data collection function in the real edge device, 
// UED (Upload Edge Data) it allows the edge device to upload a particular edge data file to the central server,
// SCS (Server Computation Service) the edge device can practice this command to request the server to
//do some basic computations on a particular data file, 
// DTE (Delete the data file (server side)), 
// AED (Active Edge Devices), request and display the active edge devices, OUT: exit this edge network, and
// UVF (Peer-to-peer Uploading Video Files)

#include "common.h"
#include "messages.h"
#include "io.c"
#include "commands.c"

INTERNAL Message
parse_command_buffer(char *command_buffer)
{
  Message result = {0};

  return result;
}

int
main(int argc, char *argv[])
{
#if defined(AUTOMATE)
  if (argc == 6)
#else
  if (argc == 4)
#endif
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

      // TODO(Ryan): For UVF have another thread
      // This is because recieving a file like this should not block incoming commands
      // However, don't have to implement case where device recieves two files simultaneously

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
          authentication_request.udp_port_num = client_udp_port;

#if defined(AUTOMATE)
          char *username = argv[4];
          memcpy(authentication_request.device_name, username, strlen(username));
          char *device_name = authentication_request.device_name;
          device_name[strcspn(device_name, "\n")] = '\0';
#else
          printf("Username: ");
          fgets(authentication_request.device_name, sizeof(authentication_request.device_name), stdin);
          char *device_name = authentication_request.device_name;
          device_name[strcspn(device_name, "\n")] = '\0';
#endif


          while (!have_authenticated)
          {
#if defined(AUTOMATE)
            char *password = argv[5];
            memcpy(authentication_request.password, password, strlen(password));
            password[strcspn(password, "\n")] = '\0';
#else
            printf("Password: ");
            fgets(authentication_request.password, sizeof(authentication_request.password), stdin);
            char *password = authentication_request.password;
            password[strcspn(password, "\n")] = '\0';
#endif

            writex(server_sock, &authentication_request, sizeof(authentication_request));

            Message authentication_response = {0};
            readx(server_sock, &authentication_response, sizeof(authentication_response));

            if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_SUCCESS)
            {
              printf("%s\n", authentication_response.response_message);
              have_authenticated = true; 
            }
            else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_FAILED)
            {
              printf("Invalid password. Please try again\n");
            }
            else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED)
            {
              printf("Your account is blocked due to multiple authentication failures. Please try again later\n");
              exit(1);
            }
            else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_BLOCKED)
            {
              printf("Invalid password. Your account has been blocked. Please try again\n");
              exit(1);
            }
          }

          bool want_to_run = true;
          while (want_to_run)
          {
            char command_buffer[1024] = {0};

            printf("Enter one of the following commands (EDG, UED, SCS, DTE, AED, UVF, OUT): ");
            fgets(command_buffer, sizeof(command_buffer), stdin);
            command_buffer[strcspn(command_buffer, "\n")] = '\0';

            Tokens tokens = split_into_tokens(command_buffer);
            if (tokens.num_tokens > 0)
            {
              char *command_name = tokens.tokens[0];

              if (strcmp(command_name, "EDG") == 0)
              {
                process_edg_command(&tokens, device_name);
              }
              else if (strcmp(command_name, "UED") == 0)
              {
                process_ued_command(&tokens, device_name, server_sock);
                // NOTE(Ryan): Filenames of those uploaded can be of any format we choose,
                // e.g could have same format as that of the server
              }
              else if (strcmp(command_name, "SCS") == 0)
              {
                process_scs_command(&tokens, device_name, server_sock);
              }
              else if (strcmp(command_name, "DTE") == 0)
              {
                process_dte_command(&tokens, device_name, server_sock);
              }
              else if (strcmp(command_name, "AED") == 0)
              {
                process_aed_command(&tokens, device_name, server_sock);
              }
              // TODO: could have working directories for each user from EDG command and subsequent UVF
              // This will first issue an AED command under the hood
              else if (strcmp(command_name, "UVF") == 0)
              {

              }
              else if (strcmp(command_name, "OUT") == 0)
              {
                process_out_command(&tokens, device_name, server_sock);
                want_to_run = false;
              }
              else
              {
                FPRINTF(stderr, "Error: Invalid command!\n");
              }
            }
          }

          exit(1);
        }
        else
        {
          FPRINTF(stderr, "Error: failed to connect (%s)\n", strerror(errno));
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
