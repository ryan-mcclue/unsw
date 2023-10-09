drop view if exists q2;
create or replace view q2(style, min_abv, max_abv)
as
select s1.name, s1.min_abv, s1.max_abv
from styles s1
where (s1.max_abv - s1.min_abv) = (select max(s.max_abv - s.min_abv) from styles s)
;

-- select * from q2; 
select * from q2 order by style;

-- Write a view Q2(style,min_abv,max_abv) that determines which
-- style(s) have the largest difference between their minimum and maximum ABV
-- values (i.e. the widest range of alcohol levels).
-- The columns in the result are:
-- • style = the name of the style
-- • min_abv = the minimum ABV for the style ( Styles.min_abv )
-- • max_abv = the maximum ABV for the style ( Styles.max_abv )
