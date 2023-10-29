-- see https://docs.snowflake.com/en/sql-reference/functions/like

SELECT * FROM like_ex WHERE subject LIKE '100\\%' ESCAPE '\\'
    ORDER BY 1;