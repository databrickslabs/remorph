-- see https://docs.snowflake.com/en/sql-reference/functions/sha2

SELECT v, v_as_sha2, v_as_sha2_hex
  FROM sha_table
  ORDER BY v;