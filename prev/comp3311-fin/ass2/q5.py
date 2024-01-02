#!/usr/bin/python3
# COMP3311 21T3 Ass2 ... progression check for a given student

from helpers import *

def q5(c, zid="5892943", program_code="", stream_code=""):
  if zid[0] == 'z':
    zid = zid[1:8]
  digits = re.compile("^\d{7}$")
  if not digits.match(zid):
    print(f"Invalid student ID {zid}")
    return

  person = get_person(c, zid)
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
    res = sql_execute_all(c, q, [p_code], False)
    p_name = res[0][0]
  else:
    enrolment = get_recent_enrolment(c, zid)
    p_code = enrolment.program_code
    s_code = enrolment.stream_code
    p_name = enrolment.program_name

  print(f"{p_code} {s_code} {p_name}")

  requirements = get_ordered_requirements(c, s_code, p_code)
  stream_reqs = []
  other_reqs = []
  for creq in requirements['core']:
    if creq.is_stream:
      stream_reqs += [creq]
    else:
      other_reqs += [creq]
  stream_reqs = sorted(stream_reqs, key=attrgetter('rid'))
  other_reqs = sorted(other_reqs, key=attrgetter('rid'))
  requirements['core'] = stream_reqs + other_reqs

  stream_reqs = []
  other_reqs = []
  for creq in requirements['elective']:
    if creq.is_stream:
      stream_reqs += [creq]
    else:
      other_reqs += [creq]
  stream_reqs = sorted(stream_reqs, key=attrgetter('rid'))
  other_reqs = sorted(other_reqs, key=attrgetter('rid'))
  requirements['elective'] = stream_reqs + other_reqs

  subjects = gather_subjects(c, zid)
  # print(subjects)
  # print_subjects(subjects); return

  completed = []

  # pprint.pprint(requirements)

  for subject in subjects:
    subject_assigned = False

    for req_name, reqs in requirements.items():
      if req_name == 'uoc' or req_name == 'stream':
        continue
      for req in reqs:
        if not subject_assigned and req.counter < req.maximum \
        and code_matches_acad(subject.course_code, req.acad) \
        and check_grade_type(subject.grade, GRADE_TYPE_REQ):
          allocated = False
          if req_name == 'core':
            if req.counter + 1 <= req.maximum:
              req.counter += 1
              allocated = True
          else:
            if req.counter + subject.uoc <= req.maximum:
              req.counter += subject.uoc
              allocated = True
          if allocated:
            subject.req_assigned = req.name
            subject_assigned = True
            completed += [subject.course_code]
            break

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
        # print(f"{req_name}: {req}")
        eligible = False
        if req_name == 'core':
          core_uoc_remaining = 0
          codes = get_remaining_acad_codes(req.acad, completed)
          for code in codes:
            uoc = get_code_uoc(c, code)
            core_uoc_remaining += uoc
          #print(f"Need {remaining_uoc * 6} more UOC for {req.name}")
          print(f"Need {core_uoc_remaining} more UOC for {req.name}")
          print_acad(c, req.acad, completed)
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

def main():
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
      db = f"host=localhost, port=5432 dbname=ass2 user=ryan password={local_db_pass}"

    connection = psycopg2.connect(db)
    c = connection.cursor()

    usage = f"Usage: {sys.argv[0]} zID [Program Stream]"
    argc = len(sys.argv)
    if argc < 2:
      print(usage)
      exit(1)
    zid = sys.argv[1]
    if zid[0] == 'z':
      zid = zid[1:8]
    digits = re.compile("^\d{7}$")
    if not digits.match(zid):
      print("Invalid student ID")
      exit(1)
    
    progCode = ""
    strmCode = ""
    
    if argc == 4:
      progCode = sys.argv[2]
      strmCode = sys.argv[3]

    q5(c, zid, progCode, strmCode)
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
