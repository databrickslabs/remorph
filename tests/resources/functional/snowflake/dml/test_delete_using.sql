-- snowflake sql:

DELETE FROM t1 USING t2 WHERE t1.c1 = t2.c2;

-- databricks sql:
MERGE INTO  t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN DELETE;
