-- see https://docs.snowflake.com/en/sql-reference/functions/sha2_binary

SELECT v, v_as_sha2_binary
  FROM sha_table
  ORDER BY v;