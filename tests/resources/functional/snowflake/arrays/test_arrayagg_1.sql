
-- snowflake sql:
select array_agg(col1) FROM test_table;

-- databricks sql:
SELECT ARRAY_AGG(col1) FROM test_table;
