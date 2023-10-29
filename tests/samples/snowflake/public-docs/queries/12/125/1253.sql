-- see https://docs.snowflake.com/en/sql-reference/functions/min_by

SELECT MIN_BY(employee_id, salary, 3), MAX_BY(employee_id, salary, 3) from employees;
