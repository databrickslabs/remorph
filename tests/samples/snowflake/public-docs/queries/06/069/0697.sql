-- see https://docs.snowflake.com/en/sql-reference/sql/insert

INSERT OVERWRITE INTO sf_employees
  SELECT * FROM employees
  WHERE city = 'San Francisco';