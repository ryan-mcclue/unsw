#!/usr/bin/python3
# COMP3311 22T3 Ass2 ... print a transcript for a given student

from helpers import *

def q4(c, zid="1234567"):
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
 
  enrolment = get_recent_enrolment(c, zid)
  print(f"{enrolment.program_code} {enrolment.stream_code} {enrolment.program_name}")

  subjects = gather_subjects(c, zid)
  print_subjects(subjects)

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

    usage = f"Usage: {sys.argv[0]} zID"
    argc = len(sys.argv)
    if argc < 2:
      print(usage)
      exit(1)
    zid = sys.argv[1]
    if zid[0] == 'z':
      zid = zid[1:8]
    digits = re.compile("^\d{7}$")
    if not digits.match(zid):
      print(f"Invalid student ID {zid}")
      exit(1)

    q4(c, zid)
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()

