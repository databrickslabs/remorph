-- see https://docs.snowflake.com/en/sql-reference/constructs/having

SELECT department_id
FROM employees
GROUP BY department_id
HAVING count(*) < 10;