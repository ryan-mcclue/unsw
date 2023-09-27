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

