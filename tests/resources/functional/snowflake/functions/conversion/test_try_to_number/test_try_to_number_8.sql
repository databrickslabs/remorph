
-- snowflake sql:
SELECT TRY_TO_DECIMAL('$345') AS str_col,
                                   TRY_TO_DECIMAL(99.56854634) AS num_col,
                                   TRY_TO_DECIMAL(-4.35) AS num_col1,
                                   TRY_TO_DECIMAL(col1) AS col1;

-- databricks sql:
SELECT CAST('$345' AS DECIMAL(38, 0)) AS str_col,
                  CAST(99.56854634 AS DECIMAL(38, 0)) AS num_col,
                  CAST(-4.35 AS DECIMAL(38, 0)) AS num_col1,
                  CAST(col1 AS DECIMAL(38, 0)) AS col1;
