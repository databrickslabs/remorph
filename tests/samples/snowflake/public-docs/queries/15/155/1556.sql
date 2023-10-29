-- see https://docs.snowflake.com/en/sql-reference/functions/bitand

SELECT bit1, bit2, BITAND(bit1, bit2), BITOR(bit1, bit2), BITXOR(bit1, BIT2)
  FROM bits
  ORDER BY bit1;