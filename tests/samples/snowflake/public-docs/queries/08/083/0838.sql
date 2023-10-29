-- see https://docs.snowflake.com/en/sql-reference/functions/is-null

SELECT * 
    FROM i 
    WHERE col1 IS NOT NULL
    ORDER BY id;