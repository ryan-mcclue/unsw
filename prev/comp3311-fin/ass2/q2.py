#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track satisfaction in a given subject

from helpers import *

def q2(c, subject_code="COMP1010"):
  # TODO(Ryan): Print if invalid
  # subjectInfo = getSubject(db,subject)
  # if not subjectInfo:
  #     print(f"Invalid subject code {code}")
  #     exit(1)
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

  q_res = sql_execute_all(c, q, [subject_code], False)
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

    nstudents = sql_execute_all(c, q2, [subject_code, term], False)[0][0]
    print(f"{term} {satisfaction:>6} {nresponses:>6} {nstudents:6d}  {convenor}")


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

    usage = f"Usage: {sys.argv[0]} SubjectCode"
    argc = len(sys.argv)
    if argc < 2:
      print(usage)
      exit(1)
    subject = sys.argv[1]
    check = re.compile("^[A-Z]{4}[0-9]{4}$")
    if not check.match(subject):
      print("Invalid subject code")
      exit(1)

    q2(c, subject)
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
