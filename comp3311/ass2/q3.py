#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... print list of rules for a program or stream

import sys
import psycopg2
import re
from helpers import getProgram, getStream

# define any local helper functions here
# ...

### set up some globals

usage = f"Usage: {sys.argv[0]} (ProgramCode|StreamCode)"
db = None

### process command-line args

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

try:
  db = psycopg2.connect("dbname=ass2")
  if codeOf == "program":
    progInfo = getProgram(db,code)
    if not progInfo:
      print(f"Invalid program code {code}")
      exit(1)
    #print(progInfo)  #debug

    # List the rules for Program

    # ... add your code here ...

  elif codeOf == "stream":
    strmInfo = getStream(db,code)
    if not strmInfo:
      print(f"Invalid stream code {code}")
      exit(1)
    #print(strmInfo)  #debug

    # List the rules for Stream

    # ... add your code here ...

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
