-- see https://docs.snowflake.com/en/sql-reference/functions/sha1_binary

SELECT v, v_as_sha1_binary
  FROM sha_table
  ORDER BY v;