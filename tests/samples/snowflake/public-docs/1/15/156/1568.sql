SELECT * 
    FROM splittable, LATERAL STRTOK_SPLIT_TO_TABLE(splittable.v, ' ')
    ORDER BY SEQ, INDEX;