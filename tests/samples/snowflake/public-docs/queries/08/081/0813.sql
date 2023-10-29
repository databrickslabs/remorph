-- see https://docs.snowflake.com/en/sql-reference/data-type-conversion

SELECT (height * width)::VARCHAR || " square meters"
    FROM dimensions;