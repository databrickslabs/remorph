-- see https://docs.snowflake.com/en/sql-reference/functions/ilike

SELECT * 
    FROM ilike_ex 
    WHERE subject ILIKE '%j%h%do%'
    ORDER BY 1;