-- see https://docs.snowflake.com/en/sql-reference/sql/select

SELECT * EXCLUDE first_name RENAME (department_id AS department, employee_id AS id) FROM employee_table;