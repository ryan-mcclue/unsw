#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement
import os
import sys
import platform
import pathlib
import subprocess

from dataclasses import dataclass

from urllib.parse import urlparse

import psycopg2

def warn(msg):
  print(msg)
  if __debug__:
    breakpoint()
    sys.exit()

def fatal_error(msg):
  print(msg)
  breakpoint()
  sys.exit()

global_cursor = None

def sql_execute(query, args):
  if __debug__:
    print(f"[ECHO-QUERY]: {global_cursor.mogrify(query, args)}")
  global_cursor.execute(query, args)

def main():
  print(f"python: {platform.python_version()} ({platform.version()})")

  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if sys.gettrace() is None:
    os.environ["PYTHONBREAKPOINT"] = "0"

  directory_of_running_script = pathlib.Path(__file__).parent.resolve()
  os.chdir(directory_of_running_script)

  try:
    db = None
    # NOTE(Ryan): Will set this env. variable on local machine to differentiate running on vxdb2
    local_db_pass = os.environ.get("LOCALDBPASS")
    if local_db_pass is None:
      db = "dbname=ass2"
    else:
      db_params = {
          "host": "localhost",
          "port": "5432",
          "dbname": "ass2",
          "user": "ryan",
          "password": local_db_pass,
      }
      db = psycopg2.extensions.make_dsn(db_params)

    connection = psycopg2.connect(db)
    global_cursor = connection.cursor()
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

  if len(sys.argv) < 2:
    fatal_error("Usage: ./{sys.argv[0]} abs-binary-path build_time flash_time flash-size ram-size arena-size loc")
  else:
    abs_binary_path = sys.argv[1]
    if not os.path.exists(abs_binary_path):
      fatal_error(f"No file found at {abs_binary_path}")
    print(get_top10_symbols(abs_binary_path))
    print(get_sizes(abs_binary_path))
    print(get_hashes())

if __name__ == "__main__": main()
