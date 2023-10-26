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
A closure is all fds from a relation

Attribute closures:
R = ABCDEFG
FD = {A->B, C->D, E->FG}
A+ = AB
C+ = CD
ACE+ = ABCDEFG (so key)

Normalisation uses normal forms, which state what level of redundancy is allowed
Boyce-Codd and 3rd-NF usually used

1NF all values must be atomic (so no arrays)
2NF all non-key attributes depend on key
3NF no attributes depend on non-key attributes (so cannot have key ABC and B->C)
BCNF may not preserve functional dependencies
