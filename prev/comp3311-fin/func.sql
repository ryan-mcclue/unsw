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

