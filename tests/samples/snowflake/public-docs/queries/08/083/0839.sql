-- see https://docs.snowflake.com/en/sql-reference/functions/is-null

SELECT * 
    FROM i 
    WHERE col1 IS NOT NULL OR col2 IS NULL
    ORDER BY id;