-- see https://docs.snowflake.com/en/sql-reference/sql/select

SELECT * EXCLUDE (department_id, employee_id) FROM employee_table;