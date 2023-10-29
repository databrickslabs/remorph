-- see https://docs.snowflake.com/en/sql-reference/functions/like

SELECT subject
    FROM like_ex
    WHERE subject LIKE '%J%h%^_do%' ESCAPE '^'
    ORDER BY subject;