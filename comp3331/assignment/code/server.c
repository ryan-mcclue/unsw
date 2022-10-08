// SPDX-License-Identifier: zlib-acknowledgement
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

#define DEVICE_BLOCK_TIME_MS 10000

INTERNAL u64
get_ms_epoch(void)
{
  u64 result = 0;

  struct timespec time_spec = {0};
  clock_gettime(CLOCK_MONOTONIC_RAW, &time_spec);

  result = (time_spec.tv_sec * 1000LL) + (time_spec.tv_nsec / 1000000.0f);

  return result;
}

typedef struct
{
  u8 *base;
  u32 size;
  u32 used;
} MemoryArena;

#define MEM_PUSH_STRUCT(arena, struct_name) \
  (struct_name *)(obtain_mem(arena, sizeof(struct_name)))

#define MEM_PUSH_ARRAY(arena, elem, len) \
  (elem *)(obtain_mem(arena, sizeof(elem) * (len)))

INTERNAL void *
obtain_mem(MemoryArena *arena, u32 size)
{
  void *result = NULL;

  assert(arena->used + size < arena->size);

  result = (u8 *)arena->base + arena->used;

  arena->used += size;

  return result;
}

#define KILOBYTES(n) ((n) * 1024UL)
#define MEGABYTES(n) (KILOBYTES(n) * 1024UL)

typedef struct
{
  volatile bool is_blocked;
  volatile char name[64];
  u64 prev_time_blocked_ms_epoch;
  u64 time_blocked_ms;
} BlockedDevice;

#define MAX_BLOCKED_DEVICES 32
typedef struct
{
  BlockedDevice *devices;
  u32 circular_index;
} BlockedDevices;

typedef struct
{
  BlockedDevices blocked_devices;
  u32 num_connected_devices;
} SharedState;

INTERNAL SharedState *
init_shared_state(u32 max_size)
{
  SharedState *result = NULL;

  void *shared_memory = mmap(NULL, max_size, PROT_READ | PROT_WRITE, 
                             MAP_SHARED | MAP_ANONYMOUS, -1, 0);
  if (shared_memory != NULL)
  {
    MemoryArena memory_arena = {0}; 
    memory_arena.base = shared_memory;
    memory_arena.size = max_size;

    result = MEM_PUSH_STRUCT(&memory_arena, SharedState);
    result->blocked_devices.devices = MEM_PUSH_ARRAY(&memory_arena, BlockedDevice, MAX_BLOCKED_DEVICES);
    result->blocked_devices.circular_index = 0; 
  }
  else
  {
    FPRINTF(stderr, "Error: unable to mmap shared (%s)\n", strerror(errno));
  }

  return result;
}

INTERNAL void
populate_timestamp(char *timestamp, u32 timestamp_size)
{
  time_t cur_time = time(NULL);
  struct tm *lt = localtime(&cur_time);

  char *month = NULL;
  switch (lt->tm_mon)
  {
    case 0: month = "January"; break;
    case 1: month = "Febuary"; break;
    case 2: month = "March"; break;
    case 3: month = "April"; break;
    case 4: month = "May"; break;
    case 5: month = "June"; break;
    case 6: month = "July"; break;
    case 7: month = "August"; break;
    case 8: month = "September"; break;
    case 9: month = "October"; break;
    case 10: month = "November"; break;
    case 11: month = "December"; break;
  }

  snprintf(timestamp, timestamp_size, "%02d %s %d %02d:%02d:%02d", lt->tm_mday, month, 
           1900 + lt->tm_year, lt->tm_hour, lt->tm_min, lt->tm_sec); 
}

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
          if (fcntl(server_sock, F_SETFL, O_NONBLOCK) != -1)
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
                SharedState *shared_state = init_shared_state(MEGABYTES(8));
                assert(shared_state != NULL);

                while (true)
                {
                  struct sockaddr_in client_addr = {0}; 
                  u32 client_size = sizeof(client_addr);
                  int client_fd = accept(server_sock, (struct sockaddr *)&client_addr, &client_size);
                  if (client_fd != -1)
                  {
                    int cur_flags = fcntl(client_fd, F_GETFL, 0);
                    assert(cur_flags != -1);
                    cur_flags &= ~O_NONBLOCK;
                    assert(fcntl(client_fd, F_SETFL, cur_flags) != -1);

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

                        u32 failed_device_connection_attempts = 0;

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

                              msg_response.type = AUTHENTICATION_RESPONSE;

                              for (u32 blocked_device_i = 0; 
                                  blocked_device_i < MAX_BLOCKED_DEVICES;
                                  blocked_device_i++)
                              {
                                BlockedDevice *blocked_device = &shared_state->blocked_devices.devices[blocked_device_i];

                                if ((strcmp((const char *)blocked_device->name, device_name) == 0) &&
                                     blocked_device->is_blocked)
                                {
                                  msg_response.authentication_status = AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED;
                                }
                              }

                              if (msg_response.authentication_status == AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED)
                              {
                                break;
                              }

                              if (verify_credentials(&client_credentials, device_name, password))
                              {
                                msg_response.authentication_status = AUTHENTICATION_REQUEST_SUCCESS;
                                strncpy(msg_response.response_message, "Welcome!", sizeof(msg_response.response_message));

                                char device_ip[INET_ADDRSTRLEN] = {0};
                                inet_ntop(AF_INET, &client_addr.sin_addr, device_ip, INET_ADDRSTRLEN);

                                shared_state->num_connected_devices++;

                                // 1; 30 September 2022 10:31:13; supersmartwatch; 129.64.31.13; 5432
                                // append_to_file("cse_edge_device_log.txt", );

                                // recieve_UDP_port_number()
                                //
                                // Active edge device sequence number; timestamp; edge device name; edge
                                // device IP address; edge device UDP server port number
                              }
                              else
                              {
                                failed_device_connection_attempts++;
                                if (failed_device_connection_attempts == number_of_consecutive_failed_attempts)
                                {
                                  msg_response.authentication_status = AUTHENTICATION_REQUEST_BLOCKED;

                                  u32 *blocked_device_index = &shared_state->blocked_devices.circular_index;
                                  BlockedDevice *blocked_device = &shared_state->blocked_devices.devices[*blocked_device_index];
                                  blocked_device->is_blocked = true;
                                  blocked_device->prev_time_blocked_ms_epoch = get_ms_epoch();
                                  strncpy((char * restrict)blocked_device->name, device_name, sizeof(blocked_device->name));

                                  if (*blocked_device_index + 1 == MAX_BLOCKED_DEVICES)
                                  {
                                    // IMPORTANT(Ryan): Locked increments here, but
                                    // we know devices aren't going to be blocked close together
                                    *blocked_device_index = 0;
                                  }
                                  else
                                  {
                                    *blocked_device_index++;
                                  }

                                }
                                else
                                {
                                  msg_response.authentication_status = AUTHENTICATION_REQUEST_FAILED;
                                }
                              }
                            } break;

                            ASSERT_DEFAULT_CASE()
                          }

                          writex(client_fd, &msg_response, sizeof(msg_response));

                          if (msg_response.type == AUTHENTICATION_RESPONSE &&
                              (msg_response.authentication_status == AUTHENTICATION_REQUEST_BLOCKED ||
                               msg_response.authentication_status == AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED))
                          {
                            exit(1);
                          }
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
                    if (errno != EWOULDBLOCK)
                    {
                      FPRINTF(stderr, "Error: unable to accept connection\n");
                    }
                    else
                    {
                      BlockedDevices *blocked_devices = &shared_state->blocked_devices;

                      for (u32 blocked_device_i = 0; 
                           blocked_device_i < MAX_BLOCKED_DEVICES;
                           blocked_device_i++)
                      {
                        BlockedDevice *blocked_device = &blocked_devices->devices[blocked_device_i];

                        if (blocked_device->is_blocked)
                        {
                          printf("device %s currently blocked for: %lu \n", blocked_device->name, blocked_device->time_blocked_ms);

                          u64 prev_time_blocked_ms_epoch = blocked_device->prev_time_blocked_ms_epoch;
                          u64 cur_ms_epoch = get_ms_epoch();
                          u64 time_to_add_ms = cur_ms_epoch - prev_time_blocked_ms_epoch;

                          blocked_device->time_blocked_ms += time_to_add_ms;

                          blocked_device->prev_time_blocked_ms_epoch = cur_ms_epoch;

                          if (blocked_device->time_blocked_ms >= DEVICE_BLOCK_TIME_MS)
                          {
                            blocked_device->is_blocked = false;
                            blocked_device->prev_time_blocked_ms_epoch = 0;
                            blocked_device->time_blocked_ms = 0;
                          }
                        }
                      }
                    }
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
            FPRINTF(stderr, "Error: unable to set server socket as non-blocking (%s)\n", strerror(errno));
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
