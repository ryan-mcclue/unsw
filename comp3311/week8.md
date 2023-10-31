<!-- SPDX-License-Identifier: zlib-acknowledgement -->

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
* renaming(like identity function on contents)
`rename[newname(attr1, attr2)](original)`
* projection(columns) 
`project[attr1,attr2](relation)`
* selection(rows, e.g:age>18)
`select[cond](relation)`
* join 
`rel1 join[key] rel2`
* union/intersection/difference (require relation compatibility)

IMPORTANT: projection is like `select distinct` in sql

