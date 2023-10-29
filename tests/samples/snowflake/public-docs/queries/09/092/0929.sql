-- see https://docs.snowflake.com/en/sql-reference/sql/select

SELECT * RENAME (department_id AS department, employee_id AS id) FROM employee_table;