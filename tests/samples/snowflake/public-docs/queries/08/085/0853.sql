-- see https://docs.snowflake.com/en/sql-reference/functions/like_any

SELECT * 
  FROM like_example 
  WHERE subject LIKE ANY ('%J%h%^_do%', 'T%^%e') ESCAPE '^'
  ORDER BY subject;