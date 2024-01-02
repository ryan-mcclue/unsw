drop view if exists brewery_ratings cascade;
create or replace view brewery_ratings(name, rating)
as
select br.name, avg(b.rating)::numeric(3, 1) -- avg() ignores null 
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

--select * from q4; 

--select * from q4 order by brewery

-- Write a view Q4(brewery,rating) that returns the brewery (or breweries)
-- with the maximum average rating for all their beers.
-- The columns in the result are:
-- • brewery = the name of the brewery
-- • rating = average rating for rated beers by that brewery
-- To avoid beweries with a single high-rated beer coming out on top, we only
-- consider breweries that have at least five rated beers. If beers are brewed
-- collaboratively, give the rating to both the breweries involved. Make sure that
-- you compute the average rating using floating point numbers; if you use
-- integers, PostgreSQL truncates to an integer like C does. Don't include beers
-- with no rating (i.e. Beers.rating is NULL ).
