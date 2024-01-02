create domain u32 as integer default 0 check (value >= 0);
create domain u64 as bigint check (value >= 0); 
create domain s32 as integer;
create domain s64 as bigint;
create domain f32 as real;
create domain f64 as double precision;

-- check (length(value) >= 3)

-- any attribute can be NULL, which indicates absence of a value
-- check only applies for values if present, so can still be NULL
-- if don't provide value on insertion, might default to NULL

create type Other as enum (asdasd, 'str1', 'str2'); -- text for string

-- IMPORTANT: use plural for table names
CREATE OR REPLACE FUNCTION drop_table_if_empty(table_name text)
RETURNS void AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = table_name) THEN
        EXECUTE 'DELETE FROM ' || table_name;  -- Delete all data in the table
        EXECUTE 'DROP TABLE ' || table_name;
    END IF;
END $$ LANGUAGE plpgsql;
SELECT drop_table_if_empty('your_table_name');

-- can only drop if no other table references it? 
-- so delete better there?


drop table if exists Movies;
create table Movies (
	id          integer, -- keywords are cases insensitive
	title       varchar(256),  -- ''
	year        integer check (year >= 1900),
	primary key (id)
);

-- sqlfluff parse --dialect postgres file.sql
-- test $? -eq 1 && error
-- use single quotes

-- check (code ~ '^[A-Z]{4}[0-9]{4}$')
create table BelongsTo (
	movie       integer references Movies(id),
	genre       varchar(32),
	primary key (movie,genre)
);

create table Actors (
	id          integer,
	familyName  varchar(64),
	givenNames  varchar(64),
	gender      char(1),
	primary key (id)
);

create table AppearsIn (
	actor       integer references Actors(id),
	movie       integer references Movies(id),
	role        varchar(64),
	primary key (movie,actor,role)
);

create table Directors (
	id          integer,
	familyName  varchar(64),
	givenNames  varchar(64),
	primary key (id)
);

create table Directs (
	director    integer references Directors(id),
	movie       integer references Movies(id),
	primary key (director,movie)
);
