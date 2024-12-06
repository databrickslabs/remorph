-- snowflake sql:
SELECT
    12345::DECIMAL(10, 2) AS decimal_val,
    12345::NUMBER(10, 2) AS number_val,
    12345::NUMERIC(10, 2) AS numeric_val,
    12345::BIGINT AS bigint_val

-- databricks sql:
SELECT
  CAST(12345 AS DECIMAL(10, 2)) AS decimal_val,
  CAST(12345 AS DECIMAL(10, 2)) AS number_val,
  CAST(12345 AS DECIMAL(10, 2)) AS numeric_val,
  CAST(12345 AS DECIMAL(38, 0)) AS bigint_val;
