-- snowflake sql:
DELETE FROM test_tbl
WHERE (version, type) NOT IN (
SELECT version1 , type2
FROM test_tbl_stg inner join test_tbl_stg_2 on test_tbl_stg_2.version3 = test_tbl_stg.version1
);

-- databricks sql:
DELETE FROM test_tbl
WHERE NOT EXISTS(
SELECT 1
FROM test_tbl_stg inner join test_tbl_stg_2 on test_tbl_stg_2.version3 = test_tbl_stg.version1
WHERE test_tbl.version = test_tbl_stg.version1
AND test_tbl.type = test_tbl_stg_2.type2
);