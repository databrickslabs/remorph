-- see https://docs.snowflake.com/en/sql-reference/sql/select

CREATE TABLE employee_table (
    employee_ID INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    department_ID INTEGER
    );

CREATE TABLE department_table (
    department_ID INTEGER,
    department_name VARCHAR
    );