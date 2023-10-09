drop view if exists q1; -- necessary to allow columns being renamed in view
create or replace view q1(state, nbreweries)
as
select l.region, count(l.region)
from locations l
join breweries b on (b.located_in = l.id)
where l.region is not null and l.country = 'Australia'
group by l.region
;

--select * from q1; 
select * from q1 order by state;

-- Write a view Q1(state,nbreweries) that returns a list of Australian
-- states and a count of the number of breweries in each state.
-- The columns in the result are:
-- • state = the name of a state (region)
-- • nbreweries = a count of the number of breweries in that state
