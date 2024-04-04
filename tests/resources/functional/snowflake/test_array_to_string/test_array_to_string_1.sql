
-- snowflake sql:
SELECT ARRAY_TO_STRING(ary_column1, '') AS no_separation FROM tbl;

-- databricks sql:
SELECT ARRAY_JOIN(ary_column1, '') AS no_separation FROM tbl;
