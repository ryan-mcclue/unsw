#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement
import os
import sys
import platform
import pathlib
import subprocess

import re

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

def sql_execute_all(query, args=[], log=True):
  if log:
    print(f"[ECHO-QUERY]: {global_cursor.mogrify(query, args).decode('utf-8')}")
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
F = False
T = True

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

  d = F
  if d:
    sql(q)
  else:
    student_counts = sql_execute_all(q)
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
        print(f"{terms[i]} {local_count:6d} {intl_count:6d} {local_count/intl_count:6.1f}")
        
        cur_starting = starting
        local_count = 0
        intl_count = 0

        i += 1

      if res[1] == 'INTL':
        intl_count = res[2]
      else:
        local_count += res[2]

    # NOTE(Ryan): Print final row
    print(f"{terms[i]} {local_count:6d} {intl_count:6d} {local_count/intl_count:6.1f}")

def q2(subject_code="COMP1521"):
  q = '''
    select t.code, coalesce(c.satisfact, -1), coalesce(c.nresponses, -1), 
    coalesce(p.full_name, \'?\'), s.title
    from subjects s
    join courses c on (c.subject = s.id)
    join terms t on (t.id = c.term)
    join staff stf on (c.convenor = stf.id)
    join people p on (p.id = stf.id)
    where t.starting between '2019-02-18' and '2023-09-11'
    and s.code = %s
    order by t.code
  '''

  q2 = '''
    select count(*)
    from courses c
    join terms t on (t.id = c.term)
    join course_enrolments ce on (ce.course = c.id)
    join subjects s on (c.subject = s.id)
    where s.code = %s and t.code = %s
  '''

  d = F
  if d:
    sql(q, [subject_code])
    # sql(q2, [subject_code, '19T2'])
  else:
    q_res = sql_execute_all(q, [subject_code])
    subject_title = q_res[0][4]
    print(f"{subject_code} {subject_title}")
    print("Term  Satis  #resp   #stu  Convenor")
    for res in q_res:
      term = res[0]
      satisfaction = str(res[1])
      if satisfaction == "-1":
        satisfaction = "?"
      nresponses = str(res[2])
      if nresponses == "-1":
        nresponses = "?"
      convenor = res[3]

      nstudents = sql_execute_all(q2, [subject_code, term], False)[0][0]
      print(f"{term} {satisfaction:>6} {nresponses:>6} {nstudents:6d}  {convenor}")

def q3(code="3707"):
  is_stream = False

  # TODO(Ryan): Is just checking length sufficient?
  if len(code) == 6:
    q = 'select 1 from streams s where s.code = %s limit 1'
    if not sql_execute_all(q, [code]):
      print(f"Invalid program code {code}")
    else:
      is_stream = True
  elif len(code) == 4:
    q = 'select 1 from programs p where p.code = %s limit 1'
    if not sql_execute_all(q, [code]):
      print(f"Invalid stream code {code}")
  else:
    print("Invalid code")

  q_start = None
  if is_stream:
    q_start = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, s.name
      from requirements r
      join streams s on (r.for_stream = s.id)
      where s.code = %s
    '''
  else:
    q_start = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, p.name
      from requirements r
      join programs p on (r.for_program = p.id)
      where p.code = %s
    '''

  q = q_start + \
    '''
    order by case
      when r.rtype = 'uoc' then 1 
      when r.rtype = 'stream' then 2
      when r.rtype = 'core' then 3
      when r.rtype = 'elective' then 4
      when r.rtype = 'gened' then 5
      when r.rtype = 'free' then 6
      else 7
    end
    '''

  res = sql_execute_all(q, [code])

  print(f"{code} {res[0][-1]}")
  print("Academic Requirements: ")

  for t in res:
    req_name = t[0]
    req_type = t[1]
    acad = t[2]
    min_req = t[3]
    max_req = t[4]

# IMPORTANT(Ryan): Lots of ifs to match examples
    if min_req and not max_req:
      req_str = f"at least {min_req}"
    elif not min_req and max_req:
      req_str = f"up to {max_req}"
    elif min_req and max_req:
      if min_req < max_req:
        req_str = f"between {min_req} and {max_req}"
      elif min_req == max_req:
        req_str = f"{min_req}"

    if req_type == "uoc":
      req_str += " UOC" 
    elif req_type == "stream":
      req_str += " stream" 

    if req_name == "Total UOC":
      print(f"Total UOC {req_str}")
      continue

    if req_type == "core":
      print(f"all courses from {req_name}")

    if req_type == "gened":
      print(f"{req_str} UOC of General Education")
    
  #print(res)
  #return
  # acad = ''
  # for acad_tokens in acad.split(','):
  #   if acad_token[0] == '{':
  #     # {s1;s2}
  #   else if '#' in acad_token:
  #     # ####s####


  stream_req = '''
    select coalesce(s.name, \'None\')
    from streams s
    where s.code = %s
  '''

  core_req = '''

  '''
  # TODO(Ryan): Handle same requirement type

  
def q4():
  pass

def q5():
  # NOTE(Ryan): UOC might not add up correctly
  # order of course assignments to requirements: core -> discipline elective -> gened -> stream electives -> free electives
  # (only consider courses that are passed)
  # e.g. first does course fit core requirement? no. does it fit discipline? etc.

  # then after iterating through all subjects on transcript, 
  # check if all uoc requirements satisfied and number of majors

  # subject = {name, mark, requirement_allocated}
  # progression = subjects[]

  # total_uoc = 0
  # stream_uoc = 0
 
  # iterate over these and check if course matches it.
  # if it does, remove from list
  # ultimately want all requirement arrays to be empty
  # requirement_maths_acad = [math1081, {math1231;math1241}, math2211]
  # ensure this doesn't exceed uoc
  # requirement_maths_uoc = range(current, required)
 
  # IMPORTANT(Ryan): computing electives no max. but treat the min as max. as well
  pass



# IMPORTANT(Ryan): Stay up-to-date on Fixes+Updates page
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

    q3()



  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
