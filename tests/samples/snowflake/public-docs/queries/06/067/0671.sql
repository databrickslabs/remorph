-- see https://docs.snowflake.com/en/sql-reference/sql/insert

INSERT INTO employees (first_name,last_name,workphone,city,postal_code)
  WITH cte AS
    (SELECT contractor_first AS first_name,contractor_last AS last_name,worknum AS workphone,city,zip_code AS postal_code
     FROM contractors)
  SELECT first_name,last_name,workphone,city,postal_code
  FROM cte;