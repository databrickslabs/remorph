-- see https://docs.snowflake.com/en/sql-reference/constructs/qualify

SELECT i, p, o
    FROM qt
    QUALIFY ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) = 1
    ;