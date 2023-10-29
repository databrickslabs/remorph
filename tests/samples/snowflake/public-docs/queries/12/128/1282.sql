-- see https://docs.snowflake.com/en/sql-reference/functions/array_agg

SELECT O_ORDERKEY AS order_keys
  FROM orders
  WHERE O_TOTALPRICE > 450000
  ORDER BY O_ORDERKEY;