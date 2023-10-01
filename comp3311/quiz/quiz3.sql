drop table if exists enrolments cascade;
create table enrolments (
    student text,
    course  text,
    mark    integer check (mark between 0 and 100),
    grade   char(1) check (grade between 'A' and 'E'),
    primary key (student,course)
);

insert into enrolments values ('james', 'COMP1917 12s1', 50, 'D'),
 ('peter', 'COMP1917 12s1', 45, 'E'),
 ('john', 'COMP1917 12s1', 90, 'A'),
 ('peter', 'COMP1917 12s2', 40, 'E'),
 ('john', 'COMP1927 12s2', 85, 'A'),
 ('james', 'COMP1927 12s2', 55, 'D'),
 ('james', 'COMP2911 13s1', 50, 'D'),
 ('john', 'COMP2911 13s1', 85, 'A'),
 ('john', 'COMP3311 13s2', 70, 'B');

-- select * from enrolments order by course;

create type stu_res as
     (student text, score numeric(5,2));
create or replace function results() returns setof stu_res
as $$
declare
    r record;  res stu_res;
    p text := '';  s integer := 0;  n integer := 0;
begin
    for r in
        select student,mark
        from   enrolments
        order  by student
    loop
        if (p <> r.student and n > 0) then
            res.student := p;
            res.score := (s::float/n)::numeric(5,2);
            return next res;
            s := 0;  n := 0;
        end if;
        n := n + 1;
        s := s + r.mark;
        p := r.student;
    end loop;
    if (n > 0) then
        res.student := r.student;
        res.score := (s::float/n)::numeric(5,2);
        return next res;
    end if;
end;
$$ language plpgsql;

select * from results() order by student;
