<!-- SPDX-License-Identifier: zlib-acknowledgement -->

relational design theory aims to minimise stored data by utilising functional dependencies, i.e. relationships between attributes in a relation
(prevent update anomalies; even though can be handled with a trigger)

normalisation method would transform schema to remove identified redundancies (non-deterministic however, so multiple ways to acheive)
normalisation involves decomposition on functional dependecies, i.e break into smaller tables

if multiple tuples contain the same attribute X and attribute Y is same, then Y functionally dependent on X

all attributes are functionally dependent on primary key/unique values
(NOTE: also have combination of unique values)

So, when looking for dependencies look for unique and identical values

Inference rules to simplify and rearrange functional dependencies
A closure is all fds from a relations fds
However, for less computation do attribute closures on all dependencies deriveable from attribute

Attribute closures (to determine key candidates):
R = ABCDEFG
FD = {A->B, C->D, E->FG}
A+ = AB
C+ = CD
ACE+ = ABCDEFG (so key)

Normalisation uses normal forms, which state what level of redundancy is allowed
Boyce-Codd and 3rd-NF usually used

IMPORTANT: key is specific to a single table
1NF all values must be atomic (e.g. no arrays)
2NF all non-key attributes must depend on key (e.g. key of table gives field1 and field1 gives field2)
3NF all non-key attributes must directly (e.g. no transitive) depend on some part of key
1. determine candidate key(s) by finding what no arrows point to
IMPORTANT: if this does not give complete candidate key, make combination which may result in multiple candidate keys
2. is lhs of fd. a superkey or rhs a prime attribute. if not split into table
3. after splitting all fds. into tables, make final candidate key table
IMPORTANT: if multiple candidate key tables, only add one where fds. flow

BCNF everything related to the whole key and nothing but the key so help me Codd (or nothing in table)
BCNF may not preserve functional dependencies and cannot have key ABC and B->C; therefore possible update anomalies)
