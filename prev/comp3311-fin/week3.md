<!-- SPDX-License-Identifier: zlib-acknowledgement -->
northwind sql sample database

`where length(name) = (select max(length(name)) from beers);`

Oftentimes may have to consider a collection of fields to be unique, e.g. name, year etc.

like group by, except only on window functions to not reduce rows
`avg(salary) OVER (PARTITION BY depname)`

the temporary table can be indexed and easier to debug as can see what is there?
they will be deleted when user logs out

but will create logs? seems inspecting logs key part of DBA? e.g. what is being inserted?
can be used for CTEs `with ...`

when doing `update` accidentally updated multiple users passwords instead of 1. how to fix? look at transaction log?
```
SELECT
PersonID
,LicenseType
,LicenseState
,LicenseID
,LicenseDate
,ROW_NUMBER() OVER(PARTITION BY PersonID, LicenseType, LicenseState ORDER BY LicenseDate desc) AS RN
INTO #temp
FROM Licenses

SELECT * FROM #temp WHERE RN = 1
```
data transformations through SSIS instead of views/procedures etc.?

union compatible mean same number and same type of attributes

`select name as "Beer" from beers;`
(double quotes is for an identifier, single quotes for string)

`select count(distinct name) from beers;`

stored procedure doesn't return a value like a function.
it's precompiled; so faster than dynamic query 


a view will create a tuple type of the same name 
When you create a view/function etc. it's not stored exactly how you type it, e.g. might have type casts
Can see with `\ev` or `\ef` etc.

GUCs (global user configuration) can be used as globals
pg_settings is part of catalog, i.e. tables that contain metadata about database
```
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_settings WHERE name = 'my_debug_flag') THEN
    -- Create a custom configuration setting if it doesn't exist
    -- This is a one-time setup.
    INSERT INTO pg_settings(name, setting, unit, category, short_desc)
    VALUES ('my_debug_flag', 'false', '', 'Custom', 'Debug flag for my PL/pgSQL functions');
  END IF;
END $$;
```
For grouping, consider aggregate functions, e.g. `string_agg(beer, '|' order by beer)`

set operations `union/intersect/except`

`where not exists`
`where name in (select names from view where counter = 1)`

For psycopg2 'call-level' interface, generic to each DBMS
For something like C, more lower level and specific to each DBMS 

`distinct` often required if no `group by`
