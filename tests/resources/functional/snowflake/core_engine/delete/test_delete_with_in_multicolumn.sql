-- snowflake sql:
DELETE FROM test_tbl
WHERE (version, type) IN (
SELECT version1 , type2
FROM test_tbl_stg
);

-- databricks sql:
DELETE FROM test_tbl
WHERE EXISTS(
SELECT 1
FROM test_tbl_stg
WHERE test_tbl.version = test_tbl_stg.version1
AND test_tbl.type = test_tbl_stg.type2
);