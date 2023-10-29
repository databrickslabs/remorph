-- see https://docs.snowflake.com/en/sql-reference/sql/select

SELECT
  employee_table.* EXCLUDE department_id,
  department_table.* RENAME department_name AS department
FROM employee_table INNER JOIN department_table
  ON employee_table.department_id = department_table.department_id
ORDER BY department, last_name, first_name;