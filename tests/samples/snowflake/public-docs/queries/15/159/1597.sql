-- see https://docs.snowflake.com/en/sql-reference/functions/abs

SELECT column1, abs(column1)
    FROM (values (0), (1), (-2), (3.5), (-4.5), (null));