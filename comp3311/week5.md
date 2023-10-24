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

triggers are atomic
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

foreign key existance will be checked automatically, however:
```
create function
  check_fk() returns trigger
as $$
begin
  perform * from S where id = new.s;
  if (not found) then
    raise NOTICE 'Invalid';
    if (TG_OP = 'INSERT') then
      return NULL;
    endif;
    if (TG_OP = 'UPDATE') then
      return old; -- return old to not pass changes
    endif;
  else
    return new;
  end if;
end;
```

When working with sql in say python, try to construct as much logic into single query as possible

```
try:
  if on_vxdb2:
    db = "dbname=ass2"
  else:
    db_params = {
        "host": "localhost",
        "port": "5432",
        "dbname": "mydb",
        "user": "graham",
        "password": "mypass",
    }
    db = psycopg2.extensions.make_dsn(db_params)

  c = psycopg2.connect(db)
  cur  = c.cursor()

  -- sql_str = cur.mogrigfy() debugging

  -- IMPORTANT(Ryan): This won't create an injection issue, as sql template understands the expected format
  -- i.e. will wrap with quotes correctly
  -- so, just use sql templates to prevent injection issues
  cur.execute("select * from R where x = %s", ["hi there"])
  res = cur.fetchall()
  if not res:
    print("no results")
  else:
    for tup in res:
      x, y, z = tup

  c.commit()
except Exception as e:
  print()
finally:
  if c:
    c.close()

```
