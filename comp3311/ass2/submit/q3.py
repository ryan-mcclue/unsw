#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... print list of rules for a program or stream
from helpers import *

def q3(c, code="ACCTAH"):
  stream_name = ""
  stream_code = ""
  program_name = ""
  program_code = ""

  if len(code) == 6:
    q = 'select s.name from streams s where s.code = %s limit 1'
    res = sql_execute_all(c, q, [code], False)
    if len(res) == 0:
      print(f"Invalid stream code {code}")
      return
    else:
      stream_name = res[0][0]
      stream_code = code
  elif len(code) == 4:
    q = 'select p.name from programs p where p.code = %s limit 1'
    res = sql_execute_all(c, q, [code], False)
    if len(res) == 0:
      print(f"Invalid program code {code}")
      return
    else:
      program_name = res[0][0]
      program_code = code
  else:
    print("Invalid code")
    return

  requirements = get_ordered_requirements(c, stream_code, program_code, True)

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
        print_acad(c, r.acad, [])
      elif req_name == "core":
        print(f"all courses from {r.name}")
        print_acad(c, r.acad, [])
      elif req_name == "gened":
        print(f"{req_str} UOC of General Education")
      elif req_name == "free":
        print(f"{req_str} UOC of {stream_code} Free Electives")
      elif req_name == "elective":
        print(f"{req_str} UOC courses from {r.name}")
        print(f"- {r.acad}")

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

    q3(c, code)
  except psycopg2.DatabaseError as error:
    fatal_error(f"psycopg2 error ({error.pgcode}): {error.pgerror}")

if __name__ == "__main__": main()
