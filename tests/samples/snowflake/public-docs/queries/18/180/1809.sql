-- see https://docs.snowflake.com/en/sql-reference/functions/sha1

SELECT v, v_as_sha1, v_as_sha1_hex
  FROM sha_table
  ORDER BY v;