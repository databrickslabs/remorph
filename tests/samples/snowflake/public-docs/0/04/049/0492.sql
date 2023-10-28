SELECT x1.i x1_i, x2.i x2_i 
    FROM x x1, x x2 
    WHERE x1.i IS NOT DISTINCT FROM x2.i
    ORDER BY x1.i;