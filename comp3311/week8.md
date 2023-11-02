<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Redundancy only applicable for user-facing, e.g. dbms may store something like min-max for column to get quick lookups

Want a lossless decomposition

Superkey more broad term for candidate key as may include non-essential attributes

Break on fds that violate BCNF
IMPORTANT: Might have to split up fds to account for missing attributes that have previously been broken up
Could also finish when no relevent fds

3NF decomposition (tends to break things up more than BCNF)
1. Reduce fds to single attributes on LHS (this is minimal cover?)
2. Create tables on each fd
3. Add in key as a new table if key not present in a table

IMPORTANT: redundant data might be for performance reasons

Relational algebra operations:
* renaming (like identity function on contents)
`rename[new_relation_name(attr1, attr2)](original_relation_name)`
* projection(columns) (like `select distinct` in sql)
`project[attr1,attr2](relation)`
* selection(rows, e.g:age>18)
`select[cond](relation)`
* union/intersection/difference (require relation compatibility)
* join (these combine non-compatible relations)
`rel1 join[key] rel2`
IMPORTANT: for any join, think of two nested for loops
IMPORTANT: join size can be larger of two table sizes as single attribute can match multiple times
* product (cartesian product, e.g. for r1 in A: for r2 in B: {r1, r2})
* natural join (like product but only on rows which have same attribute values for all SAME NAMED attributes)
* theta join (like a standard join, but allows for conditions other than just equality)
TODO: theta join must common in sql?
* division (table dividing by must share attribute name)
returns tuples that for each instance of an attribute, have a corresponding value for each divisor
so, use in 'for all' scenarios
```
-- sel[drinker=ryan || drinker=loc]

ryan_bars(Bars.*) = sel[drinker=ryan](Bars)
loc_bars(bar) = sel[drinker=loc](Bars)
both_bars(bar) = ryan_bars union loc_bars
```

Generally a correlated sub query can be replaced by a join, which is more efficient in a RDBMS.

Query Processing:
SQL is parsed into relational algebra then query optimiser.
(sql parser allows for user-defined operators?)

Transaction Processing:
