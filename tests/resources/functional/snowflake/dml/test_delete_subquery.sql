-- snowflake sql:
DELETE FROM table1 AS t1 USING (SELECT c2 FROM table2 WHERE t2.c3 = 'foo') AS t2 WHERE t1.c1 = t2.c2;

-- databricks sql:
MERGE INTO  table1 AS t1 USING (
  SELECT
    c2
  FROM table2
  WHERE
    t2.c3 = 'foo'
) AS t2
ON
  t1.c1 = t2.c2 WHEN MATCHED THEN DELETE;
