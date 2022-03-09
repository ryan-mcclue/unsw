select x.name, count(y.id)
from x join y on (x.id = y.x_id)
group by x.name;

select x.name, count(y.id)
from x left outer join y on (x.id = y.x_id)
group by x. name;

select x. name, count(y.id)
from x right outer join y on (x.id = y.x_id)
group by x.name;

select x.name,
(select count(x_id) from y where y.x_id = x.id) as count
from x full outer join y on (x.id = y.x_id);

select distinct x.name,
(select count(x_id) from y where y.x_id = x.id) as count
from x left outer join y on (x.id = y.x_id) ;



create table x
(
  id integer primary key, name varchar(20) unique
);
insert into x(id, name) values
  (1, 'ryaA'),
  (2, 'B'),
  (3, 'C');
  
create table y
(
  id integer primary key, x_id integer references x(id), defn text
);
insert into y(id, x_id, defn) values
  (1, 1, 'defn'),
  (2, 1, 'defn'),
  (3, 1, 'defn'),
  (4, 2, 'defn'),
  (5, 2, 'defn');


select sname from Suppliers where sid in 
(
  ()
  intersect
  ()
)


select * from Catalog c 
join Suppliers s using(sid)
join Parts p using(pid)
where not exists(
  (select pid from Parts where colour = 'red' or colour = 'green')
  except
  (select c.pid from Catalog c where c.sid = s.sid)
)
