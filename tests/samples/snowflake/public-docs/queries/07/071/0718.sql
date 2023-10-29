-- see https://docs.snowflake.com/en/sql-reference/functions/to_time

SELECT
       description,
       value,
       TO_TIMESTAMP(value),
       TO_TIME(value)
    FROM demo1_time
    ORDER BY value
    ;