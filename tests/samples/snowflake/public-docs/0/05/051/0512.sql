SELECT col_1, col_2, col_3
    FROM my_table
    WHERE (col_1, col_2, col_3) IN ( 
                                   (1,2,3), 
                                   (4,5,6)
                                   );