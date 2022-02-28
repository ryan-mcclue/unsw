-- weak entities will have two primary keys, one of which will be of the strong entity 
-- depending on the cardinality the relationship may not require its own table, e.g. 1-to-many
--
-- TEXTBOOK ANSWER: data modelling ensures that you record all information required and none that is extraneous or duplicated based on customer feedback, market research, etc.
-- TEXTBOOK ANSWER: different modelling diagrams for a visual and machine based medium 

create table Driver (
  employee_id int primary key,
  name varchar(30) not null,
  birthday date not null
);
