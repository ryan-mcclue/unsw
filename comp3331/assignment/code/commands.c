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
process_edg_command(Tokens *tokens, char *device_name, Message *msg_response)
{
  if (tokens->num_tokens == 3)
  {
    long int file_id = strtol(tokens->tokens[1], NULL, 10);
    if (file_id != -1)
    {
      long int data_amount = strtol(tokens->tokens[2], NULL, 10);
      if (data_amount != -1)
      {
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

        strncpy(msg_response->response, "Success: EDG command processed", sizeof(msg_response->response));
      }
      else
      {
        strncpy(msg_response->response, "Error: EDG command expects dataAmount to be an integer", sizeof(msg_response->response));
      }
    }
    else
    {
      strncpy(msg_response->response, "Error: EDG command expects fileID to be an integer", sizeof(msg_response->response));
    }
  }
  else
  {
    strncpy(msg_response->response, "Error: EDG command expects fileID and dataAmount arguments", sizeof(msg_response->response));
  }
}

INTERNAL void
process_command(char *command_buffer, char *device_name, Message *msg_response)
{
  Tokens tokens = split_into_tokens(command_buffer);

  char *command_name = tokens.tokens[0];

  if (strcmp(command_name, "EDG") == 0)
  {
    process_edg_command(&tokens, device_name, msg_response);
  }
  else if (strcmp(command_name, "UED") == 0)
  {
    // NOTE(Ryan): Filenames of those uploaded can be of any format we choose,
    // e.g could have same format as that of the server
  }
  else if (strcmp(command_name, "SCS") == 0)
  {

  }
  else if (strcmp(command_name, "DTE") == 0)
  {

  }
  else if (strcmp(command_name, "AED") == 0)
  {

  }
  else if (strcmp(command_name, "UVF") == 0)
  {

  }
  else if (strcmp(command_name, "OUT") == 0)
  {

  }
  else
  {
    strncpy(msg_response->response, "Error: Invalid command!", sizeof(msg_response->response));
  }
}
