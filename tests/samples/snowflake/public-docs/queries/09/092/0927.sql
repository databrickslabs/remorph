-- see https://docs.snowflake.com/en/sql-reference/sql/select

SELECT * ILIKE '%id%' RENAME department_id AS department FROM employee_table;