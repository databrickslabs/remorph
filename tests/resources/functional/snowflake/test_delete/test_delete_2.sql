

-- snowflake sql:

DELETE FROM t1 USING t2 WHERE t1.c1 = t2.c2;

-- databricks sql:

DELETE FROM t1 WHERE EXISTS (SELECT c2 FROM t2 WHERE t1.c1 = c2);