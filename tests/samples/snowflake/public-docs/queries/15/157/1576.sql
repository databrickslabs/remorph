-- see https://docs.snowflake.com/en/sql-reference/functions/grouping

SELECT col_x, col_y, sum(col_z), 
       grouping(col_x), grouping(col_y), grouping(col_x, col_y)
    FROM aggr2 GROUP BY GROUPING SETS ((col_x), (col_y), ())
    ORDER BY 1, 2;