<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Constraints largely refer to uniqueness, e.g. key, unqiue, referential

Relation is just foreign keys? These foreign keys are primary key?

## SQL Modelling
Effectively '1' will have foreign key, 'n' will be modelled by relationship table
* 1:1 
  could have two tables each with foreign key referencing other primary key
  however redudancy comes up, only requiring one foreign key for one of them (as can access other through them)
  what side foreign key is one depends on participation
* 1:n
  '1' side with foreign key
  relationship table with '1' and 'n' foreign key
  two tables; 'n' side with foreign key 
* n:m (cannot create n:m with total participation in sql)
  single relationship table, i.e. no attributes in host tables

A foreign key can have multiple attributes.
Can also have multiple foreign keys.
