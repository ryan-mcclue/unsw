<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Function often used interchangebly with stored procedure

`select name, func(name) from Beers;`
`select sum(my_sequence) from my_sequence(1, 10);`

Plpgsql gives data structures, looping constructs, recursion, overloading functions etc. over plain sql functions

`while i <= 1 loop end loop;`

`returns table(x integer, y integer) -> variables x, y and return next`
`returns setof r -> r.x, r.y and return next r`

`raise notice 'Name is %', name`
`raise exception` (will go into error log)

`select ...; if not found then` (found is a special local variable inside each function for previous query status)

A tuple type can be implicitly created with a table/view or explicitly
with `create type`

To get new id, `select max(id)+1 into new_id from Beers`
`insert into Beers values (name) returning id`

`create sequence my_seq start 1 increment 1;`
`select nextval('my_seq'), currval('my_seq')` (this is atomic)
(for default table) `select nextval(Table_attr_seq)` 
serial is shorthand for associating column with an integer sequence

`query_str := 'select count(*) from ' || quote_ident(table_name);`, `quote_literal()`
`execute query_str into num_tups;`

psql won't delete/update in place, i.e. will mark it for deletion at some point

```
exception
  when division_by_zero then
```

DBMS can filter really fast if have an index on that attribute, i.e. won't have to do an entire table scan

```
func(c integer, OUT square integer)
square := square * square
```

`create aggregate agg(numeric)`
