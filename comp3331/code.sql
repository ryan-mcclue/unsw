-- everything lowercase unless quoted
-- typecast '10'::integer
-- builtin functions like substring(), lower()
-- aggregations on columns/attributes count(), sum()
-- cannot use logical operators to check for null, must use: is null. coalesce() also useful

initdb, createdb/dropdb

-----------------------------
-- metadata-definition.sql --
-----------------------------
create domain Grade as char(2) check (value in ('FL', 'PS', 'CR')); -- set literal
create type Grade as enum ('FL', 'PS', 'CR');

create table Students (
  -- name, domain, constraint ... table-constraints
  employee_id int primary key, -- primary key is a constraint
  name varchar(30) not null,
  gender char(1) check (gender in ('M', 'F')),
  term char(4) not null check (term ~'[0-9]{2}T[0-3]') ,
  birthday date not null
  degree integer references Degrees(did),
);

-------------------------
-- metadata-update.sql --
-------------------------
drop table Driver
alter table Driver

-------------------------
-- data-update.sql ------
-------------------------
insert into Students(id, name) values (123123, 'Ryan') -- tuple literal

, update, delete

-------------------------
-- query.sql ------------
-------------------------
select from where
like ~'regex'

