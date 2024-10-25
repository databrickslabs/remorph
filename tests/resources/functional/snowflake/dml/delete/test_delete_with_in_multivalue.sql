-- snowflake sql:
DELETE FROM test_tbl
WHERE version
IN (1 , 2);

-- databricks sql:
DELETE FROM test_tbl
WHERE version
IN (1 , 2);