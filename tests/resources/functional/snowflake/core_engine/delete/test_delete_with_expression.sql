-- snowflake sql:
DELETE FROM test_tbl
WHERE (COALESCE(c1,c2,c3),type) IN (
select lower(version), type from test_tbl2);

-- databricks sql:
DELETE FROM
  test_tbl
WHERE
  EXISTS (
    SELECT
      1
    FROM
      test_tbl2
    WHERE
      COALESCE (test_tbl.c1, test_tbl.c2, test_tbl.c3) = lower (test_tbl2.version)
      AND test_tbl.type = test_tbl2.type
  );