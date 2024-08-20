
-- snowflake sql:
SELECT to_timestamp(col1) AS to_timestamp_col1 FROM tabl;

-- databricks sql:
SELECT CAST(col1 AS TIMESTAMP) AS to_timestamp_col1 FROM tabl;
