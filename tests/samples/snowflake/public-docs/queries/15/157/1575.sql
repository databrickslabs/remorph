-- see https://docs.snowflake.com/en/sql-reference/functions/grouping_id

SELECT col_x, col_y, sum(col_z), 
       GROUPING_ID(col_x), 
       GROUPING_ID(col_y), 
       GROUPING_ID(col_x, col_y)
    FROM aggr2 
    GROUP BY GROUPING SETS ((col_x), (col_y), ())
    ORDER BY col_x ASC, col_y DESC;