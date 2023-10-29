-- see https://docs.snowflake.com/en/sql-reference/functions/bitshiftright

SELECT bit1, bit2, BITSHIFTLEFT(bit1, 1), BITSHIFTRIGHT(bit2, 1)
  FROM bits
  ORDER BY bit1;