// SPDX-License-Identifier: zlib-acknowledgement

// LOSS_RATE is percentage packets dropped
// AVERAGE_DELAY simulates delay (for when testing on same machine)

// sends 15 ping requests to the server. 
// Each message contains a payload of data that includes the keyword PING, 
// a sequence number starting from 3,331, and a timestamp. 
// After sending each packet, the client waits up to 600 ms to receive a reply. 
// If 600 ms goes by without a reply from the server, 
// (this 600ms should be larger than RTT determined from server AVERAGE_DELAY)
// then the client assumes that its packet or the server's reply packet has been lost 
// in the network. 



// ./PingClient host port
// output:
// ping to 127.0.0.1, seq = 1, rtt = 120 ms
// ping to 127.0.0.1, seq = 2, rtt = 'time out' 
//
// message format: (assume u32s)
// PING sequence_number time CRLF

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>

typedef uint32_t u32;

typedef struct __attribute__((packed))
{
  char ping[4];
  u32 seq_num;
  u32 time;
  char crlf[2]; 
} Msg;

int
main(int argc, char *argv[])
{
  if (argc != 3)
  {
    fprintf(stderr, "Usage: ./PingClient <server> <port>\n");
  }

  char server_ip[64] = {0};
  strncpy(server_ip, argv[1], sizeof(server_ip));

  long int server_port = strtol(argv[2], NULL, 10);

#define PING_COUNT 15
#define SEQ_START 3331
#define WAIT_FOR_RESPONSE_MS 600

  // set non-blocking
  int server_sock = socket(AF_INET, SOCK_DGRAM, 0);
  if (server_sock == -1)
  {
    fprintf(stderr, "Error: unable to open socket (%s)\n", s);
  }

    int opt_val = 1;
    if (setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, (void *)&opt_val, sizeof(opt_val)) == -1)
    {
      EBP();
    }

    struct sockaddr_in server_addr = {0};
    inet_pton(AF_INET, server_ip, &server_addr.sin_addr);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);

  server_socket = ;

  Msg msg = {0};
  msg.ping = "PING";
  msg.crlf = "\r\n";

  for (u32 ping_i = 0; ping_i < PING_COUNT; ++ping_i)
  {
    msg.seq_num = ping_i;
    msg.time = clock_gettime();

    int len = sendto(server_sock, &msg, sizeof(msg), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));

    u32 wait_time_ms = 0;

    n = recvfrom(server_sock, buffer, len, 0, &from, &length);
    // time sent is ms?
  }
    close(sock);


  return 0;
}
