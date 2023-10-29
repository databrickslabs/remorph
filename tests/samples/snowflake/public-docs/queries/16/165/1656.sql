-- see https://docs.snowflake.com/en/sql-reference/functions/min

SELECT k, d
    FROM minmax_example
    ORDER BY k, d;