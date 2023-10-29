-- see https://docs.snowflake.com/en/sql-reference/sql/select

SELECT * REPLACE ('DEPT-' || department_id AS department_id) FROM employee_table;