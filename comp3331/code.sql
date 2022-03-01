-- everything lowercase unless quoted
-- typecast '10'::integer
-- builtin functions like substring(), lower()
-- aggregations on columns/attributes count(), sum()
-- cannot use logical operators to check for null, must use: is null. coalesce() also useful

initdb, createdb/dropdb, pgdump/psql -f

-----------------------------
-- metadata-definition.sql --
-----------------------------
create domain Grade as char(2) check (value in ('FL', 'PS', 'CR')); -- set literal
create type Grade as enum ('FL', 'PS', 'CR');

create table Students (
  -- name, domain, constraint ... table-constraints (primary key and foreign keys)
  employee_id serial primary key, -- primary key is a constraint
  name text not null, -- use text over varchar
  gender char(1) constraint GenderCheck check (gender in ('M', 'F')),
  term char(4) not null check (term ~'[0-9]{2}T[0-3]') ,
  birthday date not null,
  balance float default 0.0,
  -- 
  degree integer references Degrees(did),
  --
  degree integer,
  foreign key (degree) references Degrees(did),
);

-------------------------
-- metadata-update.sql --
-------------------------
drop table Driver -- will delete referencing tables
alter table Driver alter column car set default 'mini';

-------------------------
-- data-update.sql ------
-------------------------
insert into Students(id, name) values (123123, 'Ryan'); -- tuple literal
copy -- psql for efficient large insertions

delete from Students where name = 'el'; -- psql will reject deletion of a tuple if a tuple elsewhere has foreign key referencing it, i.e constraint checking is applied automatically on any change

update Students set name = 'ja' where name = 'el';

-------------------------
-- query.sql ------------
-------------------------
SELECT projectionList -- select avg(mark) as average_mark
FROM relations/joins -- from Students s join Enrolments e on s.id = e.student 
WHERE condition
GROUP BY groupingAttributes -- group by r.x 
HAVING groupCondition -- having max(r.x) < 75 

select from where
like ~'regex'

create view Name(var1, var2) as 
