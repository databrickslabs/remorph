-- see https://docs.snowflake.com/en/sql-reference/functions/first_value

SELECT
        column1,
        column2,
        FIRST_VALUE(column2) OVER (PARTITION BY column1 ORDER BY column2 NULLS LAST) AS column2_first
    FROM VALUES
       (1, 10), (1, 11), (1, null), (1, 12),
       (2, 20), (2, 21), (2, 22)
    ORDER BY column1, column2;