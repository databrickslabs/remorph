-- see https://docs.snowflake.com/en/sql-reference/functions/avg

SELECT int_col, AVG(d), AVG(s1) 
    FROM avg_example 
    GROUP BY int_col
    ORDER BY int_col;