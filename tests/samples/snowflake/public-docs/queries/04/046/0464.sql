-- see https://docs.snowflake.com/en/sql-reference/constructs/join-lateral

CREATE TABLE departments (department_id INTEGER, name VARCHAR);
CREATE TABLE employees (employee_ID INTEGER, last_name VARCHAR, 
                        department_ID INTEGER, project_names ARRAY);