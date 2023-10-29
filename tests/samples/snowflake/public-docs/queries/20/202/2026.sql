-- see https://docs.snowflake.com/en/sql-reference/constructs/where

create table departments (
    department_ID INTEGER,
    department_name VARCHAR,
    location VARCHAR
    );
insert into departments (department_id, department_name, location) values
    (10, 'CUSTOMER SUPPORT', 'CHICAGO'),
    (40, 'RESEARCH', 'BOSTON'),
    (80, 'Department with no employees yet', 'CHICAGO'),
    (90, 'Department with no projects or employees yet', 'EREHWON')
    ;

create table projects (
    project_id integer,
    project_name varchar,
    department_id integer
    );
insert into projects (project_id, project_name, department_id) values
    (4000, 'Detect fake product reviews', 40),
    (4001, 'Detect false insurance claims', 10),
    (9000, 'Project with no employees yet', 80),
    (9099, 'Project with no department or employees yet', NULL)
    ;

create table employees (
    employee_ID INTEGER,
    employee_name VARCHAR,
    department_id INTEGER,
    project_id INTEGER
    );
insert into employees (employee_id, employee_name, department_id, project_id)
  values
    (1012, 'May Aidez', 10, NULL),
    (1040, 'Devi Nobel', 40, 4000),
    (1041, 'Alfred Mendeleev', 40, 4001)
    ;