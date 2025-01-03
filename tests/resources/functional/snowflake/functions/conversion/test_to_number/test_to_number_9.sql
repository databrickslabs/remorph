
-- snowflake sql:
select TO_NUMBER(EXPR) from test_tbl;

-- databricks sql:
SELECT CAST(EXPR AS DECIMAL(38, 0)) FROM test_tbl;
