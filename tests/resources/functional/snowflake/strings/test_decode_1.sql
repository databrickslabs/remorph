
-- snowflake sql:
SELECT decode(column1, 1, 'one', 2, 'two', NULL, '-NULL-', 'other') AS decode_result;

-- databricks sql:
SELECT CASE WHEN column1 = 1 THEN 'one' WHEN column1 = 2 THEN 'two' WHEN column1 IS NULL THEN '-NULL-' ELSE 'other' END AS decode_result;
