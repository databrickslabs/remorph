SELECT x1.i x1_i, x2.i x2_i 
    FROM x x1, x x2 
    WHERE EQUAL_NULL(x1.i,x2.i);