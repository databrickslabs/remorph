-- see https://docs.snowflake.com/en/sql-reference/functions/array_agg

SELECT 
    O_ORDERSTATUS, 
    ARRAYAGG(O_CLERK) WITHIN GROUP (ORDER BY O_TOTALPRICE DESC)
  FROM orders 
  WHERE O_TOTALPRICE > 450000
  GROUP BY O_ORDERSTATUS
  ORDER BY O_ORDERSTATUS DESC;