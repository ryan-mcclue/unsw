#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track proportion of overseas students
import os
import sys
import platform
import pathlib
import subprocess
import re
import pprint
import psycopg2

from operator import attrgetter
from dataclasses import dataclass
from collections import OrderedDict
from urllib.parse import urlparse

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

def sql_execute_all(query, args=[], log=True):
  if log:
    print(f"[ECHO-QUERY]: {global_cursor.mogrify(query, args).decode('utf-8')}")
  global_cursor.execute(query, args)
  return global_cursor.fetchall()

def sql(query, args=[], log=True):
  for res in sql_execute_all(query, args, log):
    print(res)

def q1():
  q = '''
    select t.starting, s.status, count(distinct s.id)
    from students s 
    join program_enrolments pe on (pe.student = s.id)
    join terms t on (t.id = pe.term)
    where t.starting between '2019-02-18' and '2023-09-11'
    group by s.status, t.starting
    order by t.starting, s.status
  '''

  student_counts = sql_execute_all(q, [], False)
  terms = ["19T1", "19T2", "19T3", 
           "20T0", "20T1", "20T2", "20T3",
           "21T0", "21T1", "21T2", "21T3",
           "22T0", "22T1", "22T2", "22T3",
           "23T0", "23T1", "23T2", "23T3"]
  i = 0
  intl_count = 0
  local_count = 0
  cur_starting = student_counts[0][0]
  print("Term  #Locl  #Intl Proportion")
  for res in student_counts:
    starting = res[0]
    if starting != cur_starting:
      proportion = 0
      if intl_count != 0:
        proportion = local_count / intl_count
      print(f"{terms[i]} {local_count:6d} {intl_count:6d} {proportion:6.1f}")
      
      cur_starting = starting
      local_count = 0
      intl_count = 0

      i += 1

    if res[1] == 'INTL':
      intl_count = res[2]
    else:
      local_count += res[2]

  # NOTE(Ryan): Print final row
  proportion = 0
  if intl_count != 0:
    proportion = local_count / intl_count
  print(f"{terms[i]} {local_count:6d} {intl_count:6d} {proportion:6.1f}")

def main():
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

    q1()
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
