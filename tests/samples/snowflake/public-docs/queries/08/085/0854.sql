-- see https://docs.snowflake.com/en/sql-reference/functions/like_any

SELECT * 
  FROM like_example 
  WHERE subject LIKE ANY ('%Jo%oe%','T%e')
  ORDER BY subject;