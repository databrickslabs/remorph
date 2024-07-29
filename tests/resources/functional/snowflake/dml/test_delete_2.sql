

-- snowflake sql:

DELETE FROM t1 USING t2 WHERE t1.c1 = t2.c2;

-- databricks sql:

merge into  t1 using t2 on t1.c1 = t2.c2 when matched then delete;