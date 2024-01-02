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
By default, psql creates index on primary key

So, for a web app we would know what queries are going to be run and so can optimise with indexes?
Generally a correlated sub query can be replaced by a join, which is more efficient in a RDBMS.

Can do `\timing query`
Can see execution plan and time with `explain analyze query` (shows a pre-order traversal of plan)

DBMS maintain data integrity through transactions via ACID (atomic, consistent, isolated, durable)
Transaction is an atomic unit of work. Can be abstracted to only read/write operations
A schedule outlines execution of transactions; often they are run concurrently
For DBMS, serialisation means that a concurrent transaction can be transformed to an iterative transaction
1. conflict serialisability means read/write occur in 'right' order
(no cycles in precedance graphs)
(draw arrow if Read and Write. arrow direction from first)
2. view serialisability means reads see 'correct' version of data
(less conservative than conflict; so some schedules could be view but not conflict)

Lock-based concurrency or multi-version concurrency (i.e. at start, each see unique snapshot so no blocking) common.
In MVCC, each tuple effectively a linked list of recent versions. periodic vacuum process deletes tuples no longer accessible

`raise exception` will perform a `rollback`
`alter table` will `lock table`
`update` will acquire row-level lock
locks can be in `share mode` (simply reading) or `exclusive`
Can also be explicit: `begin; commit; rollback`

Some limitations of relational dbms:
1. Big data where performance inmpacted if store all in a single place; could do sharding 
2. Binary data; i.e. find songs like this
3. Inexact information retrieval, e.g. certainty of data giving probability of data being correct

TODO: noSQL, mongo etc.
Graph databases allows for knn etc.
