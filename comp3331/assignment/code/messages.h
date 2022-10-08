// SPDX-License-Identifier: zlib-acknowledgement

#pragma once

#define AUTHENTICATION_REQUEST_SUCCESS 0
#define AUTHENTICATION_REQUEST_FAILED 1
#define AUTHENTICATION_REQUEST_BLOCKED 2

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
