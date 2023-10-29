-- see https://docs.snowflake.com/en/sql-reference/constructs/where

SELECT t1.col1, t2.col1
    FROM t1 JOIN t2
        ON t2.col1 = t1.col1
    ORDER BY 1, 2;