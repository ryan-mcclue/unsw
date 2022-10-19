// SPDX-License-Identifier: zlib-acknowledgement
#pragma once

typedef struct
{
  char tokens[8][64];
  u32 num_tokens;
} Tokens;

INTERNAL Tokens
split_into_tokens(char *buffer)
{
  Tokens result = {0};

  char *at = buffer;

  u32 token_i = 0;
  while (*at != '\0')
  {
    consume_whitespace(&at); 
    char *token_start = at;
    u32 token_len = consume_identifier(&at);
    memcpy(result.tokens[token_i], token_start, token_len);
    result.tokens[token_i][token_len] = '\0';

    token_i++;
  }

  result.num_tokens = token_i;

  return result;
}

INTERNAL void
process_edg_command(Tokens *tokens, char *device_name)
{
  if (tokens->num_tokens == 3)
  {
    long int file_id = strtol(tokens->tokens[1], NULL, 10);
    if (file_id != -1)
    {
      long int data_amount = strtol(tokens->tokens[2], NULL, 10);
      if (data_amount != -1)
      {
        FPRINTF(stderr, "The edge device is generating %ld data samples\n", data_amount);
        
        char file_name[64] = {0}; 
        snprintf(file_name, sizeof(file_name), "%s-%ld.txt", device_name, file_id);

        char data[1024] = {0};
        u32 data_cursor = 0;
        u32 data_seed = 0x12345678;
        for (u32 i = 0; i < data_amount; ++i)
        {
          data_seed ^= (u32)get_ms_epoch();
          data_cursor += snprintf(data + data_cursor, sizeof(data) - data_cursor,
                                  "%d\n", data_seed);
        }

        write_entire_file(file_name, data, data_cursor);

        FPRINTF(stderr, "Data generation done, %ld data samples have been generated and stored in the file %s\n", data_amount, file_name);
      }
      else
      {
        FPRINTF(stderr, "Error: EDG command expects dataAmount to be an integer\n");
      }
    }
    else
    {
      FPRINTF(stderr, "Error: EDG command expects fileID to be an integer\n");
    }
  }
  else
  {
    FPRINTF(stderr, "Error: EDG command expects fileID and dataAmount arguments\n");
  }
}

INTERNAL void
process_ued_command(Tokens *tokens, const char *device_name)
{
  if (tokens->num_tokens == 2)
  {
    long int file_id = strtol(tokens->tokens[1], NULL, 10);
    if (file_id != -1)
    {
      char file_name[128] = {0};
      snprintf(file_name, sizeof(file_name), "%s-%ld.txt", device_name, file_id);
      if (access(file_name, F_OK) == 0)
      {

      }
      else
      {
        FPRINTF(stderr, "Error: UED command cannot find file %s to upload\n", file_name);
      }
    }
    else
    {
      FPRINTF(stderr, "Error: UED command expects fileID to be an integer\n");
    }
  }
  else
  {
    FPRINTF(stderr, "Error: UED command expects fileID as an argument\n");
  }
}
