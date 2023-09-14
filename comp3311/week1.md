<!-- SPDX-License-Identifier: zlib-acknowledgement -->
## Overview
DBMS for efficient concurrent manipulation of large amounts of data using set theory and constraints.
Queries converted to relational algebra which is built upon set theory, e.g. a table/relation is a set of tuples/rows.
So, relational algebra is a sort of machine code for psql.

SQL standard is language for managing RDBMS. 
Postgresql documentation explicit in standard conformance.
Could also have noSQL or time-series (i.e. optimised for time-based queries, i.e. index of data determines efficiency) 

Data model -> ER diagram -> Relational schema

psql 13.0, sqlite 3.x, python 3.7+, psycopg 2.8+

## Installation
initdb -> createdb/dropdb -> psql -f schema/data
On vxdb2 they make you the superuser automatically

By default, postgres user created that's only accesible via peer-authentication, i.e. no password
So, will require creating own user with a password
`$(sudo -i -u postgres)`
`$(createuser --interactive)`
`$(psql; ALTER USER ryan WITH ENCRYPTED PASSWORD 'ryan')`
`$(GRANT ALL PRIVELEGES ON Example TO ryan)`

creating pgadmin server would be localhost and name of user created 

`$(createdb Example)`
`$(psql -U ryan -h localhost -d Example)

psql \d 
\e (open up editor)
\?
\i FILE (what is the PWD of shell?)

**Procedural**
`cursor.execute("INSERT INTO users (name) VALUES ('Ryan'))`
**Declarative**
`session.add(user)`

Aggregate function operate on series of tuples

## Data Modelling
Create a table for relationship, e.g. OWNED-BY not operation, e.g BOUGHT 

how would model something linked to multiple, e.g. array for foreign keys
`Course: code, name, description, uoc, convenor(user), outcome\*`
`PartOf: assessment, course`
array of foreign keys vs seperate table, e.g. PartOf table (only if relationship as multiple attributes would you create a table?)
separate relation allows for independent access

weak entities not that common. occur when entity only exists in the context of another entity

subclasses disjoint (either-or) or overlapping (both)
common superclass would be a Person

Split large diagrams onto multiple pages, e.g. first attributes (e.g. classes), second relations

To reduce a 3-way relationship, could add a new entity
