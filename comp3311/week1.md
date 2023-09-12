<!-- SPDX-License-Identifier: zlib-acknowledgement -->
DBMS for efficient concurrent manipulation of large amounts of data using set theory and constraints
Queries converted to relational algebra which is built upon set theory, e.g. a table/relation is a set of tuples/rows
So relational algebra machine code for psql

SQL standard is language for managing relational DBMS. Postgresql documentation explicit in standard conformance.
Could also have noSQL or time-series (i.e. optimised for time-based queries, i.e. index of data determines efficiency) 

sqlite3 serverless

**Procedural**
`cursor.execute("INSERT INTO users (name) VALUES ('Ryan'))`
**Declarative**
`session.add(user)`

Data model, e.g Book entity with attribute title and many-to-many relationship
ER diagram would be in-between formality (ER diagram not formalised)
Relational schema would specify primary/foreign keys

quizzes, tut, pracs

prac 1+2

psql 13.0, sqlite 3.x, python 3.7+, psycopg 2.8+

vxdb2 server
ssh zid@d2.cse.unsw.edu.au
/localstorage/zid (storage here to install psql server)

env variables
initdb to create db
postgresql.conf (3311 initdb)
parsing psql/data/log?
psql/data/base is where located
(on vxdb2 they make you the superuser automatically)

list $(psql -l)
createdb/dropdb beer
psql beer -f schema
psql beer -f data

psql beer -f db.dump

psql \d command for describe
\e (open up editor)
\?
\i FILE (what is the PWD of shell?)

`*` represents a tuple?

## Data Modellling
Book BOUGHT and OWNED. Relationships and operations modelled by tables

how would model something linked to multiple, e.g. array for foreign keys
`Course: code, name, description, uoc, convenor(user), outcome*`
`PartOf: assessment, course`
array of foreign keys vs seperate table, e.g. PartOf table (only if relationship as multiple attributes would you create a table?)
