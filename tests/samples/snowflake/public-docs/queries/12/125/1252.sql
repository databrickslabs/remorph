-- see https://docs.snowflake.com/en/sql-reference/functions/min_by

SELECT MIN_BY(employee_id, salary), MAX_BY(employee_id, salary) from employees;
