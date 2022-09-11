-- comp3311 22T1 Assignment 1

-- Q1
-- gives the student id and name of any student who has enrolled in more than 4 distinct programs at UNSW. 
-- The name should be take from the People.name field for the student, and the student id should be taken from People.unswid. 
create or replace view Q1(unswid, name)
as
select p.unswid, p.name
from People p
join Students s on s.id = p.id
join Course_Enrolments ce on ce.student = s.id
join Courses c on c.id = ce.course
group by p.unswid, p.name -- 'group by' required for 'having'
having count(distinct c.subject) > 4
;

-- Q2
--  gives the unswid and name of the person(s) who has been course tutor of the most courses at UNSW
create or replace view Q2(unswid, name, course_cnt)
as
select p.unswid, p.name, count(*)
from People p
join Staff s on s.id = p.id
join Course_Staff cs on cs.staff = s.id
join Staff_Roles sr on sr.id = cs.role
where sr.name = 'Course Tutor'
group by p.unswid -- 'group by' scopes count(*)
order by count(*) desc
limit 1
--... SQL statements, possibly using other views/functions defined by you ...
;


-- Q3
-- all the distinct international students who have enrolled in the course offered by the School of Law (refers to the OrgUnits.Name) and got a mark higher than 85. 
create or replace view Q3(unswid, name)
as
select distinct p.unswid, p.name
from People p
join Students s on s.id = p.id
join Course_Enrolments ce on ce.student = s.id
join Courses c on c.id = ce.course
join Subjects subj on subj.id = c.subject
join Orgunits org on org.id = subj.offeredby
where s.stype = 'intl' and ce.mark > 85 and org.name = 'School of Law'
--... SQL statements, possibly using other views/functions defined by you ...
;


-- Q4
-- gives all the distinct local students who enrolled in COMP9020 and COMP9331 (refer to Subjects.code) in the same term. 

create or replace view COMP9020(unswid, name, term)
as
  select p.unswid, p.name, c.term
  from People p
  join Students s on s.id = p.id
  join Course_Enrolments ce on ce.student = s.id
  join Courses c on c.id = ce.course
  join Subjects subj on subj.id = c.subject
  where s.stype = 'local' and subj.code = 'COMP9020'
;
create or replace view COMP9331(unswid, name, term)
as
  select p.unswid, p.name, c.term
  from People p
  join Students s on s.id = p.id
  join Course_Enrolments ce on ce.student = s.id
  join Courses c on c.id = ce.course
  join Subjects subj on subj.id = c.subject
  where s.stype = 'local' and subj.code = 'COMP9331'
;

create or replace view Q4(unswid, name)
as
select distinct unswid, name
from COMP9020 c9020 
join COMP9331 c9331 on c9020.unswid = c9331.unswid
where c9020.term = c9331.term;
--... SQL statements, possibly using other views/functions defined by you ...
;


-- that gives the term and the minimum fail rate of the course COMP3311 from year 2009 to year 2012. 
create or replace view COMP3331WithMark(term, counter)
as
select c.term, count(*)
from People p
join Students s on s.id = p.id
join Course_Enrolments ce on ce.student = s.id
join Courses c on c.id = ce.course
join Subjects subj on subj.id = c.subject
join Terms t on t.id = c.term
where subj.code = 'COMP3311' and 
ce.mark is not null and 
t.year between 2009 and 2012
group by c.term
;

create or replace view COMP3331WithFailingMark(term, counter)
as
select c.term, count(*)
from People p
join Students s on s.id = p.id
join Course_Enrolments ce on ce.student = s.id
join Courses c on c.id = ce.course
join Subjects subj on subj.id = c.subject
join Terms t on t.id = c.term
where subj.code = 'COMP3311' and 
ce.mark < 50 and 
t.year between 2009 and 2012
group by c.term
;
-- Q5a
create or replace view Q5a(term, min_fail_rate)
as
select wm.term, wm.counter / fm.counter as fail_rate
from COMP3331WithMark wm join COMP3331WithFailingMark fm on wm.term = fm.term
group by wm.term, fail_rate
order by fail_rate asc
limit 1
--... SQL statements, possibly using other views/functions defined by you ...
;


-- that gives the term and the minimum fail rate of the course COMP3311 from year 2016 to year 2019.  
-- Q5b
create or replace view Q5b(term, min_fail_rate)
as
--... SQL statements, possibly using other views/functions defined by you ...
;


-- Q6
-- people.id, subjects.code
-- returns the student's mark for the course with the given subject code
create or replace function 
	Q6(id integer,code text) returns integer
as $$
select ce.mark
from People p
join Students s on s.id = $1
join Course_Enrolments ce on ce.student = s.id
join Courses c on c.id = ce.course
join Subjects subj on subj.id = c.subject
where subj.code = $2 
--... SQL statements, possibly using other views/functions defined by you ...
$$ language sql;


-- Q7
-- e.g. 2019, 'T1'
-- returns a list of all the postgraduate COMP courses (refers to Subjects.code starting with COMP) offered at the given year and session. 
-- An postgraduate course is the one whose Subjects.career is PG.
create or replace function 
	Q7(year integer, session text) returns table (code text)
as $$
select subj.code
from People p
join Students s on s.id = $1
join Course_Enrolments ce on ce.student = s.id
join Courses c on c.id = ce.course
join Subjects subj on subj.id = c.subject
join Terms t on t.id = c.term
where subj.code like ~'^COMP.*$' and subj.career = 'PG' and t.year = $1 and t.session = $2
-- TODO(Ryan): in db term session names are strange like X1, S2. No standard ones like T1 as mentioned in question? 
--... SQL statements, possibly using other views/functions defined by you ...
$$ language sql;


-- Q8
create or replace function
	Q8(zid integer) returns setof TermTranscriptRecord
as $$
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;


-- Q9
create or replace function 
	Q9(gid integer) returns setof AcObjRecord
as $$
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;


-- Q10
create or replace function
	Q10(code text) returns setof text
as $$
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;

