drop type if exists beerhops cascade;
create type beerhops as (beer text, brewery text, hops text);

drop function if exists q8 cascade;
create or replace function q8(pattern text) returns 
  setof beerhops
as $$
declare
  res beerhops;
  beer_id integer; -- perhaps prefix variable names with _
begin
  for beer_id in
    select b.id from beers b
    where lower(b.name) LIKE '%' || lower(pattern) || '%'
  loop
    select b.name, string_agg(bw.name, '+' order by bw.name) into res.beer, res.brewery
    from beers b
    join brewed_by bb on (b.id = bb.beer)
    join breweries bw on (bw.id = bb.brewery) 
    where b.id = beer_id
    group by b.name;
  
    select string_agg(i.name, ',' order by i.name) into res.hops
    from beers b
    join contains c on (c.beer = b.id)
    join ingredients i on (c.ingredient = i.id)
    where b.id = beer_id and i.itype = 'hop';

    if (res.hops is null) then
      res.hops := 'no hops recorded';
    end if;
  
    return next res;
  end loop;
end;
$$
language plpgsql ;

select * from q8('dank');

-- Write a PLpgSQL function Q8(pattern text) whose argument is a string
-- representing part of a beer name. The function returns a set of 0 or more tuples
-- for any beers whose name contains the pattern (case-insensitive matching),
-- and with the following fields:
-- • beer = full name of a beer
-- • brewery = which brewery (or breweries) the beer was made in
-- • hops = a comma-separated list of the names of hops used in the beer
-- If the beer is a collaboration beer ( brewed_by more than one brewery), the
-- names of all breweries involved must be included, separated by '+'
-- characters, and appear in alphabetical order of the brewery names.
-- The names of the hops in the list of hops contained in the beer must be
-- separated by ',' characters, and must appear in alphabetical order. If a beer
-- has no hop ingredients recorded, then the hops string should be set to:
-- no hops recorded
-- The function needs to be defined differently to the functions above that returned
-- table(...) . For this function, we need to define a new tuple type and have
-- the function return a setof tuples of that type:
-- drop type if exists BeerHops cascade;
-- create type BeerHops as (beer text, brewery text, hops text);
-- create or replace function
-- Q8(pattern text) returns setof BeerHops
-- ...
-- The drop type statement is included so that you can reload the ass1.sql
-- file multiple times without generating errors. It does, however, generate a
-- NOTICE , which looks like an error, but is actually harmless.
