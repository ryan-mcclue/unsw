<!-- SPDX-License-Identifier: zlib-acknowledgement -->
```
create function 
  product_accum(state integer, value integer) returns integer
as $$
  select state * value;
$$ language sql;

create function
  strip_comma(final text) returns text
as $$
begin
  return substring(final, 2);
end
$$ language plpgsql;

create aggregate product(integer) (
  stype = integer,
  initcond = 1,
  sfunc = product_accum,
  -- finalfunc = finalise_func 
);

-- anyelement type
```

Too expensive
```
create assertion namecount check (
  not exists (
    select p.name
    from People p
    group by p.name
    having count(*) > 10
  )
);
```

```
create trigger mytrigger
before/after insert/delete or update on table
for each row execute procedure triggerfunc();
```
insert --> new
update --> new/old
delete --> old
An exception in a trigger cause a roll-back
each row --> trigger on each tuple
each statement --> trigger when all tuples updated (so no new and old)
