drop function if exists q7 cascade;
create or replace function q7(_beerID integer) returns 
  text
as $$
declare
  beer_id integer;
  beer_name text;
  ingredient record;
  ingredients_count integer = 0;
  ret text;
begin
  select b.id, b.name into beer_id, beer_name
  from beers b
  where b.id = _beerID;

  if (beer_id is null) then
    return 'No such beer (' || _beerID || ')';
  end if;

  ret := '"' || beer_name || '"';

  for ingredient in 
    select i.name, i.itype 
    from ingredients i
    join contains c on (c.ingredient = i.id)
    join beers b on (c.beer = b.id)
    where b.id = beer_id
    order by i.name
  loop
    if (ingredients_count = 0) then
      ret := ret || E'\n' || '  contains:';
    end if;

    ret := ret || E'\n' || '    ' || ingredient.name || ' (' || ingredient.itype || ')';

    ingredients_count := ingredients_count + 1;
  end loop;

  if (ingredients_count = 0) then
    ret := ret || E'\n' || '  no ingredients recorded';
  end if;

  return ret;
end;
$$
language plpgsql ;

--select q7(123);
-- select q7(366);
-- select q7(891);
-- select q7(893);
--select q7(1202);
 select q7(1226);





-- Write a PLpgSQL function Q7(_beerID integer) whose argument is an
-- integer representing a beer ID ( Beers.id ) value. The function returns a
-- single text string, formatted as follows:
-- • if the ID does not exist in the Beers table, simply return the string
-- No such beer (_beerID)
-- • if the ID does exist, the first line contains the name of the beer enclosed in
-- "..."
-- • if the beer has no ingredients recorded, simply add a second line to the
-- return string and return the two-line string, e.g.
-- "Name of beer"
-- no ingredients recorded
-- Note that there are exactly two spaces before the no ingredients .
-- • otherwise append a string containing a list of ingredients, one per line, in
-- order of the ingredient names:
-- ◦ each line starts with exactly four spaces
-- ◦ then the name of the ingredient
-- ◦ then the type of the ingredient in (...)
-- Note that the return value of this function is a single text string. It will likely
-- contain embedded newline characters, but there should be no trailing newline
-- character. There are examples of the return values in the Examples page, in
-- case the above is not clear enough.
-- Note also that, in its output, psql uses a plus + symbol to indicate that there is
-- an embedded newline. The plus symbol is simply an artifact of the way psql
-- displays strings. Do not embed plus symbols into your return string.
