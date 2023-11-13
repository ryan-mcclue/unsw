# COMP3311 21T3 Ass2 ... Python helper functions
# add here any functions to share between Python scripts 
# you must submit this even if you add nothing

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

def sql_execute_all(c, query, args=[], log=True):
  if log:
    print(f"[ECHO-QUERY]: {c.mogrify(query, args).decode('utf-8')}")
  c.execute(query, args)
  return c.fetchall()

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

def get_course_name(c, code):
  q = '''
      select s.name from streams s
      where s.code = %s
   '''
  res = sql_execute_all(c, q, [code], False)

  if len(res) == 0:
    q = '''
        select s.title from subjects s
        where s.code = %s
    '''
    return sql_execute_all(c, q, [code], False)[0][0]
  else:
    return res[0][0]

def print_acad(c, acad, completed):
  for acad_token in acad.split(','):
    if acad_token[0] == '{':
      acad_plain = acad_token.strip('{}')
      stream_codes = acad_plain.split(';')
      stream_names = []
      for stream_code in stream_codes:
        if stream_code in completed:
          break
        else:
          stream_names += [get_course_name(c, stream_code)]
      final_str = ""
      for i in range(len(stream_names)):
        final_str += f"{stream_codes[i]} {stream_names[i]} or "
      if final_str:
        print(f"- {final_str[:-4]}")
    else:
      if acad_token not in completed:
        stream_name = get_course_name(c, acad_token)
        print(f"- {acad_token} {stream_name}")


def gather_subjects(c, zid):
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
  for row in sql_execute_all(c, q, [zid], False):
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

def get_recent_enrolment(c, zid):
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
  res = sql_execute_all(c, q, [zid], False)
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

def get_person(c, zid):
  q = '''
     select p.family_name, p.given_names
     from people p
     where p.zid = %s
  '''
  res = sql_execute_all(c, q, [zid], False)
  if res:
    return Person(zid, res[0][0], res[0][1])
  else:
    return Person(-1, "", "")

def get_ordered_requirements(c, stream_code, program_code, raw=False):
  reqs = []
  if stream_code:
    q = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, r.id
      from requirements r
      join streams s on (r.for_stream = s.id)
      where s.code = %s
    '''
    stream_requirements = sql_execute_all(c, q, [stream_code], False)
    reqs += stream_requirements
  if program_code:
    q = '''
      select r.name, r.rtype, r.acadobjs, r.min_req, r.max_req, r.id
      from requirements r
      join programs p on (r.for_program = p.id)
      where p.code = %s
    '''
    program_requirements = sql_execute_all(c, q, [program_code], False)
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





# NOTE(Ryan): Pre-existing ...
def getProgram(db,code):
  cur = db.cursor()
  cur.execute("select * from Programs where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStream(db,code):
  cur = db.cursor()
  cur.execute("select * from Streams where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStudent(db,zid):
  cur = db.cursor()
  qry = """
  select p.*
  from   People p
         join Students s on s.id = p.id
  where  p.id = %s
  """
  cur.execute(qry,[zid])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info
