#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track satisfaction in a given subject

import sys
import psycopg2
import re
from helpers import getCourse

# define any local helper functions here
# ...

### set up some globals

usage = f"Usage: {sys.argv[0]} SubjectCode"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
subject = sys.argv[1]
check = re.compile("^[A-Z]{4}[0-9]{4}$")
if not check.match(subject):
  print("Invalid subject code")
  exit(1)

try:
  db = psycopg2.connect("dbname=ass2")
  subjectInfo = getSubject(db,subject)
  if not subjectInfo:
      print(f"Invalid subject code {code}")
      exit(1)
  #print(subjectInfo)  #debug

  # List satisfaction for subject over time

  # ... add your code here ...

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
