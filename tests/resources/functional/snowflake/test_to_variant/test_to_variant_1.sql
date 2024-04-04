
-- snowflake sql:
SELECT to_variant(col1) AS json_col1 FROM dummy;

-- databricks sql:
SELECT TO_JSON(col1) AS json_col1 FROM dummy;
