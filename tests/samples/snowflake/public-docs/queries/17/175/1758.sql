-- see https://docs.snowflake.com/en/sql-reference/functions/like

SELECT subject
    FROM like_ex
    WHERE subject NOT LIKE 'John%'
    ORDER BY subject;