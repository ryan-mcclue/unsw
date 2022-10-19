// SPDX-License-Identifier: zlib-acknowledgement

#pragma once

#define AUTHENTICATION_REQUEST_SUCCESS 0
#define AUTHENTICATION_REQUEST_FAILED 1
#define AUTHENTICATION_REQUEST_BLOCKED 2
#define AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED 3

// NOTE(Ryan): mtu given by $(ifconfig), however could probably set to 65535 as using loopback
#define MTU 32768

typedef enum
{
  AUTHENTICATION_REQUEST,
  AUTHENTICATION_RESPONSE,

  UED_REQUEST,
  UED_RESPONSE,

} MESSAGE_TYPE;

typedef struct
{
  MESSAGE_TYPE type;
  union
  {
    // AUTHENTICATION
    struct
    {
      // TODO(Ryan): Increase size to accomodate largest length names think they will test
      char device_name[32];
      char password[32];
      u32 udp_port_num;
    };
    struct
    {
      u32 authentication_status;
      char response_message[128];
    };

    // FILE SENDING
    struct
    {
      u32 packet_i;
      u32 file_size;
      u32 contents_size;
      // IMPORTANT(Ryan): CSE stack limit of 8192KB is plenty for our MTU of 64KB
      char contents[MTU];
    };

    // ...
  };
} Message;

