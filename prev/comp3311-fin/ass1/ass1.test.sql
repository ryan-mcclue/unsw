drop view if exists q1;
create or replace view q1(state, nbreweries)
as
select l.region, count(l.region)
from locations l
join breweries b on (b.located_in = l.id)
where l.region is not null and l.country = 'Australia'
group by l.region
;

drop view if exists q2;
create or replace view q2(style, min_abv, max_abv)
as
select s1.name, s1.min_abv, s1.max_abv
from styles s1
where (s1.max_abv - s1.min_abv) = (select max(s.max_abv - s.min_abv) from styles s)
;

drop view if exists q3;
create or replace view q3(style, lo_abv, hi_abv, min_abv, max_abv)
as
select distinct s.name,
(select min(b1.abv) from beers b1 where b1.style = s.id), 
(select max(b1.abv) from beers b1 where b1.style = s.id),
s.min_abv, s.max_abv
from styles s
join beers b on (b.style = s.id)
where (s.min_abv != s.max_abv) and (b.abv < s.min_abv or b.abv > s.max_abv)
;

drop view if exists brewery_ratings cascade;
create or replace view brewery_ratings(name, rating)
as
select br.name, avg(b.rating)::numeric(3, 1)
from breweries br
join brewed_by bb on (bb.brewery = br.id)
join beers b on (b.id = bb.beer)
group by br.name
having count(*) >= 5
;

drop view if exists q4;
create or replace view q4(brewery, rating)
as
select name, rating
from brewery_ratings
where rating = (select max(rating) from brewery_ratings)
;

create or replace function q5(pattern text) returns table(beer text, container text, std_drinks numeric)
as $$
select b.name, b.volume || 'ml ' || b.sold_in::text, (b.volume * b.abv * 0.0008)::numeric(3, 1)
from beers b
where lower(b.name) LIKE lower('%' || $1 || '%')
$$ 
language sql ;

drop function if exists q6 cascade;
create or replace function q6(pattern text) returns 
  table(country text, first integer, nbeers integer, rating numeric)
as $$
  select l.country, min(b.brewed), count(b.name)::integer, avg(b.rating)::numeric(3, 1) from
  beers b join brewed_by bb on (b.id = bb.beer)
  join breweries bw on (bw.id = bb.brewery) 
  join locations l on (l.id = bw.located_in)
  where lower(l.country) LIKE '%' || lower(pattern) || '%'
  group by l.country 
$$
language sql ;

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

drop type if exists beerhops cascade;
create type beerhops as (beer text, brewery text, hops text);

drop function if exists q8 cascade;
create or replace function q8(pattern text) returns 
  setof beerhops
as $$
declare
  res beerhops;
  beer_id integer;
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
