// SPDX-License-Identifier: zlib-acknowledgement

typedef enum
{
  AUTHENTICATION_REQUEST,
  AUTHENTICATION_RESPONSE,


} MESSAGE_TYPE;

#define AUTHENTICATION_REQUEST_SUCCESS 0
#define AUTHENTICATION_REQUEST_FAILED 1
#define AUTHENTICATION_REQUEST_BLOCKED 2

typedef struct
{
  MESSAGE_TYPE type;
  union
  {
    struct
    {
      char username[32];
      char password[32];
    };
    struct
    {
      u32 authentication_status;
      char response_message[128];
    };

  };
} Message;
