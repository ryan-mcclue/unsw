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
    select t.code, c.satisfact, c.nresponses, p.full_name, s.title
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
    print("Term   Satis   #resp   #stu Convenor")
    for res in q_res:
      term = res[0]
      satisfaction = res[1]
      nresponses = res[2]
      convenor = res[3]

      nstudents = sql_execute_all(q2, [subject_code, term], False)[0][0]
      print(f"{term} {satisfaction:6d} {nresponses:6d} {nstudents:6d}  {convenor}")



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

    q2()



  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
