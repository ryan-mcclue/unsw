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

-- select * from q6('australia') order by country;
-- select * from q6('aust') order by country;
-- select * from q6('land') order by country;
--select * from q6('oo') order by country;



-- Write an SQL function Q6(pattern text) whose argument is a string
-- representing part of a country name. The function returns a set of 0 or more
-- tuples for any countries whose name contains the pattern (case-insensitive
-- matching), and with the following fields:
-- • country = full name of a country
-- • first = the earliest year that a beer was brewed in that country
-- • nbeers = the number of beers brewed in that country
-- • rating = the average rating of beers brewed in that country
-- You must define the function as follows
-- ... Q6(pattern text) returns
-- table(country text, first integer, nbeers integer, rating numeric)
-- The rating should be cast to type numeric(3,1) within the function.
