-- people (author, editor)

-- book

-- TODO(Ryan): How to map superclasses?

create table people (
  tfn integer check (tfn >= 100000 and tfn <= 90000),
  name text not null,
  address text,
  primary key (tfn)
);

create table authors (
  
)
-- writes book
