-- snowflake sql:
SELECT col1, TRY_PARSE_JSON(col2) FROM tabl;

-- databricks sql:
SELECT col1, PARSE_JSON(col2) FROM tabl;



