SELECT k, var_pop(v), var_pop(v2) 
    FROM aggr 
    GROUP BY k
    ORDER BY k;