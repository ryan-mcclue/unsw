drop view if exists q3;
create or replace view q3(style, lo_abv, hi_abv, min_abv, max_abv)
as
select distinct s.name,
(select min(b1.abv) from beers b1 where b1.style = s.id), -- correlated subquery
(select max(b1.abv) from beers b1 where b1.style = s.id),
s.min_abv, s.max_abv
from styles s
join beers b on (b.style = s.id)
where (s.min_abv != s.max_abv) and (b.abv < s.min_abv or b.abv > s.max_abv)
;

--select * from q3; 
select * from q3 order by style;


-- Write a view Q3(style,lo_abv,hi_abv,min_abv,max_abv) that
-- gives a list of beer styles satisfying the properties:
-- • the minimum and maximum ABVs for the style are different
-- • some beer brewed in the style has an ABV outside the min/max range
-- The columns in the result are:
-- • style = the name of the style
-- • lo_abv = lowest ABV of any beer made in that style
-- • hi_abv = highest ABV of any beer made in that style
-- • min_abv = the minimum ABV for the style ( Styles.min_abv )
-- • max_abv = the maximum ABV for the style ( Styles.max_abv )
