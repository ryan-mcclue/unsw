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
3179190	Akinola Goldberger
3286128	Karen Lau
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
3341420	Betty Liu Chong
3261810	Jared Thomas
3225933	Jinglan Ren Chaofeng
3128590	Lisa Tung
3119230	Catherine Matousek
3049611	Xianfeng Ma Xue Mei
3038152	Glen Paull
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
3075778	Gabrielle Hadassin
3233721	Adrian Fong
3246503	Jialu Wang
3256340	Anastasi Spichopoulos
3273463	Rodney Haran
3297644	Natalia Varas
3309508	Brooke Horlyck
3349456	Shaoquett Almir
3350435	Stuart Trudgeon
3388096	Leopold Seeto
9175698	Chia- Liu
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
2019 T1	0.0482
\.

-- Q6 --

create or replace function check_q6a() returns text
as $chk$
select ass1_check('function','q6','q6a_expected',
                   $$select q6(1174803,'COMP9318')$$)
$chk$ language sql;

drop table if exists q6a_expected;
create table q6a_expected (
    q6 integer
);

COPY q6a_expected (q6) FROM stdin;
73
\.

create or replace function check_q6b() returns text
as $chk$
select ass1_check('function','q6','q6b_expected',
                   $$select q6(1183756,'COMM8000')$$)
$chk$ language sql;

drop table if exists q6b_expected;
create table q6b_expected (
    q6 integer
);

COPY q6b_expected (q6) FROM stdin;
88
\.

create or replace function check_q6c() returns text
as $chk$
select ass1_check('function','q6','q6c_expected',
                   $$select q6(1194619,'AVIA5039')$$)
$chk$ language sql;

drop table if exists q6c_expected;
create table q6c_expected (
    q6 integer
);

COPY q6c_expected (q6) FROM stdin;
56
\.


-- Q7 --

create or replace function check_q7a() returns text
as $chk$
select ass1_check('function','q7','q7a_expected',
                   $$select * from q7(2015,'S2')$$)
$chk$ language sql;

drop table if exists q7a_expected;
create table q7a_expected (
    code text
);

COPY q7a_expected (code) FROM stdin;
COMP9024
COMP9331
COMP4418
COMP9415
COMP9441
COMP9336
COMP9335
COMP9020
COMP9021
COMP9511
COMP9041
COMP4121
COMP9222
COMP9161
COMP9431
COMP9945
COMP9032
\.

create or replace function check_q7b() returns text
as $chk$
select ass1_check('function','q7','q7b_expected',
                   $$select * from q7(2017,'S1')$$)
$chk$ language sql;

drop table if exists q7b_expected;
create table q7b_expected (
    code text
);

COPY q7b_expected (code) FROM stdin;
COMP9021
COMP9020
COMP9945
COMP9319
COMP9414
COMP4141
COMP9102
COMP9024
COMP9153
COMP9201
COMP9331
COMP9101
COMP9243
COMP9801
COMP9814
COMP9211
\.

create or replace function check_q7c() returns text
as $chk$
select ass1_check('function','q7','q7c_expected',
                   $$select * from q7(2019,'T1')$$)
$chk$ language sql;

drop table if exists q7c_expected;
create table q7c_expected (
    code text
);

COPY q7c_expected (code) FROM stdin;
COMP9331
COMP9414
COMP9021
COMP9024
COMP9102
COMP9020
COMP9101
COMP4141
COMP9201
COMP9945
COMP9153
COMP9283
\.


-- Q8 --

create or replace function check_q8a() returns text
as $chk$
select ass1_check('function','q8','q8a_expected',
                   $$select * from q8(3077101)$$)
$chk$ language sql;

drop table if exists q8a_expected;
create table q8a_expected (
    term char(4),
    termwam integer,
    termuocpassed integer
);

COPY q8a_expected (term, termwam, termuocpassed) FROM stdin;
15s1	73	24
15s2	73	24
16s1	73	24
16s2	78	24
17s1	85	18
17s2	81	24
18x1	75	6
18s1	84	24
18s2	80	24
OVAL	78	192
\.

create or replace function check_q8b() returns text
as $chk$
select ass1_check('function','q8','q8b_expected',
                   $$select * from q8(3068493)$$)
$chk$ language sql;

drop table if exists q8b_expected;
create table q8b_expected (
    term char(4),
    termwam integer,
    termuocpassed integer
);

COPY q8b_expected (term, termwam, termuocpassed) FROM stdin;
15s1	52	12
15s2	37	\N
16s1	54	18
16s2	59	12
17x1	\N	\N
17s1	36	6
17s2	33	6
18x1	37	\N
18s1	53	12
18s2	56	18
19T1	65	12
19T2	64	6
OVAL	48	102
\.

create or replace function check_q8c() returns text
as $chk$
select ass1_check('function','q8','q8c_expected',
                   $$select * from q8(3302593)$$)
$chk$ language sql;

drop table if exists q8c_expected;
create table q8c_expected (
    term char(4),
    termwam integer,
    termuocpassed integer
);

COPY q8c_expected (term, termwam, termuocpassed) FROM stdin;
17s1	58	12
17s2	39	\N
18x1	42	\N
OVAL	49	12
\.


-- Q9 --

create or replace function check_q9a() returns text
as $chk$
select ass1_check('function','q9','q9a_expected',
                   $$select * from q9(1155)$$)
$chk$ language sql;

drop table if exists q9a_expected;
create table q9a_expected (
    objtype text,
    objcode text
);

COPY q9a_expected (objtype, objcode) FROM stdin;
subject	CEIC8351
subject	FOOD1210
subject	CEIC8102
subject	CEIC6005
subject	FOOD4450
subject	FOOD1390
subject	POLY3000
subject	CEIC6031
subject	CEIC8330
subject	INDC3002
subject	CEIC8204
subject	CEIC3005
subject	CEIC8341
subject	CEIC4006
\.

create or replace function check_q9b() returns text
as $chk$
select ass1_check('function','q9','q9b_expected',
                   $$select * from q9(1651)$$)
$chk$ language sql;

drop table if exists q9b_expected;
create table q9b_expected (
    objtype text,
    objcode text
);

COPY q9b_expected (objtype, objcode) FROM stdin;
stream	ENVSB1
stream	ENVSC1
stream	ENVSA1
stream	ENVSR1
stream	ENVSE1
stream	ENVSF1
stream	ENVSG1
\.

create or replace function check_q9c() returns text
as $chk$
select ass1_check('function','q9','q9c_expected',
                   $$select * from q9(2000)$$)
$chk$ language sql;

drop table if exists q9c_expected;
create table q9c_expected (
    objtype text,
    objcode text
);

COPY q9c_expected (objtype, objcode) FROM stdin;
subject	ZINT1001
subject	ZEIT1500
subject	ZPEM1501
subject	ZPEM1303
subject	ZPEM1304
subject	ZEIT1502
subject	ZEIT1501
subject	ZPEM1502
\.


-- Q10 --

create or replace function check_q10a() returns text
as $chk$
select ass1_check('function','q10','q10a_expected',
                   $$select * from q10('COMP9332')$$)
$chk$ language sql;

drop table if exists q10a_expected;
create table q10a_expected (
    q10 text
);

COPY q10a_expected (q10) FROM stdin;
SENG9338
\.

create or replace function check_q10b() returns text
as $chk$
select ass1_check('function','q10','q10b_expected',
                   $$select * from q10('COMP3331')$$)
$chk$ language sql;

drop table if exists q10b_expected;
create table q10b_expected (
    q10 text
);

COPY q10b_expected (q10) FROM stdin;
COMP9333
COMP4336
COMP4337
COMP4335
COMP9447
COMP9332
COMP9243
COMP6733
\.

create or replace function check_q10c() returns text
as $chk$
select ass1_check('function','q10','q10c_expected',
                   $$select * from q10('MMAN3400')$$)
$chk$ language sql;

drop table if exists q10c_expected;
create table q10c_expected (
    q10 text
);

COPY q10c_expected (q10) FROM stdin;
MECH9410
NAVL3410
MECH4900
MECH9400
\.

