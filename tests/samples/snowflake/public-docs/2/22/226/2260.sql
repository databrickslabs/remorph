SELECT col_1, col_2, LAG(col_2) IGNORE NULLS OVER (ORDER BY col_1) 
    FROM t1
    ORDER BY col_1;