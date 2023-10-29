-- see https://docs.snowflake.com/en/sql-reference/constructs/sample

SELECT i, j
    FROM
         table1 AS t1 SAMPLE (25)     -- 25% of rows in table1
             INNER JOIN
         table2 AS t2 SAMPLE (50)     -- 50% of rows in table2
    WHERE t2.j = t1.i
    ;