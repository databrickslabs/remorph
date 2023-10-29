-- see https://docs.snowflake.com/en/sql-reference/functions/lead

CREATE OR REPLACE TABLE t1 (c1 NUMBER, c2 NUMBER);
INSERT INTO t1 VALUES (1,5),(2,4),(3,NULL),(4,2),(5,NULL),(6,NULL),(7,6);

SELECT c1, c2, LEAD(c2) IGNORE NULLS OVER (ORDER BY c1) FROM t1;
