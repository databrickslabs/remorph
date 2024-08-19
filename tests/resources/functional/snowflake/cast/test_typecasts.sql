-- snowflake sql:
SELECT
    PARSE_JSON('[1,2,3]')::ARRAY AS array_val,
    'deadbeef'::BINARY AS binary_val,
    'true'::BOOLEAN AS boolean_val,
    'deadbeef'::VARBINARY AS varbinary_val

-- databricks sql:
SELECT
  FROM_JSON('[1,2,3]', 'ARRAY') AS array_val,
  CAST('deadbeef' AS BINARY) AS binary_val,
  CAST('true' AS BOOLEAN) AS boolean_val,
  CAST('deadbeef' AS BINARY) AS varbinary_val
