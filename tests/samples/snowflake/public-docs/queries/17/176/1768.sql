-- see https://docs.snowflake.com/en/sql-reference/constructs/where

SELECT t1.c1, t2.c2
FROM t1 LEFT OUTER JOIN t2
        ON t1.c1 = t2.c2;

SELECT t1.c1, t2.c2
FROM t1, t2
WHERE t1.c1 = t2.c2(+);