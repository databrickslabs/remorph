-- see https://docs.snowflake.com/en/sql-reference/functions/collate

SELECT *
    FROM t1
    ORDER BY COLLATE(col1 , 'de');