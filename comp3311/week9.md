<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Query Processing:
SQL is parsed into relational algebra then query optimiser (outputs execution plan) then db engine.
(sql parser allows for user-defined operators)

Reordering relational algebra operations can affect the total reads and writes for an expression
So, want to minimise these memory operations

Internally, db sorting not in-place as large memory 
B-tree typically used as has low depth meaning low leaf node access time. Also good for range queries
So, a relational algebra projection could be implemented as a binary search, joining via hash-join etc.

Index (auxiliary data structure on attribute) can speed up for equality searches, i.e. filtering
(hash index if `id = 12345`, b-tree `id > 60`)
(an index would only work when you know entire key value, e.g. no `like %str%`)
So, for a web app we would know what queries are going to be run and so can optimise with indexes?
Generally a correlated sub query can be replaced by a join, which is more efficient in a RDBMS.

Transaction Processing:
