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

          char *device_name = NULL;

          bool username_entered = false;
          bool username_valid = false;

          while (!have_authenticated)
          {
            if (!username_valid)
            {
              username_entered = false;
              while (!username_entered)
              {
#if defined(AUTOMATE)
                char *username = argv[4];
                memcpy(authentication_request.device_name, username, strlen(username));
                device_name = authentication_request.device_name;
                device_name[strcspn(device_name, "\n")] = '\0';
#else
                printf("Username: ");
                fgets(authentication_request.device_name, sizeof(authentication_request.device_name), stdin);
                device_name = authentication_request.device_name;
                device_name[strcspn(device_name, "\n")] = '\0';
#endif
                username_entered = strlen(device_name);
              }
            }

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
            else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_DEVICE_NAME_INVALID)
            {
              printf("Invalid device name. Please try again\n");
            }
            else if (authentication_response.authentication_status == AUTHENTICATION_REQUEST_FAILED)
            {
              printf("Invalid password. Please try again\n");
              username_valid = true;
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

          // IMPORTANT(Ryan): This only recieves files
          pid_t fork_res = fork();
          if (fork_res == -1)
          {
            FPRINTF(stderr, "Error: failed to fork udp listener (%s)\n", strerror(errno));
          }
          else
          {
            if (fork_res == 0)
            {
              int exit_on_parent_close = prctl(PR_SET_PDEATHSIG, SIGTERM); 
              if (exit_on_parent_close == -1)
              {
                FPRINTF(stderr, "Warning: failed to set exit child on parent exit (%s)\n", strerror(errno));
              }

              int uvf_sock = socket(AF_INET, SOCK_DGRAM, 0);
              if (uvf_sock != -1)
              {
                int opt_val = 1;
                if (setsockopt(uvf_sock, SOL_SOCKET, SO_REUSEADDR, (void *)&opt_val, 
                      sizeof(opt_val)) == -1)
                {
                  FPRINTF(stderr, "Warning: unable to set resuable socket (%s)\n", strerror(errno));
                }

                struct sockaddr_in uvf_addr = {0};
                uvf_addr.sin_family = AF_INET;
                uvf_addr.sin_addr.s_addr = INADDR_ANY;
                uvf_addr.sin_port = htons(client_udp_port);

                if (bind(uvf_sock, (struct sockaddr *)&uvf_addr, sizeof(uvf_addr)) != -1)
                {
                  clear_folder(device_name);

                  while (true)
                  {
                    Message uvf_request = {0};  

                    readx(uvf_sock, &uvf_request, sizeof(uvf_request));

                    u32 byte_counter = 0;
                    void *file_mem = mallocx(uvf_request.uvf_file_size);
                    u8 *file_cursor = file_mem;

                    memcpy(file_cursor, uvf_request.uvf_contents, uvf_request.uvf_contents_size);
                    byte_counter += uvf_request.uvf_contents_size;

                    while (byte_counter != uvf_request.uvf_file_size)
                    {
                      file_cursor = file_mem + byte_counter;

                      readx(uvf_sock, &uvf_request, sizeof(uvf_request)); 
                      memcpy(file_cursor, uvf_request.uvf_contents, uvf_request.uvf_contents_size);
                      byte_counter += uvf_request.uvf_contents_size;
                    }

                    char file_name[128] = {0};
                    snprintf(file_name, sizeof(file_name), "%s/%s_%s", device_name, 
                             uvf_request.uvf_device_name, uvf_request.uvf_file_name);

                    write_entire_file(file_name, file_mem, uvf_request.uvf_file_size);

                    free(file_mem);

                    printf("Recieved %s from %s\n", file_name, uvf_request.uvf_device_name);
                    printf("Enter one of the following commands (EDG, UED, SCS, DTE, AED, UVF, OUT): ");
                    // IMPORTANT(Ryan): stdout is interactive, so line-buffered.
                    // ∴ require flushing to output as no new line entered
                    fflush(stdout);
                  }
                }
                else
                {
                  FPRINTF(stderr, "Error: failed to bind on udp socket (%s)\n", strerror(errno));
                }
              }
              else
              {
                FPRINTF(stderr, "Error: unable to create udp socket (%s)\n", strerror(errno));
              }
            }
          }

          srand(time(NULL));

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
              else if (strcmp(command_name, "UVF") == 0)
              {
                process_uvf_command(&tokens, device_name, server_sock);
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
        }
        else
        {
          FPRINTF(stderr, "Error: failed to connect (%s)\n", strerror(errno));
        }
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
  }
  else
  {
    FPRINTF(stderr, "Usage: ./client <server-ip> <server-port> <client-udp_port>\n");
  }

  return 0;
}
