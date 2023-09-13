select 
  distinct family_name || ', ' || given_name, 
  count(family_name) as family_num
from Directors 
where age >= 18
group by
  family_num
having
  count(family_name) > 2
order by 
  family_num ASC
limit 10;
