
-- source:
SELECT col1, TRY_PARSE_JSON(col2) FROM tabl;

-- databricks_sql:
SELECT col1, FROM_JSON(col2, {COL2_SCHEMA}) FROM tabl;
