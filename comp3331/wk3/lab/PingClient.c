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

#define WAIT_FOR_RESPONSE_MS 600
#define PING_COUNT 15
#define SEQ_START 3331

#define INTERNAL static

typedef uint32_t u32;
typedef uint64_t u64;
typedef float r32;

typedef struct __attribute__((packed))
{
  // IMPORTANT(Ryan): Add 2 here for space (snprintf() adds '\0')
  char ping[4 + 2];
  char seq_num[4 + 2];
  char time[32];
  char crlf[2]; 
} Msg;

INTERNAL u64
get_ms(void)
{
  u64 result = 0;

  struct timespec time_spec = {0};
  clock_gettime(CLOCK_MONOTONIC, &time_spec);

  result = (time_spec.tv_sec * 1000LL) + (time_spec.tv_nsec / 1000000.0f);

  return result;
}

int
main(int argc, char *argv[])
{
  if (argc == 3)
  {
    char server_ip[64] = {0};
    strncpy(server_ip, argv[1], sizeof(server_ip));

    long int server_port = strtol(argv[2], NULL, 10);

    int server_sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (server_sock != -1)
    {
      if (fcntl(server_sock, F_SETFL, O_NONBLOCK) != -1)
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

          Msg msg = {0};
          strncpy(msg.ping, "PING ", sizeof(msg.ping));
          strncpy(msg.crlf, "\r\n", sizeof(msg.crlf));

          u32 packets_ms[PING_COUNT] = {0};
          u32 successful_packets = 0;

          for (u32 ping_i = 0; ping_i < PING_COUNT; ++ping_i)
          {
            snprintf(msg.seq_num, sizeof(msg.seq_num), "%d ", SEQ_START + ping_i);
            snprintf(msg.time, sizeof(msg.time), "%ld", get_ms());

            int send_len = sendto(server_sock, &msg, sizeof(msg), 0, 
                (struct sockaddr *)&server_addr, sizeof(server_addr));
            // TODO(Ryan): Should we retry sending data?
            if (send_len == -1)
            {
              fprintf(stderr, "Error: sendto failed (%s)\n", strerror(errno));
            }

            u64 wait_time_ms = 0;
            int recv_len = 0;
            char recv_buf[64] = {0};
            u64 start_ms = get_ms();
            bool got_response = false;
            while (wait_time_ms < WAIT_FOR_RESPONSE_MS)
            {
              // IMPORTANT(Ryan): No need to distinguish src with recvfrom()
              recv_len = recv(server_sock, recv_buf, sizeof(recv_buf), 0);
              if (recv_len == -1)
              {
                if (errno == EAGAIN)
                {
                  u64 cur_ms = get_ms();
                  wait_time_ms += (cur_ms - start_ms);
                  start_ms = cur_ms;
                  //printf("waited %d ms\n", wait_time_ms);
                }
                else
                {
                  fprintf(stderr, "Error: recv() call failed (%s)\n", strerror(errno));
                }
              }
              else
              {
                got_response = true;
                break;
              }
            }

            // TODO(Ryan): In reality, rtt would be msg.time - time_gotten_back
            if (got_response)
            {
              packets_ms[successful_packets++] = wait_time_ms;
              printf("ping to %s, seq = %d, rtt = %ld ms\n", server_ip, ping_i + 1, wait_time_ms);
            }
            else
            {
              printf("ping to %s, seq = %d, rtt = 'time out'\n", server_ip, ping_i + 1);
            }
          }

          u32 packets_ms_sum = 0;
          u32 packets_ms_min = UINT32_MAX;
          u32 packets_ms_max = 0;
          for (u32 packet_i = 0; packet_i < successful_packets; ++packet_i)
          {
            u32 packet_ms_value = packets_ms[packet_i];

            if (packet_ms_value > packets_ms_max)
            {
              packets_ms_max = packet_ms_value;
            }

            if (packet_ms_value < packets_ms_min)
            {
              packets_ms_min = packet_ms_value;
            }

            packets_ms_sum += packet_ms_value; 
          }

          printf("min. rtt: %d ms, max. rtt: %d ms, avg. rtt: %.2f ms\n", packets_ms_min, 
                 packets_ms_max, (r32)packets_ms_sum / successful_packets);
        }
        else
        {
          fprintf(stderr, "Error: invalid server IP provided (%s)\n", strerror(errno));
        }
      }
      else
      {
        fprintf(stderr, "Error: unable to set non-blocking socket (%s)\n", strerror(errno));
      }
    }
    else
    {
      fprintf(stderr, "Error: unable to open socket (%s)\n", strerror(errno));
    }
  }
  else
  {
    fprintf(stderr, "Usage: ./PingClient <server> <port>\n");
  }


  return 0;
}
