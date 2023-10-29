-- see https://docs.snowflake.com/en/sql-reference/sql/select

INSERT INTO employee_table (employee_ID, last_name, first_name, department_ID) VALUES
    (101, 'Montgomery', 'Pat', 1),
    (102, 'Levine', 'Terry', 2),
    (103, 'Comstock', 'Dana', 2);

INSERT INTO department_table (department_ID, department_name) VALUES
    (1, 'Engineering'),
    (2, 'Customer Support'),
    (3, 'Finance');