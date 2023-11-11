#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement
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
  rid: int





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

def q2(subject_code="COMP1010"):
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

  q_res = sql_execute_all(q, [subject_code], False)
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
    subject_title = row[2][:31]
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
                "SY", "EC", "RC"]
  req = uoc

  wam = ["HD", "DN", "CR", "PS", 
                "AF", "FL", "UF", "E", "F"]

  fail = ["AF", "FL", "UF", "E", "F"]
  unresolved = ["AS","AW","NA","PW","RD","NF","NC","LE","PE","WD","WJ"]

  grade_types = [uoc, req, wam, fail, unresolved]

  return grade in grade_types[grade_type]


def print_subjects(subjects):
  uoc_acheived = 0
  uoc_attempted = 0
  weighted_mark = 0

  for subject in subjects:
    uoc = int(subject.uoc)

    subj_allocated = (subject.req_assigned != "Could not be allocated")

    if subj_allocated and check_grade_type(subject.grade, GRADE_TYPE_UOC):
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

    uoc_str = ""
    if not subj_allocated:
      uoc_str = " 0uoc" 
    elif check_grade_type(subject.grade, GRADE_TYPE_FAIL):
      uoc_str = " fail"
    elif check_grade_type(subject.grade, GRADE_TYPE_UNRESOLVED):
      uoc_str = " unrs"
    elif not subject.mark and not subject.grade:
      uoc_str = ""
    else:
      uoc_str = f"{uoc:2d}uoc"

    line = f"{subject.course_code} {subject.term_code} {subject.title:<32s}{print_mark:>3} {print_grade:>2s}  "
    line += uoc_str

    if subject.req_assigned:
      line += f" {subject.req_assigned}"

    print(line)

  uoc = uoc_acheived
  wam = weighted_mark / uoc_attempted

  print(f"UOC = {uoc}, WAM = {wam:.1f}")
  # print(f"weighted_mark = {weighted_mark}, uoc_attempted = {uoc_attempted}")

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
  res = sql_execute_all(q, [zid], False)
  if res:
    return Person(zid, res[0][0], res[0][1])
  else:
    return Person(-1, "", "")

def q4(zid="1234567"):
  if zid[0] == 'z':
    zid = zid[1:8]
  digits = re.compile("^\d{7}$")
  if not digits.match(zid):
    print(f"Invalid student ID {zid}")
    return

  person = get_person(zid)
  if person.zid == -1:
    print(f"Invalid student ID {zid}")
    return
    
  print(f"{person.zid} {person.family_name}, {person.given_names}")
 
  enrolment = get_recent_enrolment(zid)
  print(f"{enrolment.program_code} {enrolment.stream_code} {enrolment.program_name}")

  subjects = gather_subjects(zid)
  print_subjects(subjects)

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


def q5(zid="5892943", program_code="", stream_code=""):
  if zid[0] == 'z':
    zid = zid[1:8]
  digits = re.compile("^\d{7}$")
  if not digits.match(zid):
    print(f"Invalid student ID {zid}")
    return

  person = get_person(zid)
  if person.zid == -1:
    print(f"Invalid student ID {zid}")
    return

  print(f"{person.zid} {person.family_name}, {person.given_names}")

  p_code = None
  s_code = None
  p_name = ""
  if stream_code and program_code: 
    s_code = stream_code
    p_code = program_code
    q = 'select p.name from programs p where p.code = %s limit 1'
    res = sql_execute_all(q, [p_code], False)
    p_name = res[0][0]
  else:
    enrolment = get_recent_enrolment(zid)
    p_code = enrolment.program_code
    s_code = enrolment.stream_code
    p_name = enrolment.program_name

  print(f"{p_code} {s_code} {p_name}")

  requirements = get_ordered_requirements(s_code, p_code)

  subjects = gather_subjects(zid)
  # print_subjects(subjects); return

  completed = []

  for subject in subjects:
    subject_assigned = False

    for req_name, reqs in requirements.items():
      if req_name == 'uoc' or req_name == 'stream':
        continue
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
          completed += [subject.course_code]

    if not subject_assigned and check_grade_type(subject.grade, GRADE_TYPE_REQ):
      subject.req_assigned = "Could not be allocated"

  print_subjects(subjects)

  eligible = True
  for req_name, reqs in requirements.items():
    if req_name == 'uoc' or req_name == 'stream':
      continue
    for req in reqs:
      remaining_uoc = req.minimum - req.counter
      if remaining_uoc > 0:
        eligible = False
        if req_name == 'core':
          print(f"Need {remaining_uoc * 6} more UOC for {req.name}")
          print_acad(req.acad, completed)
        else:
          print(f"Need {remaining_uoc} more UOC for {req.name}")

  if eligible:
    print("Eligible to graduate")

    # pprint.pprint(requirements);

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

    q3()
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
