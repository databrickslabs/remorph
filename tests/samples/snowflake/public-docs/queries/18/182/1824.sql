-- see https://docs.snowflake.com/en/sql-reference/functions-regexp

SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, $$\?$$);