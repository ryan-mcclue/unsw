IMPORTANT(Ryan): Various UNSW CompSci servers:
General ➞  ssh z5346008@login.cse.unsw.edu.au
Course ➞  ssh z5346008@d.cse.unsw.edu.au (test work on this)
VLab ➞  tigervnc vlab.cse.unsw.edu.au:5920 

PGDATA=data files
PGHOST=socket files
pg_ctl for server, psql is a cli postgresql client application (another is createdb)

unquoted identifiers are case-insensitive, i.e table names

NOTE(Ryan): We are using Postgresql as it has better support for the SQL language (MySQL utilises too many non-standard extensions)
It's client-server based (unlike sqlite3).
For linux, /usr/lib/postgresql/12/bin/*

key constraint (cardinality) with arrows, specifically arrow points to 'one'
however, without participation constraint (bold line; aka total participation as oppose to partial) we could have none/neither as an alternative

IMPORTANT(Ryan): RDBMS involves two structuring mechanisms:
 1. Relation: object name, e.g. Movie, Actor
 2. Tuple: key value pair

er diagram relationships with multiplicity. relational diagram is drawn as a single table row. 
db schema diagram shows primary and foreign keys. 

relationship naming is not verb, e.g. owned not owns
for multiplicity we may have to introduce relations representing relationships, e.g. BelongsTo, AppearsIn, etc.

will have a schema.sql file and a data.sql file containing table inserts

with inheritance, disjoint (either), overlap (could be both)

multivalue attributes don't allow storing more information about the value, 
e.g. say we want to store favourite cuisine name, dish, etc. can't do with multivalue.

a multiattribute value will most likely result in duplication of data as oppose to a relation
furthermore, breaking out into a relation offers the ability to add more relations

for large ER diagrams can separate diagrams with entity/attribute information and then another with the relations

data modelling ensures that you record all information required and none that is extraneous or duplicated based on customer feedback, market research, etc.
different modelling diagrams for a visual and machine based medium 

IMPORTANT: If relationship has attributes may have to introduce an additional table
many-to-one (teacher teaches one subject):
2 tables, one foreign key 

many-to-many, i.e. no arrows (teacher can teach many subjects):
3 tables, all attributes on relationship table (composite pk), relations just primary keys

one-to-one ():
2 tables, two foreign keys

subclassing:
ER version is to store primary class with pk. All subclasses have fk to this

circular references: require ALTER TABLE

weak entity:
relationship is fk, pk is fk and another

pk has to be unique, so a composite pk can have one being NULL 

joins to obtain information through queries, don't have to think about accessing directly through one table

PLpgSQL interpreter for stored procedures 
