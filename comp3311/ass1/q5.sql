create or replace function q5(pattern text) returns table(beer text, container text, std_drinks numeric)
as $$
select b.name, b.volume || 'ml ' || b.sold_in::text, (b.volume * b.abv * 0.0008)::numeric(3, 1)
from beers b
where lower(b.name) LIKE lower('%' || $1 || '%')
$$ 
language sql ;

select * from q5('fairy'); 

-- Alcohol consumption is often measured in term of "standard drinks". This can
-- be calculated by the formula: <
-- volume × ABV × 0.0008
-- The number of standard drinks is usually printed on the container, but just in
-- case ...
-- Write an SQL function Q5(pattern text) whose argument is a pattern
-- representing part of a beer name. The function returns a set of 0 or more tuples
-- for any beers whose name contains the pattern, and with the following fields:
-- • beer = full name of a beer
-- • container = container that the beer is sold in (e.g. 440ml can )
-- • std_drinks = the number of standard drinks in the container
-- You must define the function as follows
-- ... Q5(pattern text) returns table(beer text, container text, std_drinks numer
-- The standard drinks value is of type numeric(3,1) . You will need to
-- determine how to construct the container string.
