-- see https://docs.snowflake.com/en/sql-reference/constructs/qualify

SELECT c2, SUM(c3) OVER (PARTITION BY c2) as r
  FROM t1
  WHERE c3 < 4
  GROUP BY c2, c3
  HAVING SUM(c1) > 3
  QUALIFY r IN (
    SELECT MIN(c1)
      FROM test
      GROUP BY c2
      HAVING MIN(c1) > 3);