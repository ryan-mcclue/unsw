# SPDX-License-Identifier: zlib-acknowledgement

# IMPORTANT(Ryan): Various UNSW CompSci servers:
# General ➞  ssh z5346008@login.cse.unsw.edu.au
# Course ➞  ssh z5346008@d.cse.unsw.edu.au
# For Vlab, access the vnc server

# NOTE(Ryan): We are using Postgresql as it has better support for the SQL language (MySQL utilises too many non-standard extensions)
# It's client-server based (unlike sqlite3).

# IMPORTANT(Ryan): RDBMS involves two structuring mechanisms:
#  1. Relation: object name, e.g. Movie, Actor
#  2. Tuple: key value pair
  
# er diagram relationships with multiplicity. db schema diagram shows primary and foreign keys.
# for multiplicity we may have to introduce relations representing relationships, e.g. BelongsTo, AppearsIn, etc.

# will have a schema.sql file and a data.sql file containing table inserts

# TODO(Ryan): Investigate advanced SQL topics: views, stored procedures, triggers, aggregates
