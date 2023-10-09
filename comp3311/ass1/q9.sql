drop type if exists collab cascade;
create type collab as (brewery text, collaborator text);

drop function if exists q9 cascade;
create or replace function q9(breweryid integer) returns 
  setof collab
as $$
declare
  collabs collab;
  bw_name text;
  collab record;
  collab_count integer = 0;
begin
  -- Check if valid
  select bw.name into bw_name
  from breweries bw
  where bw.id = breweryid;

  if (not found) then
    collabs.brewery := 'No such brewery (' || breweryid || ')'; 
    collabs.collaborator := 'none';
    return next collabs;
    return;
  end if;

  -- Collaborations
  for collab in 
    with base as (
      select *
      from brewed_by
      where brewery = breweryid
    )
    -- seems to be duplicate entries?
    select distinct bw_by.brewery 
    from brewed_by bw_by
    join base b on bw_by.beer = b.beer
    where bw_by.brewery != breweryid
    order by bw_by.brewery
  loop
    select bw.name into collabs.collaborator
    from breweries bw
    where bw.id = collab.brewery;

    if (collab_count = 0) then
      collabs.brewery := bw_name;
    else
      collabs.brewery := null;
    end if;

    return next collabs;

    collab_count := collab_count + 1;
  end loop;
  
  if (collab_count = 0) then
    collabs.brewery := bw_name;
    collabs.collaborator := 'none';
    return next collabs;
  end if;

end;
$$ 
language plpgsql ;

--select * from q9(0);
--select * from q9(49);
--select * from q9(149);
--select * from q9(267);
--select * from q9(118);
--select * from q9(183);
--select * from q9(184);





-- Write a PLpgSQL function Q9(breweryID integer) whose argument is
-- an integer, possibly containing a Breweries.id value. The function returns
-- a set of Collab tuples (see below) for the brewery, and with the following
-- fields:
-- • brewery = full name of a brewery, or NULL
-- • collaborator = full name of another brewery, the string 'none'
-- The Collab tuples give the names, in alphabetical order, of all the breweries
-- that the indicated brewery ( breweryID ) has made collaboration beers with.
-- There are a number of different cases for what appears in the Collab tuples:
-- • breweryID is not a valid Breweries.id value
-- ◦ brewery has the value 'No such brewery (breweryID)'
-- ◦ collaborator has the value 'none'
-- • the brewery has never made a collaboration beer
-- ◦ brewery contains the name of the brewery whose id is
-- breweryID
-- ◦ collaborator has the value 'none'
-- • the brewery has collaborated with exactly one other brewery
-- ◦ brewery contains the name of the brewery whose id is
-- breweryID
-- ◦ collaborator contains the name of the collaborating brewery
-- • the brewery has collaborated with more than one other brewery there are multiple tuples for this brewery
-- ◦ in the first tuple, brewery contains the name of the brewery whose
-- id is breweryID
-- ◦ in all subsequent tuples, brewery has the value NULL
-- ◦ in all tuples, collaborator contains the name of a collaborating
-- brewery
-- The function needs to be defined differently to the functions above that returned
-- table(...) . For this function, we need to define a new tuple type and have
-- the function return a setof tuples of that type:
-- drop type if exists Collab cascade;
-- create type Collab as (brewery text, collaborator text);
-- create or replace function
-- Q9(_bid integer) returns setof Collab
-- ...
-- The drop type statement is included so that you can reload the ass1.sql
-- file multiple times without generating errors. It does, however, generate a
-- NOTICE , which looks like an error, but is actually harmless.
-- Note that the function always returns at least one tuple, even if breweryID is
-- not valid. Note also that this is different to question Q6, where the list of list of
-- ingredients was formed by string concatentation; in this case, each
-- collaborating brewery is in a separate tuple.
