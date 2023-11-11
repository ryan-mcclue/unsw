#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... print list of rules for a program or stream
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

@dataclass
class Requirement:
  name: str
  minimum: int
  maximum: int
  acad: str
  counter: int
  rid: int

def get_ordered_requirements(stream_code, program_code, raw=False):
  reqs = []
  if stream_code:
    q = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, r.id
      from requirements r
      join streams s on (r.for_stream = s.id)
      where s.code = %s
    '''
    stream_requirements = sql_execute_all(q, [stream_code], False)
    reqs += stream_requirements
  if program_code:
    q = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, r.id
      from requirements r
      join programs p on (r.for_program = p.id)
      where p.code = %s
    '''
    program_requirements = sql_execute_all(q, [program_code], False)
    reqs += program_requirements

  requirements = OrderedDict()
  # NOTE(Ryan): Required for q3
  requirements['uoc'] = []

  requirements['stream'] = []
  requirements['core'] = []
  requirements['elective'] = []
  requirements['gened'] = []
  requirements['free'] = []

  for r in reqs:
    name = r[0]
    r_type = r[1]
    acad = r[2]
    rid = int(r[5])
    maximum = 0
    minimum = 0

    if r_type == 'core':
      minimum = len(acad.split(','))
      maximum = minimum
    elif raw:
      minimum = r[3]
      maximum = r[4]
    else:
      if r[3]:
        minimum = int(r[3])
      maximum = r[4]
      if not maximum:
        maximum = minimum

    r = Requirement(name, minimum, maximum, acad, 0, rid)

    requirements[r_type] += [r]

  requirements['stream'] = sorted(requirements['stream'], key=attrgetter('rid'))
  requirements['core'] = sorted(requirements['core'], key=attrgetter('rid'))
  requirements['elective'] = sorted(requirements['elective'], key=attrgetter('rid'))
  requirements['gened'] = sorted(requirements['gened'], key=attrgetter('rid'))
  requirements['free'] = sorted(requirements['free'], key=attrgetter('rid'))

  return requirements

def q3(code="ACCTAH"):
  stream_name = ""
  stream_code = ""
  program_name = ""
  program_code = ""

  if len(code) == 6:
    q = 'select s.name from streams s where s.code = %s limit 1'
    res = sql_execute_all(q, [code], False)
    if len(res) == 0:
      print(f"Invalid stream code {code}")
      return
    else:
      stream_name = res[0][0]
      stream_code = code
  elif len(code) == 4:
    q = 'select p.name from programs p where p.code = %s limit 1'
    res = sql_execute_all(q, [code], False)
    if len(res) == 0:
      print(f"Invalid program code {code}")
      return
    else:
      program_name = res[0][0]
      program_code = code
  else:
    print("Invalid code")
    return

  requirements = get_ordered_requirements(stream_code, program_code, True)

  if stream_name:
    print(f"{code} {stream_name}")
  else:
    print(f"{code} {program_name}")

  print("Academic Requirements: ")

  for req_name, reqs in requirements.items():
    for r in reqs:
      req_str = ""
      if r.minimum and not r.maximum:
        req_str = f"at least {r.minimum}"
      elif not r.minimum and r.maximum:
        req_str = f"up to {r.maximum}"
      elif r.minimum and r.maximum:
        if r.minimum < r.maximum:
          req_str = f"between {r.minimum} and {r.maximum}"
        elif r.minimum == r.maximum:
          req_str = f"{r.minimum}"

      if req_name == "uoc":
        req_str += " UOC" 
        if r.name == "Total UOC":
          print(f"Total UOC {req_str}")
        else:
          print(f"{req_str} from {r.name}")
      elif req_name == "stream":
        req_str += " stream" 
        print(f"{req_str} from {r.name}")
        print_acad(r.acad, [])
      elif req_name == "core":
        print(f"all courses from {r.name}")
        print_acad(r.acad, [])
      elif req_name == "gened":
        print(f"{req_str} UOC of General Education")
      elif req_name == "free":
        print(f"{req_str} UOC of {stream_code} Free Electives")
      elif req_name == "elective":
        print(f"{req_str} UOC courses from {r.name}")
        print(f"- {r.acad}")

def get_course_name(code):
  q = '''
      select s.name from streams s
      where s.code = %s
   '''
  res = sql_execute_all(q, [code], False)

  if len(res) == 0:
    q = '''
        select s.title from subjects s
        where s.code = %s
    '''
    return sql_execute_all(q, [code], False)[0][0]
  else:
    return res[0][0]

def print_acad(acad, completed):
  for acad_token in acad.split(','):
    if acad_token[0] == '{':
      acad_plain = acad_token.strip('{}')
      stream_codes = acad_plain.split(';')
      stream_names = []
      for stream_code in stream_codes:
        if stream_code in completed:
          break
        else:
          stream_names += [get_course_name(stream_code)]
      final_str = ""
      for i in range(len(stream_names)):
        final_str += f"{stream_codes[i]} {stream_names[i]} or "
      if final_str:
        print(f"- {final_str[:-4]}")
    else:
      if acad_token not in completed:
        stream_name = get_course_name(acad_token)
        print(f"- {acad_token} {stream_name}")

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

    usage = f"Usage: {sys.argv[0]} (ProgramCode|StreamCode)"
    argc = len(sys.argv)
    if argc < 2:
      print(usage)
      exit(1)
    code = sys.argv[1]
    if len(code) == 4:
      codeOf = "program"
    elif len(code) == 6:
      codeOf = "stream"
    else:
      print("Invalid code")
      exit(1)

    q3(code)
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
