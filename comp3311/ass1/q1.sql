create or replace view q1
as
select l.region
from locations l
;

select * from q1; 

-- Write a view Q1(state,nbreweries) that returns a list of Australian
-- states and a count of the number of breweries in each state.
-- The columns in the result are:
-- • state = the name of a state (region)
-- • nbreweries = a count of the number of breweries in that state
