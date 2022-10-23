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
#include "messages.h"
#include "io.c"
#include "commands.c"

#define DEVICE_BLOCK_TIME_MS 10000

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
                
                clear_file("cse_edge_device_log.txt");
                clear_file("upload-log.txt");
                clear_file("deletion-log.txt");

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
                        char device_name[32] = {0};
                        u32 udp_port_num = 0;

                        while (true)
                        {
                          Message msg_request = {0}; 
                          readx(client_fd, &msg_request, sizeof(msg_request)); 

                          Message msg_response = {0};

                          switch (msg_request.type)
                          {
                            case AUTHENTICATION_REQUEST:
                            {
                              // TODO(Ryan): Perhaps allow passing in device name
                              // separately and checking if it's valid, then asking for password
                              //
                              // Only block if device name is valid?
                              strncpy(device_name, msg_request.device_name, sizeof(device_name));
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
                                  break;
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
                                udp_port_num = msg_request.udp_port_num;

                                char device_ip[INET_ADDRSTRLEN] = {0};
                                inet_ntop(AF_INET, &client_addr.sin_addr, device_ip, INET_ADDRSTRLEN);

                                shared_state->num_connected_devices++;

                                char timestamp[64] = {0};
                                populate_timestamp(timestamp, sizeof(timestamp));
                                // TODO(Ryan): Keep separate data structure containing active devices ordered by access time.
                                // Write this entirely out each time to simplify reordering on device deletion
                                // write_active_devices_to_log_file();
                                append_to_file("cse_edge_device_log.txt", "%d; %s; %s; %s; %d\n", 
                                               shared_state->num_connected_devices,
                                               timestamp, device_name, device_ip, udp_port_num);
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

                              writex(client_fd, &msg_response, sizeof(msg_response));

                              if (msg_response.type == AUTHENTICATION_RESPONSE &&
                                  (msg_response.authentication_status == AUTHENTICATION_REQUEST_BLOCKED ||
                                   msg_response.authentication_status == AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED))
                              {
                                exit(1);
                              }

                            } break;

                            case UED_REQUEST:
                            {
                              u32 byte_counter = 0;
                              void *file_mem = mallocx(msg_request.file_size);
                              u8 *file_cursor = file_mem;

                              memcpy(file_cursor, msg_request.contents, msg_request.contents_size);
                              byte_counter += msg_request.contents_size;

                              while (byte_counter != msg_request.file_size)
                              {
                                readx(client_fd, &msg_request, sizeof(msg_request)); 
                                memcpy(file_cursor, msg_request.contents, msg_request.contents_size);
                                byte_counter += msg_request.contents_size;
                              }

                              char file_name[256] = {0};
                              snprintf(file_name, sizeof(file_name), "server-%s-%d.txt", device_name, msg_request.file_id);

                              write_entire_file(file_name, file_mem, msg_request.file_size);

                              char timestamp[64] = {0};
                              populate_timestamp(timestamp, sizeof(timestamp));
                              append_to_file("upload-log.txt", "%s; %s; %d; %d\n", device_name,
                                             timestamp, msg_request.file_id, msg_request.file_size);

                              free(file_mem);

                              msg_response.type = UED_RESPONSE;
                              snprintf(msg_response.response, sizeof(msg_response.response),
                                  "Data file with ID of %d has been uploaded to server",
                                  msg_request.file_id);
                              writex(client_fd, &msg_response, sizeof(msg_response));

                            } break;

                            case SCS_REQUEST:
                            {
                              msg_response.type = SCS_RESPONSE;

                              char file_name[256] = {0};
                              snprintf(file_name, sizeof(file_name), "server-%s-%d.txt", 
                                       device_name, msg_request.file_identification);
                              if (access(file_name, F_OK) == 0)
                              {
                                ReadFileResult read_res = read_entire_file(file_name);  
                                if (read_res.contents != NULL)
                                {
                                  long int file_nums[1024] = {0};
                                  char num_str[16] = {0};

                                  u32 line_num = 0;
                                  char *at = (char *)read_res.contents;     
                                  while (at[0] != '\0')
                                  {
                                    consume_whitespace(&at);
                                    char *num_start = at;
                                    u32 num_len = consume_identifier(&at);

                                    memcpy(num_str, num_start, num_len);
                                    num_str[num_len] = '\0';
                                    
                                    file_nums[line_num++] = strtol(num_str, NULL, 10);

                                    consume_whitespace(&at);
                                  }

                                  u64 sum = 0, average = 0, min = UINT32_MAX, max = 0;

                                  for (u32 num_i = 0; num_i < line_num; ++num_i)
                                  {
                                    u32 val = file_nums[num_i];
                                    sum += val; 
                                    if (val > max) max = val;
                                    if (val < min) min = val;
                                  }
                                  average = sum / line_num;

                                  if (msg_request.computation_operation == SCS_REQUEST_SUM)
                                  {
                                    msg_response.computation_result = sum;
                                  }
                                  else if (msg_request.computation_operation == SCS_REQUEST_AVERAGE)
                                  {
                                    msg_response.computation_result = average;
                                  }
                                  else if (msg_request.computation_operation == SCS_REQUEST_MIN)
                                  {
                                    msg_response.computation_result = min;
                                  }
                                  else if (msg_request.computation_operation == SCS_REQUEST_MAX)
                                  {
                                    msg_response.computation_result = max;
                                  }

                                  free(read_res.contents);
                                }
                              }
                              else
                              {
                                msg_response.computation_result = -1;
                              }

                              writex(client_fd, &msg_response, sizeof(msg_response));

                            } break;
                            
                            case DTE_REQUEST:
                            {
                              msg_response.type = DTE_RESPONSE;

                              char file_name[256] = {0};
                              snprintf(file_name, sizeof(file_name), "server-%s-%d.txt", 
                                       device_name, msg_request.dte_file_id);
                              if (access(file_name, F_OK) == 0)
                              {
                                struct stat file_stat = {0};
                                if (stat(file_name, &file_stat) != -1)
                                {
                                  u32 file_size = file_stat.st_size;
                                  if (unlink(file_name) != -1)
                                  {
                                    char timestamp[64] = {0};
                                    populate_timestamp(timestamp, sizeof(timestamp));
                                    append_to_file("deletion-log.txt", "%s; %s; %d; %d\n", device_name,
                                        timestamp, msg_request.dte_file_id, file_size);

                                    msg_response.dte_response_code = 1;
                                  }
                                  else
                                  {
                                    FPRINTF(stderr, "Error: Unable to delete file %s (%s)\n", file_name, strerror(errno));
                                  }
                                }
                                else
                                {
                                  FPRINTF(stderr, "Error: Unable to stat file %s (%s)\n", file_name, strerror(errno));
                                }
                              }
                              else
                              {
                                msg_response.dte_response_code = -1;
                              }

                              writex(client_fd, &msg_response, sizeof(msg_response));
                               
                            } break;
                            

                            ASSERT_DEFAULT_CASE()
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
