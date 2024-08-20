-- snowflake sql:
SELECT STRIP_NULL_VALUE(src:c) FROM mytable;

-- databricks sql:
SELECT STRIP_NULL_VALUE(src.c) FROM mytable;
