#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track proportion of overseas students

import sys
import psycopg2
import re

# define any local helper functions here
# ...

### set up some globals

db = None

### process command-line args


try:
  db = psycopg2.connect("dbname=ass2")

  # show term, #locals, #internationals, fraction

  # ... add your code here ...

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
