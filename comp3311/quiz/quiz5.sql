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

create type IntPair as (x integer, y integer);
create function 
    next_state(p IntPair, n integer) returns IntPair
as $$
begin
    if (p.x is null) then
        p.x := n;
    elsif (p.y is null) then
        if (n < p.x) then
            p.y := n;
        elsif (n > p.x) then
            p.y := p.x; p.x := n;
        end if;
    elsif (n > p.x) then
        p.y := p.x; p.x := n;
    elsif (n < p.x and n > p.y) then
        p.y := n;
    end if;
    return p;
end;
$$ language plpgsql;

create function
    second(p IntPair) returns integer
as $$
begin
    return p.y;
end;
$$ language plpgsql;

create aggregate max2 (int) (
    sfunc = next_state,
    stype = IntPair,
    finalfunc = second
);

select max2(mark) from Enrolments;
