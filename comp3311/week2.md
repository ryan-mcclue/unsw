<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Constraints largely refer to uniqueness, e.g. key, unqiue, referential

Relation is just foreign keys? These foreign keys are primary key?

## SQL Modelling
Effectively '1' will have foreign key, 'n' will be modelled by relationship table
* 1:1 (redudancy may come up with total participation on one side; with other side not requiring foreign key)
  two tables each with foreign key referencing other primary key
* 1:n
  '1' side with foreign key
  relationship table with '1' and 'n' foreign key
  two tables; 'n' side with foreign key 
* n:m (cannot create n:m with total participation in sql)
  single relationship table, i.e. no attributes in host tables

A foreign key can have multiple attributes.
Can also have multiple foreign keys.
