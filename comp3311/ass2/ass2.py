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

def sql_execute_all(query, args=[]):
  if __debug__:
    print(f"[ECHO-QUERY]: {global_cursor.mogrify(query, args)}")
  global_cursor.execute(query, args)
  return global_cursor.fetchall()

def sql(query, args=[]):
  for res in sql_execute_all(query, args):
    print(res)

# people id and zid
# Ass2:
# gened -> FREE#### (the # is any valid character based on given context)
# regex -> COMP[2468]###
# program --> bachelor of engineering, bachelor of computer science
# stream --> seng, embedded
#  OrgUnit --> 0 (unsw), faculties (science), schools (chemistry)
# Requirement (marks and amount of course types)
# people id and zid

# might do DFS on courses? e.g have buckets for each course type
# assume gen-ed first then go through and populate

def q1():
  print("#Locl  #Intl Proportion")
  # print(f"{TermCode} {Locals:6d} {Internationals:6d} {Proportion:6.1f}")

def main():
  print(f"python: {platform.python_version()} ({platform.version()})")

  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if sys.gettrace() is None:
    os.environ["PYTHONBREAKPOINT"] = "0"

  directory_of_running_script = pathlib.Path(__file__).parent.resolve()
  os.chdir(directory_of_running_script)

  try:
    global global_cursor
    db = None
    # NOTE(Ryan): Will set this env. variable on local machine to differentiate running on vxdb2
    local_db_pass = os.environ.get("LOCALDBPASS")
    if local_db_pass is None:
      db = "dbname=ass2"
    else:
      db = f"host=localhost, port=5432 dbname=ass2 user=ryan password={local_db_pass}"

    connection = psycopg2.connect(db)
    global_cursor = connection.cursor()

    sql('select * from students')



  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
