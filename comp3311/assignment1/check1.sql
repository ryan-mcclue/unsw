-- COMP3311 22T1 Assignment 1
--
-- check.sql ... checking functions
--
-- Written by: John Shepherd, September 2012
-- Updated by: QS, Feb 2022
--

--
-- Helper functions
--

create or replace function
	ass1_table_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_class
	where relname=tname and relkind='r';
	return (_check = 1);
end;
$$ language plpgsql;

create or replace function
	ass1_view_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_class
	where relname=tname and relkind='v';
	return (_check = 1);
end;
$$ language plpgsql;

create or replace function
	ass1_function_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_proc
	where proname=tname;
	return (_check > 0);
end;
$$ language plpgsql;

-- ass1_check_result:
-- * determines appropriate message, based on count of
--   excess and missing tuples in user output vs expected output

create or replace function
	ass1_check_result(nexcess integer, nmissing integer, Qno text) returns text
as $$
declare
	_Qno text = '';
begin
	select split_part(Qno,'_',1) into _Qno;
	if (nexcess = 0 and nmissing = 0) then
		return _Qno||': correct';
	elsif (nexcess > 0 and nmissing = 0) then
		return _Qno||': too many result tuples';
	elsif (nexcess = 0 and nmissing > 0) then
		return _Qno||': missing result tuples';
	elsif (nexcess > 0 and nmissing > 0) then
		return _Qno||': incorrect result tuples';
	end if;
end;
$$ language plpgsql;

-- ass1_check:
-- * compares output of user view/function against expected output
-- * returns string (text message) containing analysis of results

create or replace function
	ass1_check(_type text, _name text, _res text, _query text) returns text
as $$
declare
	nexcess integer;
	nmissing integer;
	excessQ text;
	missingQ text;
begin
	if (_type = 'view' and not ass1_view_exists(_name)) then
		return 'No '||_name||' view; did it load correctly?';
	elsif (_type = 'function' and not ass1_function_exists(_name)) then
		return 'No '||_name||' function; did it load correctly?';
	elsif (not ass1_table_exists(_res)) then
		return _res||': No expected results!';
	else
		excessQ := 'select count(*) '||
			   'from (('||_query||') except '||
			   '(select * from '||_res||')) as X';
		-- raise notice 'Q: %',excessQ;
		execute excessQ into nexcess;
		missingQ := 'select count(*) '||
			    'from ((select * from '||_res||') '||
			    'except ('||_query||')) as X';
		-- raise notice 'Q: %',missingQ;
		execute missingQ into nmissing;
		return ass1_check_result(nexcess,nmissing, _res);
	end if;
	return '???';
end;
$$ language plpgsql;

-- ass1_rescheck:
-- * compares output of user function against expected result
-- * returns string (text message) containing analysis of results

create or replace function
	ass1_rescheck(_type text, _name text, _res text, _query text) returns text
as $$
declare
	_sql text;
	_chk boolean;
begin
	if (_type = 'function' and not ass1_function_exists(_name)) then
		return 'No '||_name||' function; did it load correctly?';
	elsif (_res is null) then
		_sql := 'select ('||_query||') is null';
		-- raise notice 'SQL: %',_sql;
		execute _sql into _chk;
		-- raise notice 'CHK: %',_chk;
	else
		_sql := 'select ('||_query||') = '||quote_literal(_res);
		-- raise notice 'SQL: %',_sql;
		execute _sql into _chk;
		-- raise notice 'CHK: %',_chk;
	end if;
	if (_chk) then
		return 'correct';
	else
		return 'incorrect result';
	end if;
end;
$$ language plpgsql;

-- check_all:
-- * run all of the checks and return a table of results

drop type if exists TestingResult cascade;
create type TestingResult as (test text, result text);

create or replace function
	check_all() returns setof TestingResult
as $$
declare
	i int;
	testQ text;
	result text;
	out TestingResult;
	tests text[] := array[
				'q1', 'q2', 'q3', 'q4', 'q5a', 'q5b',
				'q6a', 'q6b', 'q6c', 'q7a', 'q7b', 'q7c',
				'q8a', 'q8b', 'q8c', 'q9a', 'q9b', 'q9c',
				'q10a','q10b','q10c'
				];
begin
	for i in array_lower(tests,1) .. array_upper(tests,1)
	loop
		testQ := 'select check_'||tests[i]||'()';
		execute testQ into result;
		out := (tests[i],result);
		return next out;
	end loop;
	return;
end;
$$ language plpgsql;


--
-- Test Cases
--

-- Q1 --

create or replace function check_q1() returns text
as $chk$
select ass1_check('view','q1','q1_expected',
                   $$select * from q1$$)
$chk$ language sql;

drop table if exists q1_expected;
create table q1_expected (
    unswid integer,
    name longname
);

COPY q1_expected (unswid, name) FROM stdin;
3001394	Jeffrey Caldwell
3087372	Philip Lun
3108948	Sugianto Arsie
3122927	Seaton Warburton
3132303	Amy Berg
3134147	Hannah Kola
3160479	Ksenia Mardakhaeva
3163349	Kerry Plant
3173796	Adam Rositano
3187169	Giles Erol
3207313	Livio Tjia
3209530	Su Song
3229297	Yoke Anthoney
3245227	Pollyanna Risk
3272803	Jesus Ferrer
3294743	Deviani Hongganata
\.

-- Q2 --

create or replace function check_q2() returns text
as $chk$
select ass1_check('view','q2','q2_expected',
                   $$select * from q2$$)
$chk$ language sql;

drop table if exists q2_expected;
create table q2_expected (
    unswid integer, 
	name longname, 
	course_cnt integer
);

COPY q2_expected (unswid, name, course_cnt) FROM stdin;
9511757	Rochayah Machali	39
\.


-- Q3 --

create or replace function check_q3() returns text
as $chk$
select ass1_check('view','q3','q3_expected',
                   $$select * from q3$$)
$chk$ language sql;

drop table if exists q3_expected;
create table q3_expected (
    unswid integer,
    name longname
);

COPY q3_expected (unswid, name) FROM stdin;
3163431	Dale Frye
\.


-- Q4 --

create or replace function check_q4() returns text
as $chk$
select ass1_check('view','q4','q4_expected',
                   $$select * from q4$$)
$chk$ language sql;

drop table if exists q4_expected;
create table q4_expected (
    unswid integer,
	name longname
);

COPY q4_expected (unswid,name) FROM stdin;
3031788	Melinda Uon
3129900	Veronica Kirkhope
3205692	Yvette Doumani
3255084	Yoke Tan Mustafa
3293851	Jakov Le Hoang
3310373	Tessa Marinakis
3315968	Beifang Ai Ximin
3366245	Aniruddha Jandu
3385445	Paul Took
\.


-- Q5 --

create or replace function check_q5a() returns text
as $chk$
select ass1_check('view','q5a','q5a_expected',
                   $$select * from q5a$$)
$chk$ language sql;

drop table if exists q5a_expected;
create table q5a_expected (
    term shortname,
	fail_rate numeric
);

COPY q5a_expected (term, fail_rate) FROM stdin;
Sem1 2010	0.0370
\.

create or replace function check_q5b() returns text
as $chk$
select ass1_check('view','q5b','q5b_expected',
                   $$select * from q5b$$)
$chk$ language sql;

drop table if exists q5b_expected;
create table q5b_expected (
    term shortname,
	fail_rate numeric
);

COPY q5b_expected (term, fail_rate) FROM stdin;
\.

-- Q6 --

create or replace function check_q6a() returns text
as $chk$
select ass1_check('function','q6','q6a_expected',
                   $$select q6(1013430,'COMP9332')$$)
$chk$ language sql;

drop table if exists q6a_expected;
create table q6a_expected (
    q6 integer
);

COPY q6a_expected (q6) FROM stdin;
63
\.

create or replace function check_q6b() returns text
as $chk$
select ass1_check('function','q6','q6b_expected',
                   $$select q6(1200044,'MMAN3210')$$)
$chk$ language sql;

drop table if exists q6b_expected;
create table q6b_expected (
    q6 integer
);

COPY q6b_expected (q6) FROM stdin;
100
\.

create or replace function check_q6c() returns text
as $chk$
select ass1_check('function','q6','q6c_expected',
                   $$select q6(1123474,'COMP3311')$$)
$chk$ language sql;

drop table if exists q6c_expected;
create table q6c_expected (
    q6 integer
);

COPY q6c_expected (q6) FROM stdin;
\N
\.


-- Q7 --

create or replace function check_q7a() returns text
as $chk$
select ass1_check('function','q7','q7a_expected',
                   $$select * from q7(2003,'S1')$$)
$chk$ language sql;

drop table if exists q7a_expected;
create table q7a_expected (
    code text
);

COPY q7a_expected (code) FROM stdin;
COMP4001
COMP4133
COMP4151
COMP4211
COMP4415
COMP9008
COMP9020
COMP9021
COMP9022
COMP9024
COMP9101
COMP9201
COMP9221
COMP9243
COMP9314
COMP9316
COMP9331
COMP9414
\.

create or replace function check_q7b() returns text
as $chk$
select ass1_check('function','q7','q7b_expected',
                   $$select * from q7(2008,'S1')$$)
$chk$ language sql;

drop table if exists q7b_expected;
create table q7b_expected (
    code text
);

COPY q7b_expected (code) FROM stdin;
COMP4001
COMP4141
COMP4211
COMP4415
COMP4511
COMP9009
COMP9020
COMP9021
COMP9024
COMP9032
COMP9041
COMP9101
COMP9102
COMP9152
COMP9153
COMP9201
COMP9222
COMP9243
COMP9283
COMP9314
COMP9317
COMP9331
COMP9335
COMP9414
COMP9801
COMP9814
COMP9912
COMP9945
\.

create or replace function check_q7c() returns text
as $chk$
select ass1_check('function','q7','q7c_expected',
                   $$select * from q7(2013,'S2')$$)
$chk$ language sql;

drop table if exists q7c_expected;
create table q7c_expected (
    code text
);

COPY q7c_expected (code) FROM stdin;
COMP4121
COMP4418
COMP9020
COMP9021
COMP9024
COMP9032
COMP9041
COMP9151
COMP9171
COMP9181
COMP9222
COMP9331
COMP9335
COMP9336
COMP9415
COMP9431
COMP9511
COMP9945
\.


-- Q8 --

create or replace function check_q8a() returns text
as $chk$
select ass1_check('function','q8','q8a_expected',
					$$select * from q8(1234567)$$)
$chk$ language sql;

drop table if exists q8a_expected;
create table q8a_expected (
    term char(4),
    termwam integer,
    termuocpassed integer
);

COPY q8a_expected (term, termwam, termuocpassed) FROM stdin;
\.


create or replace function check_q8b() returns text
as $chk$
select ass1_check('function','q8','q8b_expected',
                   $$select * from q8(3202320)$$)
$chk$ language sql;

drop table if exists q8b_expected;
create table q8b_expected (
    term char(4),
    termwam integer,
    termuocpassed integer
);

COPY q8b_expected (term, termwam, termuocpassed) FROM stdin;
09s1	56	18
09s2	56	24
10x1	37	\N
10s1	48	12
10s2	41	12
11x1	47	3
11s1	55	18
11s2	65	30
12x1	38	\N
12s1	55	12
12s2	53	12
OVAL	52	141
\.

create or replace function check_q8c() returns text
as $chk$
select ass1_check('function','q8','q8c_expected',
                   $$select * from q8(2261154)$$)
$chk$ language sql;

drop table if exists q8c_expected;
create table q8c_expected (
    term char(4),
    termwam integer,
    termuocpassed integer
);

COPY q8c_expected (term, termwam, termuocpassed) FROM stdin;
03s1	\N	24
03s2	\N	24
06s1	\N	24
06s2	\N	24
OVAL	\N	96
\.


-- Q9 --

create or replace function check_q9a() returns text
as $chk$
select ass1_check('function','q9','q9a_expected',
                   $$select * from q9(1530)$$)
$chk$ language sql;

drop table if exists q9a_expected;
create table q9a_expected (
    objtype text,
    objcode text
);

COPY q9a_expected (objtype, objcode) FROM stdin;
stream	BINFA1
\.

create or replace function check_q9b() returns text
as $chk$
select ass1_check('function','q9','q9b_expected',
                   $$select * from q9(1144)$$)
$chk$ language sql;

drop table if exists q9b_expected;
create table q9b_expected (
    objtype text,
    objcode text
);

COPY q9b_expected (objtype, objcode) FROM stdin;
subject	CHEM1011
subject	CHEM1031
subject	COMP1911
subject	ENGG1000
subject	ENGG1811
subject	MATH1131
subject	MATH1141
subject	MATH1231
subject	MATH1241
subject	MATS1101
subject	PHYS1121
subject	PHYS1131
\.

create or replace function check_q9c() returns text
as $chk$
select ass1_check('function','q9','q9c_expected',
                   $$select * from q9(1117)$$)
$chk$ language sql;

drop table if exists q9c_expected;
create table q9c_expected (
    objtype text,
    objcode text
);

COPY q9c_expected (objtype, objcode) FROM stdin;
subject	BABS1201
subject	BIOM1010
subject	BIOS1301
subject	CEIC1000
subject	CEIC1001
subject	CHEM1011
subject	CHEM1021
subject	CHEM1031
subject	CHEM1041
subject	COMP1921
subject	CVEN1300
subject	CVEN1701
subject	ELEC1111
subject	GEOS1111
subject	GEOS3321
subject	GMAT1110
subject	GMAT1400
subject	MATH1081
subject	MATS1101
subject	MINE1010
subject	MINE1300
subject	MMAN1130
subject	MMAN1300
subject	PHYS1231
subject	PSYC1001
subject	PTRL1010
subject	SOLA1070
\.


-- Q10 --

create or replace function check_q10a() returns text
as $chk$
select ass1_check('function','q10','q10a_expected',
                   $$select * from q10('COMP9321')$$)
$chk$ language sql;

drop table if exists q10a_expected;
create table q10a_expected (
    q10 text
);

COPY q10a_expected (q10) FROM stdin;
COMP9322
\.

create or replace function check_q10b() returns text
as $chk$
select ass1_check('function','q10','q10b_expected',
                   $$select * from q10('COMP3311')$$)
$chk$ language sql;

drop table if exists q10b_expected;
create table q10b_expected (
    q10 text
);

COPY q10b_expected (q10) FROM stdin;
COMP4314
COMP9315
COMP9318
COMP9321
\.

create or replace function check_q10c() returns text
as $chk$
select ass1_check('function','q10','q10c_expected',
                   $$select * from q10('MMAN2600')$$)
$chk$ language sql;

drop table if exists q10c_expected;
create table q10c_expected (
    q10 text
);

COPY q10c_expected (q10) FROM stdin;
AERO3630
MECH3204
MECH3540
MECH3601
MECH3602
MECH3610
MECH9620
MECH9720
MECH9751
MMAN3210
NAVL3610
\.

