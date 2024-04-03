
-- source:
SELECT ARRAY_TO_STRING(ary_column1, '') AS no_separation FROM tbl;

-- databricks_sql:
SELECT ARRAY_JOIN(ary_column1, '') AS no_separation FROM tbl;
