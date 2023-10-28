SELECT k, var_samp(v), var_samp(v2) 
    FROM aggr 
    GROUP BY k
    ORDER BY k;