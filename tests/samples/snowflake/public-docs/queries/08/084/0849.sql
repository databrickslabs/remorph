-- see https://docs.snowflake.com/en/sql-reference/functions/ilike_any

SELECT * 
  FROM ilike_example 
  WHERE subject ILIKE ANY ('jane%', '%SMITH')
  ORDER BY subject;