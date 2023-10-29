-- see https://docs.snowflake.com/en/sql-reference/functions/last_value

SELECT
    column1,
    column2,
    LAST_VALUE(column2) OVER (PARTITION BY column1 ORDER BY column2) AS column2_last
FROM VALUES
    (1, 10), (1, 11), (1, 12),
    (2, 20), (2, 21), (2, 22);
