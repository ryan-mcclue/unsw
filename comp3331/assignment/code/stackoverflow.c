// SPDX-License-Identifier: zlib-acknowledgement

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>

#include <sys/wait.h>
#include <unistd.h>

int
main(int argc, char *argv[])
{
  char username[32] = {0};
  printf("Username: ");
  fgets(username, sizeof(username), stdin);
  username[strcspn(username, "\n")] = '\0';

  char password[32] = {0};
  printf("Password: ");
  fgets(password, sizeof(password), stdin);
  password[strcspn(password, "\n")] = '\0';

  printf("\nWelcome!\n");

  char command_buffer[1024] = {0};
  pid_t fork_res = fork();
  if (fork_res == -1)
  {
    fprintf(stderr, "Error: failed to fork client (%s)\n", strerror(errno));
  }
  else
  {
    if (fork_res == 0)
    {
      while (1)
      {
        printf("Enter one of the following commands (EDG, UED, SCS, DTE, AED, UVF, OUT): ");
        if (fgets(command_buffer, sizeof(command_buffer), stdin) == NULL)
        {
          printf("null in child\n");
        }
      }
    }
    else
    {
      wait(NULL);
    }
  }

  return 0;
}
