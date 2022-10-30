// SPDX-License-Identifier: zlib-acknowledgement

#pragma once

#define AUTHENTICATION_REQUEST_SUCCESS 0
#define AUTHENTICATION_REQUEST_FAILED 1
#define AUTHENTICATION_REQUEST_BLOCKED 2
#define AUTHENTICATION_REQUEST_CURRENTLY_BLOCKED 3

#define SCS_REQUEST_SUM 0
#define SCS_REQUEST_AVERAGE 1
#define SCS_REQUEST_MAX 2
#define SCS_REQUEST_MIN 3

#define UVF_RESPONSE_DEVICE_ACTIVE 0
#define UVF_RESPONSE_DEVICE_NOT_ACTIVE 1

// NOTE(Ryan): mtu given by $(ifconfig), however could probably set to 65535 as using loopback
#define MTU 16384

typedef enum
{
  AUTHENTICATION_REQUEST,
  AUTHENTICATION_RESPONSE,

  UED_REQUEST,
  UED_RESPONSE,

  SCS_REQUEST,
  SCS_RESPONSE,

  DTE_REQUEST,
  DTE_RESPONSE,

  AED_REQUEST,
  AED_RESPONSE,

  OUT_REQUEST,
  OUT_RESPONSE,

  UVF_VERIFY,
  UVF_VERIFY_RESPONSE,
  UVF_REQUEST,
  UVF_RESPONSE,

} MESSAGE_TYPE;

typedef struct
{
  // IMPORTANT(Ryan): strcmp() cannot be used with NULL pointers, so this stack-string makes things easier
  char aed_device_name[32];
  char aed_ip[32];
  u32 aed_port;
  char aed_timestamp[64];
} AedResponse;

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

    // SCS
    struct
    {
      u64 computation_operation;
      u32 file_identification;
    };
    struct
    {
      s64 computation_result;
    };
    
    // AED
    struct
    {
      u32 aed_count;
      AedResponse aed_responses[64];
    };

    // OUT
    struct
    {
      char out_device_name[32];
    };

    // DTE
    struct
    {
      u32 dte_file_id;
    };
    struct
    {
      s32 dte_response_code;
    };
    
    // STRING RESPONSE
    struct
    {
      char response[128];
    };

    // UVF
    struct
    {
      char uvf_remote_device_name[64];
    };
    struct
    {
      s32 uvf_response;
      u32 uvf_response_port;
    };

    // UVF FILE SENDING
    struct
    {
      char uvf_device_name[32];
      char uvf_file_name[64];
      u32 uvf_file_size;
      u32 uvf_contents_size;
      // IMPORTANT(Ryan): CSE stack limit of 8192KB is plenty for our MTU
      char uvf_contents[MTU];
    };

    // UED FILE SENDING
    struct
    {
      u32 file_id;
      u32 file_size;
      u32 contents_size;
      // IMPORTANT(Ryan): CSE stack limit of 8192KB is plenty for our MTU
      char contents[MTU];
    };

    // ...
  };
} Message;

