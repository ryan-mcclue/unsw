update employees 
set salary = salary * 0.25
where age < 25;

update employees e
set e.salary = salary * 1.1 
where e.id in 
-- IMPORTANT(Ryan): This is equivalent to a join
(select eid 
 from departments d, worksin w
 where d.dname = 'Sales'
 and d.did = w.did)

create table employees (
  did integer references departments(did) on delete cascade, -- so if department deleted, this will be deleted
  did integer references departments(did) default 1, -- so if department deleted, this will be 1 (so, have a default table)
  constraint timecheck
   check (1.0 >= (select sum(w.percent) from worksin wi where w.eid = eid))
);

select distinct sid
from catalog c
natural join parts p
where p.colour = 'red' or p.colour = 'green';

and exists (select p2.pid where p2.pid = c2.pid) 

(select s.id
where p.colour = 'green')
intersect
(select s.id
where p.colour = 'red');


