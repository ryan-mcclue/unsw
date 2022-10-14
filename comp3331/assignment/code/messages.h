// SPDX-License-Identifier: zlib-acknowledgement

#pragma once

#define AUTHENTICATION_REQUEST_SUCCESS 0
#define AUTHENTICATION_REQUEST_FAILED 1
#define AUTHENTICATION_REQUEST_BLOCKED 2
#define AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED 3

typedef enum
{
  AUTHENTICATION_REQUEST,
  AUTHENTICATION_RESPONSE,

  COMMAND_REQUEST,
  COMMAND_RESPONSE,

} MESSAGE_TYPE;

typedef struct
{
  MESSAGE_TYPE type;
  union
  {
    // AUTHENTICATION
    struct
    {
      char device_name[32];
      char password[32];
      u32 udp_port_num;
    };
    struct
    {
      u32 authentication_status;
      char response_message[128];
    };

    // COMMAND
    struct
    {
      char buffer[128];
    };
    struct
    {
      char response[128];
    };

    // ...
  };
} Message;

// NOTE(Ryan): mtu given by $(ifconfig), however could probably set to 65535 as using loopback
#define MTU 1500
typedef struct
{
  u32 file_size;
  u32 contents_size;
  char contents[1024];
} FileMessage;
