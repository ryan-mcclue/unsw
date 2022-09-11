-- Q1
CREATE OR REPLACE VIEW Q1(unswid, name)
AS
SELECT p.unswid, p.name
FROM People p
JOIN Program_enrolments pe ON (p.id = pe.student)
GROUP BY p.unswid, p.name
HAVING count(distinct pe.program) > 4;


-- Q2
CREATE OR REPLACE VIEW course_tutor(unswid, course_cnt) AS
SELECT p.unswid, count(distinct cs.course)
FROM people p
JOIN staff s ON p.id = s.id
JOIN course_staff cs ON cs.staff = s.id
JOIN staff_roles sr ON sr.id = cs.role
WHERE sr.name = 'Course Tutor'
GROUP BY p.unswid;

CREATE OR REPLACE VIEW Q2(unswid, name, course_cnt) AS
SELECT ct.unswid, p.name, ct.course_cnt
FROM course_tutor ct
JOIN people p ON p.unswid = ct.unswid
WHERE ct.course_cnt = (SELECT max(course_cnt) AS max_cc FROM course_tutor);


-- Q3
CREATE OR REPLACE VIEW Q3(unswid, name)
AS
SELECT p.unswid, p.name
FROM People p, Students s1, Course_enrolments ce, Courses c, Subjects s2, OrgUnits o
WHERE p.id = s1.id AND s1.id = ce.student AND ce.course = c.id AND s2.offeredBy=o.id
AND c.subject = s2.id AND s1.stype = 'intl' AND ce.mark > 85 AND o.name = 'School of Law'
ORDER BY p.unswid DESC;


-- Q4
CREATE OR REPLACE VIEW Q4_sub(student, semester) 
AS
SELECT ce.student,
       c.term
FROM course_enrolments AS ce,
     courses AS c,
     subjects AS s
WHERE ce.course = c.id
  AND c.subject = s.id
  AND s.code = 'COMP9020' 
INTERSECT
SELECT ce.student,
       c.term
FROM course_enrolments AS ce,
     courses AS c,
     subjects AS s 
WHERE ce.course = c.id
  AND c.subject = s.id
  AND s.code = 'COMP9331';

CREATE OR REPLACE VIEW Q4(unswid, name) 
AS
SELECT DISTINCT p.unswid,
                p.name
FROM people AS p,
     Q4_sub AS q,
     students AS s
WHERE p.id = q.student
  AND q.student = s.id
  AND s.stype = 'local';


-- Q5
CREATE OR REPLACE VIEW get_count(term, year, tot, fail) AS
SELECT t.name, t.year, count(*), count(*) filter (WHERE ce.mark < 50)
FROM course_enrolments ce, courses c, terms t, subjects s
WHERE s.code = 'COMP3311'
    AND s.id = c.subject AND t.id = c.term AND ce.course = c.id
    AND ce.mark IS NOT NULL
    AND t.year >= 2009 AND t.year <= 2019
GROUP BY t.name, t.year;

CREATE OR REPLACE VIEW get_rate_a(term, rate) AS
SELECT t.term, round(t.fail::numeric / t.tot::numeric, 4)
FROM get_count AS t
WHERE t.year >= 2009 AND t.year <= 2012;

CREATE OR REPLACE VIEW Q5a(term, min_fail_rate) AS
SELECT t.term, t.rate
FROM get_rate_a t
WHERE t.rate = (SELECT min(rate) FROM get_rate_a);

CREATE OR REPLACE VIEW get_rate_b(term, rate) AS
SELECT t.term, round(t.fail::numeric / t.tot::numeric, 4)
FROM get_count AS t
WHERE t.year >= 2016 AND t.year <= 2019;

CREATE OR REPLACE VIEW Q5b(term, min_fail_rate) AS
SELECT t.term, t.rate
FROM get_rate_b t
WHERE t.rate = (SELECT min(rate) FROM get_rate_b);


-- Q6
CREATE OR REPLACE FUNCTION Q6(id integer, code text) RETURNS integer
AS
$$
SELECT ce.mark FROM People p, Course_enrolments ce, courses c, subjects s 
WHERE p.id = ce.student
AND c.id = ce.course
AND c.subject = s.id
AND p.id = $1
AND s.code = $2
$$ language sql
;


-- Q7
CREATE OR REPLACE VIEW pg_comp(pgc_year, pgc_session, pgc_code) AS
SELECT t.year, t.session, s.code
FROM Courses c
JOIN Subjects s ON c.subject = s.id
JOIN Terms t ON c.term = t.id
WHERE s.code LIKE 'COMP%'
AND s.career = 'PG';

CREATE OR REPLACE FUNCTION Q7(year integer, session text)
	RETURNS table (code text)
AS $$
SELECT pgc_code::text
FROM   pg_comp
WHERE  pgc_year = year
AND pgc_session = session
$$ language sql
;


-- Q8
CREATE OR REPLACE FUNCTION
	Q8(zid integer) RETURNS SETOF TermTranscriptRecord
AS $$
DECLARE
	r record;
	x integer;
	termmu integer;
	termu integer;
	termwam numeric;
	termuocpassed integer;
	overallmu integer = 0;
	overallu integer = 0;
	overallwam numeric;
	overalluocpassed integer = 0;
BEGIN
	SELECT s.id INTO x
	FROM   Students s 
	INNER JOIN People p ON (s.id = p.id)
	WHERE  p.unswid = zid;
	IF (x IS NULL) THEN
		-- RAISE NOTICE 'Invalid student %', zid;
        RETURN;
	END IF;
	FOR r IN 
		SELECT terms.id AS id, termName(terms.id) AS termname
			FROM people 
			INNER JOIN students ON people.id = students.id
			INNER JOIN course_enrolments ON course_enrolments.student = students.id
			INNER JOIN courses  ON course_enrolments.course = courses.id
			INNER JOIN terms ON courses.term = terms.id
			WHERE people.unswid = zid
			GROUP BY terms.id
			ORDER BY terms.starting ASC
	LOOP
		SELECT SUM(subjects.uoc) INTO termuocpassed
			FROM people 
			INNER JOIN students ON people.id = students.id
			INNER JOIN course_enrolments ON course_enrolments.student = students.id
			INNER JOIN courses  ON course_enrolments.course = courses.id
			INNER JOIN terms ON courses.term = terms.id
			INNER JOIN subjects ON courses.subject = subjects.id
			WHERE people.unswid = zid
			AND terms.id = r.id
			AND course_enrolments.grade IN ('SY', 'PT', 'PC', 'PS', 'CR', 'DN', 'HD', 'A', 'B', 'C', 'XE', 'T', 'PE', 'RC', 'RS');
		IF (termuocpassed IS NOT NULL) THEN
			overalluocpassed = overalluocpassed + termuocpassed;
		END IF;

		SELECT SUM(subjects.uoc), SUM(course_enrolments.mark * subjects.uoc) INTO termu, termmu
			FROM people 
			INNER JOIN students ON people.id = students.id
			INNER JOIN course_enrolments ON course_enrolments.student = students.id
			INNER JOIN courses  ON course_enrolments.course = courses.id
			INNER JOIN terms ON courses.term = terms.id
			INNER JOIN subjects ON courses.subject = subjects.id
			WHERE people.unswid = zid
			AND terms.id = r.id
			AND course_enrolments.mark IS NOT NULL;
		IF (termu = 0 OR termmu = 0 OR termu IS NULL OR termmu IS NULL) THEN
			termwam = null;
		ELSE
			termwam = termmu::numeric / termu::numeric;
			overallmu = overallmu + termmu;
			overallu = overallu + termu;
		END IF;
		RETURN QUERY SELECT r.termname::char(4), termwam::integer, termuocpassed;
	END LOOP;
	IF (overallu = 0 OR overallmu = 0 OR overallu IS NULL OR overallu IS NULL) THEN
		overallwam = null;
	ELSE
		overallwam = overallmu::numeric / overallu::numeric;
	END IF;
	RETURN QUERY SELECT 'OVAL'::char(4), overallwam::integer, overalluocpassed;
	RETURN;
END
$$ language plpgsql;



-- Q9
CREATE OR REPLACE FUNCTION expand(_def text) RETURNS SETOF text
AS $$
DECLARE
	_elem text;
	_patt text;
	_code text;
BEGIN
	FOR _elem IN
        SELECT * FROM regexp_split_to_table(_def,'[,;{}]')
    LOOP
		CONTINUE WHEN (_elem IS NULL OR _elem = '');
		CONTINUE WHEN (_elem ~ '(FREE|GEN|F=)');
		IF (_elem !~ '[#|[]') THEN
			RETURN NEXT _elem;
		ELSE  -- expand a pattern
			_patt = replace(_elem, '#', '.');
			FOR _code IN
				SELECT code FROM Subjects WHERE code ~ _patt
			LOOP
				RETURN NEXT _code;
			END LOOP;
		END IF;
	END LOOP;
END;
$$ language plpgsql;

-- RETURN all members of an enumerated AcObjGroup (incl child groups)

CREATE OR REPLACE FUNCTION
	all_members(grp Acad_object_groups) RETURNS SETOF AcObjRecord
AS $$
DECLARE
	rec AcObjRecord;
	code text;
	memTab text; objTab text; query text;
BEGIN
	objTab := grp.gtype||'s';
	memTab := grp.gtype||'_group_members';
	query  := 'SELECT o.code FROM '||quote_ident(memTab)||' m JOIN '||
	          quote_ident(objTab)||' o ON (m.'||quote_ident(grp.gtype)||
	          ' = o.id) WHERE ao_group = '||quote_literal(grp.id);

	FOR code IN execute query LOOP
		rec.objtype = grp.gtype; rec.objcode = code;
		RETURN NEXT rec;
	END LOOP;
	query = 'SELECT o.code FROM acad_object_groups a JOIN '||
                quote_ident(memTab)||' m ON (m.ao_group = a.id) JOIN '||
                quote_ident(objTab)||' o ON (m.'||quote_ident(grp.gtype)||
	        ' = o.id) WHERE  a.parent = '||quote_literal(grp.id);

	FOR code IN execute query LOOP
		rec.objtype = grp.gtype; rec.objcode = code;
		RETURN NEXT rec;
	END LOOP;
END;
$$ language plpgsql;

-- generate a list of AcObjRecords, possibly containing duplicates

CREATE OR REPLACE FUNCTION q9worker(gid integer) RETURNS SETOF AcObjRecord
AS $$
DECLARE
	grp acad_object_groups;
	rec AcObjRecord;
	code text;
	memTab text; objTab text; query text;
BEGIN
	SELECT * into grp
	FROM   acad_object_groups
	WHERE  id = gid;
	IF (not found) THEN
		raise 'No such group: %',gid;
	END IF;

	IF (grp.gdefby = 'enumerated') THEN
		FOR rec IN SELECT * FROM all_members(grp)
		LOOP
			RETURN NEXT rec;
		END LOOP;
	elsif (grp.gdefby = 'pattern') THEN
		IF (grp.definition IS NULL) THEN
			RETURN;
		END IF;
		FOR code IN SELECT * FROM expand(grp.definition)
		LOOP
			rec.objtype := grp.gtype; rec.objcode := code;
			RETURN NEXT rec;
		END LOOP;
	END IF;
END;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION q9(gid integer) RETURNS SETOF AcObjRecord
AS $$
DECLARE
	rec AcObjRecord;
BEGIN
	FOR rec IN SELECT distinct * FROM q9worker(gid)
	LOOP
		RETURN NEXT rec;
	END LOOP;
END;
$$ language plpgsql;

--------------------------------------------------------------
-- Q10
CREATE OR REPLACE FUNCTION
	q10worker(_code text) RETURNS SETOF text
AS $$
DECLARE
	rr record;
	gg acad_object_groups;
	nmatches integer;
BEGIN
	FOR rr IN
		SELECT distinct s.code::text, r.ao_group
		FROM   subject_prereqs p
		       JOIN rules r ON (r.id = p.rule)
		       JOIN subjects s ON (s.id = p.subject)
		WHERE  r.ao_group IS NOT NULL
	LOOP
		FOR gg IN
			SELECT *
			FROM   acad_object_groups
			WHERE  id = rr.ao_group AND gtype = 'subject'
			       and (gdefby = 'pattern')
			       and (definition LIKE '%'||_code||'%')
		LOOP
			RETURN NEXT rr.code;
		END LOOP;
		-- enumerated is omitted as it does not exist in this case
	END LOOP;
END;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION
	q10(code text) RETURNS SETOF text
AS $$
DECLARE
	r record;
BEGIN
	FOR r IN
		SELECT distinct q10worker AS _code FROM q10worker(code)
	LOOP
		RETURN NEXT r._code;
	END LOOP;
END;
$$ language plpgsql;
