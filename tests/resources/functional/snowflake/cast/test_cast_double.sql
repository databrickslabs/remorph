-- snowflake sql:
SELECT
  12345.678::DOUBLE AS double_val,
  12345.678::DOUBLE PRECISION AS double_precision_val,
  12345.678::FLOAT AS float_val,
  12345.678::FLOAT4 AS float4_val,
  12345.678::FLOAT8 AS float8_val,
  12345.678::REAL AS real_val

-- databricks sql:
SELECT
  CAST(12345.678 AS DOUBLE) AS double_val,
  CAST(12345.678 AS DOUBLE) AS double_precision_val,
  CAST(12345.678 AS DOUBLE) AS float_val,
  CAST(12345.678 AS DOUBLE) AS float4_val,
  CAST(12345.678 AS DOUBLE) AS float8_val,
  CAST(12345.678 AS DOUBLE) AS real_val;
