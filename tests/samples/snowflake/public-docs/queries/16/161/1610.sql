-- see https://docs.snowflake.com/en/sql-reference/functions/dayname

SELECT d, DAYNAME(d) 
    FROM dates
    ORDER BY d;