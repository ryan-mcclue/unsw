#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement
import os
import sys
import platform
import pathlib
import subprocess

import re

import pprint


from dataclasses import dataclass

from collections import OrderedDict

from urllib.parse import urlparse

import psycopg2

@dataclass
class Subject:
  course_code: str
  term_code: str
  title: str
  mark: str
  grade: str
  uoc: str
  req_assigned: str

@dataclass
class Enrolment:
  program_code: str
  program_name: str
  stream_code: str

@dataclass
class Person:
  zid: str
  family_name: str
  given_names: str

@dataclass
class Requirement:
  name: str
  minimum: int
  maximum: int
  acad: str
  counter: int

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

def print_acad(acad):
  for acad_token in acad.split(','):
    if acad_token[0] == '{':
      acad_plain = acad_token.strip('{}')
      stream_codes = acad_plain.split(';')
      stream_names = []
      for stream_code in stream_codes:
        stream_names += [get_course_name(stream_code)]
      final_str = ""
      for i in range(len(stream_names)):
        final_str += f"{stream_codes[i]} {stream_names[i]} or "
      print(f"- {final_str[:-4]}")
    else:
      stream_name = get_course_name(acad_token)
      print(f"- {acad_token} {stream_name}")


def q3(code="3707"):
  is_stream = False

  # TODO(Ryan): Handle same requirement type
  # TODO(Ryan): Is just checking length sufficient?
  if len(code) == 6:
    q = 'select 1 from streams s where s.code = %s limit 1'
    if len(sql_execute_all(q, [code])) == 0:
      print(f"Invalid program code {code}")
      return
    else:
      is_stream = True
  elif len(code) == 4:
    q = 'select 1 from programs p where p.code = %s limit 1'
    if len(sql_execute_all(q, [code])) == 0:
      print(f"Invalid stream code {code}")
      return
  else:
    print("Invalid code")
    return

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
      if req_name == "Total UOC":
        print(f"Total UOC {req_str}")
      else:
        print(f"{req_str} from {req_name}")
    elif req_type == "stream":
      req_str += " stream" 
      print(f"{req_str} from {req_name}")
      print_acad(acad)
    elif req_type == "core":
      print(f"all courses from {req_name}")
      print_acad(acad)
    elif req_type == "gened":
      print(f"{req_str} UOC of General Education")
    elif req_type == "free":
      print(f"{req_str} UOC of Free Electives")
    elif req_type == "elective":
      print(f"{req_str} UOC courses from {req_name}")
      print(f"- {acad}")

def gather_subjects(zid):
  q = '''
    select subj.code, t.code, subj.title, ce.mark, ce.grade, subj.uoc
    from people p
    join students s on (s.id = p.id)
    join course_enrolments ce on (ce.student = s.id)
    join courses c on (ce.course = c.id)
    join subjects subj on (c.subject = subj.id)
    join terms t on (c.term = t.id)
    where p.zid = %s
    order by t.code, subj.code
  '''
  subjects = []
  for row in sql_execute_all(q, [zid], False):
    course_code = row[0]
    term = row[1]
    subject_title = row[2][:32]
    mark = row[3]
    grade = row[4]
    uoc = row[5]

    subject = Subject(course_code, term, subject_title, mark, grade, uoc, "")
    subjects += [subject]

  return subjects

GRADE_TYPE_UOC = 0
GRADE_TYPE_REQ = 1
GRADE_TYPE_WAM = 2
GRADE_TYPE_FAIL = 3
GRADE_TYPE_UNRESOLVED = 4
def check_grade_type(grade, grade_type):
  uoc = ["A", "A+", "A-", "B", "B+", "B-", "C", "C+", "C-", "D", "D+", "D-",
                "HD", "DN", "CR", "PS",
                "XE", "T", 
                "SY", "EC", "RC", "NC"]
  req = uoc

  wam = ["HD", "DN", "CR", "PS", 
                "AF", "FL", "UF", "E", "F"]

  fail = ["AF", "FL", "UF", "E", "F"]
  unresolved = ["AS","AW","NA","PW","RD","NF","LE","PE","WD","WJ"]

  grade_types = [uoc, req, wam, fail, unresolved]

  return grade in grade_types[grade_type]


def print_subjects(subjects):
  uoc_acheived = 0
  uoc_attempted = 0
  weighted_mark = 0

  for subject in subjects:
    uoc = int(subject.uoc)

    if check_grade_type(subject.grade, GRADE_TYPE_UOC):
      uoc_acheived += uoc
    if check_grade_type(subject.grade, GRADE_TYPE_WAM):
      uoc_attempted += uoc
      if subject.mark:
        weighted_mark += (uoc * subject.mark)

    print_mark = subject.mark
    print_grade = subject.grade
    if not subject.mark:
      print_mark = '-'
    if not subject.grade:
      print_grade = '-'

    line = f"{subject.course_code} {subject.term_code} {subject.title:<32s}{print_mark:>3} {print_grade:>2s}  "
    if check_grade_type(subject.grade, GRADE_TYPE_FAIL):
      line += " fail"
    elif check_grade_type(subject.grade, GRADE_TYPE_UNRESOLVED):
      line += " unrs"
    else:
      line += f"{uoc:2d}uoc"

    if subject.req_assigned:
      line += f" {subject.req_assigned}"

    print(line)

  uoc = uoc_acheived
  wam = weighted_mark / uoc_attempted

  print(f"UOC = {uoc}, WAM = {wam:.1f}")
  print(f"weighted_mark = {weighted_mark}, uoc_attempted = {uoc_attempted}")

def get_recent_enrolment(zid):
  q = '''
    select pr.code, pr.name, str.code, string_agg(t.code, ',' order by t.code)
    from people p
    join students s on (s.id = p.id)
    join program_enrolments pe on (pe.student = s.id)
    join stream_enrolments se on (se.part_of = pe.id)
    join streams str on (se.stream = str.id)
    join programs pr on (pr.id = pe.program)
    join terms t on (pe.term = t.id)
    where p.zid = %s
    group by (pr.code, pr.name, str.code)
  '''
  res = sql_execute_all(q, [zid], False)
  recent_enrolment = res[0]
  cur_max_term = '19T0' # 19T0 - 23T3

  for enrolment in res:
    terms = enrolment[3]
    max_term = terms.split(',')[0]
    if max_term > cur_max_term:
      cur_max_term = max_term
      recent_enrolment = enrolment
 
  program_code = recent_enrolment[0]
  program_name = recent_enrolment[1]
  stream_code = recent_enrolment[2]

  e = Enrolment(program_code, program_name, stream_code)

  return e

def get_person(zid):
  q = '''
     select p.family_name, p.given_names
     from people p
     where p.zid = %s
  '''
  info = sql_execute_all(q, [zid], False)[0]
  family_name = info[0]
  given_names = info[1]

  return Person(zid, family_name, given_names)


def q4(zid="5893146"):
  if zid[0] == 'z':
    zid = zid[1:8]
  digits = re.compile("^\d{7}$")
  if not digits.match(zid):
    print(f"Invalid student ID {zid}")
    return

  person = get_person(zid)
  print(f"{person.zid} {person.family_name}, {person.given_names}")
 
  enrolment = get_recent_enrolment(zid)
  print(f"{enrolment.program_code} {enrolment.stream_code} {enrolment.program_name}")

  subjects = gather_subjects(zid)
  print_subjects(subjects)

def get_ordered_requirements(stream_code, program_code):
  reqs = []
  if stream_code:
    q = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, s.name
      from requirements r
      join streams s on (r.for_stream = s.id)
      where s.code = %s
    '''
    stream_requirements = sql_execute_all(q, [stream_code], False)
    reqs += stream_requirements
  if program_code:
    q = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, p.name
      from requirements r
      join programs p on (r.for_program = p.id)
      where p.code = %s
    '''
    program_requirements = sql_execute_all(q, [program_code], False)
    reqs += program_requirements

  requirements = OrderedDict()
  requirements['stream'] = []
  requirements['core'] = []
  requirements['elective'] = []
  requirements['gened'] = []
  requirements['free'] = []

  for r in reqs:
    name = r[0]
    r_type = r[1]
    acad = r[2]
    maximum = 0
    if r[3]:
      minimum = int(r[3])
    maximum = r[4]
    if not maximum:
      maximum = minimum

    if r_type == 'core':
      minimum = len(acad.split(','))
      maximum = minimum

    if name == 'Total UOC':
      continue

    r = Requirement(name, minimum, maximum, acad, 0)

    requirements[r_type] += [r]

  return requirements

def code_matches_acad(code, acad):
  for acad_token in acad.split(','):
    if acad_token[0] == '{':
      acad_plain = acad_token.strip('{}')
      stream_codes = acad_plain.split(';')
      for stream_code in stream_codes:
        if code_matches_acad_code(code, stream_code):
          return True
    else:
      if code_matches_acad_code(code, acad_token):
        return True
   
  return False

def code_matches_acad_code(code, acad_code):
  if acad_code == 'FREE####' or acad_code == 'GEN#####':
    return True

  at = 0
  while at < len(code):
    acad_ch = acad_code[at]
    code_ch = code[at]
    if acad_ch == '#':
      if (at < 4 and not code_ch.isalpha()) or not code_ch.isdigit():
        return False
    elif acad_ch != code_ch:
      return False
    at += 1

  return True


def q5(zid="5893146", program_code="", stream_code=""):
  if zid[0] == 'z':
    zid = zid[1:8]
  digits = re.compile("^\d{7}$")
  if not digits.match(zid):
    print(f"Invalid student ID {zid}")
    return

  if program_code and stream_code:
    program_info = 0
    stream_info = 0
  else:
    person = get_person(zid)
    print(f"{person.zid} {person.family_name}, {person.given_names}")

    enrolment = get_recent_enrolment(zid)
    print(f"{enrolment.program_code} {enrolment.stream_code} {enrolment.program_name}")

    requirements = get_ordered_requirements(enrolment.stream_code, enrolment.program_code)

    subjects = gather_subjects(zid)
    # print_subjects(subjects); return

    for subject in subjects:
      subject_assigned = False

      for req_name, reqs in requirements.items():
        for req in reqs:
          if not subject_assigned and req.counter < req.maximum \
          and code_matches_acad(subject.course_code, req.acad) \
          and check_grade_type(subject.grade, GRADE_TYPE_REQ):
            if req_name == 'core':
              req.counter += 1
            else:
              req.counter += subject.uoc
            subject.req_assigned = req.name
            subject_assigned = True

      if not subject_assigned and check_grade_type(subject.grade, GRADE_TYPE_REQ):
        subject.req_assigned = "Could not be allocated"

    print_subjects(subjects)

    for req_name, reqs in requirements.items():
      for req in reqs:
        remaining_uoc = req.minimum - req.counter
        if remaining_uoc > 0:
          print(f"Need {remaining_uoc} more UOC for {req.name}")

    pprint.pprint(requirements);

  # NOTE(Ryan): UOC might not add up correctly
  # order of course assignments to requirements: core -> discipline elective -> gened -> stream electives -> free electives
  # (only consider courses that are passed)
  # e.g. first does course fit core requirement? no. does it fit discipline? etc.

  # then after iterating through all subjects on transcript, 
  # check if all uoc requirements satisfied and number of majors
 
  # IMPORTANT(Ryan): computing electives no max. but treat the min as max. as well



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

    q5()



  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
