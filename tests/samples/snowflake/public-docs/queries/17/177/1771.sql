-- see https://docs.snowflake.com/en/sql-reference/constructs/join

SELECT t1.col1, t2.col1
    FROM t1 CROSS JOIN t2
    WHERE t2.col1 = t1.col1
    ORDER BY 1, 2;