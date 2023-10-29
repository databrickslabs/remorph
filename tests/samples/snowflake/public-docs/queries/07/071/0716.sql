-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

SELECT
       description,
       value,
       TO_TIMESTAMP(value),
       TO_DATE(value)
    FROM demo1
    ORDER BY value
    ;