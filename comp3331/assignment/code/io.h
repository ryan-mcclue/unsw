// SPDX-License-Identifier: zlib-acknowledgement
#pragma once

typedef struct 
{
  void *contents;
  u32 size;
} ReadFileResult;

typedef struct
{
  char name[64];
  char password[64];
} ClientCredential;

typedef struct
{
  ClientCredential credentials[64];
  u32 num_credentials;
} ClientCredentials;

