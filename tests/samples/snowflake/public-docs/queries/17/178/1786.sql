-- see https://docs.snowflake.com/en/sql-reference/functions/regexp

SELECT v
    FROM strings
    WHERE v REGEXP 'San* [fF].*'
    ORDER BY v;