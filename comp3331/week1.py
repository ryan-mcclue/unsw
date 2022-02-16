# SPDX-License-Identifier: zlib-acknowledgement

# IMPORTANT(Ryan): Various UNSW CompSci servers:
# General ➞  ssh z5346008@login.cse.unsw.edu.au
# Course ➞  ssh z5346008@d.cse.unsw.edu.au (test work on this)
# For Vlab, access the vnc server

# PGDATA=data files
# PGHOST=socket files
# pg_ctl for server, psql is a cli postgresql client application (another is createdb)

# unquoted identifiers are case-insensitive, i.e table names

# NOTE(Ryan): We are using Postgresql as it has better support for the SQL language (MySQL utilises too many non-standard extensions)
# It's client-server based (unlike sqlite3).

# IMPORTANT(Ryan): RDBMS involves two structuring mechanisms:
#  1. Relation: object name, e.g. Movie, Actor
#  2. Tuple: key value pair
  
# select summary_function(argument [fields|*]) from [table] order by [field] where [condition]

# er diagram relationships with multiplicity. db schema diagram shows primary and foreign keys.
# for multiplicity we may have to introduce relations representing relationships, e.g. BelongsTo, AppearsIn, etc.

# will have a schema.sql file and a data.sql file containing table inserts

# TODO(Ryan): Investigate advanced SQL topics: views, stored procedures, triggers, aggregates
