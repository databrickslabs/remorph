-- snowflake sql:
SELECT
  '12345'::VARCHAR(10) AS varchar_val,
  '12345'::STRING AS string_val,
  '12345'::TEXT AS text_val,
  'A'::CHAR(1) AS char_val,
  'A'::CHARACTER(1) AS character_val

-- databricks sql:
SELECT
  CAST('12345' AS STRING) AS varchar_val,
  CAST('12345' AS STRING) AS string_val,
  CAST('12345' AS STRING) AS text_val,
  CAST('A' AS STRING) AS char_val,
  CAST('A' AS STRING) AS character_val;
