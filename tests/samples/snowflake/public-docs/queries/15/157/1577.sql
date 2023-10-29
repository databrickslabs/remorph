-- see https://docs.snowflake.com/en/sql-reference/functions/grouping_id

SELECT col_x, sum(col_z), GROUPING_ID(col_x)
    FROM aggr2 
    GROUP BY col_x
    ORDER BY col_x;