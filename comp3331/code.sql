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

CREATE VIEW
CourseMarksAndAverages(course,term,student,mark,avg)
AS
SELECT s.code, termName(t.id), e.student, e.mark,
avg(mark) OVER (PARTITION BY course)
FROM CourseEnrolments e
JOIN Courses c on c.id = e.course
JOIN Subjects s on s.id = c.subject
JOIN Terms t on t.id = c.term;

SELECT b1.name, b2.name
FROM Beers b1 JOIN Beers b2 ON (b1.brewer = b2.brewer)
WHERE b1.name < b2.name;

left outer join -- if lhs exists and rhs doesn't, null fill rhs
right outer join -- if rhs exists and lhs right doesn't, null fill lhs

SELECT *
FROM R
WHERE R.a > ALL(SELECT x FROM S WHERE Cond) -- set condition operator
-- INTERSECT, EXCEPT, UNION

-- GROUP BY produces one tuple for each group; HAVING filters these groups

-- PARTITION augments each tuple with group based values (TODO: is this a window function?)
SELECT city, date, temperature
min(temperature) OVER (PARTITION BY city) as lowest,
max(temperature) OVER (PARTITION BY city) as highest
FROM Weather;

SELECT course, student, mark
FROM (
  SELECT course, student, mark,
  avg(mark) OVER (PARTITION BY course)
  FROM Enrolments
) AS CourseMarksWithAvg -- subquery must be named, even if not used
WHERE mark < avg;

WITH CourseMarksWithAvg AS
(SELECT course, student, mark,
avg(mark) OVER (PARTITION BY course)
FROM Enrolments)
SELECT course, student, mark, avg
FROM CourseMarksWithAvg
WHERE mark < avg;

-- TODO: understand
-- finds all sub-parts in a part (sub-parts, sub-sub-parts, etc.)
WITH RECURSIVE IncludedParts(sub_part, part, quantity) AS (
SELECT sub_part, part, quantity
FROM Parts WHERE part = GivenPart
UNION ALL
SELECT p.sub_part, p.part, p.quantity
FROM IncludedParts i, Parts p
WHERE p.part = i.sub_part
)
SELECT sub_part, SUM(quantity) as total_quantity
FROM IncludedParts
GROUP BY sub_part

-- 
