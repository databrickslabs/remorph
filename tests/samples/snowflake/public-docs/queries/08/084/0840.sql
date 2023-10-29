-- see https://docs.snowflake.com/en/sql-reference/functions/is-null

SELECT * 
    FROM i 
    WHERE col2 IS NULL
    ORDER BY id;