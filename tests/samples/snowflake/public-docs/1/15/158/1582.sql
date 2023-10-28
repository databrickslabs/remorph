SELECT * 
    FROM splittable, LATERAL SPLIT_TO_TABLE(splittable.v, '.')
    ORDER BY SEQ, INDEX;