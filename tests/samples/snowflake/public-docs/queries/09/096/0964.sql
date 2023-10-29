-- see https://docs.snowflake.com/en/sql-reference/functions/array_agg

SELECT ARRAY_AGG(O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY ASC)
  FROM orders 
  WHERE O_TOTALPRICE > 450000;