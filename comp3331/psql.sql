create table Employee (
  ssn, birthdate, name, 
  working_department references Department(name),
);

create table Department (
  name, phone, location, mdate, 
  manager references Employee(ssn),
);

create table Project (
  pnum, title
);

create table Participation (
  employee, project, time 
);

create table Dependents (
  family references Employee(ssn) not null,
  name, relation, birthdate
  primary key (family, name)
);
