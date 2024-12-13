-- snowflake sql:
select sha2(test_col), sha2(test_col, 256), sha2(test_col, 224) from test_tbl;

-- databricks sql:
SELECT
  SHA2(test_col, 256),
  SHA2(test_col, 256),
  SHA2(test_col, 224)
FROM test_tbl;
